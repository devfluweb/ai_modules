"""
JD Extraction Route - FastAPI endpoint
Handles the /api/jd/extract endpoint for two-step extraction
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
import logging

# Import the extractor service
from jd_extractor_service import JDExtractorService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/jd", tags=["JD Extraction"])


# ============================================
# REQUEST/RESPONSE SCHEMAS
# ============================================

class JDExtractRequest(BaseModel):
    """Request schema for JD extraction"""
    jd_text: str = Field(..., min_length=50, description="Raw job description text")
    ai_model: Optional[str] = Field("gemini", description="AI model to use")
    
    @validator("jd_text")
    def validate_jd_text(cls, v):
        if not v or not v.strip():
            raise ValueError("JD text cannot be empty")
        if len(v.strip()) < 50:
            raise ValueError("JD text too short - minimum 50 characters required")
        return v.strip()
    
    @validator("ai_model")
    def validate_ai_model(cls, v):
        allowed_models = ["gemini", "claude", "gpt"]
        if v not in allowed_models:
            raise ValueError(f"AI model must be one of: {allowed_models}")
        return v


class KeywordsData(BaseModel):
    """Schema for extracted keywords"""
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    must_have_skills: Optional[str] = None
    good_to_have_skills: Optional[str] = None
    domain: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    notice_period: Optional[str] = None
    job_description: Optional[str] = None
    responsibilities: Optional[str] = None
    qualifications: Optional[str] = None
    benefits: Optional[str] = None
    remote_work: Optional[str] = None
    visa_sponsorship: Optional[str] = None
    soft_skills: Optional[str] = None
    certifications: Optional[str] = None
    tools_technologies: Optional[str] = None
    education: Optional[str] = None
    team_size: Optional[str] = None
    reporting_to: Optional[str] = None
    work_culture: Optional[str] = None


class JDExtractResponse(BaseModel):
    """Response schema for JD extraction"""
    status: str = Field(..., description="success/partial/failed")
    data: Optional[Dict[str, Any]] = Field(None, description="Extracted data")
    error: Optional[str] = Field(None, description="Error message if failed")
    extraction_time: Optional[str] = Field(None, description="Time taken for extraction")
    steps_completed: Optional[int] = Field(None, description="Number of steps completed")


# ============================================
# ROUTES
# ============================================

@router.post("/extract", response_model=JDExtractResponse)
async def extract_jd_data(request: JDExtractRequest):
    """
    Extract structured data from raw JD text
    
    **Two-Step Process:**
    1. Extract keywords from JD (Step 1)
    2. Generate LinkedIn snapshot (Step 2) - after 2-second delay
    
    **Request Body:**
    ```json
    {
        "jd_text": "Full job description text...",
        "ai_model": "gemini"  // optional: gemini, claude, gpt
    }
    ```
    
    **Response:**
    ```json
    {
        "status": "success",
        "data": {
            "keywords": {
                "job_title": "Senior Software Engineer",
                "company_name": "TechCorp",
                "must_have_skills": "Python, React, AWS",
                ...
            },
            "snapshot": "🚀 Exciting opportunity alert!\n\n**Senior Software Engineer | TechCorp**\n\n..."
        },
        "extraction_time": "0:00:05.234567",
        "steps_completed": 2
    }
    ```
    """
    try:
        logger.info(f"Received JD extraction request - Model: {request.ai_model}, Text length: {len(request.jd_text)}")
        
        # Initialize extractor service
        extractor = JDExtractorService(ai_model=request.ai_model)
        
        # Run extraction (handles both steps with 2-second delay internally)
        result = await extractor.extract_jd_data(request.jd_text)
        
        # Log result
        if result["status"] == "success":
            logger.info(f"✅ Extraction successful - Job: {result['keywords'].get('job_title')}")
        elif result["status"] == "partial":
            logger.warning(f"⚠️ Partial extraction - Keywords extracted but snapshot failed")
        else:
            logger.error(f"❌ Extraction failed - {result.get('error')}")
        
        return JDExtractResponse(**result)
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
        
    except Exception as e:
        logger.error(f"Extraction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        )


@router.post("/extract/keywords-only", response_model=Dict[str, Any])
async def extract_keywords_only(request: JDExtractRequest):
    """
    Extract only keywords (Step 1) without snapshot generation
    
    Useful for testing or when snapshot is not needed
    """
    try:
        logger.info("Extracting keywords only (no snapshot)")
        
        extractor = JDExtractorService(ai_model=request.ai_model)
        keywords_result = await extractor._extract_keywords(request.jd_text)
        
        if not keywords_result["success"]:
            raise HTTPException(status_code=500, detail=keywords_result["error"])
        
        return {
            "status": "success",
            "keywords": keywords_result["data"]
        }
        
    except Exception as e:
        logger.error(f"Keywords extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract/snapshot-only", response_model=Dict[str, Any])
async def extract_snapshot_only(keywords_data: KeywordsData, original_jd: str):
    """
    Generate snapshot (Step 2) from pre-extracted keywords
    
    Useful for regenerating snapshots without re-extracting keywords
    """
    try:
        logger.info("Generating snapshot from provided keywords")
        
        extractor = JDExtractorService()
        snapshot_result = await extractor._generate_snapshot(
            keywords_data.dict(), 
            original_jd
        )
        
        if not snapshot_result["success"]:
            raise HTTPException(status_code=500, detail=snapshot_result["error"])
        
        return {
            "status": "success",
            "snapshot": snapshot_result["data"]
        }
        
    except Exception as e:
        logger.error(f"Snapshot generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# INTEGRATION INSTRUCTIONS
# ============================================

"""
To integrate this route into your main FastAPI app:

1. In backend/main.py:

   from backend.routes import jd_extraction_routes
   
   app.include_router(jd_extraction_routes.router)

2. Ensure dependencies are installed:
   
   pip install google-generativeai  # for Gemini
   pip install anthropic             # for Claude
   pip install openai               # for GPT

3. Set environment variables:
   
   GEMINI_API_KEY=your_gemini_key
   ANTHROPIC_API_KEY=your_claude_key
   OPENAI_API_KEY=your_gpt_key

4. Test the endpoint:
   
   curl -X POST http://localhost:8000/api/jd/extract \
     -H "Content-Type: application/json" \
     -d '{"jd_text": "Your JD text here...", "ai_model": "gemini"}'
"""