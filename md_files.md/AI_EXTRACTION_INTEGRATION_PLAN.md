# 🔌 AI EXTRACTION MODULES - RECTOOL INTEGRATION PLAN

## 📁 WHAT YOU HAVE (Uploaded Files)

### ✅ Working Modules
1. **jd_extractor.py** (Flask on port 5000)
   - `/extract-keywords` → Extracts must_have, good_to_have, soft_skills
   - `/generate-snapshot` → Creates social media snapshot
   
2. **cv_extractor.py** (Flask on port 5001)
   - `/extract-text` → PDF/DOCX text extraction
   - `/analyze-text` → Extracts primary/secondary/soft skills + snapshot

3. **prompts.py** → AI prompt templates (Gemini)
   - `get_jd_skill_extraction_prompt()` ✅
   - `get_snapshot_generation_prompt()` ✅
   - `get_cv_skill_extraction_prompt()` ✅
   - `get_cv_snapshot_generation_prompt()` ✅

4. **.env** → GEMINI_API_KEY configured ✅

---

## 🎯 INTEGRATION STRATEGY

### Option 1: Microservices Architecture (Current Setup)
**Keep Flask services separate, call them from RecTool backend**

**Pros:**
- Already working ✅
- Easy to deploy independently
- Language agnostic (Flask + FastAPI)

**Cons:**
- Network overhead (HTTP calls between services)
- Need to manage 3 servers (JD extractor, CV extractor, RecTool backend)
- More complex deployment

**Implementation:**
```python
# backend/services/ai_extraction_client.py
import requests

class AIExtractionClient:
    JD_EXTRACTOR_URL = "http://localhost:5000"
    CV_EXTRACTOR_URL = "http://localhost:5001"
    
    @staticmethod
    def extract_jd_keywords(jd_text: str):
        response = requests.post(
            f"{AIExtractionClient.JD_EXTRACTOR_URL}/extract-keywords",
            json={"jd_text": jd_text}
        )
        return response.json()
    
    @staticmethod
    def extract_cv_skills(cv_text: str):
        response = requests.post(
            f"{AIExtractionClient.CV_EXTRACTOR_URL}/analyze-text",
            json={"cv_text": cv_text}
        )
        return response.json()
```

---

### Option 2: Direct Integration (Recommended) ⭐
**Convert Flask logic to Python services, integrate directly into RecTool backend**

**Pros:**
- Single backend server ✅
- Faster (no network calls)
- Easier deployment (one Railway service)
- Better error handling

**Cons:**
- Need to refactor Flask code slightly
- RecTool backend becomes dependent on Gemini

**Implementation:**
```
backend/
├── services/
│   ├── jd_service.py (existing)
│   ├── cv_service.py (existing)
│   ├── ai_extraction_service.py  ← NEW (contains all AI logic)
│   ├── matchmaker_orchestrator.py ← NEW
│   └── ...
├── ai_prompts/
│   └── prompts.py  ← COPY from your upload
```

---

## 🚀 IMPLEMENTATION PLAN (Option 2 - Recommended)

### Step 1: Copy Files to RecTool Backend
```bash
# Create AI module structure
mkdir -p backend/services/ai_extraction
mkdir -p backend/ai_prompts

# Copy your files
cp prompts.py backend/ai_prompts/
cp requirements.txt backend/requirements_ai.txt
```

### Step 2: Create Unified AI Extraction Service

