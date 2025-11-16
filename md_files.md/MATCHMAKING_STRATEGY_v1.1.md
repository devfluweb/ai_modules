# 🎯 MATCHMAKING STRATEGY v1.1 - Keyword Extraction & AI Matching

## 📋 DATABASE SCHEMA STATUS

### ✅ JD Table - Existing Fields
```sql
- must_have_skills          TEXT    ✅ Exists
- good_to_have_skills       TEXT    ✅ Exists  
- soft_skills               TEXT    ✅ Exists
- exception_skills          TEXT    ✅ Exists
- jd_special_instruction    TEXT    ✅ Exists
- jd_snapshot               TEXT    ✅ Exists
- raw_jd_text               TEXT    ✅ Exists
- op_experience_min         INT     ✅ Exists
- op_experience_max         INT     ✅ Exists
- op_budget_min             DECIMAL ✅ Exists
- op_budget_max             DECIMAL ✅ Exists
- exp_match_percent         DECIMAL ✅ Exists (as match_cutoff_percentage)
```

### ❌ JD Table - Missing Fields (NEED TO ADD)
```sql
ALTER TABLE job_descriptions ADD COLUMN domain_expertise TEXT;
ALTER TABLE job_descriptions ADD COLUMN accolades_keyword TEXT;
ALTER TABLE job_descriptions ADD COLUMN exception_list TEXT;
```

### ✅ CV Table - All Fields Exist
```sql
- cv_must_to_have           TEXT    ✅ Exists (processed keywords)
- cv_good_to_have           TEXT    ✅ Exists
- cv_soft_skills            TEXT    ✅ Exists
- cv_domain_expertise       TEXT    ✅ Exists
- cv_accolades              TEXT    ✅ Exists
- cv_tech_keywords          JSON    ✅ Exists
- cv_snapshot               TEXT    ✅ Exists
- cv_total_words            INT     ✅ Exists
- cv_match_perc             INT     ✅ Exists
- matched_jd_title          TEXT    ✅ Exists
- date_of_match             TEXT    ✅ Exists
```

---

## 🔑 KEYWORD EXTRACTION STRATEGY

### 1️⃣ **JD Keyword Extraction** (from `raw_jd_text`)

#### Input Sources:
- Primary: `raw_jd_text` (full JD description)
- Secondary: Manually entered fields (if raw_jd_text is empty)

#### Extraction Categories:

**A. Must-Have Skills** (Critical Technical Requirements)
- Programming languages (Python, Java, React, etc.)
- Frameworks & libraries (Django, Spring Boot, Angular, etc.)
- Databases (MySQL, MongoDB, PostgreSQL, etc.)
- Cloud platforms (AWS, Azure, GCP, etc.)
- DevOps tools (Docker, Kubernetes, Jenkins, etc.)
- **Extraction Method:** Pattern matching + NER (Named Entity Recognition)
- **Storage:** `must_have_skills` (comma-separated string)

**B. Good-to-Have Skills** (Nice-to-Have)
- Additional technologies mentioned without "required"/"must"
- Certifications (AWS Certified, PMP, etc.)
- Bonus tools/frameworks
- **Extraction Method:** Skills mentioned with "preferred", "nice to have", "plus"
- **Storage:** `good_to_have_skills` (comma-separated string)

**C. Soft Skills** (Behavioral Traits)
- Communication, Leadership, Teamwork
- Problem-solving, Analytical thinking
- Time management, Adaptability
- **Extraction Method:** Keyword matching from soft skills dictionary
- **Storage:** `soft_skills` (comma-separated string)

**D. Domain Expertise** (Industry/Vertical Knowledge)
- Fintech, Healthcare, E-commerce, Banking
- Retail, Manufacturing, Education, SaaS
- **Extraction Method:** Industry keyword dictionary + context analysis
- **Storage:** `domain_expertise` (comma-separated string)

