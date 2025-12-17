# 4.3 Level 1 Data Flow Diagram (DFD)

The **Level 1 Data Flow Diagram (DFD)** expands upon the Context Diagram by "zooming in" on the single "Smart Placement Portal" process. It decomposes the system into its major sub-processes to illustrate the internal data processing logic and data storage interactions.

In this system, the Level 1 DFD is divided into five core operational processes:

## 1.0 Authentication & User Management Process
This process acts as the gatekeeper for the entire system, handling security and identity verification.
*   **Inputs**:
    *   **Login Credentials**: Email and Password provided by Students, TPOs, or HODs.
    *   **Registration Data**: New user details (Name, Dept, Roll No).
*   **Processing**:
    *   **Password Hashing**: Converts plain-text passwords into secure hashes (using Bcrypt).
    *   **Validation**: Checks credentials against the `Users Database`.
    *   **Session Creation**: Generates a secure HTTP session upon successful login.
*   **Outputs**:
    *   **Auth Token/Session**: Grants access to role-specific dashboards.
    *   **Error Message**: Returned if authentication fails.

## 2.0 Student Profile & Resume Manager
This process handles the ingestion and verification of student data.
*   **Inputs**:
    *   **Resume File**: PDF or DOCX file uploaded by the student.
    *   **Verification Status**: "Approved" or "Rejected" signal from the HOD.
*   **Processing**:
    *   **File Storage**: Saves the physical file to the storage server (Render Disk/S3).
    *   **Text Extraction**: Extracts raw text from the resume for AI processing.
    *   **Status Update**: Updates the student's profile status based on HOD input.
*   **Data Store Interaction**: Reads/Writes to the `Resumes Table` and `Users Table`.

## 3.0 Drive Management Process
This process enables the Training & Placement Officer (TPO) to manage recruitment events.
*   **Inputs**:
    *   **Drive Details**: Company Name, Job Role, CTC, Eligibility Criteria (Minimum CGPA).
*   **Processing**:
    *   **Creation**: Creates a new record in the database.
    *   **Filtering Logic**: When a student requests to view drives, this process filters out companies where the student does not meet the CGPA/Backlog criteria.
*   **Outputs**:
    *   **Active Drive List**: Displayed to eligible students.
    *   **Drive Notification**: Trigger for the Email Service.

## 4.0 AI Intelligence Engine
This is the core differentiator of the project, handling all Generative AI tasks.
*   **Inputs**:
    *   **Resume Text**: Extracted from Process 2.0.
    *   **Job Description**: Fetched from Process 3.0.
    *   **Audio Input**: Voice data from the Mock Interview module.
*   **Processing**:
    *   **Prompt Engineering**: Constructs a structured prompt (e.g., "Act as an ATS and score this resume...").
    *   **API Call**: Sends data to the **Google Gemini API**.
    *   **Response Parsing**: Converts the AI's textual response into structured JSON (Match Score, Skill Gaps).
*   **Outputs**:
    *   **Compatibility Score**: 0-100 score saved to the database.
    *   **Feedback Report**: Detailed suggestions displayed to the student.

## 5.0 Application & Notification Handler
This process manages the lifecycle of a job application.
*   **Inputs**:
    *   **Apply Intent**: Student clicking "Apply Now".
    *   **status Updates**: TPO marking a student as "Shortlisted" or "Selected".
*   **Processing**:
    *   **Eligibility Check**: Final verification of whether the student is allowed to apply (e.g., checks if already placed).
    *   **linkage**: Creates a relationship record between `Student ID` and `Drive ID`.
*   **Outputs**:
    *   **Application Acknowledgement**: Confirmation message to the student.
    *   **Updated Applicant List**: Refreshed view for the TPO.
