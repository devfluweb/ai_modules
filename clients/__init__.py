
"""
Clients Module
API and storage clients for AI modules
"""

from .gemini_client import GeminiClient, get_gemini_client

# R2Client import is optional (not yet implemented)
try:
    from .r2_client import R2Client, get_r2_client
    __all__ = [
        "GeminiClient",
        "get_gemini_client",
        "R2Client", 
        "get_r2_client"
    ]
except ImportError:
    # R2 client not yet implemented
    __all__ = [
        "GeminiClient",
        "get_gemini_client"
    ]