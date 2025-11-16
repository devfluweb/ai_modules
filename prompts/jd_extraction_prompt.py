"""
JD Extraction Prompt - Final Version for Gemini 2.5 Flash
Extracts: must_have_skills, good_to_have_skills, soft_skills,
domain_expertise, accolades_keyword, exception_skills, jd_snapshot

NOTE:
- This prompt is optimized for Gemini 2.5 Flash.
- It is used for CV–JD matching in a production system.
- Keep this file structure the same to avoid integration issues.
"""

def get_jd_extraction_prompt(jd_text: str) -> str:
    """
    Gemini 2.5 Flash optimized JD extraction prompt.
    Generates a structured JSON and a LinkedIn-style job snapshot.
    """
    return f"""You are a PRODUCTION-GRADE Job Description Extractor inside an AI Recruitment Platform.
Your output will be used for automated CV–JD matching and scoring.
Accuracy, consistency, and NO hallucinations are critical.

You MUST follow ALL instructions below EXACTLY.

────────────────────────────────────────────────────────
PHASE 1 — UNDERSTAND THE JD (INTERNAL ONLY)
────────────────────────────────────────────────────────

1. Carefully read the ENTIRE job description (JD) provided later.
2. Internally infer (for your reasoning only, DO NOT output directly):
   - Role type (e.g., backend, frontend, fullstack, ml, data, devops, mobile, security, qa, embedded, enterprise, cloud, etc.)
   - Experience level (e.g., junior, mid, senior, lead)
   - Core responsibilities and main problem space

You will NOT output these internal inferences directly.
They are only to guide your extraction quality.

────────────────────────────────────────────────────────
PHASE 2 — SKILL EXTRACTION LOGIC (VERY IMPORTANT)
────────────────────────────────────────────────────────

You must extract ONLY SKILLS / CAPABILITIES, not generic phrases or responsibilities.

All skill tokens MUST be:
- lowercase
- without spaces (use camelCase or single tokens where needed)
- specific and meaningful

Examples:
- "Node.js" → "nodejs"
- "REST APIs" → "restapi"
- "Time management" → "timemanagement"
- "C++" → "c++"

Never include generic phrases like "software development", "web applications", "excellent", "strong", etc., as skills.


────────────────────────────────────────────────────────
PHASE 2.1 — MUST-HAVE SKILLS (STRICT MODE)
────────────────────────────────────────────────────────

You are in STRICT mode for must_have_skills.

A skill MUST be placed under "must_have_skills" ONLY IF:

1) It is clearly part of the CORE tech stack or responsibilities, AND
2) It is described as REQUIRED, MANDATORY, or ESSENTIAL using words such as:
   - "must have", "required", "mandatory", "non-negotiable"
   - "strong experience in", "hands-on experience with", "proficient in", "expert in"
   - "X+ years of experience with [skill]"
   AND/OR
3) The job title itself strongly implies that skill as central
   - "React Developer" → react is must-have
   - "Node.js Backend Engineer" → nodejs is must-have
   - "Python Data Engineer" → python is must-have

ADDITIONAL RULES:
- You MUST be selective.
- Do NOT dump every mentioned technology into must_have_skills.
  - Choose ONLY the most critical ones based on:
    - direct connection to primary responsibilities,
    - frequency of mention,
    - importance for performing the role,
    - alignment with the job title.

If a skill is important but not clearly mandatory, put it in good_to_have_skills instead.


────────────────────────────────────────────────────────
PHASE 2.2 — GOOD-TO-HAVE SKILLS
────────────────────────────────────────────────────────

A skill belongs to "good_to_have_skills" if:

- It is clearly OPTIONAL:
  - Keywords in JD: "nice to have", "preferred", "good to have", "bonus", "a plus", "added advantage", "optional"
- It appears as part of a long tech list but is not emphasized as core.
- It supports the role but is not essential to perform daily responsibilities.
- It is mentioned as "familiarity with", "exposure to", "knowledge of", or "experience with" without strong mandatory wording.

You can include more skills here than in must_have_skills, but still avoid random noise.


────────────────────────────────────────────────────────
PHASE 2.3 — OR-CONDITION / ALTERNATIVE SKILLS
────────────────────────────────────────────────────────

The JD may specify ALTERNATIVE or OPTIONAL skills, like:

- "SQL or MongoDB"
- "Kafka or RabbitMQ"
- "React / Angular / Vue"
- "AWS, GCP or Azure"
- "MySQL/PostgreSQL"

For ANY such alternative set, you MUST:

1) Combine them into ONE skill token with "/" between them, e.g.:
   - "sql/mongodb"
   - "kafka/rabbitmq"
   - "react/angular/vue"
   - "aws/gcp/azure"
   - "mysql/postgresql"

2) Do NOT split these alternatives into separate skills.
3) By default, treat these combined tokens as good_to_have_skills,
   UNLESS the JD clearly states that one of them is mandatory (e.g., "must have experience in either AWS, GCP or Azure").
4) If the JD clearly states that at least one of the alternatives is mandatory for the role,
   you MAY put the combined token (e.g., "aws/gcp/azure") under must_have_skills,
   but still respect the MAX 8 must-have skills rule.


────────────────────────────────────────────────────────
PHASE 3 — WIDE DOMAIN SKILL COVERAGE
────────────────────────────────────────────────────────

You must support extraction across the full CS/IT spectrum, including but not limited to:

- Frontend: react, angular, vue, html, css, javascript, typescript
- Backend: nodejs, express, django, flask, fastapi, spring, dotnet, go, ruby, php, laravel
- Mobile: kotlin, swift, flutter, reactnative
- DevOps / Cloud: aws, azure, gcp, docker, kubernetes, terraform, ansible, jenkins, githubactions, gitlabci
- Data Engineering: spark, kafka, airflow, dbt, hadoop
- Databases: mysql, postgresql, sqlserver, oracle, mongodb, cassandra, redis, dynamodb, elasticsearch
- ML / AI: python, tensorflow, pytorch, sklearn, xgboost, langchain, vectordb
- Cybersecurity: siem, soc, vulnerabilityassessment, penetrationtesting, iam, zeroTrust
- QA / Automation: selenium, cypress, playwright, junit, pytest
- Embedded / IoT: c, c++, rtos, microcontrollers, freertos
- Enterprise: sap, salesforce, oracle-fusion, dynamics365

Normalize everything to lowercase.


────────────────────────────────────────────────────────
PHASE 4 — SOFT SKILLS
────────────────────────────────────────────────────────

Extract ONLY genuine soft skills, not technical skills.

Valid soft skills include (but are not limited to):

- communication
- teamwork
- leadership
- ownership
- accountability
- problemsolving
- criticalthinking
- adaptability
- selfmanagement
- timemanagement
- collaboration
- analytical
- agile
- mentoring
- stakeholdermanagement

RULES:
- Even if the JD says "must have excellent communication skills", it still goes under soft_skills.
- Do NOT put soft skills into must_have_skills or good_to_have_skills.
- No duplicates. Each soft skill should appear once at most.


────────────────────────────────────────────────────────
PHASE 5 — DOMAIN EXPERTISE
────────────────────────────────────────────────────────

"domain_expertise" is about INDUSTRY / BUSINESS CONTEXT, not technologies.

Examples of domain expertise values:

- fintech
- banking
- insurance
- ecommerce
- retail
- healthcare
- pharma
- telecom
- saas
- ai-ml
- cybersecurity
- gaming
- education-tech
- travel
- logistics
- manufacturing
- govtech
- media

If the JD clearly indicates a domain (e.g., "payments", "e-commerce platform", "healthcare systems"), add appropriate short tokens.

If there is NO obvious domain, return ["none"].


────────────────────────────────────────────────────────
PHASE 6 — ACCOLADES / CERTIFICATIONS / EDUCATION
────────────────────────────────────────────────────────

"accolades_keyword" should contain only explicit certifications or education-type requirements, such as:

- btech
- be
- bsc
- mca
- msc
- mba
- phd
- aws-certified
- azure-certified
- gcp-certified
- cissp
- pmp
- scrum-master
- istqb

Normalize to lowercase, short readable tokens.

If the JD does NOT mention any education or certifications, return ["none"].


────────────────────────────────────────────────────────
PHASE 7 — EXCEPTION SKILLS
────────────────────────────────────────────────────────

"exception_skills" is for technical skills that the JD explicitly says to AVOID.

Examples:
- "No PHP developers"
- "Should not have mainframe experience"
- "No WordPress-only profiles"

In such cases, extract the mentioned tech as tokens:
- "php"
- "mainframe"
- "wordpress"

If there are NO such exclusion statements, return ["none"].


────────────────────────────────────────────────────────
PHASE 8 — LINKEDIN SNAPSHOT (jd_snapshot)
────────────────────────────────────────────────────────

You must generate a short LinkedIn-style job post (6–8 lines), based ONLY on the JD.

Rules:

- DO NOT hallucinate company name, salary, or benefits.
- Use an engaging but professional tone.
- Use checkmarks (✔) for bullet points.
- Use emojis: 📍 for location, 📩 for email if present, 👉 for call-to-action.
- Rough structure:

Line 1: Attention-grabbing header with job title  
Line 2–3: One-line summary of role and experience  
Line 4–6: 3–5 bullets with ✔ for key requirements or stack  
Line 7: Location line if available (📍)  
Line 8: Application or call-to-action line (📩 / 👉)

Keep it concise and scannable (not more than ~120–150 words).


────────────────────────────────────────────────────────
PHASE 9 — OUTPUT FORMAT (STRICT JSON ONLY)
────────────────────────────────────────────────────────

You MUST return ONLY a single JSON object with this EXACT structure:

{{
  "must_have_skills": [],
  "good_to_have_skills": [],
  "soft_skills": [],
  "domain_expertise": [],
  "accolades_keyword": [],
  "exception_skills": [],
  "jd_snapshot": ""
}}

CRITICAL RULES:
- The root type MUST be a JSON object.
- All keys MUST exist even if values are empty.
- If no values, use empty list [] or a list with "none" as described above.
- "jd_snapshot" MUST be a non-empty string.
- Do NOT wrap JSON in ```json or any markdown.
- Do NOT add any explanation, comments, or text outside the JSON.
- Do NOT include your reasoning in the output.

────────────────────────────────────────────────────────
JOB DESCRIPTION TO ANALYZE
────────────────────────────────────────────────────────

{jd_text}

────────────────────────────────────────────────────────
NOW RETURN THE JSON OUTPUT ONLY
────────────────────────────────────────────────────────
"""