**E. Accolades/Achievements Keywords**
- "Award-winning", "Top performer", "Published author"
- "Speaker at conferences", "Open-source contributor"
- **Extraction Method:** Achievement phrase patterns
- **Storage:** `accolades_keyword` (comma-separated string)

**F. Exception Skills/Red Flags**
- Skills to AVOID (e.g., "No PHP", "Avoid candidates from competitor X")
- Negative patterns (job hopping, gaps in resume)
- **Extraction Method:** Manual entry primarily, pattern detection for negations
- **Storage:** `exception_skills` + `exception_list` (comma-separated strings)

---

### 2️⃣ **CV Keyword Extraction** (from resume file/text)

#### Input Sources:
- Primary: Uploaded CV file (PDF/DOCX) → Extract text
- Secondary: Manually entered fields in CV form

#### Extraction Categories:

**A. Must-Have Keywords** (`cv_must_to_have`)
- Technical skills from resume (languages, frameworks, tools)
- Years of experience with each skill
- **Extraction Method:** PDF/DOCX text extraction → NER → Skills taxonomy matching
- **Storage:** `cv_must_to_have` (comma-separated with years)
  - Example: "Python (5 years), React (3 years), AWS (2 years)"

**B. Good-to-Have Keywords** (`cv_good_to_have`)
- Secondary skills mentioned in resume
- Side projects, personal interests
- **Extraction Method:** Skills outside primary expertise
- **Storage:** `cv_good_to_have` (comma-separated)

**C. Soft Skills** (`cv_soft_skills`)
- Leadership roles (Team Lead, Project Manager)
- Communication indicators (presentations, training, mentoring)
- **Extraction Method:** Role titles + achievement descriptions
- **Storage:** `cv_soft_skills` (comma-separated)

**D. Domain Expertise** (`cv_domain_expertise`)
- Industries worked in (from company descriptions)
- Projects/products built (e.g., "Built fintech payment gateway")
- **Extraction Method:** Company names → Industry mapping + project descriptions
- **Storage:** `cv_domain_expertise` (comma-separated)

**E. Accolades** (`cv_accolades`)
- Awards, certifications, publications
- GitHub stars, open-source contributions
- **Extraction Method:** Pattern matching for achievement phrases
- **Storage:** `cv_accolades` (comma-separated)

**F. Technical Keywords** (`cv_tech_keywords`)
- Comprehensive list of ALL technical terms
- **Extraction Method:** Technical taxonomy dictionary
- **Storage:** JSON format
  ```json
  {
    "languages": ["Python", "JavaScript"],
    "frameworks": ["Django", "React"],
    "databases": ["MySQL", "MongoDB"],
    "cloud": ["AWS", "Docker"]
  }
  ```

---

## 🤖 AI MATCHING PROMPT DESIGN

### **Prompt Template for JD2CV Matching**

