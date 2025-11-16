"""
Matchmaker Scoring Algorithm
Calculates match percentage using 100-point scoring system
"""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class MatchmakerScoring:
    """
    100-point scoring system for JD-CV matching
    
    Breakdown:
    - Must-have skills: 40 points
    - Good-to-have skills: 25 points
    - Soft skills: 15 points
    - Domain expertise: 10 points
    - Experience fit: 10 points
    - Accolades bonus: +10 points
    - Exception penalty: -50 points per violation
    """
    
    @staticmethod
    def parse_skills(skills_text: Optional[str]) -> List[str]:
        """Parse comma-separated skills string into list"""
        if not skills_text:
            return []
        
        # Split by comma and clean each skill
        skills = [s.strip().lower() for s in str(skills_text).split(',') if s.strip()]
        return skills
    
    @staticmethod
    def calculate_skill_match(
        jd_skills: List[str], 
        cv_skills: List[str], 
        ai_similar_skills: List[str] = None
    ) -> tuple[int, List[str], List[str]]:
        """
        Calculate skill match count
        
        Args:
            jd_skills: Skills required by JD
            cv_skills: Skills from CV
            ai_similar_skills: Similar skills detected by AI (e.g., "Flask~Django")
        
        Returns:
            (match_count, matched_skills, missing_skills)
        """
        if not jd_skills:
            return 0, [], []
        
        matched = []
        missing = []
        
        # Normalize for comparison
        jd_normalized = [s.lower().strip() for s in jd_skills]
        cv_normalized = [s.lower().strip() for s in cv_skills]
        
        for jd_skill in jd_normalized:
            if jd_skill in cv_normalized:
                matched.append(jd_skill)
            else:
                missing.append(jd_skill)
        
        # Add AI-detected similar skills
        if ai_similar_skills:
            for similar in ai_similar_skills:
                # Format: "Flask~Django" means Flask (CV) is similar to Django (JD)
                if '~' in similar:
                    cv_skill, jd_skill = similar.split('~')
                    if jd_skill.lower().strip() in missing:
                        matched.append(f"{jd_skill} (similar: {cv_skill})")
                        missing.remove(jd_skill.lower().strip())
        
        return len(matched), matched, missing
    
    @staticmethod
    def calculate_experience_score(
        cv_experience: Optional[float],
        jd_exp_min: Optional[int],
        jd_exp_max: Optional[int]
    ) -> int:
        """
        Calculate experience fit score (0-10 points)
        
        Rules:
        - Within range: 10 points
        - 1 year off from range: 5 points
        - Outside range: 0 points
        """
        if cv_experience is None:
            return 0
        
        if jd_exp_min is None and jd_exp_max is None:
            return 10  # No requirement, give full points
        
        exp_min = jd_exp_min or 0
        exp_max = jd_exp_max or 100
        
        # Within range
        if exp_min <= cv_experience <= exp_max:
            return 10
        
        # 1 year tolerance
        if abs(cv_experience - exp_min) <= 1 or abs(cv_experience - exp_max) <= 1:
            return 5
        
        # Outside range
        return 0
    
    @staticmethod
    def calculate_domain_match(
        jd_domain: Optional[str],
        cv_domain: Optional[str]
    ) -> int:
        """
        Calculate domain expertise match (0-10 points)
        
        Simple keyword overlap check
        """
        if not jd_domain or not cv_domain:
            return 0
        
        jd_keywords = set(jd_domain.lower().split())
        cv_keywords = set(cv_domain.lower().split())
        
        overlap = jd_keywords.intersection(cv_keywords)
        
        if overlap:
            return 10
        return 0
    
    @staticmethod
    def calculate_accolades_bonus(cv_accolades: Optional[str]) -> int:
        """
        Calculate accolades bonus (0-10 points)
        
        2 points per accolade, max 10 points
        """
        if not cv_accolades:
            return 0
        
        accolades_list = [a.strip() for a in str(cv_accolades).split(',') if a.strip()]
        bonus = min(len(accolades_list) * 2, 10)
        return bonus
    
    @staticmethod
    def check_exceptions(
        cv_skills: List[str],
        cv_companies: Optional[str],
        jd_exception_skills: Optional[str],
        jd_exception_list: Optional[str]
    ) -> int:
        """
        Check for exception penalties (-50 per violation)
        
        Penalties:
        - Has exception skill: -50
        - Worked at blacklisted company: -50
        """
        penalty = 0
        
        # Check exception skills
        if jd_exception_skills:
            exception_skills = [s.strip().lower() for s in jd_exception_skills.split(',') if s.strip()]
            cv_skills_lower = [s.lower() for s in cv_skills]
            
            for exc_skill in exception_skills:
                if exc_skill in cv_skills_lower:
                    penalty -= 50
                    logger.warning(f"Exception skill found: {exc_skill}")
                    break  # Only penalize once
        
        # Check blacklisted companies
        if jd_exception_list and cv_companies:
            blacklist = [c.strip().lower() for c in jd_exception_list.split(',') if c.strip()]
            
            for blacklisted in blacklist:
                if blacklisted in cv_companies.lower():
                    penalty -= 50
                    logger.warning(f"Blacklisted company found: {blacklisted}")
                    break  # Only penalize once
        
        return penalty
    
    @classmethod
    def calculate_total_score(
        cls,
        jd: Dict,
        cv: Dict,
        ai_matches: Dict
    ) -> Dict:
        """
        Calculate total match score using 100-point system
        
        Args:
            jd: JD data with keywords
            cv: CV data with keywords
            ai_matches: AI-detected matches and similar skills
        
        Returns:
            Dict with total score, breakdown, rating, matched/missing skills
        """
        # Parse skills
        jd_must_have = cls.parse_skills(jd.get('must_have_skills'))
        jd_good_to_have = cls.parse_skills(jd.get('good_to_have_skills'))
        jd_soft_skills = cls.parse_skills(jd.get('soft_skills'))
        
        cv_must_have = cls.parse_skills(cv.get('cv_must_to_have'))
        cv_good_to_have = cls.parse_skills(cv.get('cv_good_to_have'))
        cv_soft_skills = cls.parse_skills(cv.get('cv_soft_skills'))
        
        # Get AI-detected similar skills
        ai_must_similar = ai_matches.get('must_have_similar', [])
        ai_good_similar = ai_matches.get('good_to_have_similar', [])
        ai_soft_similar = ai_matches.get('soft_skills_similar', [])
        
        # 1. Must-have skills (40 points)
        must_match_count, must_matched, must_missing = cls.calculate_skill_match(
            jd_must_have, cv_must_have, ai_must_similar
        )
        must_have_score = 0
        if jd_must_have:
            must_have_score = int((must_match_count / len(jd_must_have)) * 40)
        
        # 2. Good-to-have skills (25 points)
        good_match_count, good_matched, good_missing = cls.calculate_skill_match(
            jd_good_to_have, cv_good_to_have, ai_good_similar
        )
        good_to_have_score = 0
        if jd_good_to_have:
            good_to_have_score = int((good_match_count / len(jd_good_to_have)) * 25)
        
        # 3. Soft skills (15 points)
        soft_match_count, soft_matched, soft_missing = cls.calculate_skill_match(
            jd_soft_skills, cv_soft_skills, ai_soft_similar
        )
        soft_skills_score = 0
        if jd_soft_skills:
            soft_skills_score = int((soft_match_count / len(jd_soft_skills)) * 15)
        
        # 4. Domain expertise (10 points)
        domain_score = cls.calculate_domain_match(
            jd.get('domain_expertise'),
            cv.get('cv_domain_expertise')
        )
        
        # 5. Experience fit (10 points)
        experience_score = cls.calculate_experience_score(
            cv.get('cv_experience'),
            jd.get('op_experience_min'),
            jd.get('op_experience_max')
        )
        
        # 6. Accolades bonus (+10 points)
        accolades_bonus = cls.calculate_accolades_bonus(cv.get('cv_accolades'))
        
        # 7. Exception penalties (-50 per violation)
        all_cv_skills = cv_must_have + cv_good_to_have
        exception_penalty = cls.check_exceptions(
            all_cv_skills,
            cv.get('cv_current_company'),
            jd.get('exception_skills'),
            jd.get('exception_list')
        )
        
        # Calculate total score (cap at 0-100)
        total_score = (
            must_have_score +
            good_to_have_score +
            soft_skills_score +
            domain_score +
            experience_score +
            accolades_bonus +
            exception_penalty
        )
        
        match_percentage = max(0, min(100, total_score))
        
        # Calculate rating (1-5 stars)
        if match_percentage >= 90:
            rating = 5
        elif match_percentage >= 75:
            rating = 4
        elif match_percentage >= 60:
            rating = 3
        elif match_percentage >= 40:
            rating = 2
        else:
            rating = 1
        
        # Combine all matched and missing skills
        all_matched = must_matched + good_matched + soft_matched
        all_missing = must_missing + good_missing + soft_missing
        
        return {
            'match_percentage': match_percentage,
            'rating': rating,
            'breakdown': {
                'must_have': must_have_score,
                'good_to_have': good_to_have_score,
                'soft_skills': soft_skills_score,
                'domain': domain_score,
                'experience': experience_score,
                'accolades': accolades_bonus,
                'penalties': exception_penalty
            },
            'matched_skills': all_matched,
            'missing_skills': all_missing
        }