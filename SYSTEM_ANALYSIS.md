# 3. System Analysis

## 3.1 Existing System
- **Manual Data Entry**: Student data collected via Google Forms or Excel sheets, leading to data redundancy and errors.
- **Lack of Feedback**: Students typically receive a generic "Rejected" status without knowing why they were not selected.
- **Coordination Issues**: Significant communication gaps exist between TPOs and HODs regarding student eligibility and verification status.
- **Static Preparation**: Students rely on generic websites for preparation, which may not align with specific company requirements.
- **Limited Analytics**: No real-time visualization of placement statistics for decision-making.

## 3.2 Proposed System
The proposed system addresses these limitations with:
- **Centralized Database**: A single source of truth for all placement activities, ensuring data consistency.
- **AI Feedback Loop**: Automated resume analysis and mock interviews provide instant, personalized improvement tips to students.
- **Role-Based Access Control (RBAC)**: secure and distinct access levels for Students, TPOs, and HODs to manage their respective workflows.
- **Gamification**: Leaderboards and badges to motivate student preparation and engagement.
- **Real-time Analytics**: Dashboards for TPOs and HODs to monitor drive status and student performance.

## 3.3 Feasibility Study
Before developing the project, a detailed feasibility study was conducted to ensure its viability.

### 3.3.1 Technical Feasibility
The project uses **Python (Flask)** for the backend, which is a mature and widely used framework. The database is **MySQL/TiDB**, ensuring reliable data storage. The core innovation, **Generative AI**, is implemented using Google's typically reliable **Gemini API**. All technologies are well-documented and supported, making the project technically feasible.

### 3.3.2 Operational Feasibility
The system simplifies existing workflows rather than complicating them. TPOs save time on filtering, and students get better utility. The UI is designed to be user-friendly (Glassmorphism), ensuring high adoption rates. Therefore, the system is operationally viable.

### 3.3.3 Economic Feasibility
The project uses **Open Source technologies** (Python, Flask, MySQL) and free-tier cloud services (Render, TiDB Cloud, Gemini Free Tier). The development cost is primarily time and effort, with zero initial licensing costs, making it economically highly feasible for an educational institution.

## 3.4 Requirement Analysis

### 3.4.1 Functional Requirements
1.  **Student Module**:
    *   Registration and Profile Management (Resume, Skills, Social Links).
    *   **AI Resume Analysis**: Upload resume to get a score and feedback.
    *   **Job Application**: Apply for active drives with one click.
    *   **AI Mock Interview**: Voice-enabled practice interviews.
    *   **Skill Gap Analysis**: Get course recommendations based on target roles.
2.  **TPO Module**:
    *   **Drive Management**: Create, Update, and Delete placement drives.
    *   **Application Tracking**: View list of applicants and their status.
    *   **Analytics**: View department-wise placement stats.
    *   **Communication**: Send automated emails to students.
3.  **HOD Module**:
    *   **Student Verification**: Approve student accounts.
    *   **Department Stats**: View placement progress of their department.

### 3.4.2 Non-Functional Requirements
1.  **Performance**: The system must handle concurrent access by 500+ students during a drive.
2.  **Security**:
    *   All passwords must be hashed (Bcrypt).
    *   SQL Injection prevention using ORM/Parameterized queries.
    *   Secure file uploads (checking extensions and size).
3.  **Availability**: The system should be available 24/7 (Hosted on Cloud).
4.  **Scalability**: The database should handle increasing data volume over years (TiDB Distributed SQL).
