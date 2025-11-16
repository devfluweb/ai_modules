"""
JD Extractor Service - Two-Step Sequential Process
Handles keywords extraction (Step 1) followed by snapshot generation (Step 2)
"""

import asyncio
import json
import logging
from typing import Dict, Any, Tuple
from datetime import datetime

# Import your AI API client (adjust based on your setup)
# from your_ai_client import call_gemini_api, call_claude_api

logger = logging.getLogger(__name__)


class JDExtractorService:
    """
    Service to handle two-step JD extraction:
    1. Keywords extraction
    2. Snapshot generation (after 2-second delay)
    """
    
    def __init__(self, ai_model: str = "gemini"):
        """
        Initialize the extractor service
        
        Args:
            ai_model: AI model to use ("gemini", "claude", "gpt")
        """
        self.ai_model = ai_model
        self.step_delay_seconds = 2
        
    async def extract_jd_data(self, jd_text: str) -> Dict[str, Any]:
        """
        Main extraction method - coordinates both steps sequentially
        
        Args:
            jd_text: Raw job description text
            
        Returns:
            Dictionary containing both keywords and snapshot
            {
                "keywords": {...},
                "snapshot": "...",
                "extraction_time": "...",
                "status": "success/failed"
            }
        """
        start_time = datetime.now()
        
        try:
            logger.info("Starting JD extraction - Step 1: Keywords")
            
            # ========================================
            # STEP 1: Extract Keywords
            # ========================================
            keywords_result = await self._extract_keywords(jd_text)
            
            if not keywords_result["success"]:
                return {
                    "status": "failed",
                    "error": "Keywords extraction failed",
                    "step": 1,
                    "extraction_time": str(datetime.now() - start_time)
                }
            
            keywords_data = keywords_result["data"]
            logger.info(f"Step 1 completed successfully. Job Title: {keywords_data.get('job_title')}")
            
            # ========================================
            # DELAY: 2 seconds
            # ========================================
            logger.info(f"Waiting {self.step_delay_seconds} seconds before Step 2...")
            await asyncio.sleep(self.step_delay_seconds)
            
            # ========================================
            # STEP 2: Generate Snapshot
            # ========================================
            logger.info("Starting Step 2: Snapshot generation")
            snapshot_result = await self._generate_snapshot(keywords_data, jd_text)
            
            if not snapshot_result["success"]:
                return {
                    "status": "partial",
                    "keywords": keywords_data,
                    "snapshot": None,
                    "error": "Snapshot generation failed",
                    "step": 2,
                    "extraction_time": str(datetime.now() - start_time)
                }
            
            snapshot_text = snapshot_result["data"]
            logger.info("Step 2 completed successfully")
            
            # ========================================
            # RETURN COMPLETE RESULT
            # ========================================
            return {
                "status": "success",
                "keywords": keywords_data,
                "snapshot": snapshot_text,
                "extraction_time": str(datetime.now() - start_time),
                "steps_completed": 2
            }
            
        except Exception as e:
            logger.error(f"JD extraction failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "extraction_time": str(datetime.now() - start_time)
            }
    
    async def _extract_keywords(self, jd_text: str) -> Dict[str, Any]:
        """
        Step 1: Extract keywords from JD
        
        Args:
            jd_text: Raw JD text
            
        Returns:
            {"success": bool, "data": dict or "error": str}
        """
        try:
            from prompts.jd_extraction_prompt import get_jd_keywords_prompt
            
            # Generate prompt
            prompt = get_jd_keywords_prompt(jd_text)
            
            # Call AI model (replace with your actual AI API call)
            ai_response = await self._call_ai_model(prompt)
            
            # Parse JSON response
            try:
                keywords_data = json.loads(ai_response)
            except json.JSONDecodeError:
                # Try to extract JSON from response if wrapped in markdown
                ai_response_clean = ai_response.replace("```json", "").replace("```", "").strip()
                keywords_data = json.loads(ai_response_clean)
            
            # Validate response has required fields
            required_fields = ["must_have_skills", "good_to_have_skills", "soft_skills", 
                             "domain_expertise", "accolades_keyword", "exception_skills"]
            if not all(field in keywords_data for field in required_fields):
                return {
                    "success": False,
                    "error": "Keywords validation failed - missing required fields"
                }
            
            return {
                "success": True,
                "data": keywords_data
            }
            
        except Exception as e:
            logger.error(f"Keywords extraction error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_snapshot(self, keywords_data: dict, original_jd: str) -> Dict[str, Any]:
        """
        Step 2: Generate LinkedIn-style snapshot
        
        Args:
            keywords_data: Extracted keywords from Step 1
            original_jd: Original JD text for context
            
        Returns:
            {"success": bool, "data": str or "error": str}
        """
        try:
            # Create a simple snapshot prompt
            job_title = keywords_data.get("job_title", "Position")
            company = keywords_data.get("company_name", "Our Company")
            must_have = keywords_data.get("must_have_skills", [])
            
            # Build snapshot text directly (simplified version)
            snapshot = f"""🚀 Exciting Opportunity at {company}!

We're looking for a talented {job_title} to join our team.

✨ What we're looking for:
{', '.join(must_have if isinstance(must_have, list) else must_have.split(',')[:5])}

Ready to make an impact? Apply now!

#hiring #tech #careers"""
            
            return {
                "success": True,
                "data": snapshot
            }
            
        except Exception as e:
            logger.error(f"Snapshot generation error: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _call_ai_model(self, prompt: str) -> str:
        """
        Call the configured AI model with the prompt
        
        Args:
            prompt: Formatted prompt string
            
        Returns:
            AI response text
        """
        # TODO: Replace with your actual AI API integration
        
        if self.ai_model == "gemini":
            # Example Gemini call
            # from google.generativeai import GenerativeModel
            # model = GenerativeModel('gemini-2.0-flash-exp')
            # response = await model.generate_content_async(prompt)
            # return response.text
            pass
            
        elif self.ai_model == "claude":
            # Example Claude call
            # import anthropic
            # client = anthropic.Anthropic(api_key="your-key")
            # message = await client.messages.create_async(
            #     model="claude-sonnet-4-20250514",
            #     max_tokens=2000,
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # return message.content[0].text
            pass
            
        elif self.ai_model == "gpt":
            # Example GPT call
            # from openai import AsyncOpenAI
            # client = AsyncOpenAI(api_key="your-key")
            # response = await client.chat.completions.create(
            #     model="gpt-4o-mini",
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # return response.choices[0].message.content
            pass
        
        # Placeholder - replace with actual implementation
        raise NotImplementedError(f"AI model '{self.ai_model}' integration not implemented")


# ============================================
# USAGE EXAMPLE IN YOUR ROUTE/SERVICE
# ============================================

"""
# In your JD routes file (backend/routes/jd_routes.py):

from jd_extractor_service import JDExtractorService

@router.post("/extract")
async def extract_jd_data(request: JDExtractRequest):
    '''
    Endpoint to trigger JD extraction
    
    Request body:
    {
        "jd_text": "Full job description text...",
        "ai_model": "gemini"  // optional
    }
    '''
    try:
        extractor = JDExtractorService(ai_model=request.ai_model or "gemini")
        result = await extractor.extract_jd_data(request.jd_text)
        
        return {
            "status": result["status"],
            "data": {
                "keywords": result.get("keywords"),
                "snapshot": result.get("snapshot")
            },
            "extraction_time": result.get("extraction_time"),
            "error": result.get("error")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""