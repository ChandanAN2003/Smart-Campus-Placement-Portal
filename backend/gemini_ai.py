"""
Google Gemini API integration for AI features
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def _get_generative_model(model_name="gemini-2.5-flash"):
    """
    Get generative model
    """
    # Strictly use the requested model (2.5)
    print(f"[DEBUG] Initializing model: {model_name}")
    model = genai.GenerativeModel(model_name)
    return model

def analyze_resume(resume_text, job_role, job_description=""):
    """
    Analyze resume using Gemini API and return job-fit analysis
    """
    if not GEMINI_API_KEY:
        return {
            'skills': [],
            'education': 'Not analyzed',
            'experience': 'Not analyzed',
            'job_fit_score': 0,
            'suggestions': 'Gemini API key not configured'
        }
    
    try:
        prompt = f"""
        Analyze this resume for the role: {job_role}
        
        Job Description: {job_description if job_description else 'Not provided'}
        
        Resume Content:
        {resume_text[:5000]}  # Limit to 5000 chars
        
        Please provide a JSON response with the following structure:
        {{
            "skills": ["skill1", "skill2", ...],
            "education": "Summary of education",
            "experience": "Summary of experience",
            "job_fit_score": 85,
            "suggestions": "Improvement suggestions"
        }}
        
        Calculate job_fit_score (0-100) based on:
        - Relevant skills match
        - Education alignment
        - Experience relevance
        - Overall fit for the role
        
        Provide specific, actionable suggestions for improvement.
        """
        
        model = _get_generative_model("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        # Parse response (Gemini may return markdown or plain text)
        response_text = response.text.strip()
        
        # Try to extract JSON from response
        import json
        import re
        
        # Look for JSON in the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                result = json.loads(json_match.group())
                return result
            except:
                pass
        
        # Fallback: parse manually if JSON extraction fails
        return {
            'skills': extract_skills_from_text(response_text),
            'education': extract_field(response_text, 'education'),
            'experience': extract_field(response_text, 'experience'),
            'job_fit_score': extract_score(response_text),
            'suggestions': response_text[:500] if len(response_text) > 500 else response_text
        }
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {
            'skills': [],
            'education': 'Analysis failed',
            'experience': 'Analysis failed',
            'job_fit_score': 0,
            'suggestions': f'Error: {str(e)}'
        }

def perform_skill_gap_analysis(resume_text, job_role, job_description=""):
    """
    Perform detailed skill gap analysis and suggest learning path
    """
    if not GEMINI_API_KEY:
        return None
        
    try:
        prompt = f"""
        Perform a detailed Skill Gap Analysis matching this resume against the target role: {job_role}
        
        Job Description: {job_description if job_description else 'Standard industry requirements for this role'}
        
        Resume Content:
        {resume_text[:4000]}
        
        Provide a JSON response with this EXACT structure:
        {{
            "ats_score": 85,
            "missing_skills": ["skill1", "skill2"],
            "skill_gap_analysis": "Detailed analysis of gaps...",
            "recommended_courses": [
                {{"title": "Course Name 1", "platform": "Coursera/Udemy/etc", "duration": "4 weeks"}},
                {{"title": "Course Name 2", "platform": "Platform", "duration": "Duration"}}
            ],
            "project_ideas": [
                {{"title": "Project 1", "description": "Description...", "tech_stack": "React, Node.js"}}
            ],
            "interview_prep_topics": ["Topic 1", "Topic 2"]
        }}
        """
        
        model = _get_generative_model("gemini-2.5-flash")
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        import json
        import re
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return None
        
    except Exception as e:
        print(f"Skill gap analysis error: {e}")
        return None

def generate_mock_test(job_role, difficulty="Medium"):
    """
    Generate technical mock test questions
    """
    if not GEMINI_API_KEY:
        return []
        
    try:
        prompt = f"""
        Generate a technical mock test for the role: {job_role}
        Difficulty: {difficulty}
        
        Generate 10 technical multiple choice questions (MCQs).
        
        Composition:
        - 5 Questions: LeetCode-style Data Structures & Algorithms (DSA) logic (e.g., Time Complexity, Arrays, Linked Lists, Trees, Graph logic, or identifying the correct algorithm for a problem).
        - 5 Questions: Language-specific coding output/logic (based on the requested role).
        
        Focus on code snippets, algorithmic logic, and technical concepts.
        
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
        
        model = _get_generative_model("gemini-2.5-flash")
        print("[DEBUG] Prompt generated. Calling model.generate_content...")
        response = model.generate_content(prompt)
        print("[DEBUG] Response received.")
        response_text = response.text.strip()
        print(f"[DEBUG] Response text (first 100 chars): {response_text[:100]}")
        
        import json
        import re
        
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            print("[DEBUG] JSON match found.")
            return json.loads(json_match.group())
        
        print("[DEBUG] No JSON match found in response.")
        return []
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Mock test generation error: {e}")
        return []

