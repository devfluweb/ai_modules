"""
Matchmaker Routes
FastAPI endpoint for JD-to-CV matching
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from matchmaker_service import get_matchmaker_service
from matchmaker_schemas import MatchmakerRequest, MatchmakerResponse

# Import database dependency
import sys
import os
backend_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, backend_path)
from backend.models.database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/matchmaker",
    tags=["matchmaker"]
)


@router.post(
    "/jd-to-cv",
    response_model=MatchmakerResponse,
    status_code=status.HTTP_200_OK,
    summary="Match CVs to a Job Description",
    description="""
    Find matching CVs for a given Job Description using AI-powered 3-stage matching.
    
    **Stage 1:** SQL pre-filtering (experience, budget, stage, status)
    **Stage 2:** AI similarity detection + Python scoring (100-point system)
    **Stage 3:** Database updates (cv_match_perc, cv_rating, date_of_match)
    
    **Scoring Breakdown:**
    - Must-have skills: 40 points
    - Good-to-have skills: 25 points
    - Soft skills: 15 points
    - Domain expertise: 10 points
    - Experience fit: 10 points
    - Accolades bonus: +10 points
    - Exception penalties: -50 points per violation
    
    **Rating System:**
    - 90-100%: 5 stars ⭐⭐⭐⭐⭐
    - 75-89%: 4 stars ⭐⭐⭐⭐
    - 60-74%: 3 stars ⭐⭐⭐
    - 40-59%: 2 stars ⭐⭐
    - 0-39%: 1 star ⭐
    """
)
async def match_jd_to_cv(
    request: MatchmakerRequest,
    db: Session = Depends(get_db)
):
    """
    Match CVs to a Job Description
    
    Args:
        request: MatchmakerRequest with jd_id and min_match_percentage
        db: Database session (injected)
    
    Returns:
        MatchmakerResponse with list of matched CVs sorted by match %
    
    Raises:
        404: JD not found
        500: Processing error
    """
    try:
        logger.info(f"Matchmaking request: JD {request.jd_id}, min threshold {request.min_match_percentage}%")
        
        # Get matchmaker service
        service = get_matchmaker_service()
        
        # Run matchmaking
        result = service.match_jd_to_cvs(
            jd_id=request.jd_id,
            min_match_percentage=request.min_match_percentage,
            db=db
        )
        
        logger.info(f"Matchmaking complete: {result.total_matched_cvs}/{result.total_filtered_cvs} CVs matched")
        
        return result
        
    except ValueError as e:
        # JD not found or validation error
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
    except Exception as e:
        # Unexpected error
        logger.error(f"Matchmaking failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Matchmaking failed: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if matchmaker service is operational"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "matchmaker",
        "version": "1.0.0"
    }


# Export router
__all__ = ['router']