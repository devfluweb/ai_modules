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
from utils.r2_client import get_r2_client  # NEW IMPORT

class CVExtractor:
    """
    Extract skills, domain, accolades, and snapshot from CVs.
    Supports: Local files, R2 bucket files
    """
    
    def __init__(self):
        """Initialize CV extractor with Gemini + R2 clients"""
        self.gemini = get_gemini_client()
        self.file_extractor = FileTextExtractor()
        self.r2_client = get_r2_client()  # NEW
        print("✅ CV Extractor initialized (Gemini 2.5 Flash + R2)")
    
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
        - Don't start with / or C:\ 
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
        try:
            # Check if file exists in R2
            if not self.r2_client.file_exists(r2_key):
                raise FileNotFoundError(f"File not found in R2: {r2_key}")
            
            # Get f
