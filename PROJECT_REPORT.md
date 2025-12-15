# 🎓 Project Report: AI-Integrated Smart Campus Placement Portal

## 1. Abstract

The **AI-Integrated Smart Campus Placement Portal** is a comprehensive solution designed to automate and enhance the campus recruitment process. Unlike traditional management systems, this project integrates cutting-edge **Generative AI (Google Gemini)** to provide intelligent features like automated resume scoring, personalized skill gap analysis, and realistic AI-driven mock interviews. The platform bridges the gap between students, Training & Placement Officers (TPOs), and Heads of Departments (HODs) by providing a unified, role-based dashboard for managing drives, applications, and performance analytics.

## 2. Introduction

Campus placement is a critical activity for educational institutions. The current manual or semi-automated processes are often inefficient, lacking transparency and real-time feedback for students. This project aims to revolutionize this domain by leveraging:
-   **Automation**: Streamlining application tracking and drive management.
-   **Intelligence**: Using LLMs to analyze student potential and provide actionable feedback.
-   **Transparency**: giving all stakeholders (TPO, HOD, Student) real-time visibility into the process.

## 3. System Analysis

### 3.1 Existing System
-   **Manual Data Entry**: Student data collected via Google Forms or Excel sheets.
-   **Lack of Feedback**: Students typically receive a generic "Rejected" status without knowing why.
-   **Coordination Issues**: Communication gaps between TPOs and HODs regarding student eligibility.
-   **Static Preparation**: Students rely on generic websites for preparation, which may not align with specific company requirements.

### 3.2 Proposed System
The proposed system addresses these limitations with:
-   **Centralized Database**: Single source of truth for all placement activities.
-   **AI Feedback Loop**: Resume analysis and mock interviews provide instant, personalized improvement tips.
-   **Role-Based Access Control (RBAC)**: Secure access for different user types.
-   **Gamification**: Leaderboards and badges to motivate student preparation.

## 4. Requirement Analysis

### 4.1 Functional Requirements
1.  **Student Module**: Profile management, Resume Upload, Drive Application, AI Resume Analysis, AI Mock Interview, Skill Gap Analysis.
2.  **TPO Module**: Create Drives, Manage Applications, View Analytics, Send Notifications/Emails.
3.  **HOD Module**: Approve/Reject Student Profiles, View Departmental Stats, Export Reports.

### 4.2 Non-Functional Requirements
1.  **Performance**: The system should handle concurrent users during recruitment drives.
2.  **Security**: Passwords hashed (SHA256/Bcrypt), SQL Injection protection, secure file uploads.
3.  **Scalability**: Deployed on cloud infrastructure (Render + TiDB).

## 5. System Design

### 5.1 Tech Stack
-   **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript, Three.js (Visuals).
-   **Backend**: Python (Flask).
-   **Database**: MySQL (TiDB Cloud).
-   **AI Services**: Google Gemini 1.5 Pro.

### 5.2 Database Schema (Brief)
-   `users`: Stores login info and role (Student, TPO, HOD).
-   `drives`: Details of placement drives (Company, Role, Date).
-   `applications`: Links Students to Drives with status (Applied, Selected, etc.).
-   `resumes`: Stores file paths and AI analysis scores.
-   `notifications`: System updates for users.

## 6. Implementation Details

### 6.1 AI Resume Analyzer
This feature extracts text from PDF/DOCX resumes and sends a prompt to the Gemini API containing the resume text and the job description. The AI returns a JSON response with a matching score (0-100) and list of missing keywords.

### 6.2 AI Mock Interview
Implemented using the Web Speech API (speech-to-text) and Gemini. The system maintains conversation history, allowing the AI to ask follow-up questions based on the student's previous answers, simulating a real HR or Technical interview.

### 6.3 Secure Deployment
The application is containerized and deployed on **Render**, with database connectivity to **TiDB Cloud** via SSL, ensuring production-grade reliability and security.

## 7. Testing

| Test Case | Description | Expected Result | Status |
| :--- | :--- | :--- | :--- |
| **TC-01** | User Registration | User created in DB; Hash stored | ✅ Pass |
| **TC-02** | Resume Analysis | Returns valid JSON score | ✅ Pass |
| **TC-03** | Drive Creation | Drive visible to eligible students | ✅ Pass |
| **TC-04** | HOD Approval | Student can only login after approval | ✅ Pass |

## 8. Conclusion

The Smart Campus Placement Portal successfully modernizes the recruitment workflow. By integrating Generative AI, it transforms a passive management tool into an active career mentor for students. The feedback loops created by the AI Interview and Resume Scorer modules are expected to significantly improve placement conversion rates.

## 9. Future Scope
-   **Mobile Application**: For easier access to notifications.
-   **Blockchain Integration**: For verified, tamper-proof offer letters and certificates.
-   **Alumni Connect**: Module to connect current students with placed alumni.

---
*Generated for Final Year Project Documentation*
