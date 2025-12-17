# 5.4 Use Case Diagram

A Use Case Diagram captures the dynamic aspect of the system by depicting the interactions between external **Actors** and the **System Functions** (Use Cases).

## 5.4.1 Actors Identification
1.  **Student**: The primary end-user seeking placement.
2.  **TPO (Training & Placement Officer)**: The administrator managing the recruitment process.
3.  **HOD (Head of Department)**: The verifier ensuring student data authenticity.
4.  **AI Service (System Actor)**: The background intelligence (Gemini) performing analysis.

## 5.4.2 Use Cases per Actor

### **Student Use Cases**
*   **Register/Login**: Access the portal securely.
*   **Manage Profile**: Update academic details (CGPA) and personal info.
*   **Upload Resume**: Upload PDF/DOCX for AI parsing.
*   **View Drives**: Browse list of eligible companies.
*   **Apply for Drive**: Submit a one-click application.
*   **Take Mock Interview**: Engage in a voice-based AI interview sessions.
*   **View Analysis**: See resume score and skill gaps.

### **TPO Use Cases**
*   **Manage Drives**: Create, Update, or Delete placement drives.
*   **View Applicants**: See list of students who applied for a specific drive.
*   **Shortlist Students**: Mark students as 'Selected' or 'Rejected'.
*   **Send Notifications**: Trigger email alerts to students.

### **HOD Use Cases**
*   **Verify Student**: Review new registrations and approve them.
*   **View Dept Stats**: Access analytics for their specific department.

---

## 5.4.3 Interaction Overview

The system interactions are structured around the core "Placement Drive" lifecycle.

1.  **Authentication Layer (Common)**:
    *   All actors (Student, TPO, HOD) must first authenticate via the **Login/Register** interface. This is a prerequisite for all other actions.

2.  **Student Workflow**:
    *   **Upload Resume (Primary)**: Limits access to the "Apply" feature. When a student uploads a resume, it *automatically triggers* the backend AI analysis process (<<include>> relationship).
    *   **Apply for Drive**: This uses the data from the "Manage Profile" use case to verify eligibility before submission.

3.  **HOD Workflow**:
    *   **Verify Student**: This acts as a gateway. A student profile remains "Inactive" until the HOD performs this use case.

4.  **TPO Workflow**:
    *   **Shortlist Students**: TPOs rely on the output of the "Apply for Drive" use cases to generate their lists.

### Dependencies
*   **<<include>> Relationship**: The **"Analyze Resume"** use case is mandatorily included whenever **"Upload Resume"** is executed. The system cannot accept a resume without scoring it.
*   **<<extend>> Relationship**: The **"View Analysis"** use case extends "Upload Resume," as it is an optional step the student takes *after* the upload is complete to view their detailed feedback.
