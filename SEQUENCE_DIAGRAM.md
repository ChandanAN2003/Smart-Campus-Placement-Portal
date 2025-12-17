# 5.5 Sequence Diagram Description

A Sequence Diagram illustrates the interaction between objects in a specific time-ordered sequence. It shows which objects interact with each other and in what order to perform a specific function.

Below are the detailed sequential flows for the critical modules of the **Smart Placement Portal**.

## 5.5.1 Sequence: AI User Resume Analysis
This sequence depicts the core AI interaction where a student uploads a resume and receives feedback.

**Participating Objects:**
*   **Student (Actor)**
*   **Frontend (UI)**
*   **Backend Server (Flask)**
*   **Resume Database (SQL)**
*   **Gemini AI (External Service)**

**Step-by-Step Flow:**
1.  **Student** logs in and navigates to the "Resume Analyzer" page.
2.  **Student** uploads a file (`resume.pdf`) via the **Frontend**.
3.  **Frontend** sends a POST request with the file to the **Backend Server**.
4.  **Backend Server** validates the file type and size.
    *   *Alt Flow*: If invalid, returns an error message to **Student**.
5.  **Backend Server** uses `PyPDF2` to extract raw text strings from the PDF.
6.  **Backend Server** sends the extracted text + Job Description Prompt to **Gemini AI**.
7.  **Gemini AI** processes the NLP request and returns a structured JSON response (Match Score, Missing Skills).
8.  **Backend Server** saves the analysis result into the **Resume Database** associated with the `User ID`.
9.  **Backend Server** returns the formatted data to the **Frontend**.
10. **Frontend** renders the "Skill Gap Analysis" chart and displays it to the **Student**.

---

## 5.5.2 Sequence: Drive Application Process
This sequence explains the logic of applying for a company, involving eligibility checks.

**Participating Objects:**
*   **Student (Actor)**
*   **Drive Dashboard (UI)**
*   **Application Controller (Server)**
*   **User DB** & **Drive DB**

**Step-by-Step Flow:**
1.  **Student** views the list of "Active Drives" on the **Drive Dashboard**.
2.  **Student** clicks the "Apply Now" button for a specific Company.
3.  **Drive Dashboard** sends a request (`apply_for_drive(drive_id)`) to the **Application Controller**.
4.  **Application Controller** fetches the `Drive Criteria` (e.g., Min CGPA 7.0) from the **Drive DB**.
5.  **Application Controller** fetches the `Student Profile` (e.g., Student CGPA) from the **User DB**.
6.  **Application Controller** compares the values:
    *   **Condition**: `If Student_CGPA >= Drive_Min_CGPA`:
        7.  Create a new record in the **Applications Table** with status 'Applied'.
        8.  Return "Success: Application Submitted" to the **UI**.
    *   **Else**:
        7.  Return "Error: Eligibility Criteria Not Met" to the **UI**.
9.  **Drive Dashboard** displays the final success/error notification to the **Student**.

---

## 5.5.3 Sequence: TPO HOD Verification Workflow
This sequence ensures only verified students access the portal features.

**Participating Objects:**
*   **New Student (Actor)**
*   **HOD (Actor)**
*   **Registration Portal**
*   **Admin Dashboard**
*   **Database**

**Step-by-Step Flow:**
1.  **New Student** submits details (Name, Dept, Roll No) via **Registration Portal**.
2.  **Registration Portal** saves details in **Database** with `is_approved = FALSE`.
3.  **HOD** logs into the **Admin Dashboard** and views "Pending Approvals".
4.  **Admin Dashboard** fetches the list of unapproved students from **Database**.
5.  **HOD** reviews the details and clicks "Verify".
6.  **Admin Dashboard** sends an update request to the **Database** setting `is_approved = TRUE`.
7.  **Database** confirms the update.
8.  **System** triggers a "Welcome Email" to the **Student** (via Email Service).
9.  **Student** can now log in successfully.
