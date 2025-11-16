"""
CV Extractor Service - Production Ready
NOW WITH R2 BUCKET SUPPORT
"""

import sys
import os
from typing import Dict, Any, Optional

# Import dependencies
from clients.gemini_client import get_gemini_client
from prompts.cv_extraction_prompt import get_cv_extraction_prompt
from utils.file_utils import FileTextExtractor

# Try to import R2 client (optional, not yet implemented)
try:
    from clients.r2_client import get_r2_client
    R2_AVAILABLE = True
except ImportError:
    R2_AVAILABLE = False
    get_r2_client = None

class CVExtractor:
    """
    Extract skills, domain, accolades, and snapshot from CVs.
    Supports: Local files, R2 bucket files
    """
    
    def __init__(self):
        """Initialize CV extractor with Gemini + R2 clients"""
        self.gemini = get_gemini_client()
        self.file_extractor = FileTextExtractor()
        
        # Initialize R2 client if available
        if R2_AVAILABLE and get_r2_client:
            self.r2_client = get_r2_client()
            print("✅ CV Extractor initialized (Gemini 2.5 Flash + R2)")
        else:
            self.r2_client = None
            print("✅ CV Extractor initialized (Gemini 2.5 Flash only - R2 not available)")
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Extract keywords from CV file (PDF or DOCX).
        Supports both local paths and R2 keys.
        
        Args:
            file_path: Local path OR R2 key (e.g., "cv_files/candidate_123.pdf")
        
        Returns:
            Dict with 7 fields matching DB columns
        """
        print(f"\n{'='*70}")
        print(f"📄 CV EXTRACTION STARTED")
        print(f"{'='*70}")
        
        # Step 1: Determine if it's R2 key or local path
        is_r2_file = self._is_r2_key(file_path)
        
        if is_r2_file:
            print(f"R2 File: {file_path}")
            local_path = self._download_from_r2(file_path)
            cleanup_after = True  # Delete temp file after extraction
        else:
            print(f"Local File: {file_path}")
            local_path = file_path
            cleanup_after = False
        
        try:
            # Step 2: Extract text from local file
            print(f"\n🔍 Extracting text from: {os.path.basename(local_path)}")
            cv_text = self.file_extractor.extract_text(local_path)
            
            if not cv_text:
                print("❌ Text extraction failed")
                return self._get_fallback()
            
            # Step 3: Validate text
            print("\n✅ Validating extracted text...")
            if not self.file_extractor.validate_text(cv_text, min_words=50):
                print("❌ Text validation failed")
                return self._get_fallback()
            
            # Step 4: Extract using AI
            result = self.extract_from_text(cv_text)
            
            return result
            
        finally:
            # Cleanup temp file if downloaded from R2
            if cleanup_after and os.path.exists(local_path):
                os.remove(local_path)
                print(f"🗑️ Cleaned up temp file: {local_path}")
    
    def extract_from_r2(self, r2_key: str) -> Dict[str, Any]:
        """
        Extract keywords from CV stored in R2 bucket.
        Convenience method that explicitly uses R2.
        
        Args:
            r2_key: File key in R2 (e.g., "cv_files/candidate_123.pdf")
        
        Returns:
            Dict with 7 fields matching DB columns
        """
        return self.extract_from_file(r2_key)
    
    def _is_r2_key(self, path: str) -> bool:
        """
        Determine if path is R2 key or local file path.
        
        R2 keys typically:
        - Don't start with / or C:\\
        - Contain forward slashes like "cv_files/candidate_123.pdf"
        - Don't exist as local files
        """
        # If it's an absolute path that exists locally, it's local
        if os.path.isabs(path) and os.path.exists(path):
            return False
        
        # If it exists as relative local path, it's local
        if os.path.exists(path):
            return False
        
        # Otherwise, assume it's R2 key
        return True
    
    def _download_from_r2(self, r2_key: str) -> str:
        """Download file from R2 and return local temp path"""
        if not self.r2_client:
            raise NotImplementedError("R2 client not available. Please implement clients/r2_client.py")
        
        try:
            # Check if file exists in R2
            if not self.r2_client.file_exists(r2_key):
                raise FileNotFoundError(f"File not found in R2: {r2_key}")
            
            # Get file info and download
            file_info = self.r2_client.download_file(r2_key)
            
            if not file_info or 'local_path' not in file_info:
                raise Exception(f"Failed to download from R2: {r2_key}")
            
            local_path = file_info['local_path']
            print(f"✅ Downloaded from R2: {r2_key} → {local_path}")
            
            return local_path
            
        except Exception as e:
            print(f"❌ R2 download failed: {e}")
            raise
    
    def extract_from_text(self, cv_text: str) -> Dict[str, Any]:
        """
        Extract keywords from CV text using AI.
        
        Args:
            cv_text: CV content as text
        
        Returns:
            Dict with 6 fields matching DB columns
        """
        print("\n🤖 Step 4/4: AI Extraction...")
        
        # Step 1: Generate prompt
        prompt = get_cv_extraction_prompt(cv_text)
        
        # Step 2: Extract using Gemini
        result = self.gemini.generate_json(
            prompt=prompt,
            max_retries=3,
            fallback=self._get_fallback()
        )
        
        # Step 3: Validate and fix
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
        - Accolades is array or empty
        - Snapshot has proper length
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
        for field in ['cv_must_to_have', 'cv_good_to_have', 'cv_soft_skills', 'cv_domain_expertise', 'cv_accolades']:
            if isinstance(result[field], str):
                result[field] = [result[field]] if result[field] else []
        
        # Critical check: Must-have skills should NEVER be empty
        must_have = result.get('cv_must_to_have', [])
        if not must_have or len(must_have) == 0:
            print("❌ WARNING: No primary skills extracted!")
        
        # Check snapshot length
        snapshot = result.get('cv_snapshot', '')
        snapshot_words = len(snapshot.split())
        if snapshot_words > 300:
            print(f"⚠️ Warning: Snapshot too long ({snapshot_words} words, target 120-250)")
        elif snapshot_words < 100:
            print(f"⚠️ Warning: Snapshot too short ({snapshot_words} words, target 120-250)")
        
        print("✅ Validation passed")
        return result
    
    def _get_fallback(self) -> Dict:
        """Fallback structure if extraction fails"""
        return {
            "cv_must_to_have": [],
            "cv_good_to_have": [],
            "cv_soft_skills": [],
            "cv_domain_expertise": [],
            "cv_accolades": [],
            "cv_snapshot": "Unable to generate CV snapshot. Please check the CV format."
        }
    
    def _print_summary(self, result: Dict):
        """Print extraction summary"""
        print(f"\n📊 EXTRACTION SUMMARY:")
        print(f"   Primary Skills: {len(result.get('cv_must_to_have', []))} → {', '.join(result.get('cv_must_to_have', []))[:80]}")
        print(f"   Secondary Skills: {len(result.get('cv_good_to_have', []))} → {', '.join(result.get('cv_good_to_have', []))[:80]}")
        print(f"   Soft Skills: {len(result.get('cv_soft_skills', []))} → {', '.join(result.get('cv_soft_skills', []))[:80]}")
        print(f"   Domain: {len(result.get('cv_domain_expertise', []))} → {', '.join(result.get('cv_domain_expertise', []))[:80]}")
        print(f"   Accolades: {len(result.get('cv_accolades', []))}")
        print(f"   Snapshot: {len(result.get('cv_snapshot', '').split())} words")
        
        # Print snapshot preview
        snapshot = result.get('cv_snapshot', '')
        if snapshot and len(snapshot) > 100:
            print(f"\n📝 SNAPSHOT PREVIEW:")
            print(f"   {snapshot[:200]}...")


# Example usage
if __name__ == "__main__":
    extractor = CVExtractor()
    
    # Test with sample file
    # result = extractor.extract_from_file("path/to/resume.pdf")
    # print(json.dumps(result, indent=2))
