# 🧪 Local Testing Guide

Complete guide to test CV and JD extraction modules locally using the web interface.

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Gemini API Key** from Google AI Studio
3. **All dependencies** installed

## 🚀 Quick Start (5 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-generativeai` - Gemini API
- `Flask` - Web server
- `PyMuPDF` - PDF extraction
- `python-docx` - DOCX extraction
- `python-dotenv` - Environment variables

### Step 2: Set Up API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Get your API key:**
1. Go to https://aistudio.google.com/app/apikey
2. Create a new API key
3. Copy and paste it in the `.env` file

### Step 3: Start the Server

```bash
python app.py
```

You should see:

```
🚀 AI EXTRACTION TESTING SERVER
======================================================================

📍 Server starting at: http://localhost:5000

✅ Available endpoints:
   - GET  /              → Main testing interface
   - POST /api/extract-jd → JD extraction
   - POST /api/extract-cv → CV extraction
   - GET  /api/health     → Health check

💡 Open http://localhost:5000 in your browser
======================================================================
```

### Step 4: Open Browser

Open your browser and go to:
```
http://localhost:5000
```

### Step 5: Start Testing!

You'll see a beautiful purple interface with two buttons:
- **📋 JD Extraction** - Test job description extraction
- **📄 CV Extraction** - Test CV/resume extraction

---

## 📋 Testing JD Extraction

### How to Use:

1. **Click "JD Extraction" button** (top left)
2. **Paste a job description** in the text area
3. **Click "🔍 Scan & Extract"**
4. **View results** in organized sections below

### What You'll See:

**Statistics:**
- Must-Have Skills count
- Good-to-Have Skills count
- Soft Skills count
- Total words analyzed

**Extracted Data:**
1. **🎯 Must-Have Skills** - Required technical skills
2. **✨ Good-to-Have Skills** - Preferred/bonus skills
3. **💡 Soft Skills** - Non-technical abilities
4. **🏢 Domain Expertise** - Industry/sector focus
5. **🏆 Accolades/Certifications** - Required certifications
6. **🚫 Exception Skills** - Skills to avoid
7. **📱 LinkedIn Job Post Snapshot** - Social media ready post

### Sample JD for Testing:

```
Senior Python Developer - 5+ years experience

We're looking for an experienced Backend Developer to join our fintech team.

Required Skills:
- Strong Python and Django expertise
- PostgreSQL database design and optimization
- AWS cloud services (EC2, S3, RDS)
- RESTful API development
- Docker containerization

Nice to have:
- Kubernetes orchestration
- Redis caching
- React/Frontend experience

You'll work in an agile team building payment processing systems.
Strong communication skills required for client interactions.

Certifications preferred: AWS Certified Solutions Architect
```

---

## 📄 Testing CV Extraction

### How to Use:

1. **Click "CV Extraction" button** (top right)
2. **Upload a CV file** (PDF or DOCX)
   - Click the upload area, or
   - Drag & drop a file
3. **Click "🔍 Scan & Extract"**
4. **View results** in organized sections below

### What You'll See:

**Statistics:**
- Primary Skills count
- Secondary Skills count
- Soft Skills count
- Total words analyzed

**Extracted Data:**
1. **📄 Extracted Text from CV** - Raw text extracted from the file
2. **🎯 Primary Technical Skills** - Recent/core technical skills
3. **✨ Secondary Technical Skills** - Additional/older skills
4. **💡 Soft Skills** - Interpersonal abilities
5. **🏢 Domain Expertise** - Industries worked in
6. **🏆 Accolades & Certifications** - Awards, certifications, education
7. **👤 Professional Snapshot** - 120-250 word summary

### Supported File Formats:

- ✅ PDF (`.pdf`)
- ✅ Word DOCX (`.docx`)
- ✅ Word DOC (`.doc`)
- ❌ Images, plain text (not supported)

### Max File Size: 16MB

---

## 🔍 API Endpoints (for Advanced Testing)

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

Returns Gemini client status and model info.

### 2. JD Extraction API
```bash
curl -X POST http://localhost:5000/api/extract-jd \
  -H "Content-Type: application/json" \
  -d '{"jd_text": "Your job description here..."}'
```

### 3. CV Extraction API
```bash
curl -X POST http://localhost:5000/api/extract-cv \
  -F "cv_file=@path/to/resume.pdf"
```

---

## 🎨 Interface Features

### Beautiful UI:
- 🌈 Purple gradient background
- 💫 Smooth animations and transitions
- 📱 Responsive design (works on mobile too)
- 🎯 Organized result cards
- 🏷️ Color-coded skill tags
- 📊 Visual statistics

