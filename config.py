
"""
AI Modules Configuration
Centralized configuration for extraction and matching services
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration for AI modules"""
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_RATE_LIMIT_MS: int = 100  # Minimum ms between requests
    GEMINI_MAX_RETRIES: int = 3
    
    # R2 Storage Configuration
    R2_ACCOUNT_ID: str = os.getenv("R2_ACCOUNT_ID", "")
    R2_ACCESS_KEY_ID: str = os.getenv("R2_ACCESS_KEY_ID", "")
    R2_SECRET_ACCESS_KEY: str = os.getenv("R2_SECRET_ACCESS_KEY", "")
    R2_BUCKET_NAME: str = os.getenv("R2_BUCKET_NAME", "cv-pdf")
    R2_ENDPOINT_URL: Optional[str] = None  # Auto-generated from account_id
    
    # File Processing Configuration
    PDF_MIN_WORDS: int = 50
    DOCX_MIN_WORDS: int = 50
    MAX_FILE_SIZE_MB: int = 10
    
    # Extraction Configuration
    CV_SNAPSHOT_MIN_WORDS: int = 120
    CV_SNAPSHOT_MAX_WORDS: int = 250
    JD_SNAPSHOT_TARGET_WORDS: int = 200
    CV_RECENT_EXPERIENCE_YEARS: int = 4
    
    # Matching Configuration
    MATCH_MIN_SCORE: int = 0
    MATCH_MAX_SCORE: int = 100
    MATCH_WEIGHTS = {
        "must_have_skills": 40,
        "domain_expertise": 25,
        "soft_skills": 15,
        "good_to_have_skills": 20
    }
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required = [
            ("GEMINI_API_KEY", cls.GEMINI_API_KEY),
            ("R2_ACCOUNT_ID", cls.R2_ACCOUNT_ID),
            ("R2_ACCESS_KEY_ID", cls.R2_ACCESS_KEY_ID),
            ("R2_SECRET_ACCESS_KEY", cls.R2_SECRET_ACCESS_KEY),
        ]
        
        missing = [name for name, value in required if not value]
        
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def get_r2_endpoint(cls) -> str:
        """Generate R2 endpoint URL from account ID"""
        if not cls.R2_ACCOUNT_ID:
            raise ValueError("R2_ACCOUNT_ID not configured")
        return f"https://{cls.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"


# Singleton config instance
config = Config()