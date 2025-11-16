"""
Matchmaker Schemas
Pydantic models for matchmaking API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class MatchmakerRequest(BaseModel):
    """Request schema for JD-to-CV matching"""
    jd_id: int = Field(..., description="Job Description ID to match CVs against")
    min_match_percentage: Optional[int] = Field(
        60, 
        ge=0, 
        le=100, 
        description="Minimum match percentage to return (default 60%)"
    )


class ScoreBreakdown(BaseModel):
    """Detailed score breakdown for a match"""
    must_have: int = Field(..., description="Must-have skills score (0-40)")
    good_to_have: int = Field(..., description="Good-to-have skills score (0-25)")
    soft_skills: int = Field(..., description="Soft skills score (0-15)")
    domain: int = Field(..., description="Domain expertise score (0-10)")
    experience: int = Field(..., description="Experience fit score (0-10)")
    accolades: int = Field(..., description="Accolades bonus (0-10)")
    penalties: int = Field(..., description="Exception penalties (can be negative)")


class CVMatch(BaseModel):
    """Individual CV match result"""
    cv_id: int
    cv_name: str
    cv_email: str
    cv_mobile: str
    cv_experience: Optional[float]
    cv_current_company: Optional[str]
    cv_role: Optional[str]
    match_percentage: int = Field(..., ge=0, le=100)
    rating: int = Field(..., ge=1, le=5, description="Star rating (1-5)")
    breakdown: ScoreBreakdown
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)


class MatchmakerResponse(BaseModel):
    """Response schema for matchmaking results"""
    jd_id: int
    jd_title: str
    jd_company: str
    total_filtered_cvs: int = Field(..., description="CVs after Stage 1 SQL filtering")
    total_matched_cvs: int = Field(..., description="CVs above min match percentage")
    processing_time_seconds: float
    matches: List[CVMatch] = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "jd_id": 123,
                "jd_title": "Senior Python Developer",
                "jd_company": "TechCorp",
                "total_filtered_cvs": 100,
                "total_matched_cvs": 45,
                "processing_time_seconds": 12.5,
                "matches": [
                    {
                        "cv_id": 456,
                        "cv_name": "John Doe",
                        "cv_email": "john@example.com",
                        "cv_mobile": "9876543210",
                        "cv_experience": 7.5,
                        "cv_current_company": "ABC Corp",
                        "cv_role": "Python Developer",
                        "match_percentage": 85,
                        "rating": 4,
                        "breakdown": {
                            "must_have": 32,
                            "good_to_have": 20,
                            "soft_skills": 12,
                            "domain": 10,
                            "experience": 10,
                            "accolades": 1,
                            "penalties": 0
                        },
                        "matched_skills": ["Python", "Django", "AWS"],
                        "missing_skills": ["Kubernetes"]
                    }
                ]
            }
        }


class AIBatchRequest(BaseModel):
    """Internal schema for AI batch processing"""
    jd_keywords: Dict[str, List[str]]
    cvs: List[Dict]


class AIBatchResponse(BaseModel):
    """Internal schema for AI batch response"""
    matches: List[Dict]