```
You are an expert technical recruiter specializing in IT candidate-job matching.

Your task: Analyze a candidate's CV against a job description and provide a precise match score.

**Job Description Details:**
- Position: {job_title}
- Company: {company_name}
- Experience Required: {op_experience_min}-{op_experience_max} years
- Budget Range: ${op_budget_min}-${op_budget_max}

**Critical Skills (Must-Have):**
{must_have_skills}

**Preferred Skills (Good-to-Have):**
{good_to_have_skills}

**Soft Skills Required:**
{soft_skills}

**Domain Expertise:**
{domain_expertise}

**Bonus Points (Accolades):**
{accolades_keyword}

**Red Flags (Exception Skills/Companies):**
{exception_skills}, {exception_list}

**Special Instructions:**
{jd_special_instruction}

---

**Candidate CV Summary:**
- Name: {cv_name}
- Total Experience: {cv_experience} years
- Current Company: {cv_current_company}
- Current Role: {cv_role}
- Technical Skills: {cv_must_to_have}
- Additional Skills: {cv_good_to_have}
- Soft Skills: {cv_soft_skills}
- Domain Expertise: {cv_domain_expertise}
- Accolades: {cv_accolades}
- Current CTC: ${cv_ctc}
- Expected CTC: ${cv_ectc}
- Notice Period: {cv_notice_period} days

---

**Evaluation Criteria:**

1. **Must-Have Skills Match (40 points):**
   - Count how many critical skills the candidate has
   - Deduct points for missing critical skills
   - Award 40 points if ALL must-have skills are present

2. **Good-to-Have Skills Match (25 points):**
   - Count how many preferred skills the candidate has
   - Proportional scoring (5 out of 10 = 12.5 points)

3. **Soft Skills Match (15 points):**
   - Evaluate behavioral fit based on soft skills
   - Leadership, communication, teamwork alignment

4. **Domain Expertise Match (10 points):**
   - Relevant industry experience
   - Similar product/project background

5. **Experience Range Match (10 points):**
   - Within required experience range: 10 points
   - Slightly under/over: 5 points
   - Way off range: 0 points

6. **Accolades Bonus (+10 points max):**
   - Certifications, awards, publications
   - Open-source contributions, speaking engagements

7. **Exception Penalties (-50 points per violation):**
   - Has exception skills: -50 points
   - Worked at blacklisted company: -50 points
   - Violates special instructions: -50 points

**Output Format (STRICT JSON ONLY):**
```json
{
  "match_percentage": 85,
  "rating": 4,
  "cv_recommendation": "Strong candidate with 7+ years of Python/React experience. Has 8/10 must-have skills. Missing Kubernetes and microservices experience. Salary expectations align with budget. Notice period of 30 days is acceptable. Recommended for interview.",
  "breakdown": {
    "must_have_score": 32,
    "good_to_have_score": 20,
    "soft_skills_score": 12,
    "domain_score": 8,
    "experience_score": 10,
    "accolades_bonus": 3,
    "exception_penalty": 0
  },
  "missing_critical_skills": ["Kubernetes", "Microservices"],
  "matching_skills": ["Python", "React", "AWS", "MySQL", "Docker", "CI/CD", "Agile", "REST APIs"],
  "red_flags": []
}
```

**Important Rules:**
- Match percentage must be 0-100
- Rating must be 1-5 (1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent)
- Be honest about skill gaps
- Consider budget vs. expectations
- Factor in notice period vs. urgency
- Return ONLY valid JSON, no markdown, no comments
```

---

## 📊 SCORING ALGORITHM BREAKDOWN

### **Score Calculation:**
```python
total_score = 0

# 1. Must-Have Skills (40 points max)
must_have_matches = count_matching_skills(jd_must_have, cv_must_have)
must_have_total = len(jd_must_have)
must_have_score = (must_have_matches / must_have_total) * 40
total_score += must_have_score

# 2. Good-to-Have Skills (25 points max)
good_to_have_matches = count_matching_skills(jd_good_to_have, cv_good_to_have)
good_to_have_total = len(jd_good_to_have)
good_to_have_score = (good_to_have_matches / good_to_have_total) * 25 if good_to_have_total > 0 else 0
total_score += good_to_have_score

# 3. Soft Skills (15 points max)
soft_matches = count_matching_skills(jd_soft_skills, cv_soft_skills)
soft_total = len(jd_soft_skills)
soft_score = (soft_matches / soft_total) * 15 if soft_total > 0 else 0
total_score += soft_score

# 4. Domain Expertise (10 points max)
domain_match = check_domain_overlap(jd_domain, cv_domain)
domain_score = 10 if domain_match else 0
total_score += domain_score

# 5. Experience Range (10 points max)
if op_experience_min <= cv_experience <= op_experience_max:
    experience_score = 10
elif abs(cv_experience - op_experience_min) <= 1 or abs(cv_experience - op_experience_max) <= 1:
    experience_score = 5
else:
    experience_score = 0
total_score += experience_score

# 6. Accolades Bonus (up to +10 points)
accolades_bonus = min(len(cv_accolades) * 2, 10)
total_score += accolades_bonus

# 7. Exception Penalties (-50 per violation)
exception_penalty = 0
if has_exception_skills(cv, jd_exception_skills):
    exception_penalty -= 50
if worked_at_blacklisted_company(cv, jd_exception_list):
    exception_penalty -= 50
total_score += exception_penalty

# Final Match Percentage (cap at 0-100)
match_percentage = max(0, min(100, total_score))

# Rating (1-5 stars)
if match_percentage >= 90:
    rating = 5
elif match_percentage >= 75:
    rating = 4
elif match_percentage >= 60:
    rating = 3
elif match_percentage >= 40:
    rating = 2
else:
    rating = 1
```

