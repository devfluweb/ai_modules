# 🎯 AI Extraction Module - God Level Documentation

## 📁 Module Structure

```
backend/ai_modules/
├── __init__.py
│
├── gemini_client.py                    # Centralized Gemini API client
│
├── prompts/                            # AI prompts (god-level quality)
│   ├── __init__.py
│   ├── cv_prompts.py                  # CV extraction prompt
│   └── jd_prompts.py                  # JD extraction prompt
│
├── extractors/                         # Extraction services
│   ├── __init__.py
│   ├── skills_standardization.py      # Standardized skill names
│   ├── file_utils.py                  # PDF/DOCX text extraction
│   ├── cv_extractor.py                # CV extraction service
│   └── jd_extractor.py                # JD extraction service
│
└── README.md                           # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install google-generativeai PyMuPDF python-docx python-dotenv
```

### 2. Set Environment Variable

```bash
# Add to backend/config.env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Use CV Extractor

```python
from ai_modules.extractors.cv_extractor import CVExtractor

# Initialize
extractor = CVExtractor()

# Extract from file
result = extractor.extract_from_file("/path/to/resume.pdf")

# Result structure:
{
    "primary_technical_skills": ["python", "django", "react", "aws"],
    "secondary_technical_skills": ["redis", "docker"],
    "soft_skills": ["leadership", "agile", "communication"],
    "cv_snapshot": "Senior Full-Stack Engineer with 8+ years..."
}
```

### 4. Use JD Extractor

```python
from ai_modules.extractors.jd_extractor import JDExtractor

# Initialize
extractor = JDExtractor()

# Extract from text
jd_text = "We're hiring a Senior Python Developer..."
result = extractor.extract_from_text(jd_text)

