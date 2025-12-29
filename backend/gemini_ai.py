"""
Google Gemini API integration for AI features
"""
import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Try to import groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# API Key Management
GEMINI_KEYS = []
if os.getenv('GEMINI_API_KEY'):
    GEMINI_KEYS.append(os.getenv('GEMINI_API_KEY'))
if os.getenv('GEMINI_API_KEYS'):
    GEMINI_KEYS.extend([k.strip() for k in os.getenv('GEMINI_API_KEYS').split(',') if k.strip()])

i = 1
while os.getenv(f'GEMINI_API_KEY_{i}'):
    GEMINI_KEYS.append(os.getenv(f'GEMINI_API_KEY_{i}'))
    i += 1

GEMINI_KEYS = list(dict.fromkeys(GEMINI_KEYS))
CURRENT_KEY_INDEX = 0

def configure_gemini():
    """Configure Gemini with the current key"""
    global CURRENT_KEY_INDEX
    if GEMINI_KEYS:
        key = GEMINI_KEYS[CURRENT_KEY_INDEX]
        masked_key = key[:4] + "..." + key[-4:] if len(key) > 8 else "***"
        print(f"[DEBUG] Configuring Gemini with Key #{CURRENT_KEY_INDEX + 1}: {masked_key}")
        genai.configure(api_key=key)

def rotate_key():
    """Switch to the next available Gemini API key"""
    global CURRENT_KEY_INDEX
    if len(GEMINI_KEYS) > 1:
        CURRENT_KEY_INDEX = (CURRENT_KEY_INDEX + 1) % len(GEMINI_KEYS)
        print(f"[INFO] Rotating to Gemini Key index: {CURRENT_KEY_INDEX}")
        configure_gemini()
        return True
    return False

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
configure_gemini()

class SafeGenerativeModel:
    def __init__(self, primary_model_name, fallback_models=None):
        self.primary_model_name = primary_model_name
        self.fallback_models = fallback_models or [
            "llama-3.3-70b-versatile", 
            "mixtral-8x7b-32768", 
            "llama3-70b-8192", 
            "gemini-1.5-flash"
        ]
        self.current_model = genai.GenerativeModel(primary_model_name)
        self.groq_client = None
        if GROQ_AVAILABLE and GROQ_API_KEY:
            self.groq_client = Groq(api_key=GROQ_API_KEY)

    def generate_content(self, prompt, **kwargs):
        try:
            return self.current_model.generate_content(prompt, **kwargs)
        except Exception as e:
            error_str = str(e).lower()
            print(f"[WARN] Error with {self.primary_model_name}: {error_str}. Switching to fallbacks...")
            
            if "quota" in error_str or "429" in error_str or "limit" in error_str or "resource exhausted" in error_str:
                if rotate_key():
                     print(f"[INFO] Retrying {self.primary_model_name} with new API key...")
                     try:
                         return self.current_model.generate_content(prompt, **kwargs)
                     except Exception as retry_e:
                         print(f"[WARN] Retry with new key failed: {retry_e}")

            for model_name in self.fallback_models:
                print(f"[DEBUG] Attempting fallback: {model_name}")
                if "llama" in model_name or "mixtral" in model_name:
                    if self.groq_client:
                        try:
                            completion = self.groq_client.chat.completions.create(
                                model=model_name,
                                messages=[{"role": "user", "content": prompt}],
                                temperature=kwargs.get('temperature', 1),
                                max_tokens=1024,
                                top_p=1,
                                stream=False,
                                stop=None
                            )
                            class MockResponse:
                                def __init__(self, text): self.text = text
                            return MockResponse(completion.choices[0].message.content)
                        except Exception as groq_err:
                            print(f"[WARN] Groq failed: {groq_err}")
                            continue
                try:
                    fallback_model = genai.GenerativeModel(model_name)
                    return fallback_model.generate_content(prompt, **kwargs)
                except Exception as fallback_error:
                    print(f"[WARN] Failed with {model_name}: {fallback_error}")
                    continue
            raise e

