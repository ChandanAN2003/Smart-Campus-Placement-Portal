# 3. Software Requirement Specification (SRS)

## 3.1 Overview
The **Software Requirement Specification (SRS)** document describes the functional and non-functional requirements for the **AI-Integrated Smart Campus Placement Portal**. This document serves as a guideline for developers, testers, and stakeholders to ensure that the final product meets the specified objectives.

The system is designed to automate the campus recruitment process, provide AI-driven mentorship to students, and offer real-time analytics to college administration.

## 3.2 Functional Requirements
Functional requirements define the specific behaviors and functions of the system.

### 3.2.1 Student Module
*   **FR-01 Registration & Login**: System must allow students to register with their college email and log in securely.
*   **FR-02 Profile Management**: Students should be able to update their academic details (CGPA, Branch) and upload resumes (PDF/DOCX).
*   **FR-03 View Drives**: System must display a list of "Active" placement drives for which the student is eligible.
*   **FR-04 Apply for Drive**: Students must be able to apply for a drive with a single click. The system should prevent duplicate applications.
*   **FR-05 AI Resume Analysis**: Upon upload, the system must process the resume using Gemini AI and return a "Job Fit Score" and "Missing Skills".
*   **FR-06 AI Mock Interview**: The system must provide a voice-enabled interface where an AI bot asks technical questions and records the student's answers (as text).
*   **FR-07 Skill Gap Analysis**: System must analyze the student's skills against a target role and suggest specific courses.

### 3.2.2 TPO (Training & Placement Officer) Module
*   **FR-08 Drive Management**: TPOs must be able to Create, Update, and Delete placement drives (Company Name, Role, Date, Eligibility Criteria).
*   **FR-09 Application Monitoring**: TPOs should view the list of all students who have applied for a specific drive.
*   **FR-10 Automated Filtering**: System must allow TPOs to filter applicants based on CGPA > X or Backlogs < Y.
*   **FR-11 Send Notifications**: TPOs must be able to trigger batched emails (e.g., "Shortlisted") to selected students.

### 3.2.3 HOD (Head of Department) Module
*   **FR-12 Student Verification**: HODs must be able to view pending student registrations and "Approve" or "Reject" them.
*   **FR-13 Department Analytics**: System must show graphs of "Placed vs Unplaced" students for their specific department.

## 3.3 Non-Functional Requirements
Non-functional requirements specify the quality attributes of the system.

### 3.3.1 Performance
*   **NFR-01 Response Time**: The web pages should load within 2 seconds under normal load.
*   **NFR-02 AI Latency**: Resume analysis results should be returned within 5-10 seconds.
*   **NFR-03 Concurrency**: The system must support at least 500 concurrent users during peak "Drive Application" windows without crashing.

### 3.3.2 Security
*   **NFR-04 Data Integrity**: User passwords must be stored as Salted Hashes (Bcrypt), never as plain text.
*   **NFR-05 Access Control**: APIs must validate the user's Role (Student/TPO) before processing requests (RBAC).
*   **NFR-06 Secure Communication**: All data in transit must be encrypted via HTTPS (SSL/TLS).

### 3.3.3 Reliability & Availability
*   **NFR-07 Uptime**: The system should aim for 99.9% availability during business hours (9 AM - 5 PM).
*   **NFR-08 Disaster Recovery**: The database (TiDB Cloud) handles automated daily backups to prevent data loss.

### 3.3.4 Usability
*   **NFR-09 User Interface**: The UI should follow "Glassmorphism" design principles for a modern, clean look.
*   **NFR-10 Responsiveness**: The dashboard must be fully responsive and usable on Mobile devices (360px width) and Desktops.