**File:** `backend/services/ai_extraction_service.py`
```python
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any

# Import prompts
import sys
sys.path.append(os.path.dirname(__file__))
from ..ai_prompts.prompts import (
    get_jd_skill_extraction_prompt,
    get_snapshot_generation_prompt,
    get_cv_skill_extraction_prompt,
    get_cv_snapshot_generation_prompt
)

class AIExtractionService:
    def __init__(self):
        # Load Gemini API key from .env
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    def extract_jd_keywords(self, jd_text: str) -> Dict[str, Any]:
        """Extract must_have, good_to_have, soft_skills from JD"""
        try:
            prompt = get_jd_skill_extraction_prompt(jd_text)
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"❌ JD keyword extraction failed: {e}")
            return {
                "must_have_skills": [],
                "good_to_have_skills": [],
                "soft_skills": []
            }
    
    def generate_jd_snapshot(self, jd_text: str) -> str:
        """Generate social media snapshot from JD"""
        try:
            prompt = get_snapshot_generation_prompt(jd_text)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ JD snapshot generation failed: {e}")
            return "Error generating snapshot"
    
    def extract_cv_skills(self, cv_text: str) -> Dict[str, Any]:
        """Extract primary, secondary, soft skills from CV"""
        try:
            prompt = get_cv_skill_extraction_prompt(cv_text)
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"❌ CV skill extraction failed: {e}")
            return {
                "primary_technical_skills": [],
                "secondary_technical_skills": [],
                "soft_skills": []
            }
    
    def generate_cv_snapshot(self, cv_text: str) -> str:
        """Generate professional CV snapshot"""
        try:
            prompt = get_cv_snapshot_generation_prompt(cv_text)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ CV snapshot generation failed: {e}")
            return "Error generating CV snapshot"
```

### Step 3: Integrate into JD Service

**Modify:** `backend/services/jd_service.py`
```python
from .ai_extraction_service import AIExtractionService

class JDService:
    def __init__(self):
        # ... existing init ...
        self.ai_service = AIExtractionService()
    
    def create_jd(self, jd_data: JDCreate, db: Session) -> JDResponse:
        """Create JD with AI keyword extraction"""
        
        # 1. If raw_jd_text exists, extract keywords
        if jd_data.raw_jd_text:
            extracted = self.ai_service.extract_jd_keywords(jd_data.raw_jd_text)
            
            # Auto-populate skills fields if empty
            if not jd_data.must_have_skills:
                jd_data.must_have_skills = ", ".join(extracted["must_have_skills"])
            if not jd_data.good_to_have_skills:
                jd_data.good_to_have_skills = ", ".join(extracted["good_to_have_skills"])
            if not jd_data.soft_skills:
                jd_data.soft_skills = ", ".join(extracted["soft_skills"])
            
            # Generate snapshot
            if not jd_data.jd_snapshot:
                jd_data.jd_snapshot = self.ai_service.generate_jd_snapshot(jd_data.raw_jd_text)
        
        # 2. Continue with existing JD creation logic
        db_jd = JD(**jd_data.model_dump())
        db.add(db_jd)
        db.commit()
        # ... rest of existing code ...
```

### Step 4: Integrate into CV Service

**Modify:** `core/cv/services/cv_services.py`
```python
from backend.services.ai_extraction_service import AIExtractionService
import PyPDF2
import docx

class CVService:
    def __init__(self):
        # ... existing init ...
        self.ai_service = AIExtractionService()
    
    def process_cv_file(self, file_path: str, cv_id: int, db: Session):
        """Process uploaded CV file and extract keywords"""
        
        # 1. Extract text from file
        cv_text = self._extract_text_from_file(file_path)
        
        # 2. Extract skills using AI
        skills = self.ai_service.extract_cv_skills(cv_text)
        
        # 3. Generate snapshot
        snapshot = self.ai_service.generate_cv_snapshot(cv_text)
        
        # 4. Update CV record
        cv = db.query(CVTable).filter(CVTable.cv_id == cv_id).first()
        if cv:
            cv.cv_must_to_have = ", ".join(skills["primary_technical_skills"])
            cv.cv_good_to_have = ", ".join(skills["secondary_technical_skills"])
            cv.cv_soft_skills = ", ".join(skills["soft_skills"])
            cv.cv_snapshot = snapshot
            cv.cv_total_words = len(cv_text.split())
            db.commit()
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        if file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._extract_from_docx(file_path)
        return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        return "".join(page.get_text() for page in doc)
    
    def _extract_from_docx(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
```

### Step 5: Add New Dependencies

**Update:** `backend/requirements.txt`
```txt
# Existing dependencies
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
...

# Add AI extraction dependencies
google-generativeai
PyMuPDF
python-docx
```

### Step 6: Environment Variables

