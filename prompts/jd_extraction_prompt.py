"""
JD Extraction Prompt - Final Version for Gemini 2.5 Flash
Extracts: must_have_skills, good_to_have_skills, soft_skills, 
domain_expertise, accolades_keyword, exception_skills, jd_snapshot
"""

def get_jd_extraction_prompt(jd_text: str) -> str:
    """
    Gemini 2.5 Flash optimized JD extraction prompt.
    Generates LinkedIn-style social media snapshot (~200 words).
    """
    return f"""You are an ELITE Technical Recruiter AND Social Media Expert. Extract JD details with 100% accuracy AND create an engaging LinkedIn post.

═══════════════════════════════════════════════════════════════
MISSION: Extract skills + Generate LinkedIn-ready job post
═══════════════════════════════════════════════════════════════

## STEP 1: ANALYZE JD CONTEXT

Read the ENTIRE JD to understand:
- Role level (junior/mid/senior/lead/principal)
- Domain (backend/frontend/cloud/security/data/devops)
- Company type (startup/enterprise/product)
- Tech stack ecosystem

## STEP 2: EXTRACT MUST-HAVE SKILLS

**MUST-HAVE = Non-negotiable technical requirements**

✅ Extract if:
- "Required", "must have", "mandatory", "essential"
- "Strong experience in", "proficient with", "expert in"
- "X+ years of experience with [skill]"
- Skills in PRIMARY responsibilities (first 3-4 bullets)
- Core tech stack in job title or role overview

**Context-based extraction:**
- "Senior Python Developer" → python is must-have
- "Strong Azure experience required" → azure is must-have
- Just "Python" listed without context → must-have (default)

**Standardization (use abbreviated/short forms):**
react, angular, vue, python, java, javascript, nodejs, typescript,
aws, azure, gcp, docker, kubernetes, terraform, jenkins,
mysql, postgresql, mongodb, redis, elasticsearch,
django, flask, fastapi, spring, express,
ml, ai, tensorflow, pytorch, sklearn,
restapi, graphql, microservices, cicd

## STEP 3: EXTRACT GOOD-TO-HAVE SKILLS

**GOOD-TO-HAVE = Beneficial but not required**

✅ Extract if:
- "Nice to have", "preferred", "bonus", "plus", "a plus"
- "Familiarity with", "exposure to", "knowledge of"
- "Would be great if you know"
- Secondary/additional technologies
- Skills in "preferred" or "bonus" section

Use same standardization as must-have.

## STEP 4: EXTRACT SOFT SKILLS

**SOFT = Non-technical abilities**

✅ Extract if mentioned:
- Collaboration: "team player", "cross-functional", "stakeholder management"
- Communication: "excellent communication", "client-facing", "presentations"
- Leadership: "mentor", "lead projects", "technical leadership"
- Methodologies: "agile", "scrum", "kanban"
- Problem-solving: "analytical thinking", "creative problem solver"

**CRITICAL:** Even if JD says "must have strong communication", it goes in soft_skills (NOT must-have)!

Common soft skills (lowercase):
leadership, communication, teamwork, problemsolving, agile, scrum,
mentoring, collaboration, projectmanagement, analytical

## STEP 5: EXTRACT DOMAIN EXPERTISE

**DOMAIN = Industry/sector focus**

✅ Extract industry + specific areas:
- "Fintech experience with payment gateways" → ["fintech", "payment systems"]
- "Healthcare compliance background" → ["healthcare", "regulatory compliance"]
- "E-commerce platform development" → ["ecommerce", "retail"]

Common domains:
fintech, banking, healthcare, ecommerce, insurance, telecom,
education, cybersecurity, cloud services, legal, manufacturing

## STEP 6: EXTRACT ACCOLADES/CERTIFICATIONS

**ACCOLADES = Required/preferred certifications & qualifications**

✅ Extract:
- "AWS Certified Solutions Architect preferred"
- "Azure Administrator certification"
- "PMP certification is a plus"
- "MBA preferred"
- "B.Tech/BE required"

❌ If NO certifications mentioned → Return: "none"

## STEP 7: EXTRACT EXCEPTION SKILLS

**EXCEPTIONS = Technical skills to AVOID**

✅ Extract ONLY technical skills to avoid:
- "No PHP experience"
- "Should not have worked with legacy mainframes"
- "No WordPress developers"

❌ Ignore non-technical exceptions (agency, competitor, fresher restrictions)

❌ If NO exceptions mentioned → Return: "none"

## STEP 8: GENERATE JD SNAPSHOT (LinkedIn Format)

**SNAPSHOT = ~200 word LinkedIn post**

**CRITICAL FORMAT RULES (Follow examples exactly):**

**Structure:**
1. **Eye-catching header** (one line with emoji/power words)
2. **Job title + experience** (bold formatting with **)
3. **Brief role description** (1 sentence)
4. **Key requirements** (3-5 bullets with ✔ emoji)
5. **Location** (📍 emoji)
6. **Application email** (📩 emoji)
7. **Follow CTA** (👉 emoji)
8. **Hashtags** (4-6 relevant, all start with #)

**Example Headers (vary these, DON'T repeat):**
- "This time it is – [Job Title]"
- "Hiring Security Champs – [Job Title]"
- "Looking for [skill] experts? Here's an opportunity."
- "We're now hiring [Job Title]"
- "Big opportunity alert – [Job Title]"
- "Join us as [Job Title]"

**Example Footers (vary these):**
- "Follow Ankyah Nexus for more such opportunities!"
- "If not started yet, follow Ankyah Nexus for more openings!"
- "Stay connected with Ankyah Nexus for latest tech jobs!"

**Tone:** Professional but engaging, NOT boring corporate speak!

**Rules:**
- ❌ DON'T mention company name (unless it's a well-known brand boost)
- ❌ DON'T mention salary/benefits
- ✅ Keep it crisp: ~200 words
- ✅ Use emojis strategically (not overdone)
- ✅ Make it scannable with line breaks

═══════════════════════════════════════════════════════════════
⚠️ QUALITY CHECKLIST
═══════════════════════════════════════════════════════════════

☑ Did I read FULL JD before extracting?
☑ Are must-have skills truly REQUIRED?
☑ Did I standardize all skills (aws not "Amazon Web Services")?
☑ Are soft skills separate from technical?
☑ Is snapshot ~200 words with engaging header/footer?
☑ Did I use ✔ checkmarks for requirements?
☑ Did I include location, email, hashtags?
☑ Did I avoid company name & salary details?

═══════════════════════════════════════════════════════════════
📤 OUTPUT FORMAT (STRICT JSON - NO MARKDOWN)
═══════════════════════════════════════════════════════════════

Return ONLY this JSON. NO ```json wrapper. NO explanations.

{{
  "must_have_skills": ["python", "django", "aws", "postgresql", "docker"],
  "good_to_have_skills": ["kubernetes", "redis", "terraform"],
  "soft_skills": ["leadership", "agile", "communication"],
  "domain_expertise": ["fintech", "payment systems"],
  "accolades_keyword": ["AWS Certified Solutions Architect", "BTech Computer Science"],
  "exception_skills": "none",
  "jd_snapshot": "This time it is – Senior Backend Engineer (Python/Django)\\n\\nWe are looking for a Senior Backend Engineer (5-7 years experience) with strong expertise in building scalable APIs and payment systems.\\n\\nYou should have working exposure on:\\n✔ Python, Django, and RESTful API design\\n✔ AWS cloud infrastructure (EC2, S3, RDS)\\n✔ PostgreSQL database optimization\\n✔ Docker containerization and microservices\\n✔ Agile development and team collaboration\\n\\n📍 Location: Remote\\n📩 Share your profile to nextjob@ankyahnexus.com\\n👉 Follow Ankyah Nexus for more such opportunities!\\n\\n#Backend #Python #Django #AWS #RemoteJobs #NowHiring"
}}

═══════════════════════════════════════════════════════════════
🎯 PERFECT EXAMPLES
═══════════════════════════════════════════════════════════════

**EXAMPLE 1: Cloud Security Role**

**Input JD:**
"Job Title: Azure Cloud Security Engineer
Experience: 4-5 years
We need an Azure security expert to secure cloud workloads and automate security processes. Must have deep expertise in Microsoft Defender, Purview, and DLP solutions. Required: Azure Security Engineer certification, PowerShell scripting, ISO 27001 knowledge. Nice to have: Python automation experience."

**Perfect Output:**
{{
  "must_have_skills": ["azure", "microsoft defender", "purview", "dlp", "powershell", "iso27001"],
  "good_to_have_skills": ["python", "automation"],
  "soft_skills": ["collaboration", "analytical"],
  "domain_expertise": ["cloud security", "compliance"],
  "accolades_keyword": ["Azure Security Engineer Associate certification"],
  "exception_skills": "none",
  "jd_snapshot": "Hiring Security Champs – Azure Cloud Security Engineer | Remote\\n\\nLooking to invest your cloud security expertise? Here is an opportunity. We're now hiring an Azure Cloud Security Engineer (4–5 years experience) to lead cloud security, automation, and data protection initiatives.\\n\\nYou should have work on:\\n✔ Microsoft Defender, Purview & DLP implementation\\n✔ Azure security automation & PowerShell scripting\\n✔ Threat monitoring, compliance (ISO 27001/GDPR), and incident response\\n\\n📍 Location: Remote\\n📩 Share your profile to nextjob@ankyahnexus.com\\n👉 If not started yet, follow Ankyah Nexus for more openings!\\n\\n#CloudSecurity #AzureSecurity #MicrosoftDefender #CyberSecurityJobs #NowHiring"
}}

**EXAMPLE 2: GRC Role**

**Input JD:**
"Job Title: GRC Specialist – Third-Party Risk Management
Experience: 2-3 years
Seeking GRC specialist for vendor risk management and compliance. Must have: ISO 27001, GDPR, third-party risk assessment experience. Should manage risk registers and policy governance. Excellent communication required."

**Perfect Output:**
{{
  "must_have_skills": ["grc", "tprm", "iso27001", "gdpr", "risk assessment", "vendor management"],
  "good_to_have_skills": [],
  "soft_skills": ["communication", "analytical", "projectmanagement"],
  "domain_expertise": ["governance", "compliance", "risk management"],
  "accolades_keyword": "none",
  "exception_skills": "none",
  "jd_snapshot": "This time it is – GRC Specialist (Third-Party Risk Management)\\n\\nWe are looking for a GRC Specialist (2–3 years experience) with strong expertise in vendor risk management, compliance, and governance frameworks.\\n\\nYou should have working exposure on:\\n✔ Managing Third-Party Risk (onboarding, due diligence)\\n✔ ISO 27001, GDPR, Indian Privacy Law compliance\\n✔ Risk registers, policy governance & executive reporting\\n\\n📍 Location: Remote\\n📩 Share your profile to nextjob@ankyahnexus.com\\n👉 Follow Ankyah Nexus for more such opportunities!\\n\\n#GRCJobs #TPRM #Compliance #InfoSecJobs #RiskManagement #Hiring"
}}

**Why These Are Perfect:**
✅ Must-have: Core technical requirements clearly identified
✅ Good-to-have: Bonus skills properly separated
✅ Soft skills: Non-technical abilities extracted
✅ Domain: Industry + specific focus areas
✅ Snapshot: Follows exact LinkedIn format with emojis, checkmarks, email, hashtags
✅ ~200 words, engaging, scannable
✅ Different headers to avoid repetition

═══════════════════════════════════════════════════════════════
📄 JOB DESCRIPTION TO ANALYZE:
═══════════════════════════════════════════════════════════════

{jd_text}

═══════════════════════════════════════════════════════════════
⚡ EXTRACT NOW WITH 100% ACCURACY
═══════════════════════════════════════════════════════════════
"""