---

## 🛠️ IMPLEMENTATION CHECKLIST

### **Phase 1: Database Schema Updates**
- [ ] Add `domain_expertise` to JD table
- [ ] Add `accolades_keyword` to JD table
- [ ] Add `exception_list` to JD table
- [ ] Create migration script
- [ ] Test schema changes on Railway

### **Phase 2: Keyword Extraction Modules**
- [ ] Build JD keyword extractor (`backend/services/jd_keyword_extractor.py`)
- [ ] Build CV keyword extractor (`backend/services/cv_keyword_extractor.py`)
- [ ] Create skills taxonomy dictionary (10,000+ tech terms)
- [ ] Create soft skills dictionary (100+ behavioral traits)
- [ ] Create domain/industry mapping (50+ industries)
- [ ] PDF/DOCX text extraction utility (PyPDF2, python-docx)
- [ ] NER model integration (spaCy, Transformers)

### **Phase 3: AI Matching Service**
- [ ] Create AI prompt templates (`backend/services/matchmaker_prompts.py`)
- [ ] Build LLM integration (Gemini/Claude/GPT with fallback)
- [ ] Implement scoring algorithm (`backend/services/matchmaker_scoring.py`)
- [ ] Create JSON validation & error handling
- [ ] Add retry logic for LLM failures

### **Phase 4: Orchestration Services**
- [ ] Stage 1 Pre-filter service (`backend/services/matchmaker_stage1.py`)
- [ ] Stage 2 AI matching service (`backend/services/matchmaker_ai.py`)
- [ ] Stage 3 Update service (`backend/services/matchmaker_update.py`)
- [ ] Main orchestrator (`backend/services/matchmaker_orchestrator.py`)

### **Phase 5: API & Frontend**
- [ ] API routes (`backend/routes/matchmaker_routes.py`)
- [ ] Frontend UI (`frontend/src/pages/MatchMaker.jsx`)
- [ ] Real-time progress tracking
- [ ] Match results display with charts

### **Phase 6: Testing & Optimization**
- [ ] Unit tests for each module
- [ ] Integration tests for full pipeline
- [ ] Performance testing (100+ CVs vs 1 JD)
- [ ] LLM cost optimization (batch processing)
- [ ] Caching strategy for repeated matches

---

## 🎯 NEXT STEPS

**Immediate Actions:**
1. Add missing JD table columns (domain_expertise, accolades_keyword, exception_list)
2. Build skills taxonomy dictionary
3. Create JD keyword extraction prompt
4. Create CV keyword extraction prompt
5. Build AI matching prompt template
6. Decide on LLM provider (Gemini/Claude/GPT)

**Questions to Answer:**
1. Which LLM API should we use? (I recommend Gemini for cost + Claude for quality)
2. Should we batch process CVs or one-by-one? (Recommend one-by-one for better accuracy)
3. What's the max LLM cost per match? (Budget consideration)
4. Should we cache match results? (Recommend YES with 24hr TTL)

---

Ready to start building? Let me know which module to tackle first! 🚀
