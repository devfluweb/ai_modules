"""
Gemini 2.5 Flash API Client - Production Ready
Model: gemini-2.5-flash (stable)
Cost: $0.30 input / $2.50 output per 1M tokens
"""

import os
import json
import google.generativeai as genai
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import time

class GeminiClient:
    """
    Centralized Gemini 2.5 Flash client for all AI operations.
    Handles authentication, rate limiting, retries, and error handling.
    """
    
    def __init__(self):
        """Initialize Gemini 2.5 Flash with API key"""
        load_dotenv()
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash (stable, best for structured extraction)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
        print("✅ Gemini 2.5 Flash Client initialized")
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def generate_json(
        self, 
        prompt: str, 
        max_retries: int = 3,
        fallback: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate JSON response from Gemini 2.5 Flash.
        
        Args:
            prompt: The prompt to send
            max_retries: Number of retry attempts on failure
            fallback: Fallback response if all retries fail
        
        Returns:
            Dict containing the parsed JSON response
        """
        for attempt in range(max_retries):
            try:
                # Rate limiting
                self._wait_for_rate_limit()
                
                # Generate content with Gemini 2.5 Flash
                response = self.model.generate_content(prompt)
                
                # Extract text
                response_text = response.text.strip()
                
                # Clean response (remove markdown if present)
                if response_text.startswith("```json"):
                    response_text = response_text.replace("```json", "").replace("```", "").strip()
                
                # Parse JSON
                parsed = json.loads(response_text)
                
                print(f"✅ Gemini 2.5 Flash: Successful extraction (attempt {attempt + 1})")
                return parsed
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed (attempt {attempt + 1}/{max_retries})")
                print(f"   Error: {e}")
                print(f"   Response preview: {response_text[:200]}...")
                
                if attempt < max_retries - 1:
                    print("   Retrying in 1 second...")
                    time.sleep(1)
                    continue
                else:
                    print(f"❌ All retries exhausted. Using fallback.")
                    return fallback or self._get_empty_fallback()
            
            except Exception as e:
                print(f"❌ Gemini API error (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt < max_retries - 1:
                    print("   Retrying in 2 seconds...")
                    time.sleep(2)
                    continue
                else:
                    print("❌ Using fallback after API errors")
                    return fallback or self._get_empty_fallback()
        
        return fallback or self._get_empty_fallback()
    
    def _get_empty_fallback(self) -> Dict:
        """Default empty fallback structure"""
        return {
            "error": "Extraction failed after all retries",
            "data": {}
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model": "gemini-2.5-flash",
            "status": "stable",
            "pricing": {
                "input": "$0.30 per 1M tokens",
                "output": "$2.50 per 1M tokens",
                "cv_extraction_cost": "$0.00225",
                "jd_extraction_cost": "$0.00180"
            },
            "features": [
                "Native JSON mode",
                "Thinking mode enabled",
                "1M token context window",
                "Fast inference (<3 sec)"
            ]
        }

# Singleton instance
_gemini_client = None

def get_gemini_client() -> GeminiClient:
    """Get or create the singleton Gemini client"""
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
