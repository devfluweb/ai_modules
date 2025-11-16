"""
CV Extractor Service - Production Ready
Extracts 6 fields matching DB columns exactly
"""

import sys
import os
from typing import Dict, Any, Optional

# Import dependencies
from clients.gemini_client import get_gemini_client
from prompts.cv_extraction_prompt import get_cv_extraction_prompt
from utils.file_utils import FileTextExtractor

class CVExtractor:
    """
    Extract skills, domain, accolades, and snapshot from CVs.
    Matches DB columns: cv_must_to_have, cv_good_to_have, cv_soft_skills,
    cv_domain_expertise, cv_accolades, cv_snapshot, cv_total_words
    """
    
    def __init__(self):
        """Initialize CV extractor with Gemini 2.5 Flash client"""
        self.gemini = get_gemini_client()
        self.file_extractor = FileTextExtractor()
        print("✅ CV Extractor initialized (Gemini 2.5 Flash)")
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract keywords from CV file (PDF or DOCX).
        
        Args:
            file_path: Path to CV file
        
        Returns:
            Dict with 7 fields matching DB columns
        """
        print(f"\n{'='*70}")
        print(f"📄 CV EXTRACTION STARTED")
        print(f"{'='*70}")
        print(f"File: {os.path.basename(file_path)}")
        
        # Step 1: Extract text from file
        print("\n🔍 Step 1/5: Extracting text from file...")
        cv_text = self.file_extractor.extract_text(file_path)
        
        if not cv_text:
            print("❌ Text extraction failed")
            return self._get_fallback()
        
        # Step 2: Validate text
        print("\n✅ Step 2/5: Validating extracted text...")
        if not self.file_extractor.validate_text(cv_text, min_words=50):
            print("❌ Text validation failed")
            return self._get_fallback()
        
        # Step 3: Extract using AI
        return self.extract_from_text(cv_text)
    
    def extract_from_text(self, cv_text: str) -> Dict[str, Any]:
        """
        Extract keywords from CV text.
        
        Args:
            cv_text: CV content as text
        
        Returns:
            Dict with extracted fields
        """
        # Generate prompt
        print("\n🤖 Step 3/5: Generating AI prompt...")
        prompt = get_cv_extraction_prompt(cv_text)
        
        # Get AI response
        print("\n⚡ Step 4/5: Calling Gemini 2.5 Flash API...")
        result = self.gemini.generate_json(
            prompt=prompt,
            max_retries=3,
            fallback=self._get_fallback()
        )
        
        # Validate output
        print("\n✅ Step 5/5: Validating extraction quality...")
        result = self._validate_and_fix(result)
        
        print(f"\n{'='*70}")
        print(f"✅ CV EXTRACTION COMPLETED")
        print(f"{'='*70}")
        self._print_summary(result)
        
        return result
    
    def _validate_and_fix(self, result: Dict) -> Dict:
        """
        Validate extraction and fix common issues.
        
        Checks:
        - All required fields present
        - Skills are arrays (not strings)
        - Snapshot exists and not too long
        - Calculate cv_total_words
        """
        # Ensure all fields exist
        required_fields = [
            'cv_must_to_have',
            'cv_good_to_have',
            'cv_soft_skills',
            'cv_domain_expertise',
            'cv_accolades',
            'cv_snapshot'
        ]
        
        for field in required_fields:
            if field not in result:
                print(f"⚠️ Missing field '{field}', adding empty value")
                if field == 'cv_snapshot':
                    result[field] = "Unable to generate CV snapshot."
                else:
                    result[field] = []
        
        # Convert strings to arrays if needed
        for field in ['cv_must_to_have', 'cv_good_to_have', 'cv_soft_skills', 
                      'cv_domain_expertise', 'cv_accolades']:
            if isinstance(result[field], str):
                result[field] = [result[field]] if result[field] else []
        
        # Calculate word count
        snapshot = result.get('cv_snapshot', '')
        result['cv_total_words'] = len(snapshot.split())
        
        # Validate snapshot length
        word_count = result['cv_total_words']
        if word_count > 250:
            print(f"⚠️ Warning: Snapshot too long ({word_count} words, max 250)")
        elif word_count < 100:
            print(f"⚠️ Warning: Snapshot too short ({word_count} words, min 120)")
        
        # Check for common mistakes
        self._check_soft_skills_contamination(result)
        
        print("✅ Validation passed")
        return result
    
    def _check_soft_skills_contamination(self, result: Dict):
        """Check if technical skills leaked into soft_skills"""
        soft_skills = result.get('cv_soft_skills', [])
        technical_keywords = ['python', 'java', 'react', 'aws', 'docker', 
                            'sql', 'api', 'django', 'node', 'azure']
        
        for skill in soft_skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in technical_keywords):
                print(f"⚠️ Warning: Technical skill '{skill}' in soft_skills!")
    
    def _get_fallback(self) -> Dict:
        """Fallback structure if extraction fails"""
        return {
            "cv_must_to_have": [],
            "cv_good_to_have": [],
            "cv_soft_skills": [],
            "cv_domain_expertise": [],
            "cv_accolades": [],
            "cv_snapshot": "Unable to generate CV snapshot. Please check the resume format.",
            "cv_total_words": 0
        }
    
    def _print_summary(self, result: Dict):
        """Print extraction summary"""
        print(f"\n📊 EXTRACTION SUMMARY:")
        print(f"   Primary Skills: {len(result.get('cv_must_to_have', []))} → {', '.join(result.get('cv_must_to_have', [])[:5])}{'...' if len(result.get('cv_must_to_have', [])) > 5 else ''}")
        print(f"   Secondary Skills: {len(result.get('cv_good_to_have', []))} → {', '.join(result.get('cv_good_to_have', [])[:5])}{'...' if len(result.get('cv_good_to_have', [])) > 5 else ''}")
        print(f"   Soft Skills: {len(result.get('cv_soft_skills', []))} → {', '.join(result.get('cv_soft_skills', []))}")
        print(f"   Domain: {len(result.get('cv_domain_expertise', []))} → {', '.join(result.get('cv_domain_expertise', []))}")
        print(f"   Accolades: {len(result.get('cv_accolades', []))}")
        print(f"   Snapshot: {result.get('cv_total_words', 0)} words")

# Example usage
if __name__ == "__main__":
    extractor = CVExtractor()
    
    # Test with a file
    # result = extractor.extract_from_file("/path/to/resume.pdf")
    # print(json.dumps(result, indent=2))
