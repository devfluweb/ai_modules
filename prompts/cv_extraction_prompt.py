"""
CV Extraction Prompt - PRODUCTION GRADE (STRICT)
Extracts 6 fields with RIGOROUS classification rules
"""

def get_cv_extraction_prompt(cv_text: str) -> str:
    """
    Generate STRICT CV extraction prompt.
    Primary = PROVEN job experience only
    Domain = Based on PRIMARY skills only
    Accolades = TECHNICAL certifications only
    Snapshot = AI analysis for recruiter
    """
    
    prompt = f"""You are an expert technical recruiter analyzing a CV. Extract information with EXTREME STRICTNESS.

===========================================
CRITICAL CLASSIFICATION RULES
===========================================

**SKILL STANDARDIZATION PROCESS (3 STEPS):**
1. RAW SKILL → 2. CORE SKILL → 3. STANDARDIZED NAME

Examples:
- "ReactJS 18 with Hooks and Redux" → "React" → "react"
- "AWS Lambda Functions & API Gateway" → "AWS Lambda" → "aws-lambda"
- "PostgreSQL 14 Database" → "PostgreSQL" → "postgresql"
- "Machine Learning with TensorFlow" → "TensorFlow" → "tensorflow"
- "Node.js Backend Development" → "Node.js" → "nodejs"
- "Docker Containerization" → "Docker" → "docker"

**ALWAYS use lowercase, no spaces, hyphenate multi-word skills**

===========================================
PRIMARY TECHNICAL SKILLS (EXTREMELY STRICT)
===========================================

**ONLY INCLUDE IF ALL 3 CONDITIONS MET:**
1. ✅ Used in PAID JOB (not college/personal projects)
2. ✅ Used in PRODUCTION/REAL SYSTEMS (not learning/training)
3. ✅ Used in LAST 4 YEARS from most recent job

**INCLUDE:**
✅ "3 years production experience with Django REST API"
✅ "Built payment gateway using Stripe in current role"
✅ "Leading team using React for 2+ years"
✅ "Deployed microservices with Kubernetes at ABC Corp"

**EXCLUDE (put in secondary):**
❌ "Familiar with Docker" → too vague
❌ "Basic knowledge of AWS" → not production level
❌ "College project using MongoDB" → not job experience
❌ "Completed online course in Machine Learning" → training only
❌ "Currently learning Rust" → not used yet
❌ Skills mentioned but no proof of work experience

**If uncertain → PUT IN SECONDARY, NOT PRIMARY**

===========================================
SECONDARY TECHNICAL SKILLS
===========================================

**INCLUDE:**
- Skills from jobs OLDER than 4 years
- Skills mentioned but no clear job usage
- Training/certifications but no production use
- "Familiar with", "Basic knowledge", "Exposure to"
- College/personal projects (if experienced candidate)
- Skills candidate is currently learning

===========================================
SOFT SKILLS (MUST HAVE PROOF)
===========================================

**ONLY INCLUDE WITH CLEAR EVIDENCE:**
✅ "Led team of 5 engineers" → leadership
✅ "Conducted daily standups and sprint planning" → agile
✅ "Mentored 3 junior developers" → mentoring
✅ "Presented to C-suite executives" → communication

**EXCLUDE:**
❌ Generic claims without proof
❌ "Good communication skills" (no evidence)
❌ "Team player" (no specifics)

**Standardized soft skills list:**
leadership, mentoring, agile, scrum, communication, problem-solving, team-collaboration

===========================================
DOMAIN EXPERTISE (BASED ON PRIMARY SKILLS)
===========================================

**DERIVE FROM PRIMARY SKILLS ONLY, NOT FROM:**
❌ Job titles
❌ Company names
❌ Personal interests
❌ Non-technical experience

**Logic:**
primary_skills = ["django", "postgresql", "stripe", "payment-gateway"]
→ domain = ["fintech", "payment-systems", "backend-development"]

primary_skills = ["react", "typescript", "figma", "css"]
→ domain = ["frontend-development", "ui-development"]

primary_skills = ["aws", "terraform", "kubernetes", "docker"]
→ domain = ["cloud-infrastructure", "devops", "platform-engineering"]

primary_skills = ["tensorflow", "pytorch", "nlp", "computer-vision"]
→ domain = ["machine-learning", "ai", "data-science"]

**If you can infer industry from company description, add it:**
"fintech company" → add "fintech"
"healthcare startup" → add "healthcare"
"e-commerce platform" → add "e-commerce"

===========================================
ACCOLADES (TECHNICAL CERTIFICATIONS ONLY)
===========================================

**INCLUDE ONLY:**
✅ Technical certifications (AWS, Azure, GCP, etc.)
✅ Technical degrees (B.Tech CS, M.Tech, MS, PhD)
✅ Technical training completion (official courses)
✅ Technical awards (Best Innovation, Tech Excellence)

**EXCLUDE:**
❌ Sports achievements
❌ Non-technical awards ("Employee of the Month")
❌ Volunteering/social work
❌ Hobbies and interests

**Examples:**
✅ "AWS Certified Solutions Architect"
✅ "Google Cloud Professional Data Engineer"
✅ "M.Tech Computer Science, IIT Delhi"
✅ "Certified Kubernetes Administrator (CKA)"

❌ "State level cricket player"
❌ "Best employee award 2023"
❌ "Volunteer at NGO"

===========================================
CV SNAPSHOT (AI ANALYSIS FOR RECRUITER)
===========================================

**PURPOSE:** Help recruiter understand candidate in 30 seconds WITHOUT reading full CV

**FORMAT:** Professional analysis paragraph (150-200 words)

**MUST INCLUDE:**
1. Seniority level (Junior/Mid/Senior)
2. Primary role (Backend Engineer, Full-Stack, DevOps, etc.)
3. Total experience (years)
4. Key technical strengths (from PRIMARY skills)
5. Domain expertise
6. Notable achievements (quantified if possible)
7. Current/most recent company type

**MUST EXCLUDE:**
❌ Personal details (name, email, phone, address)
❌ Company names (use "a leading fintech firm", "a Fortune 500 company")
❌ Job-seeking language ("Looking for opportunities")
❌ Generic fluff ("passionate", "dedicated")

**GOOD EXAMPLE:**
"Senior Backend Engineer with 6 years in fintech. Strong Python/Django expertise with production experience building payment systems handling $50M+ monthly transactions. Proven AWS cloud architecture skills including Lambda, RDS, and S3. Led team of 4 engineers in microservices migration. Domain expertise in payment gateways, fraud detection, and real-time transactions. AWS Certified Solutions Architect. Currently at a Series-B fintech startup."

**BAD EXAMPLE:**
"Passionate software developer looking for challenging opportunities. Good team player with excellent communication skills. Experience in various technologies. Worked at ABC Corp and XYZ Ltd. Contact: john@email.com"

===========================================
ANALYSIS INSTRUCTIONS
===========================================

**STEP 1: READ ENTIRE CV**
- Understand career progression
- Identify job vs. non-job experience
- Note proof vs. claims

**STEP 2: EXTRACT WITH STRICTNESS**
- Primary = PROVEN + PRODUCTION + RECENT (last 4 years)
- Secondary = everything else technical
- Domain = derive from primary skills
- Accolades = technical only
- Soft skills = evidence-based only

**STEP 3: STANDARDIZE**
- Apply 3-step standardization (raw → core → standard)
- Use lowercase, hyphens, no spaces
- Check against common variations

**STEP 4: VALIDATE**
- No technical skills in soft_skills
- Domain matches primary skills
- Accolades are technical
- Snapshot has no personal details
- Primary skills have clear job evidence

===========================================
OUTPUT FORMAT (STRICT JSON)
===========================================

{{
  "cv_must_to_have": ["skill1", "skill2", "skill3"],
  "cv_good_to_have": ["skill4", "skill5"],
  "cv_soft_skills": ["leadership", "agile"],
  "cv_domain_expertise": ["fintech", "backend-development"],
  "cv_accolades": ["AWS Certified", "M.Tech CS"],
  "cv_snapshot": "Professional analysis paragraph here...",
  "cv_total_words": 185
}}

**CRITICAL:** 
- Output ONLY valid JSON
- NO markdown blocks
- NO explanations
- NO comments

===========================================
CV TEXT TO ANALYZE
===========================================

{cv_text}

===========================================
EXTRACT NOW WITH EXTREME STRICTNESS
===========================================
"""
    
    return prompt