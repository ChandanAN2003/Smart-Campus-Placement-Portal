# 4. System Design

## 4.1 Overview
System design defines the architecture, components, modules, interfaces, and data for a system to satisfy specified requirements. The **AI-Integrated Smart Campus Placement Portal** follows the **Model-View-Controller (MVC)** architectural pattern (implied by Flask's structure) combined with a **Service-Oriented** approach for the AI components.

## 4.2 Architectural Design (High-Level)
The system is divided into three main layers: the **Presentation Layer** (Frontend), the **Application Layer** (Backend Logic), and the **Data Layer** (Database & External APIs).

### 4.2.1 Presentation Layer (Client Side)
*   **Responsibility**: Handles user interaction and visualization.
*   **Components**:
    *   **Browsers**: Chrome/Firefox running on Student/Staff devices.
    *   **Templates**: Jinja2 HTML templates enhanced with CSS (Glassmorphism) and JS.
    *   **Assets**: Static files (Images, Three.js animations).

### 4.2.2 Application Layer (Server Side)
*   **Responsibility**: Processes requests, executes business logic, and communicates with the AI engines.
*   **Framework**: **Python Flask**.
*   **Key Modules**:
    *   **Auth Manager**: Handles Login, Registration, and Session management.
    *   **Drive Controller**: Manages creation and listing of placement drives.
    *   **AI Service Adapter**: A specialized module (`gemini_ai.py`) that constructs prompts and sends them to the Google Gemini API. It handles retries and response parsing.
    *   **Notification Engine**: Generates and sends emails.

### 4.2.3 Data Layer
*   **Responsibility**: Persistent storage of structured data.
*   **Primary Database**: **TiDB Cloud (MySQL)**.
    *   Stores `Users`, `Resumes`, `Applications`, `Drives`.
*   **External Intelligence**:
    *   **Google Gemini API**: Not a database, but a critical "Knowledge Source" used for resume verification and content generation.

## 4.3 Data Flow Architecture
A typical data flow for the "Resume Analysis" feature is as follows:
1.  **Student** uploads a PDF via the Frontend.
2.  **Flask Server** receives the file and saves it temporarily.
3.  **Parser Module** (`PyPDF2`) extracts raw text from the PDF.
4.  **AI Service** sends this text + Job Description to **Gemini API**.
5.  **Gemini** returns a JSON analysis (Score + Gaps).
6.  **Flask Server** saves this result to the **TiDB Database**.
7.  **Frontend** renders the result as a chart/list for the student.

## 4.4 Use Case Diagram (Text Description)
*   **Actor: Student**
    *   Use Cases: Register, Upload Resume, Apply for Drive, Take Mock Test.
*   **Actor: TPO**
    *   Use Cases: Post Drive, Download Applicant List, Send Offer Letter.
*   **Actor: HOD**
    *   Use Cases: Approve Student, View Dept Stats.
*   **Actor: System (AI)**
    *   Use Cases: Analyze Resume, Generate Interview Questions.

## 4.5 Security Architecture
*   **SSL/TLS**: All traffic between Client, Server, and Database is encrypted.
*   **Input Validation**: All form inputs are sanitized to prevent SQL Injection (SQLi) and Cross-Site Scripting (XSS).
*   **Secure Config**: API Keys (Gemini) and DB Credentials are stored in Environment Variables (`.env`), not in the source code.
