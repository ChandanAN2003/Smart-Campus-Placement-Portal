
# 🎓 Smart Campus Placement & Talent Management Portal
## 📘 Comprehensive Exam Master Guide (2026) -> "The Bible for Project Work"

*Last Updated for Final Exam Revision*

---

# 📚 Table of Contents
1.  **Project Abstract & Executive Summary**
2.  **System Requirements (Functional & Non-Functional)**
3.  **Software Architecture (MVC Pattern + File Structure)**
4.  **Database Design (ER Logic & Constraints)**
5.  **Core Modules & Feature Deep-Dive (RBAC)**
6.  **AI Integration Logic (The "Brain")**
7.  **Frontend Deep-Dive (Three.js & Web Speech)** 🆕
8.  **Algorithms & Logic Flow** 🆕
9.  **Deployment & Security** 🆕
10. **Challenges Faced & Solutions** 🆕
11. **Viva Voce: Code Defense (Q&A)** 🆕

---

# 1. Project Abstract
The **Smart Campus Placement Portal** is a production-grade web application designed to bridge the gap between academic institutions and company recruitment standards. Traditional placement systems rely on manual data entry and lack personalized guidance. This project introduces an **AI-First Approach**, leveraging **Google Gemini 1.5 Pro** to provide:
1.  **Automated Resume Screening (ATS)**
2.  **Personalized Career Coaching (Skill Gap Analysis)**
3.  **Mock Interview Simulation (Voice-Enabled)**
4.  **Centralized Management (TPO/HOD Dashboards)**

---

# 2. System Requirements
### **A. Functional Requirements**
*   **RBAC:** Students, TPOs, HODs have distinct dashboards.
*   **Recruitment:** Create drives, track applications (Applied → Selected).
*   **AI Services:** Resume Parsing, Chatbot assistance, Code Evaluation.
*   **Gamification:** Points/Badges system to encourage daily practice.

### **B. Non-Functional Requirements**
*   **Scalability:** Uses SQLAlchemy Connection Pooling (`QueuePool`) for 500+ concurrent users.
*   **Security:** Passwords hashed with `PBKDF2-SHA256` (Werkzeug).
*   **Availability:** Fallback to Groq API if Gemini is down.
*   **UI/UX:** Responsive Glassmorphism design using Bootstrap 5.

---

# 3. Software Architecture (MVC + File Structure)

### **A. Project Directory Structure**
When showing your project folder, explain this structure:
```
Smart-Campus-Placement-Portal/
├── backend/
│   ├── app.py                # CONTROLLER: Main Flask Routes
│   ├── database.py           # MODEL: Connection Pooling & Queries
│   ├── gemini_ai.py          # SERVICE: AI Logic (Resume, Chat, Interview)
│   ├── gamification_service.py # SERVICE: Points & Badges Logic
│   └── leetcode_service.py   # SERVICE: Coding Problem Fetcher
├── frontend/
│   ├── templates/            # VIEW: HTML Files (Jinja2)
│   │   ├── student_dashboard.html
│   │   └── tpo_dashboard.html
│   └── static/
│       ├── css/              # Styles (Glassmorphism)
│       └── js/
│           ├── background3d.js # Three.js Animation
│           └── chat_widget.js  # Voice Chat Logic
```

### **B. MVC Pattern Applied**
1.  **Model:** `database.py` manages connections. We use "Raw SQL" via SQLAlchemy to demonstrate deep understanding of queries during the exam.
2.  **View:** HTML templates receive variables like `{{ student.name }}` from Flask.
3.  **Controller:** `app.py` ties everything together. E.g., The `/login` route validates input -> checks DB -> sets Session -> returns View.

---

# 4. Database Design (ER Logic)
**Relationships:**
*   **User (1) ↔ (M) Applications:** A student applies to many jobs.
*   **Drive (1) ↔ (M) Applications:** A job has many applicants.
*   **Constraint:** `UNIQUE (student_id, drive_id)` in `applications` table.
    *   *Why?* It physically prevents the same student from applying twice to the same company.

---

# 5. Core Modules & Feature Deep-Dive

## **A. Student Module**
1.  **AI Resume Analyzer:**
    *   Upload PDF -> Text Extraction (`PyPDF2`) -> Gemini Prompt -> JSON Output.
2.  **Gamification:**
    *   Logic: `update users set score = score + 50`.
    *   Badges: "Code Ninja", "Placement Ready".
3.  **Mock Test:**
    *   AI generates 5 MCQs based on Job Role.

## **B. TPO Module**
1.  **Drive Management:**
    *   Supports **"Just-In-Time" Migration**. IF the DB schema is old, the code detects it and adds columns (`vacancy_count`) automatically.
2.  **Offer Upload:**
    *   Auto-emails student when offer is uploaded.

