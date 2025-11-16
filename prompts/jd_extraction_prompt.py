"""
JD Keywords Extraction Prompt - STEP 1 (STRICT)
Extracts 6 keyword fields with rigorous classification
"""

def get_jd_keywords_prompt(jd_text: str) -> str:
    """
    Generate STRICT JD keywords extraction prompt.
    Step 1: Extract keywords only (no snapshot)
    """
    
    prompt = f"""You are an expert technical recruiter analyzing a Job Description. Extract keywords with EXTREME STRICTNESS.

===========================================
CRITICAL CLASSIFICATION RULES
===========================================

**SKILL STANDARDIZATION PROCESS (3 STEPS):**
1. RAW SKILL → 2. CORE SKILL → 3. STANDARDIZED NAME

Examples:
- "5+ years in ReactJS" → "React" → "react"
- "AWS cloud services" → "AWS" → "aws"
- "PostgreSQL or MySQL database" → "PostgreSQL, MySQL" → "postgresql, mysql"
- "Experience with Docker containers" → "Docker" → "docker"

**ALWAYS use lowercase, no spaces, hyphenate multi-word skills**

===========================================
MUST-HAVE SKILLS (CRITICAL REQUIREMENTS)
===========================================

**Context-based detection - look for:**
- "Must have", "Required", "Essential"
- "X+ years required"
- "Strong expertise in"
- Skills in job title (e.g., "Senior Python Developer" → python is must-have)
- Skills mentioned multiple times
- Skills in "key requirements" section

**INCLUDE:**
✅ "5+ years Python experience" → python
✅ "Strong Django REST framework skills" → django
✅ "AWS cloud deployment required" → aws
✅ "Proficiency in React mandatory" → react

**EXCLUDE (put in good-to-have):**
❌ "Familiarity with Docker is a plus"
❌ "Nice to have: Kubernetes"
❌ "Bonus: GraphQL experience"

===========================================
GOOD-TO-HAVE SKILLS (NICE TO HAVE)
===========================================

**Look for:**
- "Nice to have", "Bonus", "Plus"
- "Preferred", "Desired"
- "Familiarity with"
- Skills mentioned once casually

**INCLUDE:**
✅ "Docker/Kubernetes knowledge is a plus"
✅ "Familiarity with Redis preferred"
✅ "GraphQL experience would be nice"

===========================================
SOFT SKILLS (NON-TECHNICAL ONLY)
===========================================

**INCLUDE ONLY NON-TECHNICAL:**
✅ leadership, communication, mentoring
✅ agile, scrum, team-collaboration
✅ problem-solving, critical-thinking

**EXCLUDE TECHNICAL:**
❌ "AWS" (technical skill, not soft skill)
❌ "Python" (technical skill)
❌ "Agile development with Scrum" → extract only "agile, scrum"

**Standardized soft skills list:**
leadership, mentoring, agile, scrum, communication, problem-solving, team-collaboration, time-management, stakeholder-management

===========================================
DOMAIN EXPERTISE
===========================================

**Extract industry/sector + technical domain:**

**Industry:**
- fintech, banking, insurance → if financial services
- healthcare, medtech → if medical
- e-commerce, retail → if online shopping
- edtech, education → if learning platforms

**Technical Domain:**
- backend-development, frontend-development, full-stack
- cloud-infrastructure, devops, platform-engineering
- data-engineering, machine-learning, ai
- mobile-development, web-development

**Examples:**
JD for "Backend Engineer at fintech startup"
→ domain = ["fintech", "backend-development"]

JD for "DevOps Engineer managing AWS infrastructure"
→ domain = ["cloud-infrastructure", "devops"]

===========================================
ACCOLADES KEYWORDS (CERTIFICATIONS)
===========================================

**Extract REQUIRED certifications ONLY:**

✅ "AWS Certified Solutions Architect required"
✅ "Must have Google Cloud Professional certification"
✅ "CKA certification mandatory"

**If NO certification required:**
→ Return "none"

**EXCLUDE:**
❌ "Degree in Computer Science" (not a certification)
❌ "Nice to have: AWS certification" (not mandatory)

===========================================
EXCEPTION SKILLS (MUST AVOID)
===========================================

**Look for red flags:**
- "No experience in X required"
- "Should not have worked with Y"
- "Avoid candidates with Z background"
- Skills that disqualify candidate

**Examples:**
✅ "Should not have C++ background" → exception_skills: "c++"
✅ "No PHP experience needed" → exception_skills: "php"

**If NO exceptions mentioned:**
→ Return "none"

===========================================
ANALYSIS INSTRUCTIONS
===========================================

**STEP 1: READ ENTIRE JD**
- Understand role requirements
- Identify must-have vs nice-to-have
- Note required vs preferred

**STEP 2: CLASSIFY SKILLS STRICTLY**

**MUST-HAVE = Skills that are REQUIRED/MANDATORY:**
- Explicitly stated as "required", "must have", "essential"
- Years of experience specified (e.g., "5+ years Python")
- Core technologies for the role
- Skills repeated multiple times in JD
- Technologies in job title

**GOOD-TO-HAVE = Skills that are OPTIONAL/BONUS:**
- Explicitly stated as "nice to have", "plus", "bonus", "preferred"
- Mentioned casually without emphasis
- "Familiarity with" or "exposure to"
- Listed in separate "nice to have" section
- Skills mentioned only once

**STEP 3: STANDARDIZE**
- Apply 3-step standardization
- Lowercase, hyphens, no spaces
- Consistent naming

**STEP 4: VALIDATE BEFORE RETURNING**
- Must-have: 5-15 skills typically
- Good-to-have: 3-10 skills typically
- Soft skills: non-technical only (3-8 items)
- Domain: 2-4 items (industry + technical area)
- No technical skills in soft_skills
- Accolades = certifications only (or "none")
- Exceptions = disqualifying skills (or "none")

===========================================
OUTPUT FORMAT (STRICT JSON)
===========================================

{{
  "must_have_skills": ["python", "django", "aws", "postgresql"],
  "good_to_have_skills": ["docker", "kubernetes", "redis"],
  "soft_skills": ["leadership", "agile", "communication"],
  "domain_expertise": ["fintech", "backend-development"],
  "accolades_keyword": "AWS Certified Solutions Architect",
  "exception_skills": "none"
}}

**CRITICAL:** 
- Output ONLY valid JSON
- NO markdown blocks
- NO explanations
- NO snapshot field (that's step 2)
- Use "none" for accolades/exceptions if not mentioned

===========================================
JD TEXT TO ANALYZE
===========================================

{jd_text}

===========================================
EXTRACT KEYWORDS NOW (STEP 1 ONLY)
===========================================
"""
    
    return prompt