"""
JD Extractor Service - Production Ready
Extracts 7 fields + LinkedIn-style social snapshot
"""

import sys
import os
from typing import Dict, Any

# Import dependencies
from clients.gemini_client import get_gemini_client
from prompts.jd_extraction_prompt import get_jd_extraction_prompt

class JDExtractor:
    """
    Extract skills, domain, and generate social media snapshot from JDs.
    Returns: must_have_skills, good_to_have_skills, soft_skills,
    domain_expertise, accolades_keyword, exception_skills, jd_snapshot
    """
    
    def __init__(self):
        """Initialize JD extractor with Gemini 2.5 Flash client"""
        self.gemini = get_gemini_client()
        print("✅ JD Extractor initialized (Gemini 2.5 Flash)")
    
    def extract_from_text(self, jd_text: str) -> Dict[str, Any]:
        """
        Extract keywords and generate LinkedIn snapshot from JD text.
        
        Args:
            jd_text: Job description content as text
        
        Returns:
            Dict with 7 extracted fields
        """
        print(f"\n{'='*70}")
        print(f"📋 JD EXTRACTION STARTED")
        print(f"{'='*70}")
        
        # Step 1: Validate input
        print("\n🔍 Step 1/4: Validating JD text...")
        if not jd_text or len(jd_text.strip()) < 100:
            print("❌ JD text too short or empty")
            return self._get_fallback()
        
        word_count = len(jd_text.split())
        print(f"✅ JD contains {word_count} words")
        
        # Step 2: Generate prompt
        print("\n🤖 Step 2/4: Generating AI prompt...")
        prompt = get_jd_extraction_prompt(jd_text)
        
        # Step 3: Extract using AI
        print("\n⚡ Step 3/4: Calling Gemini 2.5 Flash API...")
        result = self.gemini.generate_json(
            prompt=prompt,
            max_retries=3,
            fallback=self._get_fallback()
        )
        
        # Step 4: Validate output
        print("\n✅ Step 4/4: Validating extraction quality...")
        result = self._validate_and_fix(result)
        
        print(f"\n{'='*70}")
        print(f"✅ JD EXTRACTION COMPLETED")
        print(f"{'='*70}")
        self._print_summary(result)
        
        return result
    
    def _validate_and_fix(self, result: Dict) -> Dict:
        """
        Validate extraction and fix common issues.
        
        Checks:
        - All required fields present
        - Must-have skills not empty (critical!)
        - Skills are arrays (not strings)
        - Snapshot has proper formatting
        """
        # Ensure all fields exist
        required_fields = [
            'must_have_skills',
            'good_to_have_skills',
            'soft_skills',
            'domain_expertise',
            'accolades_keyword',
            'exception_skills',
            'jd_snapshot'
        ]
        
        for field in required_fields:
            if field not in result:
                print(f"⚠️ Missing field '{field}', adding empty value")
                if field == 'jd_snapshot':
                    result[field] = "Unable to generate JD snapshot."
                elif field in ['accolades_keyword', 'exception_skills']:
                    result[field] = "none"
                else:
                    result[field] = []
        
        # Convert strings to arrays if needed (except accolades and exceptions)
        for field in ['must_have_skills', 'good_to_have_skills', 'soft_skills', 'domain_expertise']:
            if isinstance(result[field], str):
                result[field] = [result[field]] if result[field] else []
        
        # Handle accolades_keyword (can be array or "none")
        if isinstance(result['accolades_keyword'], list) and len(result['accolades_keyword']) == 0:
            result['accolades_keyword'] = "none"
        
        # Handle exception_skills (can be array or "none")
        if isinstance(result['exception_skills'], list) and len(result['exception_skills']) == 0:
            result['exception_skills'] = "none"
        
        # Critical check: Must-have skills should NEVER be empty
        must_have = result.get('must_have_skills', [])
        if not must_have or len(must_have) == 0:
            print("❌ CRITICAL: No must-have skills extracted!")
        
        # Check snapshot format
        snapshot = result.get('jd_snapshot', '')
        if '\\n' not in snapshot and len(snapshot) > 50:
            print("⚠️ Warning: Snapshot missing line breaks (should have \\n)")
        
        # Check for technical skills in soft_skills
        self._check_soft_skills_contamination(result)
        
        # Validate snapshot length
        snapshot_words = len(snapshot.split())
        if snapshot_words > 250:
            print(f"⚠️ Warning: Snapshot too long ({snapshot_words} words, target ~200)")
        elif snapshot_words < 150:
            print(f"⚠️ Warning: Snapshot too short ({snapshot_words} words, target ~200)")
        
        print("✅ Validation passed")
        return result
    
    def _check_soft_skills_contamination(self, result: Dict):
        """Check if technical skills leaked into soft_skills"""
        soft_skills = result.get('soft_skills', [])
        technical_keywords = ['python', 'java', 'react', 'aws', 'docker', 
                            'sql', 'api', 'django', 'node', 'azure']
        
        for skill in soft_skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in technical_keywords):
                print(f"⚠️ Warning: Technical skill '{skill}' in soft_skills!")
    
    def _get_fallback(self) -> Dict:
        """Fallback structure if extraction fails"""
        return {
            "must_have_skills": [],
            "good_to_have_skills": [],
            "soft_skills": [],
            "domain_expertise": [],
            "accolades_keyword": "none",
            "exception_skills": "none",
            "jd_snapshot": "Unable to generate JD snapshot. Please check the job description format."
        }
    
    def _print_summary(self, result: Dict):
        """Print extraction summary"""
        print(f"\n📊 EXTRACTION SUMMARY:")
        print(f"   Must-Have: {len(result.get('must_have_skills', []))} → {', '.join(result.get('must_have_skills', []))}")
        print(f"   Good-to-Have: {len(result.get('good_to_have_skills', []))} → {', '.join(result.get('good_to_have_skills', []))}")
        print(f"   Soft Skills: {len(result.get('soft_skills', []))} → {', '.join(result.get('soft_skills', []))}")
        print(f"   Domain: {len(result.get('domain_expertise', []))} → {', '.join(result.get('domain_expertise', []))}")
        print(f"   Accolades: {result.get('accolades_keyword', 'none')}")
        print(f"   Exceptions: {result.get('exception_skills', 'none')}")
        print(f"   Snapshot: {len(result.get('jd_snapshot', '').split())} words")
        
        # Print snapshot preview
        snapshot = result.get('jd_snapshot', '')
        if snapshot and len(snapshot) > 100:
            print(f"\n📝 SNAPSHOT PREVIEW:")
            print(f"   {snapshot[:200]}...")

# Example usage
if __name__ == "__main__":
    extractor = JDExtractor()
    
    # Test with sample JD
    sample_jd = """
    Senior Backend Developer - Python/Django
    
    We're looking for an experienced Backend Developer with 5+ years of experience.
    
    Required Skills:
    - Strong Python and Django expertise
    - PostgreSQL database design
    - AWS cloud services (EC2, S3, RDS)
    - RESTful API development
    
    Nice to have:
    - Docker and Kubernetes experience
    - Redis caching
    
    You'll work in an agile team and mentor junior developers.
    """
    
    # result = extractor.extract_from_text(sample_jd)
    # print(json.dumps(result, indent=2))
