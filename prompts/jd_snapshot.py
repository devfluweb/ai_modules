"""
JD Snapshot Generation Prompt - STEP 2
Creates LinkedIn-style job post from extracted keywords
"""

def get_jd_snapshot_prompt(jd_text: str, keywords: dict) -> str:
    """
    Generate LinkedIn-style snapshot from JD and extracted keywords.
    Step 2: Create engaging social media post
    
    Args:
        jd_text: Original JD text
        keywords: Extracted keywords from Step 1
    """
    
    prompt = f"""You are a social media expert creating a LinkedIn job post. Create an engaging post that attracts top talent.

===========================================
EXTRACTED KEYWORDS (USE THESE)
===========================================

Must-Have Skills: {', '.join(keywords.get('must_have_skills', []))}
Good-to-Have Skills: {', '.join(keywords.get('good_to_have_skills', []))}
Soft Skills: {', '.join(keywords.get('soft_skills', []))}
Domain: {', '.join(keywords.get('domain_expertise', []))}
Required Certification: {keywords.get('accolades_keyword', 'none')}

===========================================
SNAPSHOT REQUIREMENTS
===========================================

**LENGTH:** ~200 words (150-250 acceptable)

**STRUCTURE:**
1. Eye-catching header (varied, creative)
2. Job title + experience level
3. Key requirements (use ✔ checkmarks)
4. Location (if mentioned)
5. Email: nextjob@ankyahnexus.com
6. Call-to-action: "Follow Ankyah Nexus for more opportunities!"
7. Hashtags (3-5 relevant)

**MUST EXCLUDE:**
❌ Company name
❌ Salary/compensation
❌ Benefits
❌ Application deadline

**HEADER VARIATIONS (use different each time):**
- "This time it is –"
- "We're hiring –"
- "Exciting opportunity –"
- "Join our team –"
- "Ready to level up? –"
- "Your next role –"

===========================================
SNAPSHOT EXAMPLES
===========================================

**EXAMPLE 1: Backend Role**
```
This time it is – Senior Backend Engineer (Python/Django)

We are looking for a backend expert with 5+ years of experience.

✔ Strong Python & Django REST framework
✔ AWS cloud deployment experience
✔ PostgreSQL database optimization
✔ Microservices architecture
✔ Leadership & mentoring skills

Bonus: Docker, Kubernetes, Redis experience

📍 Location: Remote
📩 Share your profile: nextjob@ankyahnexus.com
👉 Follow Ankyah Nexus for more opportunities!

#BackendDevelopment #Python #Django #RemoteJobs #Hiring
```

**EXAMPLE 2: DevOps Role**
```
Ready to level up? – DevOps Engineer (AWS/Kubernetes)

Seeking a DevOps expert with 4+ years managing cloud infrastructure.

✔ AWS services (EC2, S3, RDS, Lambda)
✔ Kubernetes & Docker orchestration
✔ Terraform infrastructure-as-code
✔ CI/CD pipeline automation
✔ Agile team collaboration

Nice-to-have: Prometheus, Grafana monitoring

📍 Location: Hybrid (Bangalore)
📩 Interested? Email: nextjob@ankyahnexus.com
👉 Follow Ankyah Nexus for more opportunities!

#DevOps #AWS #Kubernetes #CloudEngineering #Hiring
```

**EXAMPLE 3: Full-Stack Role**
```
Your next role – Full-Stack Developer (React/Node.js)

Looking for a versatile engineer with 3+ years in modern web development.

✔ React.js with TypeScript
✔ Node.js backend APIs
✔ MongoDB/PostgreSQL databases
✔ RESTful & GraphQL APIs
✔ Agile development practices

Bonus: Next.js, AWS, Docker knowledge

📍 Location: Remote (India)
📩 Apply: nextjob@ankyahnexus.com
👉 Follow Ankyah Nexus for more opportunities!

#FullStack #React #NodeJS #JavaScript #RemoteWork
```

===========================================
FORMATTING RULES
===========================================

1. **Use emojis:** ✔ for requirements, 📍 for location, 📩 for email, 👉 for CTA
2. **Short lines:** Easy to scan
3. **Bullet points:** Use ✔ checkmarks
4. **Hashtags:** 3-5 relevant, no spaces
5. **Professional tone:** Friendly but not casual
6. **Action-oriented:** "Join", "Apply", "Share"

===========================================
ORIGINAL JD (FOR CONTEXT)
===========================================

{jd_text}

===========================================
CREATE LINKEDIN POST NOW
===========================================

Generate a compelling LinkedIn-style job post using the extracted keywords and following all formatting rules.

**Output ONLY the snapshot text, NO JSON, NO explanations.**
"""
    
    return prompt