### User-Friendly:
- Drag & drop file upload
- Real-time file info display
- Loading spinners during processing
- Clear error messages
- Results organized by category
- Copy-friendly text outputs

### Smart Features:
- Automatic file cleanup after processing
- File type validation
- Size limit protection (16MB)
- Error handling and fallbacks
- Word count tracking
- Timestamp tracking

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Make sure `.env` file exists with your API key:
```env
GEMINI_API_KEY=your_key_here
```

### Issue: "No module named 'flask'"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "PDF extraction failed"
**Solution:** 
- Check if file is corrupted
- Try a different PDF
- Ensure PyMuPDF is installed: `pip install PyMuPDF`

### Issue: "Port 5000 already in use"
**Solution:** Either:
- Stop the other process using port 5000, or
- Change the port in `app.py`:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001
  ```

### Issue: Server crashes on extraction
**Solution:**
- Check Gemini API quota/limits
- Verify API key is valid
- Check error logs in terminal

---

## 📊 Understanding Results

### Must-Have vs Good-to-Have (JD)
- **Must-Have**: Skills mentioned as "required", "mandatory", "must have"
- **Good-to-Have**: Skills mentioned as "nice to have", "preferred", "bonus"

### Primary vs Secondary (CV)
- **Primary**: Skills used in last 4 years professionally
- **Secondary**: Older skills or mentioned without recent usage

### Soft Skills
- Non-technical abilities like leadership, communication, teamwork
- Extracted only if context/proof is mentioned in CV/JD

### Domain Expertise
- Industries: fintech, healthcare, ecommerce, etc.
- Specific areas: payment systems, cloud services, etc.

### Snapshots
- **JD Snapshot**: LinkedIn-style job post (~200 words)
- **CV Snapshot**: Professional summary (120-250 words)
- Both exclude personal details and company names

---

## 🎯 Testing Tips

### For Best Results:

1. **JD Testing:**
   - Use complete job descriptions (300+ words)
   - Include sections: skills, requirements, responsibilities
   - Mention experience level
   - Include domain/industry if applicable

2. **CV Testing:**
   - Use well-formatted PDFs or DOCX files
   - Ensure text is extractable (not scanned images)
   - Include: experience, skills, projects, education
   - Test with different CV formats

3. **Quality Checks:**
   - Verify extracted skills match the input
   - Check if soft skills have proper context
   - Ensure snapshots exclude personal details
   - Validate domain inference from companies

---

## 🔧 Advanced Configuration

### Modify Extraction Settings

Edit `clients/gemini_client.py` to adjust:
- **Rate limiting**: Change `min_request_interval`
- **Max retries**: Change `max_retries` parameter
- **Model**: Switch to different Gemini model

### Customize Web Interface

Edit `templates/index.html` to:
- Change colors/styling (CSS section)
- Modify layout
- Add new features
- Customize result display

---

## 📝 Sample Test Cases

### Test Case 1: Senior Backend Developer (JD)
```
Senior Backend Developer - Python/Django
5-7 years experience required

Required:
- Python, Django, PostgreSQL
- AWS (EC2, S3, RDS)
- RESTful APIs, Microservices
- Docker, CI/CD

Nice to have:
- Kubernetes, Terraform
- React basics

Domain: Fintech, Payment systems
```

**Expected Results:**
- Must-have: 8-10 skills
- Good-to-have: 2-4 skills
- Domain: fintech, payment systems
- Snapshot: LinkedIn-ready post

### Test Case 2: Junior Frontend Developer (CV)
Create a sample CV with:
- 2 years of React experience
- Projects using JavaScript, HTML, CSS
- Basic Node.js knowledge
- Education: B.Tech CS
- Soft skills mentioned with context

**Expected Results:**
- Primary: react, javascript, html, css
- Secondary: nodejs
- Snapshot: 140-180 words

---

## 🚀 Next Steps

After testing locally:

1. **Verify extraction quality** - Check if results match expectations
2. **Test edge cases** - Try malformed CVs, short JDs
3. **Performance testing** - Test with large files
4. **Integration** - Connect to your backend/database
5. **Production deployment** - Deploy the Flask app or use modules in your app

---

## 📞 Support

If you encounter issues:
1. Check error messages in browser console
2. Check terminal logs where Flask is running
3. Verify all dependencies are installed
4. Ensure `.env` file has valid API key
5. Test API endpoints directly with curl

---

**Happy Testing! 🎉**

Last Updated: November 16, 2025