## **C. HOD Module**
1.  **Verification Layer:**
    *   Prevents fake registrations. Students cannot login until `is_approved=True`.

---

# 6. AI Integration Logic (The "Brain")

### **Strategy: "Persona-Based Prompting"**
We define specific personas for the AI in `gemini_ai.py`.
*   **Interview Persona:** "You are a strict HR manager. Ask strictly one question at a time."
*   **ATS Persona:** "You are an ATS scanner. Output ONLY JSON."

### **SafeGenerativeModel Wrapper**
We wrapped the standard Gemini call in a class `SafeGenerativeModel`.
*   **Why?** To handle API Quota limits.
*   **Logic:** `try: call_gemini() except QuotaError: call_groq()`.
*   This ensures the demo **never fails** in front of the external examiner.

---

# 7. Frontend Deep-Dive (Visuals) 🆕

### **A. Three.js Background (`background3d.js`)**
*   **What is it?** A particle wave animation on the login page.
*   **Tech:** Uses WebGL render engine.
*   **Logic:** We create a grid of `60x60` particles. In the `render()` loop, we change their Y-position using a `Math.sin()` wave function to create the "floating ocean" effect.

### **B. Voice Chat Widget (`chat_widget.js`)**
*   **Speech-to-Text:** Uses browser's native `window.SpeechRecognition` API.
*   **Text-to-Speech:** Uses `window.speechSynthesis` API.
*   **Smart Voice Selection:** The code builds a list of available voices and tries to pick a "Google" voice matching the selected language (e.g., `hi-IN` for Hindi) for a more natural accent.

---

# 8. Algorithms & Logic Flow 🆕

### **Algorithm 1: LeetCode Fetching (`leetcode_service.py`)**
1.  **Attempt 1:** Send a GraphQL POST request to `leetcode.com/graphql`.
2.  **Failure Check:** If LeetCode blocks the request (Anti-Bot), catch the Exception.
3.  **Fallback:** Load questions from a local Dictionary `FALLBACK_PROBLEMS`.
4.  **Result:** The user *always* sees questions, even without internet.

### **Algorithm 2: Skill Gap Analysis**
1.  **Input:** Resume Text + Job Description.
2.  **AI Processing:** Identify set `A` (Resume Skills) and set `B` (Job Skills).
3.  **Gap:** Compute `B - A` (Set Difference).
4.  **Mapping:** Map missing keywords to a predefined list of "Course Recommendations".

---

# 9. Deployment & Security 🆕

### **Security Measures**
1.  **SQL Injection:** We use **Parameterized Queries** (`%s` placeholders) in `db.execute_query`. We *never* use f-strings for SQL values.
2.  **XSS Protection:** Jinja2 templates auto-escape variables.
3.  **Session Hijacking:** Flask signs the session cookie with a secret key.

### **Deployment (Render.com)**
*   **Dockerfile:** Installs Python 3.10, creates a virtualenv, and runs `gunicorn` (Production Server).
*   **Environment Variables:** API Keys secrets are stored in Environment Variables, not in the code.

---

# 10. Challenges Faced & Solutions 🆕
*Asking this is the Examiner's favorite question.*

1.  **Challenge:** "Gemini API has a rate limit (RPM)."
    *   **Solution:** Implemented a Key Rotation system (switches between multiple API keys) and a Fallback to Groq API.
2.  **Challenge:** "Resumes are in different formats (PDF/DOCX)."
    *   **Solution:** Used `PyPDF2` for PDFs and `python-docx` for Word files to handle both.
3.  **Challenge:** "Real-time Voice Chat latency."
    *   **Solution:** Used browser-side Web Speech API (instead of sending audio to server) to make recognition instant.

---

# 11. Viva Voce: Code Defense (Q&A) 🆕

**Q: Show me your Database Connection code.**
**A:** Open `backend/database.py`. Point to `pool_size=10` and explain: "Sir, I used a QueuePool to allow multiple users to connect simultaneously without crashing MySQL."

**Q: How does the Chatbot speak Hindi?**
**A:** Open `backend/gemini_ai.py`. Show the prompt: *"YOU MUST RESPOND IN {target_lang}"*. Then open `frontend/js/chat_widget.js` and show `utterance.lang = 'hi-IN'`.

**Q: Where is the AI logic?**
**A:** "It is in `backend/gemini_ai.py`. I created modular functions like `analyze_resume` and `generate_mock_test` so they can be reused."

**Q: Why didn't you use React/Angular?**
**A:** "For a Single Page Application (SPA) feel, I used vanilla JS with asynchronous `fetch()` calls. This kept the architecture simple and avoided the overhead of a separate frontend build process for this timeline."

---
**Final Note:** Speak with confidence. You built a system that handles **Data**, **AI**, **Voice**, and **Gamification**. That is impressive. Good luck!