**Update:** `backend/config.env`
```env
# Existing config
DB_USER=jd_user
DB_PASSWORD=jd_password
...

# Add Gemini API Key
GEMINI_API_KEY=AIzaSyCNgdmNYcQLrj0Cx0iNUELPTtXqg6AmVjU
```

---

## 🎯 MATCHMAKING INTEGRATION

Now that we have keyword extraction, create the matchmaker:

**File:** `backend/services/matchmaker_orchestrator.py`
```python
from typing import List, Dict
from sqlalchemy.orm import Session
from .ai_extraction_service import AIExtractionService

class MatchmakerOrchestrator:
    def __init__(self):
        self.ai_service = AIExtractionService()
    
    def match_jd_to_cvs(self, jd_id: int, db: Session) -> List[Dict]:
        """
        Stage 1: Pre-filter CVs
        Stage 2: AI-powered matching
        Stage 3: Update CV table
        """
        
        # Get JD
        jd = db.query(JD).filter(JD.id == jd_id).first()
        
        # Stage 1: SQL pre-filtering
        cvs = self._stage1_prefilter(jd, db)
        
        # Stage 2: AI matching
        matches = self._stage2_ai_matching(jd, cvs)
        
        # Stage 3: Update CV table
        self._stage3_update_cvs(matches, db)
        
        return matches
    
    def _stage1_prefilter(self, jd, db):
        """Filter CVs by experience, budget, status"""
        query = db.query(CVTable).filter(
            CVTable.cv_experience >= jd.op_experience_min,
            CVTable.cv_experience <= jd.op_experience_max,
            CVTable.cv_ectc >= jd.op_budget_min,
            CVTable.cv_ectc <= jd.op_budget_max,
            CVTable.cv_stage.in_(['Screening Negotiation', 'Shortlisted', 'Interview']),
            CVTable.cv_status.in_(['Staging', 'Reviewed']),
            CVTable.cv_active == True
        )
        return query.all()
    
    def _stage2_ai_matching(self, jd, cvs):
        """Use AI to calculate match percentage"""
        matches = []
        for cv in cvs:
            # Build matching prompt
            match_result = self._calculate_match(jd, cv)
            matches.append(match_result)
        
        # Sort by match percentage
        matches.sort(key=lambda x: x['match_percentage'], reverse=True)
        return matches
    
    def _calculate_match(self, jd, cv):
        """AI-powered match calculation"""
        prompt = self._build_matching_prompt(jd, cv)
        response = self.ai_service.model.generate_content(prompt)
        
        # Parse AI response
        result = json.loads(response.text)
        return {
            "cv_id": cv.cv_id,
            "match_percentage": result["match_percentage"],
            "rating": result["rating"],
            "recommendation": result["cv_recommendation"]
        }
```

---

## 📋 DEPLOYMENT CHECKLIST

### Railway Deployment
1. [ ] Add GEMINI_API_KEY to Railway environment variables
2. [ ] Update backend/requirements.txt with new dependencies
3. [ ] Deploy backend to Railway
4. [ ] Test keyword extraction endpoints
5. [ ] Test matchmaking flow

### Testing Plan
1. [ ] Test JD keyword extraction with sample JD text
2. [ ] Test CV keyword extraction with sample resume
3. [ ] Test full matchmaking pipeline (JD → CVs)
4. [ ] Verify database updates (match%, rating, recommendation)

---

## ❓ NEXT STEPS - YOUR INPUT NEEDED

1. **Which integration approach?**
   - Option 1: Keep Flask services separate (microservices)
   - Option 2: Direct integration into backend (recommended) ⭐

2. **Prompt tuning needed?**
   - Current prompts output: must_have, good_to_have, soft_skills
   - Do we need to add: domain_expertise, accolades, exception_skills?

3. **Matchmaking scoring weights?**
   - Must-have: 40 points
   - Good-to-have: 25 points
   - Soft skills: 15 points
   - Domain: 10 points
   - Experience: 10 points
   - Are these weights good or need adjustment?

4. **Cost considerations?**
   - Gemini API pricing: ~$0.00015 per 1000 characters
   - Estimate: 100 CVs vs 1 JD = ~$0.015 per match run
   - Is this budget acceptable?

Let me know your preference and I'll implement! 🚀