def _get_generative_model(model_name="gemini-1.5-flash"):
    return SafeGenerativeModel(model_name)

# ==========================================
# PLACEMENT-AI SYSTEM PROMPT
# ==========================================
PLACEMENT_AI_SYSTEM_PROMPT = """
You are “PLACEMENT-AI”, an intelligent Large Language Model assistant
integrated into a Smart College Placement Portal.

ROLE & PURPOSE:
Your primary role is to assist students, Training & Placement Officers (TPOs),
and Heads of Departments (HODs) by providing accurate, unbiased, and
context-aware guidance related to campus placements.

You do NOT replace human decision-making.
You act as an AI assistant that supports placement activities.

────────────────────────────────────
DOMAIN KNOWLEDGE SCOPE
────────────────────────────────────
You are strictly limited to the following domains:

1. Campus placement processes
2. Resume analysis and improvement
3. ATS (Applicant Tracking System) scoring
4. Job eligibility evaluation
5. Skill-gap analysis
6. Interview preparation (HR + Technical)
7. Company-specific hiring patterns
8. Career guidance for students
9. Portal usage instructions and rules

If a query is outside this scope, politely decline and redirect the user
to placement-related topics only.

────────────────────────────────────
USER ROLES & BEHAVIOR
────────────────────────────────────
Student:
- Explain eligibility clearly
- Give resume improvement tips
- Suggest missing skills
- Provide interview guidance
- Maintain a friendly and motivating tone

TPO / HOD:
- Provide concise analytical responses
- Summarize candidate strengths/weaknesses
- Assist in fair and unbiased shortlisting
- Use professional and formal language

────────────────────────────────────
ETHICS & SAFETY
────────────────────────────────────
• Do NOT discriminate based on gender, caste, religion, or background
• Do NOT generate false eligibility
• Always mention that final decisions rest with TPOs
• Handle student data confidentially
• Avoid absolute guarantees (e.g., “You will be selected”)
"""

def analyze_resume(resume_text, job_role, job_description="", user_role="Student"):
    """
    Analyze resume using Gemini API and return job-fit analysis
    """
    if not GEMINI_KEYS:
        return {
            'skills': [],
            'matching_skills': [],
            'missing_skills': [],
            'education': 'Not analyzed',
            'experience': 'Not analyzed',
            'job_fit_score': 0,
            'ats_score': 0,
            'eligibility_status': 'Unknown',
            'reason': 'Gemini API key not configured',
            'suggestions': 'Gemini API key not configured'
        }
    
    try:
        prompt = f"""
        {PLACEMENT_AI_SYSTEM_PROMPT}

        CONTEXT:
        User Role: {user_role}

        OUTPUT FORMAT RULES:
        When analyzing resumes against job roles, you MUST strictly follow this JSON structure:
        {{
            "ats_score": (Integer 0-100),
            "matching_skills": ["Skill 1", "Skill 2"],
            "missing_skills": ["Skill A", "Skill B"],
            "eligibility_status": "Eligible" or "Not Eligible" or "Needs Review",
            "reason_for_decision": "Clear justification based on rules + resume",
            "improvement_suggestions": ["Actionable advice 1", "Actionable advice 2"],
            "education_summary": "Extracted education summary",
            "experience_summary": "Extracted experience summary"
        }}

        TASK: Analyze this resume for the role: {job_role}
        
        Job Description: {job_description if job_description else 'Standard requirements for this role'}
        
        Resume Content:
        {resume_text[:12000]}
        
        Provide the analysis in the strict JSON format defined above.
        """
        
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text.strip()
        
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        result = {}
        if json_match:
            try:
                result = json.loads(json_match.group())
            except:
                pass
        
        def get_list(key):
            val = result.get(key, [])
            if isinstance(val, str): return [val]
            return val
            
        suggestions_list = get_list('improvement_suggestions')
        suggestions_str = "\\n".join(suggestions_list)
        
        final_result = {
            'job_fit_score': result.get('ats_score', 0),
            'ats_score': result.get('ats_score', 0),
            'skills': get_list('matching_skills'), # Backward compat
            'matching_skills': get_list('matching_skills'),
            'missing_skills': get_list('missing_skills'),
            'eligibility_status': result.get('eligibility_status', 'Unknown'),
            'reason': result.get('reason_for_decision', 'No reason provided.'),
            'suggestions': suggestions_str,
            'improvement_suggestions': suggestions_list,
            'education': result.get('education_summary', 'Not extracted'),
            'experience': result.get('experience_summary', 'Not extracted')
        }
        
        if not result and response_text:
             final_result['suggestions'] = response_text[:1000]
             final_result['skills'] = extract_skills_from_text(response_text)
             final_result['job_fit_score'] = extract_score(response_text)
             
        return final_result
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {
            'skills': [],
            'education': 'Analysis failed',
            'experience': 'Analysis failed',
            'job_fit_score': 0,
            'suggestions': f'Error details: {str(e)}'
        }

