# AI Modules - CV & JD Extraction System

A production-ready AI-powered system for extracting structured data from CVs and Job Descriptions using Google's Gemini 2.5 Flash API. Includes intelligent matching algorithms for candidate-job pairing.

## 🚀 Features

- **CV Extraction**: Extract skills, domain expertise, accolades, and generate professional snapshots from PDFs and DOCX files
- **JD Extraction**: Extract must-have/good-to-have skills, soft skills, and generate LinkedIn-style job posts
- **R2 Integration**: Support for Cloudflare R2 bucket storage (planned)
- **Smart Matching**: Exact and partial matching algorithms with scoring engine (in development)
- **Production Ready**: Error handling, rate limiting, retries, and comprehensive logging

## 📁 Project Structure

```
ai_modules/
│
├── config.py                    [EMPTY - Configuration settings]
│
├── clients/                     [Client integrations]
│   ├── __init__.py             [EMPTY]
│   ├── gemini_client.py        [✓ Gemini 2.5 Flash API client]
│   └── r2_client.py            [EMPTY - R2 bucket client]
│
├── extractors/                  [Data extraction services]
│   ├── __init__.py             [EMPTY]
│   ├── cv_extractor.py         [✓ CV extraction with R2 support]
│   ├── jd_extractor.py         [✓ JD extraction service]
│   └── file_utils.py           [EMPTY]
│
├── prompts/                     [AI prompt templates]
│   ├── __init__.py             [EMPTY]
│   ├── cv_extraction_prompt.py [✓ CV extraction prompt]
│   └── jd_extraction_prompt.py [✓ JD extraction prompt]
│
├── matcher/                     [Matching algorithms - IN DEVELOPMENT]
│   ├── exact_matcher.py        [EMPTY]
│   ├── partial_matcher.py      [EMPTY]
│   ├── match_service.py        [EMPTY]
│   └── scoring_engine.py       [EMPTY]
│
├── utils/                       [Utility functions]
│   └── file_utils.py           [✓ PDF/DOCX text extraction]
│
└── md_files.md/                 [Documentation]
    ├── AI_EXTRACTION_INTEGRATION_PLAN.md
    ├── backend_ai_modules_README.md
    ├── DEPLOYMENT_STRUCTURE.md
    ├── EXTRACTION_MODULE_SUMMARY.md
    ├── FINAL_DELIVERY_SUMMARY.md
    ├── IMPLEMENTATION_GUIDE.md
    ├── MATCHMAKING_STRATEGY_v1.1.md
    └── QUICK_START_GUIDE.md
```

## 🔴 Empty Files (Need Implementation)

The following files are empty and require implementation:

### Configuration
- `config.py` - Environment configuration and settings

### Clients
- `clients/__init__.py` - Client module exports
- `clients/r2_client.py` - Cloudflare R2 bucket integration

### Extractors
- `extractors/__init__.py` - Extractor module exports
- `extractors/file_utils.py` - Additional file utilities (duplicate of utils/file_utils.py)

### Prompts
- `prompts/__init__.py` - Prompt module exports

### Matcher (Complete Module - All Empty)
- `matcher/exact_matcher.py` - Exact skill matching algorithm
- `matcher/partial_matcher.py` - Fuzzy/partial matching algorithm
- `matcher/match_service.py` - Main matching service orchestrator
- `matcher/scoring_engine.py` - Score calculation engine

**Total Empty Files: 10**

## ✅ Implemented Modules

### 1. Gemini Client (`clients/gemini_client.py`)
- Google Gemini 2.5 Flash API integration
- Rate limiting and retry logic
- JSON response parsing with fallback handling
- Singleton pattern for efficient resource usage

### 2. CV Extractor (`extractors/cv_extractor.py`)
- Extracts 6 fields: must-have skills, good-to-have skills, soft skills, domain expertise, accolades, CV snapshot
- Supports local files and R2 bucket files (planned)
- PDF and DOCX support via file utilities
- Comprehensive validation and error handling

### 3. JD Extractor (`extractors/jd_extractor.py`)
- Extracts 7 fields: must-have/good-to-have/soft skills, domain, accolades, exceptions, JD snapshot
- Generates LinkedIn-style job posts (~200 words)
- Advanced validation and quality checks
- Prevents soft skills contamination

### 4. File Utilities (`utils/file_utils.py`)
- PDF text extraction using PyMuPDF
- DOCX text extraction using python-docx
- Text validation and word counting
- Auto-detection of file types

### 5. Prompt Engineering (`prompts/`)
- Expert-crafted prompts for Gemini 2.5 Flash
- Comprehensive extraction rules and examples
- Quality checklists and validation steps
- Standardized output formats

