"""
Matchmaker Service
Main orchestrator for JD-to-CV matching with 3-stage process
"""

import os
import sys
import json
import time
import logging
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from dotenv import load_dotenv
import google.generativeai as genai

# Add backend path to import models and database
backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, backend_path)

from backend.models.database import get_db
from backend.models.jd_models import JD
from backend.models.cv_models import CV
from matchmaker_scoring import MatchmakerScoring
from matchmaker_schemas import MatchmakerResponse, CVMatch, ScoreBreakdown

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from ai_modules/.env
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not found in .env file")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")


class MatchmakerService:
    """
    Three-stage matchmaking orchestrator
    
    Stage 1: SQL + Python pre-filtering
    Stage 2: AI-powered batch matching (10 CVs per batch)
    Stage 3: Database updates
    """
    
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.batch_size = 10
        self.max_retries = 3
        self.scorer = MatchmakerScoring()
    
    def match_jd_to_cvs(
        self, 
        jd_id: int, 
        min_match_percentage: int = 60,
        db: Session = None
    ) -> MatchmakerResponse:
        """
        Main entry point for JD-to-CV matching
        
        Args:
            jd_id: Job Description ID
            min_match_percentage: Minimum match % to return (default 60)
            db: Database session
        
        Returns:
            MatchmakerResponse with all matched CVs
        """
        start_time = time.time()
        
        try:
            # Stage 1: Pre-filter CVs
            logger.info(f"Stage 1: Pre-filtering CVs for JD {jd_id}")
            jd, filtered_cvs = self._stage1_prefilter(jd_id, db)
            
            if not filtered_cvs:
                logger.warning(f"No CVs found after Stage 1 filtering for JD {jd_id}")
                return MatchmakerResponse(
                    jd_id=jd_id,
                    jd_title=jd.job_title,
                    jd_company=jd.company_name,
                    total_filtered_cvs=0,
                    total_matched_cvs=0,
                    processing_time_seconds=time.time() - start_time,
                    matches=[]
                )
            
            logger.info(f"Stage 1 complete: {len(filtered_cvs)} CVs filtered")
            
            # Stage 2: AI matching with batching
            logger.info(f"Stage 2: AI matching with batch size {self.batch_size}")
            match_results = self._stage2_ai_matching(jd, filtered_cvs)
            
            logger.info(f"Stage 2 complete: {len(match_results)} CVs scored")
            
            # Filter by minimum match percentage
            qualified_matches = [
                m for m in match_results 
                if m['match_percentage'] >= min_match_percentage
            ]
            
            # Sort by match percentage (descending)
            qualified_matches.sort(key=lambda x: x['match_percentage'], reverse=True)
            
            logger.info(f"Found {len(qualified_matches)} CVs above {min_match_percentage}% threshold")
            
            # Stage 3: Update database
            logger.info("Stage 3: Updating CV table with match results")
            self._stage3_update_cvs(qualified_matches, jd_id, db)
            
            logger.info("Stage 3 complete: Database updated")
            
            # Build response
            response = MatchmakerResponse(
                jd_id=jd_id,
                jd_title=jd.job_title,
                jd_company=jd.company_name,
                total_filtered_cvs=len(filtered_cvs),
                total_matched_cvs=len(qualified_matches),
                processing_time_seconds=time.time() - start_time,
                matches=[self._build_cv_match(m) for m in qualified_matches]
            )
            
            logger.info(f"Matchmaking complete in {response.processing_time_seconds:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"Matchmaking failed: {str(e)}", exc_info=True)
            raise
    
    def _stage1_prefilter(self, jd_id: int, db: Session) -> tuple:
        """
        Stage 1: SQL + Python filtering
        
        Filters CVs by:
        - cv_stage IN ('Screening Negotiation', 'Shortlisted', 'Interview')
        - cv_status IN ('Staging', 'Reviewed')
        - cv_active = True
        - cv_experience in range
        - cv_ectc in budget range
        
        Returns:
            (jd_object, list_of_filtered_cvs)
        """
        # Get JD
        jd = db.query(JD).filter(JD.id == jd_id).first()
        if not jd:
            raise ValueError(f"JD with id {jd_id} not found")
        
        # Build filter conditions
        filters = [
            CV.cv_active == True,
            CV.cv_stage.in_(['Screening Negotiation', 'Shortlisted', 'Interview']),
            CV.cv_status.in_(['Staging', 'Reviewed'])
        ]
        
        # Add experience filter if specified
        if jd.op_experience_min is not None and jd.op_experience_max is not None:
            filters.append(CV.cv_experience >= jd.op_experience_min)
            filters.append(CV.cv_experience <= jd.op_experience_max)
        
        # Add budget filter if specified
        if jd.op_budget_min is not None and jd.op_budget_max is not None:
            filters.append(CV.cv_ectc >= jd.op_budget_min)
            filters.append(CV.cv_ectc <= jd.op_budget_max)
        
        # Execute query
        cvs = db.query(CV).filter(and_(*filters)).all()
        
        logger.info(f"Stage 1: Found {len(cvs)} CVs matching criteria")
        
        return jd, cvs
    
    def _stage2_ai_matching(self, jd, cvs: List) -> List[Dict]:
        """
        Stage 2: AI-powered batch matching
        
        Processes CVs in batches of 10, sends to Gemini for similarity detection
        
        Returns:
            List of dicts with cv_id, match_percentage, rating, breakdown
        """
        all_results = []
        
        # Split into batches
        num_batches = (len(cvs) + self.batch_size - 1) // self.batch_size
        
        for i in range(num_batches):
            start_idx = i * self.batch_size
            end_idx = min((i + 1) * self.batch_size, len(cvs))
            batch = cvs[start_idx:end_idx]
            
            logger.info(f"Processing batch {i+1}/{num_batches} ({len(batch)} CVs)")
            
            # Process batch with retry logic
            batch_results = self._process_batch_with_retry(jd, batch)
            all_results.extend(batch_results)
        
        return all_results
    
    def _process_batch_with_retry(self, jd, batch: List) -> List[Dict]:
        """Process a batch of CVs with retry logic"""
        for attempt in range(self.max_retries):
            try:
                return self._process_batch(jd, batch)
            except Exception as e:
                logger.warning(f"Batch processing attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Batch processing failed after {self.max_retries} attempts")
                    # Return zero scores for this batch as fallback
                    return self._fallback_scoring(jd, batch)
    
    def _process_batch(self, jd, batch: List) -> List[Dict]:
        """
        Process a batch of CVs through AI
        
        Sends JD keywords + batch of CV keywords to Gemini
        Gets back similarity matches, then calculates scores in Python
        """
        # Build prompt
        prompt = self._build_ai_prompt(jd, batch)
        
        # Call Gemini API
        logger.debug("Sending batch to Gemini API")
        response = self.model.generate_content(prompt)
        
        # Parse AI response
        ai_response = self._parse_ai_response(response.text)
        
        # Calculate scores using Python scoring algorithm
        results = []
        for cv in batch:
            # Find AI matches for this CV
            ai_matches = next(
                (m for m in ai_response['matches'] if m['cv_id'] == cv.cv_id),
                {'must_have_matches': [], 'must_have_similar': [], 
                 'good_to_have_matches': [], 'good_to_have_similar': [],
                 'soft_skills_matches': [], 'soft_skills_similar': []}
            )
            
            # Calculate score
            jd_dict = {
                'must_have_skills': jd.must_have_skills,
                'good_to_have_skills': jd.good_to_have_skills,
                'soft_skills': jd.soft_skills,
                'domain_expertise': getattr(jd, 'domain_expertise', None),
                'exception_skills': jd.exception_skills,
                'exception_list': getattr(jd, 'exception_list', None),
                'op_experience_min': jd.op_experience_min,
                'op_experience_max': jd.op_experience_max
            }
            
            cv_dict = {
                'cv_must_to_have': cv.cv_must_to_have,
                'cv_good_to_have': cv.cv_good_to_have,
                'cv_soft_skills': cv.cv_soft_skills,
                'cv_domain_expertise': getattr(cv, 'cv_domain_expertise', None),
                'cv_accolades': getattr(cv, 'cv_accolades', None),
                'cv_experience': cv.cv_experience,
                'cv_current_company': cv.cv_current_company
            }
            
            score_result = self.scorer.calculate_total_score(
                jd_dict, cv_dict, ai_matches
            )
            
            # Add CV metadata
            score_result['cv_id'] = cv.cv_id
            score_result['cv_name'] = cv.cv_name
            score_result['cv_email'] = cv.cv_email
            score_result['cv_mobile'] = cv.cv_mobile
            score_result['cv_experience'] = cv.cv_experience
            score_result['cv_current_company'] = cv.cv_current_company
            score_result['cv_role'] = cv.cv_role
            
            results.append(score_result)
        
        return results
    
    def _build_ai_prompt(self, jd, batch: List) -> str:
        """
        Build prompt for Gemini API
        
        Format:
        - JD keywords in categories
        - Batch of CV keywords (numbered)
        - Request for similarity detection
        """
        prompt = f"""You are a technical recruiter matching CVs to job requirements.

JOB REQUIREMENTS:
Must-Have Skills: {jd.must_have_skills or 'None'}
Good-to-Have Skills: {jd.good_to_have_skills or 'None'}
Soft Skills: {jd.soft_skills or 'None'}

CVs TO MATCH ({len(batch)} candidates):
"""
        
        for i, cv in enumerate(batch, 1):
            prompt += f"""
[CV-{cv.cv_id}]
Must-Have: {cv.cv_must_to_have or 'None'}
Good-to-Have: {cv.cv_good_to_have or 'None'}
Soft Skills: {cv.cv_soft_skills or 'None'}
"""
        
        prompt += """

TASK:
For each CV, identify:
1. Exact matches with JD skills (case-insensitive)
2. Similar/equivalent skills (e.g., Flask is similar to Django, PostgreSQL is similar to MySQL)

IMPORTANT:
- Only detect TECHNICAL similarity (e.g., Flask~Django, React~Vue)
- DO NOT force matches where none exist
- Return ONLY valid JSON, no markdown, no comments

OUTPUT FORMAT (STRICT JSON):
{
  "matches": [
    {
      "cv_id": 123,
      "must_have_matches": ["Python", "AWS"],
      "must_have_similar": ["Flask~Django", "PostgreSQL~MySQL"],
      "good_to_have_matches": ["Docker"],
      "good_to_have_similar": [],
      "soft_skills_matches": ["Leadership"],
      "soft_skills_similar": []
    }
  ]
}
"""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse Gemini API response as JSON"""
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # Parse JSON
            data = json.loads(cleaned)
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise ValueError("AI returned invalid JSON")
    
    def _fallback_scoring(self, jd, batch: List) -> List[Dict]:
        """
        Fallback scoring if AI fails
        Uses exact string matching only (no AI similarity detection)
        """
        logger.warning("Using fallback scoring without AI similarity detection")
        
        results = []
        for cv in batch:
            jd_dict = {
                'must_have_skills': jd.must_have_skills,
                'good_to_have_skills': jd.good_to_have_skills,
                'soft_skills': jd.soft_skills,
                'domain_expertise': getattr(jd, 'domain_expertise', None),
                'exception_skills': jd.exception_skills,
                'exception_list': getattr(jd, 'exception_list', None),
                'op_experience_min': jd.op_experience_min,
                'op_experience_max': jd.op_experience_max
            }
            
            cv_dict = {
                'cv_must_to_have': cv.cv_must_to_have,
                'cv_good_to_have': cv.cv_good_to_have,
                'cv_soft_skills': cv.cv_soft_skills,
                'cv_domain_expertise': getattr(cv, 'cv_domain_expertise', None),
                'cv_accolades': getattr(cv, 'cv_accolades', None),
                'cv_experience': cv.cv_experience,
                'cv_current_company': cv.cv_current_company
            }
            
            # No AI matches, only exact matching
            ai_matches = {
                'must_have_matches': [],
                'must_have_similar': [],
                'good_to_have_matches': [],
                'good_to_have_similar': [],
                'soft_skills_matches': [],
                'soft_skills_similar': []
            }
            
            score_result = self.scorer.calculate_total_score(
                jd_dict, cv_dict, ai_matches
            )
            
            score_result['cv_id'] = cv.cv_id
            score_result['cv_name'] = cv.cv_name
            score_result['cv_email'] = cv.cv_email
            score_result['cv_mobile'] = cv.cv_mobile
            score_result['cv_experience'] = cv.cv_experience
            score_result['cv_current_company'] = cv.cv_current_company
            score_result['cv_role'] = cv.cv_role
            
            results.append(score_result)
        
        return results
    
    def _stage3_update_cvs(self, match_results: List[Dict], jd_id: int, db: Session):
        """
        Stage 3: Update CV table with match results
        
        Updates:
        - matched_jd_title (using JD job_title)
        - cv_match_perc
        - cv_rating
        - date_of_match
        """
        from datetime import datetime
        
        # Get JD title for updating matched_jd_title
        jd = db.query(JD).filter(JD.id == jd_id).first()
        jd_title = jd.job_title if jd else f"JD-{jd_id}"
        
        for result in match_results:
            cv = db.query(CV).filter(CV.cv_id == result['cv_id']).first()
            if cv:
                cv.matched_jd_title = jd_title
                cv.cv_match_perc = result['match_percentage']
                cv.cv_rating = result['rating']
                cv.date_of_match = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        db.commit()
        logger.info(f"Updated {len(match_results)} CVs in database")
    
    def _build_cv_match(self, result: Dict) -> CVMatch:
        """Convert dict result to CVMatch schema"""
        return CVMatch(
            cv_id=result['cv_id'],
            cv_name=result['cv_name'],
            cv_email=result['cv_email'],
            cv_mobile=result['cv_mobile'],
            cv_experience=result['cv_experience'],
            cv_current_company=result['cv_current_company'],
            cv_role=result['cv_role'],
            match_percentage=result['match_percentage'],
            rating=result['rating'],
            breakdown=ScoreBreakdown(**result['breakdown']),
            matched_skills=result['matched_skills'],
            missing_skills=result['missing_skills']
        )


# Singleton instance
_matchmaker_service = None

def get_matchmaker_service() -> MatchmakerService:
    """Get singleton matchmaker service instance"""
    global _matchmaker_service
    if _matchmaker_service is None:
        _matchmaker_service = MatchmakerService()
    return _matchmaker_service