def perform_skill_gap_analysis(resume_text, job_role, job_description=""):
    """
    Perform detailed skill gap analysis and suggest learning path
    """
    if not GEMINI_KEYS:
        return None

    try:
        prompt = f"""
        {PLACEMENT_AI_SYSTEM_PROMPT}
        
        TASK: Perform a detailed Skill Gap Analysis matching this resume against the target role: {job_role}.
        
        RESUME CONTENT:
        {resume_text[:10000]}
        
        REQUIREMENTS:
        {job_description if job_description else 'Standard industry requirements for this role'}
        
        OUTPUT FORMAT:
        Return ONLY a raw JSON object. Do NOT wrap it in markdown code blocks.
        
        JSON STRUCTURE:
        {{
            "ats_score": 85,
            "missing_skills": ["List", "Of", "Missing", "Skills"],
            "skill_gap_analysis": "A short paragraph explaining the gaps.",
            "recommended_courses": [
                {{"title": "Course Title", "platform": "Platform Name", "link": "#", "duration": "Estimate"}}
            ],
            "project_ideas": [
                {{"title": "Project Title", "description": "Short desc", "tech_stack": "Tools used"}}
            ],
            "interview_prep_topics": ["Topic 1", "Topic 2", "Topic 3"]
        }}
        """
        
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean potential markdown wrapping
        if response_text.startswith("```json"): response_text = response_text[7:]
        if response_text.startswith("```"): response_text = response_text[3:]
        if response_text.endswith("```"): response_text = response_text[:-3]
        response_text = response_text.strip()

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {
                "ats_score": 75,
                "missing_skills": ["Analysis failed to parse"],
                "skill_gap_analysis": "We could not automatically parse the AI response.",
                "recommended_courses": [],
                "project_ideas": [],
                "interview_prep_topics": ["General Prep"]
            }

    except Exception as e:
        print(f"Skill gap analysis error: {e}")
        return {
            "ats_score": 0,
            "missing_skills": [],
            "skill_gap_analysis": f"Analysis Error: {str(e)}",
            "recommended_courses": [],
            "project_ideas": [],
            "interview_prep_topics": []
        }

