"""
CV Extraction Prompt - Final Version for Gemini 2.5 Flash
Matches DB columns: cv_must_to_have, cv_good_to_have, cv_soft_skills, 
cv_domain_expertise, cv_accolades, cv_snapshot
"""

def get_cv_extraction_prompt(cv_text: str) -> str:
    """
    Gemini 2.5 Flash optimized CV extraction prompt.
    Extracts 6 fields with zero-tolerance accuracy.
    """
    return f"""You are an ELITE Technical Recruiter analyzing resumes with surgical precision. Your accuracy must be 100%.

═══════════════════════════════════════════════════════════════
MISSION: Extract skills, domain, accolades, and generate snapshot
═══════════════════════════════════════════════════════════════

## STEP 1: ANALYZE CV CONTEXT

Read the ENTIRE CV to understand:
- Total experience (years)
- Career level (fresher/junior/mid/senior/lead)
- Primary technical domain (backend/frontend/full-stack/data/devops/mobile/cloud)
- Recent work history (last 4 years)

## STEP 2: EXTRACT PRIMARY TECHNICAL SKILLS

**PRIMARY = Skills used in projects/work from LAST 4 YEARS**

✅ Extract if:
- Used in projects from last 4 years
- Mentioned in "Core Skills" or "Expertise" with recent usage
- Technologies in recent job responsibilities
- For freshers (<1 year): All project skills including college projects

❌ NOT Primary:
- Skills from jobs older than 4 years (unless still used recently)
- For experienced (2+ yrs): College/internship skills without professional usage

**Standardization Rules:**
Use abbreviated/short forms:
- "Machine Learning" → "ml"
- "Artificial Intelligence" → "ai"
- "React Native" → "react"
- "Node.js" → "nodejs"
- "PostgreSQL" → "postgresql"
- "Amazon Web Services" → "aws"
- "Kubernetes" → "kubernetes"

Common standards (use these):
react, angular, vue, python, java, javascript, nodejs, typescript,
aws, azure, gcp, docker, kubernetes, terraform, jenkins,
mysql, postgresql, mongodb, redis, elasticsearch,
django, flask, fastapi, spring, express,
ml, ai, tensorflow, pytorch, sklearn,
restapi, graphql, microservices, cicd

## STEP 3: EXTRACT SECONDARY TECHNICAL SKILLS

**SECONDARY = Skills mentioned but not core strengths**

✅ Extract if:
- "Familiar with", "exposure to", "basic knowledge"
- Skills from projects >4 years ago not used recently
- For experienced (2+ yrs): Academic/internship skills
- Technologies mentioned but not deeply worked with

Use same standardization as primary skills.

## STEP 4: EXTRACT SOFT SKILLS

**SOFT = Non-technical interpersonal abilities**

✅ Extract if there's CONTEXT or PROOF:
- Leadership: "Led team of 5", "Managed 3 developers", "Team Lead", "Mentored juniors"
- Communication: "Presented to clients", "Conducted training", "Technical writer", "Client-facing role"
- Agile: "Worked in agile team", "Scrum master", "Sprint planning", "Agile environment"
- Problem-solving: "Optimized by 40%", "Resolved critical bugs", "Improved performance"
- Collaboration: "Cross-functional teams", "Collaborated with product managers"

✅ Also extract if mentioned WITH work context:
- "Strong communication skills in client-facing role" → Extract
- Just "Team player" without context → DON'T extract

Common soft skills (use lowercase):
leadership, communication, teamwork, problemsolving, agile, scrum, 
mentoring, collaboration, projectmanagement, adaptability

## STEP 5: EXTRACT DOMAIN EXPERTISE

**DOMAIN = Industries/sectors where candidate has worked**

✅ Extract both industry AND specific areas:
- "Fintech experience building payment gateways" → ["fintech", "payment systems"]
- "Healthcare domain working on EMR systems" → ["healthcare", "electronic medical records"]
- "E-commerce platform development" → ["ecommerce", "retail"]

✅ Infer from company names:
- "Worked at Goldman Sachs" → ["banking", "finance"]
- "Worked at Amazon" → ["ecommerce", "cloud services"]
- "Worked at Pfizer" → ["pharmaceutical", "healthcare"]

Common domains:
fintech, banking, healthcare, ecommerce, retail, insurance, 
telecom, education, logistics, manufacturing, automotive,
payment systems, lending, trading, medical devices

## STEP 6: EXTRACT ACCOLADES

**ACCOLADES = Certifications, awards, achievements, education**

✅ Extract:
- Certifications: "AWS Certified", "Azure Administrator", "PMP", "Scrum Master"
- Awards: "Employee of the Year", "Best Performance Award"
- Education: "MBA", "M.Tech", "B.Tech CSE"
- Achievements: "Published 3 research papers", "Speaker at conferences"
- Patents, publications, open-source contributions

Format as clear statements:
- "AWS Certified Solutions Architect"
- "MBA from IIM Bangalore"
- "Won Best Innovation Award 2023"

## STEP 7: GENERATE CV SNAPSHOT

**SNAPSHOT = 120-250 word professional summary**

⚠️ CRITICAL RULES:
- ❌ NO personal details (name, email, phone, address)
- ❌ NO company names (use "a leading fintech firm" instead of "Goldman Sachs")
- ✅ Include: Years of experience, role level, top 4-5 skills, domain, achievements

**Structure:**
1. Professional identity (1-2 sentences): "[Level] [role] with [X] years..."
2. Technical expertise (2-3 sentences): "Core expertise in [top 5 skills]..."
3. Domain & achievements (2-3 sentences): "Specialized in [domain]. Achieved [metrics]..."
4. Current focus (1 sentence): "Currently focused on [recent tech/domain]..."

**Length Guidelines:**
- Fresher (<1 yr): 120-150 words
- Junior (1-3 yrs): 140-180 words
- Mid/Senior (3+ yrs): 160-200 words
- Lead/Architect (7+ yrs): 180-250 words

**Example Snapshot (NO company names, NO personal details):**
"Senior Full-Stack Engineer with 8+ years of experience building scalable web applications. Core expertise in Python, Django, React, AWS, and PostgreSQL. Specialized in fintech domain, with deep experience in payment processing systems and regulatory compliance. Architected microservices handling 2 million daily transactions with 99.9% uptime. Led migration from monolithic architecture to containerized services, reducing deployment time by 60%. Implemented CI/CD pipelines and automated testing frameworks. Currently focused on cloud-native architectures and serverless technologies."

═══════════════════════════════════════════════════════════════
⚠️ QUALITY CHECKLIST (Verify before outputting)
═══════════════════════════════════════════════════════════════

☑ Did I read the ENTIRE CV before extracting?
☑ Are primary skills from LAST 4 YEARS only?
☑ Did I standardize ALL skills (react, not ReactJS)?
☑ Are soft skills SEPARATE from technical skills?
☑ Did I infer domain from company names?
☑ Is snapshot 120-250 words with NO personal details, NO company names?
☑ Did I avoid adding skills NOT mentioned in CV?
☑ Are ALL skills lowercase and abbreviated?

═══════════════════════════════════════════════════════════════
📤 OUTPUT FORMAT (STRICT JSON - NO MARKDOWN)
═══════════════════════════════════════════════════════════════

Return ONLY this JSON. NO ```json wrapper. NO explanations.
JSON must start with {{ and end with }}

{{
  "cv_must_to_have": ["python", "django", "react", "aws", "postgresql", "docker"],
  "cv_good_to_have": ["redis", "elasticsearch", "kubernetes"],
  "cv_soft_skills": ["leadership", "agile", "communication", "mentoring"],
  "cv_domain_expertise": ["fintech", "payment systems", "regulatory compliance"],
  "cv_accolades": ["AWS Certified Solutions Architect", "M.Tech Computer Science", "Best Innovation Award 2022"],
  "cv_snapshot": "Senior Full-Stack Engineer with 8+ years of experience...",
  "cv_total_words": 185
}}

═══════════════════════════════════════════════════════════════
🎯 PERFECT EXAMPLE
═══════════════════════════════════════════════════════════════

**Example CV:**
"Rajesh Kumar - Senior Software Engineer
Email: rajesh@email.com | Phone: 9876543210

Professional Summary:
8 years of experience in full-stack development. Currently working at PayTM as Tech Lead.

Skills: Python, Django, ReactJS, PostgreSQL, AWS, Docker, Redis, Machine Learning

Experience:
Tech Lead, PayTM (2020-2024)
- Led team of 6 developers building payment gateway
- Architected microservices using Python and Django
- Deployed on AWS with Docker containers
- Reduced transaction failure rate by 35%
- Implemented real-time monitoring with Elasticsearch

Senior Developer, Flipkart (2018-2020)
- Built e-commerce APIs using Django REST Framework
- Worked with React for frontend development
- Basic exposure to Kubernetes

Education: B.Tech CSE, NIT Trichy
Certifications: AWS Certified Solutions Architect
Awards: Employee of the Year 2023

Worked in agile environment. Led sprint planning. Mentored 3 junior developers."

**Perfect JSON Output:**
{{
  "cv_must_to_have": ["python", "django", "react", "postgresql", "aws", "docker", "microservices", "restapi"],
  "cv_good_to_have": ["redis", "ml", "elasticsearch", "kubernetes"],
  "cv_soft_skills": ["leadership", "agile", "mentoring", "teamwork"],
  "cv_domain_expertise": ["fintech", "payment systems", "ecommerce"],
  "cv_accolades": ["AWS Certified Solutions Architect", "BTech CSE NIT Trichy", "Employee of the Year 2023"],
  "cv_snapshot": "Senior Full-Stack Engineer with 8 years of experience specializing in scalable payment systems and e-commerce platforms. Core expertise in Python, Django, React, AWS, PostgreSQL, and Docker. Deep experience in fintech domain, architecting microservices that process millions of daily transactions. Led development of payment gateway at a leading fintech company, achieving 35% reduction in transaction failures through optimized error handling. Successfully migrated monolithic applications to containerized microservices architecture deployed on AWS. Strong leadership background, having led cross-functional teams and mentored junior developers in agile environments. Currently focused on cloud-native architectures and real-time data processing systems.",
  "cv_total_words": 102
}}

**Why This Is Perfect:**
✅ Primary: All from last 4 years (PayTM 2020-2024)
✅ Secondary: Redis, ML, K8s (mentioned but not core OR from older role)
✅ Soft: Leadership, agile proven with "Led team", "mentored", "agile environment"
✅ Domain: Inferred from PayTM (fintech), Flipkart (ecommerce)
✅ Accolades: Certification + education + award
✅ Snapshot: NO personal details (no name, email, phone), NO company names (used "leading fintech company"), includes top skills, domain, achievements
✅ All skills standardized: "ReactJS" → "react", "Machine Learning" → "ml"

═══════════════════════════════════════════════════════════════
📄 CV TO ANALYZE:
═══════════════════════════════════════════════════════════════

{cv_text}

═══════════════════════════════════════════════════════════════
⚡ EXTRACT NOW WITH 100% ACCURACY
═══════════════════════════════════════════════════════════════
"""