# ... helper functions extract_skills_from_text, extract_field, extract_score omitted as they are unchanged ... 
# (Wait, replace tool replaces range, so I need to be careful to not cut them off if they are in range)

def generate_email_content(email_type, recipient_name, company_name, job_role, additional_info=""):
    """
    Generate professional email content using Gemini
    """
    if not GEMINI_API_KEY:
        return get_default_email(email_type, recipient_name, company_name, job_role)
    
    try:
        prompt = f"""
        Generate a professional {email_type} email for a college placement scenario.
        
        Recipient: {recipient_name}
        Company: {company_name}
        Position: {job_role}
        Additional Info: {additional_info}
        
        Email Type: {email_type}
        
        Requirements:
        - Professional and courteous tone
        - Clear and concise
        - Include relevant details
        - Appropriate for college placement context
        
        Provide the email in this format:
        SUBJECT: [subject line]
        BODY:
        [email body]
        """
        
        model = _get_generative_model("gemini-2.5-flash")
        response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
            max_output_tokens=1000,
            temperature=0.7
        ))
        
        response_text = response.text.strip()
        
        # Parse subject and body
        lines = response_text.split('\n')
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
        
        body = '\n'.join(body_lines).strip() if body_lines else response_text
        
        if not subject:
            subject = get_default_subject(email_type, company_name, job_role)
        
        return {
            'subject': subject,
            'body': body if body else get_default_email(email_type, recipient_name, company_name, job_role)['body']
        }
        
    except Exception as e:
        print(f"Email generation error: {e}")
        return get_default_email(email_type, recipient_name, company_name, job_role)

def get_default_email(email_type, recipient_name, company_name, job_role):
    """Fallback default emails if Gemini fails"""
    templates = {
        'offer': {
            'subject': f'Congratulations! Offer Letter from {company_name}',
            'body': f'Dear {recipient_name},\n\nWe are pleased to inform you that you have been selected for the position of {job_role} at {company_name}.\n\nPlease find the offer letter attached.\n\nCongratulations!\n\nBest regards,\nPlacement Office'
        },
        'rejection': {
            'subject': f'Application Update - {company_name}',
            'body': f'Dear {recipient_name},\n\nThank you for your interest in the {job_role} position at {company_name}.\n\nAfter careful consideration, we regret to inform you that we will not be moving forward with your application at this time.\n\nWe wish you the best in your future endeavors.\n\nBest regards,\nPlacement Office'
        },
        'shortlist': {
            'subject': f'Shortlisted for {job_role} - {company_name}',
            'body': f'Dear {recipient_name},\n\nCongratulations! You have been shortlisted for the {job_role} position at {company_name}.\n\nFurther details regarding the interview process will be shared soon.\n\nBest regards,\nPlacement Office'
        }
    }
    return templates.get(email_type, templates['rejection'])

def get_default_subject(email_type, company_name, job_role):
    """Default email subjects"""
    subjects = {
        'offer': f'Congratulations! Offer Letter from {company_name}',
        'rejection': f'Application Update - {company_name}',
        'shortlist': f'Shortlisted for {job_role} - {company_name}'
    }
    return subjects.get(email_type, f'Update from {company_name}')