def generate_mock_test(job_role, difficulty="Medium"):
    """
    Generate technical mock test questions
    """
    fallback_questions = [
        {"id": 1, "question": "Time complexity of BST search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "correct_answer": "O(log n)", "explanation": "Logarithmic time."},
        {"id": 2, "question": "LIFO data structure?", "options": ["Queue", "Stack", "List", "Tree"], "correct_answer": "Stack", "explanation": "Stack is LIFO."}
    ]

    if not GEMINI_KEYS:
        return fallback_questions

    try:
        prompt = f"""
        Generate a professional mock test for the role: {job_role}
        Difficulty: {difficulty}
        
        Generate 5 multiple choice questions (MCQs).
        Provide JSON response in this format:
        [
            {{
                "id": 1,
                "question": "Question text...",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "explanation": "Why it is correct..."
            }}
        ]
        """
        
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            questions = json.loads(json_match.group())
            if len(questions) > 0:
                 return questions
        return fallback_questions
        
    except Exception:
        return fallback_questions

def generate_email_content(email_type, recipient_name, company_name, job_role, additional_info=""):
    """Generate professional email content"""
    if not GEMINI_KEYS:
        return get_default_email(email_type, recipient_name, company_name, job_role)
    
    try:
        prompt = f"""
        Generate a professional {email_type} email for a college placement scenario.
        Recipient: {recipient_name}, Company: {company_name}, Position: {job_role}
        Additional Info: {additional_info}
        
        Format:
        SUBJECT: [subject line]
        BODY: [email body]
        """
        
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(max_output_tokens=1000, temperature=0.7))
        response_text = response.text.strip()
        
        lines = response_text.split('\\n')
        subject = ""
        body_lines = []
        in_body = False
        
        for line in lines:
            if line.startswith('SUBJECT:'):
                subject = line.replace('SUBJECT:', '').strip()
            elif line.startswith('BODY:'):
                in_body = True
            elif in_body:
                body_lines.append(line)
        
        body = '\\n'.join(body_lines).strip() if body_lines else response_text
        if not subject: subject = get_default_subject(email_type, company_name, job_role)
        
        return {'subject': subject, 'body': body if body else get_default_email(email_type, recipient_name, company_name, job_role)['body']}
        
    except Exception as e:
        print(f"Email generation error: {e}")
        return get_default_email(email_type, recipient_name, company_name, job_role)

def get_default_email(email_type, recipient_name, company_name, job_role):
    templates = {
        'offer': {
            'subject': f'Congratulations! Offer Letter from {company_name}',
            'body': f'Dear {recipient_name},\\n\\nWe are pleased to inform you that you have been selected for the position of {job_role} at {company_name}.\\n\\nCongratulations!'
        },
        'rejection': {
            'subject': f'Application Update - {company_name}',
            'body': f'Dear {recipient_name},\\n\\nThank you for your interest in the {job_role} position at {company_name}.\\n\\nWe regret to inform you that we will not be moving forward with your application.'
        },
        'shortlist': {
            'subject': f'Shortlisted for {job_role} - {company_name}',
            'body': f'Dear {recipient_name},\\n\\nCongratulations! You have been shortlisted for the {job_role} position at {company_name}.'
        }
    }
    return templates.get(email_type, templates['rejection'])

def generate_coding_problem(topic, difficulty):
    """Generate LeetCode-style coding problem"""
    if not GEMINI_KEYS: return None
    try:
        prompt = f"""
        Generate a unique LeetCode-style coding problem.
        Topic: {topic}, Difficulty: {difficulty}
        Provide JSON output with keys: title, description, examples, constraints, starter_code.
        """
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
        if json_match: return json.loads(json_match.group())
        return None
    except Exception: return None

def evaluate_code_submission(code, language, problem_data):
    """Evaluate code submission"""
    if not GEMINI_KEYS: return {"status": "error", "output": "API Key Missing"}
    try:
        prompt = f"""
        Act as a Code Judge.
        Problem: {problem_data.get('title')}
        Code ({language}): {code}
        JSON Response: {{ "status": "success/error", "output": "...", "analysis": "...", "error": "..." }}
        """
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        json_match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)
        if json_match: return json.loads(json_match.group())
        return {"status": "error", "output": "Failed to parse AI judge response."}
    except Exception as e: return {"status": "error", "output": str(e)}

def generate_interview_response(history, topic, language="en-US"):
    """Generate interview response"""
    if not GEMINI_KEYS: return "AI Configuration Error."
    try:
        lang_map = {"en-US": "English", "hi-IN": "Hindi"}
        context_str = f"You are a strict but professional Interviewer conducting a {topic} interview in {lang_map.get(language, language)}.\\nAsk one question at a time.\\n"
        for turn in history:
            role = "Candidate" if turn['role'] == 'user' else "Interviewer"
            context_str += f"{role}: {turn['message']}\\n"
        context_str += "Interviewer:"
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(context_str)
        return response.text.strip()
    except Exception: return "Connection trouble."

