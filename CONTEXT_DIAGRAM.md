# 4.2 Context Diagram

A **Context Diagram** (Level 0 DFD) provides a high-level view of the system, showing its boundaries and interactions with external entities.

It treats the **Smart Placement Portal** as a single "Black Box" process and defines the flow of information between the system and its external users/services.

---

### Explanation of the Context Diagram

A Context Diagram, also known as a Level-0 Data Flow Diagram (DFD), offers the most abstract view of the information system. Its primary purpose is to define the **scope** and **boundary** of the system by illustrating the inputs and outputs between the system and external entities.

In the Context Diagram for the **Smart Campus Placement Portal**, the entire software system is represented as a single central process (bubble) named "Smart Placement Portal." This central process interacts with five distinct external entities:

1.  **Student (User Entity)**:
    *   **Inputs**: The student sends their registration details, uploads resume files (PDF/DOCX), submits applications for specific company drives, and provides voice input during AI mock interviews.
    *   **Outputs**: The system returns a "Match Score" for their resume, detailed feedback on missing skills, interview performance results, and notifications about upcoming drives.

2.  **Training & Placement Officer (TPO) (Admin Entity)**:
    *   **Inputs**: The TPO feeds the system with new "Drive Details" (Company Name, CTC, Eligibility Criteria) and initiates batch email notifications.
    *   **Outputs**: The system provides the TPO with "Filtered Student Lists" (eligible candidates) and high-level "Placement Analytics" (charts showing placement % per department).

3.  **Head of Department (HOD) (Admin Entity)**:
    *   **Inputs**: The HOD provides verification status (Approve/Reject) for students belonging to their department.
    *   **Outputs**: The system generates "Departmental Reports," giving the HOD visibility into which students are unplaced and require attention.

4.  **Google Gemini AI (External Service)**:
    *   **Role**: This acts as the "Intelligence Engine."
    *   **Data Flow**: The system sends anonymized resume text and job descriptions to Gemini. Gemini processes this unstructured data and returns structured JSON containing scores, skill gaps, and generated interview questions. This is a critical two-way flow that differentiates this system from a standard CRUD app.

5.  **Email Service (External Service)**:
    *   **Role**: Handles communication delivery.
    *   **Data Flow**: The system triggers SMTP requests with email content (Subject, Body, Recipient). The service then delivers the actual email (Offer Letters, OTPs) to the users' inboxes.

This diagram clearly demarcates that while **User Management** and **Drive Application** happen *inside* the system boundary, the **Intelligence Processing** (Gemini) and **Communication Delivery** (SMTP) are handled by external agents interactively.

---

### Description of Interactions

1.  **Student ↔ System**:
    *   **Input**: Students provide Personal Data, Resumes, and Voice Input (during interviews).
    *   **Output**: The System provides Job Notifications, Resume Scores, Skill Gap Reports, and Interview Feedback.

2.  **TPO ↔ System**:
    *   **Input**: TPOs input Drive details (Company, Package, Eligibility).
    *   **Output**: The System provides filtered lists of eligible students and statistical reports.

3.  **HOD ↔ System**:
    *   **Input**: HODs provide verification decisions (Approve/Reject).
    *   **Output**: The System provides real-time placement status of the department.

4.  **System ↔ Google Gemini AI**:
    *   **Input**: The System sends anonymized resume text and job descriptions.
    *   **Output**: The AI returns structured analysis (ATS Score, Missing Skills, Generated Questions).

5.  **System ↔ Email Service**:
    *   **Output**: The System triggers automated emails for registration confirmation, exam alerts, and offer letters.
