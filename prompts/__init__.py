
"""
Prompts Module
AI prompt templates for extraction
"""

from .cv_extraction_prompt import get_cv_extraction_prompt
from .jd_extraction_prompt import get_jd_extraction_prompt

__all__ = [
    "get_cv_extraction_prompt",
    "get_jd_extraction_prompt"
]