def get_default_subject(email_type, company_name, job_role):
    subjects = {
        'offer': f'Congratulations! Offer Letter from {company_name}',
        'rejection': f'Application Update - {company_name}',
        'shortlist': f'Shortlisted for {job_role} - {company_name}'
    }
    return subjects.get(email_type, f'Update from {company_name}')

def generate_aptitude_questions(count=5):
    """Generate aptitude questions"""
    if not GEMINI_KEYS: return []
    try:
        prompt = f"Generate {count} MCQs (Aptitude/Logical). JSON Output: [{{'question': '...', 'options': [], 'correct_index': 0, 'explanation': '...'}}]"
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(prompt)
        json_match = re.search(r'\[.*\]', response.text.strip(), re.DOTALL)
        if json_match: return json.loads(json_match.group())
        return []
    except Exception: return []

# --- Helper Functions (Restored) ---

def extract_skills_from_text(text):
    """Extract skills from text (fallback)"""
    try:
        # Simple heuristic: Look for lines with 'Skills:' or bullet points
        skills = []
        lines = text.split('\\n')
        recording = False
        for line in lines:
            if 'Skill' in line or 'Technical' in line:
                recording = True
                continue
            if recording and (line.strip().startswith('-') or line.strip().startswith('•')):
                skills.append(line.replace('-', '').replace('•', '').strip())
            if recording and line.strip() == '':
                recording = False
        return skills if skills else ["General Skills (Extraction failed)"]
    except:
        return []

def extract_field(text, field_name):
    """Extract a field like Education or Experience"""
    try:
        lines = text.split('\\n')
        # Check for headers
        for i, line in enumerate(lines):
            if field_name.lower() in line.lower():
                # Return next few lines
                return "\\n".join(lines[i+1:i+6])
        return "Not found"
    except:
        return "Not found"

def extract_score(text):
    """Extract score from text"""
    try:
        match = re.search(r'(\d{1,3})%', text)
        if match: return int(match.group(1))
        match = re.search(r'Score:\s*(\d{1,3})', text)
        if match: return int(match.group(1))
        return 0
    except:
        return 0

def chat_with_placement_ai(message, history=[], user_role="Student", language="en-US"):
    """
    General purpose chat with PLACEMENT-AI persona
    """
    if not GEMINI_KEYS: return "AI Configuration Error: API Key missing."
    
    try:
        # Language Mapping
        lang_map = {
            "en-US": "English",
            "hi-IN": "Hindi",
            "kn-IN": "Kannada",
            "ta-IN": "Tamil",
            "te-IN": "Telugu",
            "ml-IN": "Malayalam"
        }
        target_lang = lang_map.get(language, "English")

        # Construct context
        context = f"""
        {PLACEMENT_AI_SYSTEM_PROMPT}
        
        CURRENT CONTEXT:
        User Role: {user_role}
        TARGET LANGUAGE: {target_lang}
        
        INSTRUCTIONS:
        - Provide a helpful, concise response to the user's query.
        - YOU MUST RESPOND IN {target_lang}. THIS IS CRITICAL.
        - Even if the user asks in English, if the TARGET LANGUAGE is {target_lang}, reply in {target_lang}.
        - Maintain the defined persona (Friendly for Student, Professional for TPO/HOD).
        - If the user asks about something outside the 'DOMAIN KNOWLEDGE SCOPE', politely decline (in {target_lang}).
        - Use markdown for formatting if needed.
        """
        
        full_prompt = context + "\\n\\nCHAT HISTORY:\\n"
        # Limit history to last 10 turns to save tokens
        recent_history = history[-10:] if history else []
        
        for turn in recent_history:
            role_label = "User" if turn.get('role') == 'user' else "PLACEMENT-AI"
            content = turn.get('message', '')
            full_prompt += f"{role_label}: {content}\\n"
            
        full_prompt += f"User: {message}\\nPLACEMENT-AI (in {target_lang}):"
        
        model = _get_generative_model("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"Chat error: {e}")
        return "I apologize, but I am encountering some technical issues. Please try again later."