# 📁 DEPLOYMENT FOLDER STRUCTURE

## Copy files to your RecTool project like this:

```
REC_1/
├── backend/
│   ├── ai_modules/                           ← CREATE THIS FOLDER
│   │   ├── __init__.py                      ← CREATE EMPTY FILE
│   │   ├── gemini_client_final.py           ← COPY FILE 1
│   │   ├── file_utils_final.py              ← COPY FILE 2
│   │   ├── cv_extraction_prompt_final.py    ← COPY FILE 3
│   │   ├── jd_extraction_prompt_final.py    ← COPY FILE 4
│   │   ├── cv_extractor_final.py            ← COPY FILE 5
│   │   └── jd_extractor_final.py            ← COPY FILE 6
│   │
│   ├── config.env                           ← ADD GEMINI_API_KEY HERE
│   ├── services/
│   │   └── jd_service.py                    ← INTEGRATE HERE
│   └── ...
│
├── core/
│   └── cv/
│       └── services/
│           └── cv_services.py               ← INTEGRATE HERE
│
└── docs/
    └── IMPLEMENTATION_GUIDE.md              ← COPY FILE 7 (REFERENCE)
```

---

## Step-by-Step Setup

### 1. Create Folder
```bash
cd REC_1/backend
mkdir ai_modules
cd ai_modules
touch __init__.py
```

### 2. Copy Files
```bash
# Copy all 6 Python files to backend/ai_modules/
cp /path/to/downloads/gemini_client_final.py .
cp /path/to/downloads/file_utils_final.py .
cp /path/to/downloads/cv_extraction_prompt_final.py .
cp /path/to/downloads/jd_extraction_prompt_final.py .
cp /path/to/downloads/cv_extractor_final.py .
cp /path/to/downloads/jd_extractor_final.py .
```

### 3. Add API Key
```bash
# Edit backend/config.env
echo "GEMINI_API_KEY=your_api_key_here" >> backend/config.env
```

### 4. Install Dependencies
```bash
pip install google-generativeai PyMuPDF python-docx python-dotenv
```

---

## Integration Example

### In JD Service (backend/services/jd_service.py)

```python
# Add import at top
from ai_modules.jd_extractor_final import JDExtractor

class JDService:
    def __init__(self):
        self.jd_extractor = JDExtractor()
    
    def create_jd(self, jd_data: JDCreate, db: Session):
        # Extract if raw text provided
        if jd_data.raw_jd_text:
            extracted = self.jd_extractor.extract_from_text(jd_data.raw_jd_text)
            
            # Populate fields
            jd_data.must_have_skills = ", ".join(extracted["must_have_skills"])
            jd_data.good_to_have_skills = ", ".join(extracted["good_to_have_skills"])
            jd_data.soft_skills = ", ".join(extracted["soft_skills"])
            jd_data.domain_expertise = ", ".join(extracted["domain_expertise"])
            jd_data.accolades_keyword = extracted["accolades_keyword"]
            jd_data.exception_skills = extracted["exception_skills"]
            jd_data.jd_snapshot = extracted["jd_snapshot"]
        
        # Continue normal JD creation...
```

### In CV Service (core/cv/services/cv_services.py)

```python
# Add import at top
import sys
sys.path.append('../../backend')  # Adjust path as needed
from ai_modules.cv_extractor_final import CVExtractor

class CVService:
    def __init__(self):
        self.cv_extractor = CVExtractor()
    
    def process_cv_upload(self, file_path: str, cv_id: int, db: Session):
        # Extract from uploaded file
        extracted = self.cv_extractor.extract_from_file(file_path)
        
        # Update CV in database
        cv = db.query(CVTable).filter(CVTable.cv_id == cv_id).first()
        
        if cv:
            cv.cv_must_to_have = ", ".join(extracted["cv_must_to_have"])
            cv.cv_good_to_have = ", ".join(extracted["cv_good_to_have"])
            cv.cv_soft_skills = ", ".join(extracted["cv_soft_skills"])
            cv.cv_domain_expertise = ", ".join(extracted["cv_domain_expertise"])
            cv.cv_accolades = ", ".join(extracted["cv_accolades"])
            cv.cv_snapshot = extracted["cv_snapshot"]
            cv.cv_total_words = extracted["cv_total_words"]
            
            db.commit()
```

---

## Test Script

Create `backend/ai_modules/test_extraction.py`:

```python
"""Test extraction locally before deployment"""

from cv_extractor_final import CVExtractor
from jd_extractor_final import JDExtractor

# Test CV
print("Testing CV Extraction...")
cv_extractor = CVExtractor()
cv_result = cv_extractor.extract_from_file("path/to/test_resume.pdf")
print(f"✅ CV Primary Skills: {cv_result['cv_must_to_have']}")

# Test JD
print("\nTesting JD Extraction...")
jd_extractor = JDExtractor()
jd_text = """
Senior Python Developer
5+ years required
Must have: Python, Django, AWS
Nice to have: Docker
"""
jd_result = jd_extractor.extract_from_text(jd_text)
print(f"✅ JD Must-Have: {jd_result['must_have_skills']}")

print("\n✅ All tests passed!")
```

Run test:
```bash
cd backend/ai_modules
python test_extraction.py
```

---

## Railway Deployment

### 1. Update requirements.txt
```txt
# Add to backend/requirements.txt
google-generativeai==0.3.2
PyMuPDF==1.23.8
python-docx==1.1.0
```

### 2. Set Environment Variable on Railway
```
Dashboard → Variables → Add
GEMINI_API_KEY = your_api_key_here
```

### 3. Deploy
```bash
git add backend/ai_modules/
git commit -m "Add AI extraction module"
git push origin main
```

Railway will auto-deploy.

---

## Verification Checklist

After deployment:
- [ ] Files in correct folder structure
- [ ] `__init__.py` exists in ai_modules/
- [ ] GEMINI_API_KEY in environment
- [ ] Dependencies installed
- [ ] Test script runs locally
- [ ] Integration in JD service works
- [ ] Integration in CV service works
- [ ] Railway deployment successful
- [ ] Test extraction on Railway

---

**Ready to deploy! Follow this structure exactly.** 🚀