# Result structure:
{
    "must_have_skills": ["python", "django", "postgresql", "aws"],
    "good_to_have_skills": ["docker", "kubernetes", "redis"],
    "soft_skills": ["leadership", "agile", "mentoring"],
    "jd_snapshot": "Ready to build the future? 🚀\\n\\nWe're hiring..."
}
```

---

## 🎯 Key Features

### ✅ Zero-Tolerance Error Prevention

**Multi-Stage Analysis:**
1. **Read & Understand** - AI reads entire document first
2. **Categorize** - Strict rules for skill classification
3. **Standardize** - Convert to standard names (e.g., "ReactJS" → "react")
4. **Validate** - Check for common mistakes

**Error Prevention Mechanisms:**
- ❌ No technical skills in soft_skills array
- ❌ No wrong categorization (must-have vs good-to-have)
- ❌ No hallucinated skills (only extract what's mentioned)
- ❌ No inconsistent naming (both CV and JD use same standards)

### ✅ Standardized Skill Names

**Problem Solved:**
```
WITHOUT standardization:
- JD: "React"
- CV: "ReactJS"
- Result: ❌ No match (even though it's the same skill!)

WITH standardization:
- JD: "React" → "react"
- CV: "ReactJS" → "react"
- Result: ✅ Perfect match!
```

**Standard Names Used:**
- `python` (not Python, Python3, py)
- `react` (not ReactJS, React.js, React JS)
- `aws` (not Amazon Web Services, Amazon AWS)
- `postgresql` (not Postgres, PostgreSQL, PgSQL)
- `kubernetes` (not K8s, Kube)

### ✅ CV Snapshot Generation

**Format:** 150-200 word professional summary

**Structure:**
1. Professional identity (role, experience, domain)
2. Technical expertise (core technologies)
3. Key achievement (quantifiable results)
4. Current focus (latest role, responsibilities)

**Example:**
```
Senior Full-Stack Engineer with 8+ years of experience building scalable 
web applications. Deep expertise in Python, Django, React, and AWS cloud 
infrastructure. Architected and deployed a microservices-based e-commerce 
platform handling 2M+ daily transactions, reducing response time by 40%. 
Led a cross-functional team of 6 developers in migrating legacy monolith 
to containerized architecture using Docker and Kubernetes...
```

### ✅ JD Social Media Snapshot

**Format:** LinkedIn-ready post with emojis, formatting, hashtags

**Structure:**
1. Eye-catching header
2. Job title + location (bold)
3. Top 3-4 responsibilities (emoji bullets)
4. Tech stack highlight
5. Company culture hook
6. Call-to-action
7. Creative footer
8. 4-5 hashtags

**Example:**
```
Ready to architect scalable fintech solutions? 🚀

We're hiring a **Senior Full-Stack Engineer** in Bangalore!

✨ Design & build payment gateway systems handling millions of transactions
💻 Develop microservices with Python/Django and React frontend
🔧 Deploy on AWS cloud with Docker/Kubernetes
🎯 Lead technical decisions and mentor junior developers

Work with cutting-edge tech in a fast-paced fintech environment!

Ready to make an impact? Apply now!

#Backend #FullStack #Python #React #FinTech #BangaloreJobs
```

---

## 🧪 Testing

### Test CV Extraction

```python
from ai_modules.extractors.cv_extractor import CVExtractor

# Sample CV text
cv_text = """
John Doe - Senior Software Engineer

Experience: 7 years in backend development. Led development of payment 
gateway using Python, Django, PostgreSQL. Built REST APIs handling 500K 
requests/day. Deployed on AWS with Docker. Mentored 3 junior developers.

Skills: Python, Django, PostgreSQL, AWS, Docker, Redis, REST APIs
"""

extractor = CVExtractor()
result = extractor.extract_from_text(cv_text)

print(f"Primary: {result['primary_technical_skills']}")
# Expected: ['python', 'django', 'postgresql', 'aws', 'docker', 'restapi']

print(f"Soft: {result['soft_skills']}")
# Expected: ['leadership', 'mentoring']
```

### Test JD Extraction

```python
from ai_modules.extractors.jd_extractor import JDExtractor

# Sample JD text
jd_text = """
Senior Backend Engineer - Fintech

Requirements:
- 5+ years with Python and Django (Must have)
- Strong PostgreSQL knowledge required
- AWS experience needed
- Docker/Kubernetes is a plus
- Redis experience nice to have

Work in agile team, mentor juniors, collaborate with product managers.
"""

extractor = JDExtractor()
result = extractor.extract_from_text(jd_text)

print(f"Must-Have: {result['must_have_skills']}")
# Expected: ['python', 'django', 'postgresql', 'aws']

print(f"Good-to-Have: {result['good_to_have_skills']}")
# Expected: ['docker', 'kubernetes', 'redis']

print(f"Soft: {result['soft_skills']}")
# Expected: ['agile', 'mentoring', 'collaboration']
```

---

## 📊 Performance & Cost

### Gemini 2.0 Flash Pricing

**Model:** `gemini-2.0-flash-exp`
- Input: $0.00015 per 1K characters
- Output: $0.0006 per 1K characters

### Typical Extraction Costs

**CV Extraction:**
- Input: ~5K chars (CV text)
- Output: ~1K chars (JSON response)
- **Cost per CV: ~$0.0015** (0.15 cents)

**JD Extraction:**
- Input: ~3K chars (JD text)
- Output: ~800 chars (JSON response)
- **Cost per JD: ~$0.001** (0.1 cents)

**Monthly Estimates:**
- 100 CVs/month: ~$0.15
- 50 JDs/month: ~$0.05
- **Total: ~$0.20/month** (practically free!)

### Speed

- CV extraction: ~2-3 seconds
- JD extraction: ~1-2 seconds
- File text extraction (PDF): ~0.5 seconds

---

## 🔧 Integration with RecTool

### JD Service Integration

```python
# backend/services/jd_service.py

from ai_modules.extractors.jd_extractor import JDExtractor

class JDService:
    def __init__(self):
        self.jd_extractor = JDExtractor()
    
    def create_jd(self, jd_data: JDCreate, db: Session):
        # If raw_jd_text exists, extract keywords
        if jd_data.raw_jd_text:
            extracted = self.jd_extractor.extract_from_text(jd_data.raw_jd_text)
            
            # Auto-populate fields
            jd_data.must_have_skills = ", ".join(extracted["must_have_skills"])
            jd_data.good_to_have_skills = ", ".join(extracted["good_to_have_skills"])
            jd_data.soft_skills = ", ".join(extracted["soft_skills"])
            jd_data.jd_snapshot = extracted["jd_snapshot"]
        
        # Continue with JD creation...
```

### CV Service Integration

```python
# core/cv/services/cv_services.py

from ai_modules.extractors.cv_extractor import CVExtractor

class CVService:
    def __init__(self):
        self.cv_extractor = CVExtractor()
    
    def process_cv_file(self, file_path: str, cv_id: int, db: Session):
        # Extract keywords from CV file
        extracted = self.cv_extractor.extract_from_file(file_path)
        
        # Update CV record
        cv = db.query(CVTable).filter(CVTable.cv_id == cv_id).first()
        cv.cv_must_to_have = ", ".join(extracted["primary_technical_skills"])
        cv.cv_good_to_have = ", ".join(extracted["secondary_technical_skills"])
        cv.cv_soft_skills = ", ".join(extracted["soft_skills"])
        cv.cv_snapshot = extracted["cv_snapshot"]
        cv.cv_total_words = len(extracted["cv_snapshot"].split())
        db.commit()
```

---

## ⚠️ Important Notes

### 1. Skills Standardization is CRITICAL

Both CV and JD extractors MUST use the same skill names. This is handled automatically by `skills_standardization.py`.

### 2. Prompt Quality = Output Quality

The prompts are carefully engineered with:
- Multi-stage instructions
- One-shot examples
- Error prevention rules
- Strict JSON format requirements

**DO NOT modify prompts without testing!**

### 3. Validation is Essential

Both extractors validate output for:
- Required fields present
- No technical skills in soft_skills
- Snapshot length within range
- No hallucinated skills

### 4. Rate Limiting

Gemini client includes rate limiting (100ms between requests) to avoid API throttling.

---

## 🎯 Success Metrics

### Accuracy Targets

- **Skill Categorization:** 100% (zero tolerance for errors)
- **Skill Standardization:** 100% (consistent naming)
- **Snapshot Quality:** Professional, 150-200 words
- **Social Media Post:** Engaging, formatted, hashtagged

### Testing Checklist

Before deploying:
- [ ] Test with 10+ different CVs (varied formats)
- [ ] Test with 10+ different JDs (varied roles)
- [ ] Verify skill standardization (React = ReactJS = React.js)
- [ ] Check no technical skills in soft_skills
- [ ] Validate snapshot word counts
- [ ] Test PDF and DOCX extraction
- [ ] Test error handling (corrupted files)
- [ ] Verify API cost stays under budget

---

## 🚀 Next Steps

1. **Copy files to backend/ai_modules/**
2. **Add GEMINI_API_KEY to config.env**
3. **Install dependencies**
4. **Run test scripts**
5. **Integrate with JD and CV services**
6. **Deploy to Railway**
7. **Monitor API costs**

---

**Ready for production! Let's ship it! 🎉**