## 🛠️ Installation

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
Gemini API Key (from Google AI Studio)
```

### Required Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Gemini 2.5 Flash API
- `python-dotenv` - Environment variables
- `PyMuPDF` - PDF extraction
- `python-docx` - DOCX extraction
- `Flask` - Web server (for local testing)

### Environment Setup
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

## 🧪 Local Testing

### Quick Start (Web Interface)

**Windows:**
```bash
start_server.bat
```

**Linux/Mac:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Or manually:**
```bash
python app.py
```

Then open http://localhost:5000 in your browser.

### Features:
- 🎨 Beautiful web interface with purple gradient
- 📋 **JD Extraction** - Paste job descriptions and extract structured data
- 📄 **CV Extraction** - Upload PDF/DOCX and extract keywords
- 📊 Visual statistics and organized results
- 🏷️ Color-coded skill tags
- 📱 LinkedIn-ready snapshots
- ⚡ Real-time processing

### What You Can Test:
1. **JD Extraction:** Paste any job description → Get 7 fields extracted
2. **CV Extraction:** Upload PDF/DOCX → See extracted text + 6 fields

**Read the complete testing guide:** [TESTING_GUIDE.md](TESTING_GUIDE.md)

## 📖 Usage Examples

### CV Extraction
```python
from extractors.cv_extractor import CVExtractor

# Initialize extractor
extractor = CVExtractor()

# Extract from local file
result = extractor.extract_from_file("path/to/resume.pdf")

# Extract from R2 bucket (planned)
result = extractor.extract_from_r2("cv_files/candidate_123.pdf")

# Output structure
{
    "cv_must_to_have": ["python", "django", "aws"],
    "cv_good_to_have": ["kubernetes", "redis"],
    "cv_soft_skills": ["leadership", "agile"],
    "cv_domain_expertise": ["fintech", "payment systems"],
    "cv_accolades": ["AWS Certified", "M.Tech CS"],
    "cv_snapshot": "Senior Engineer with 8+ years..."
}
```

### JD Extraction
```python
from extractors.jd_extractor import JDExtractor

# Initialize extractor
extractor = JDExtractor()

# Extract from text
jd_text = "Senior Python Developer with 5+ years..."
result = extractor.extract_from_text(jd_text)

# Output structure
{
    "must_have_skills": ["python", "django", "aws"],
    "good_to_have_skills": ["kubernetes"],
    "soft_skills": ["leadership", "communication"],
    "domain_expertise": ["fintech"],
    "accolades_keyword": "none",
    "exception_skills": "none",
    "jd_snapshot": "This time it is – Senior Python Developer..."
}
```

## 🎯 Key Features

### Extraction Quality
- **Smart Skill Classification**: Differentiates must-have, good-to-have, and soft skills
- **Temporal Awareness**: Focuses on recent experience (last 4 years for CVs)
- **Standardization**: Consistent skill naming (e.g., "ReactJS" → "react")
- **Domain Intelligence**: Infers domains from company names and project context
- **Snapshot Generation**: Creates professional summaries without personal details

### Production Features
- **Rate Limiting**: Prevents API quota exhaustion
- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback Handling**: Graceful degradation on errors
- **Comprehensive Logging**: Detailed extraction progress tracking
- **Validation**: Multi-level quality checks on outputs

### API Cost Optimization
- **Model**: Gemini 2.5 Flash (stable)
- **Pricing**: $0.30 input / $2.50 output per 1M tokens
- **Avg Cost**: ~$0.002-0.003 per extraction
- **Context Window**: 1M tokens
- **Speed**: <3 seconds per extraction

## 🔧 Configuration

### Gemini 2.5 Flash Settings
- **Model**: `gemini-2.5-flash`
- **Min Request Interval**: 100ms between requests
- **Max Retries**: 3 attempts
- **Timeout**: Automatic with exponential backoff

### File Support
- **PDF**: Via PyMuPDF (fitz)
- **DOCX**: Via python-docx
- **DOC**: Via python-docx (limited support)

## 🚧 In Development

### Matcher Module (Planned)
- **Exact Matcher**: Direct skill matching with scoring
- **Partial Matcher**: Fuzzy matching for similar skills
- **Match Service**: Orchestrates matching algorithms
- **Scoring Engine**: Calculates match percentage

### R2 Integration (Planned)
- Upload/download CV files from Cloudflare R2
- Temporary file management
- Bucket configuration and authentication

## 📚 Documentation

Detailed documentation available in `md_files.md/`:
- `QUICK_START_GUIDE.md` - Getting started tutorial
- `IMPLEMENTATION_GUIDE.md` - Technical implementation details
- `EXTRACTION_MODULE_SUMMARY.md` - Module overview
- `MATCHMAKING_STRATEGY_v1.1.md` - Matching algorithm specs
- `DEPLOYMENT_STRUCTURE.md` - Deployment guidelines

## 🤝 Contributing

This is a private module for AI-powered recruitment. Contact the repository owner for contribution guidelines.

## 📄 License

Proprietary - All rights reserved

## 👤 Author

**devfluweb**
- GitHub: [@devfluweb](https://github.com/devfluweb)
- Repository: [ai_modules](https://github.com/devfluweb/ai_modules)

## 🐛 Issues & Support

For bugs or feature requests, contact the repository owner or create an issue on GitHub.

---

**Last Updated**: November 16, 2025
**Version**: 1.0.0
**Status**: Production Ready (Extraction Modules) | In Development (Matcher Module)
