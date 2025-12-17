# Project Description

## 1. Overview
The **AI-Integrated Smart Campus Placement Prediction & Management System** is a next-generation web-based platform designed to revolutionize the campus recruitment ecosystem. By bridging the gap between academic preparation and industry expectations, the system addresses the critical inefficiencies of traditional, manual placement processes. It provides a centralized interface for **Students**, **Training and Placement Officers (TPOs)**, and **Heads of Departments (HODs)** to manage the entire lifecycle of placement drives—from posting job openings to tracking final offer letters.

System differentiation lies in its integration of **Generative AI (Google Gemini 1.5 Pro)**. While traditional portals act as passive databases, this application functions as an active *Career Mentor*, offering real-time, data-driven feedback to students to enhance their employability.

## 2. Core Objectives
*   **Automation**: To eliminate manual data entry and excel-based sorting of eligible students.
*   **Employability Enhancement**: To provide students with AI-driven insights into their resumes and interview skills.
*   **Transparency**: To ensure all stakeholders have a real-time view of placement statistics and drive statuses.
*   **Scalability**: To provide a robust cloud-native architecture capable of handling high-traffic placement events.

## 3. Key Features

### 3.1 For Students (The "Intelligence" Layer)
*   **AI Resume Analyzer (ATS)**: Students can upload PDF/DOCX resumes. The system uses Large Language Models (LLMs) to semantically compare the resume against a specific job description, generating a **Match Score (0-100%)** and a detailed report on **Missing Skills**.
*   **Skill Gap Analysis**: Based on the job role, the AI identifies proficiency gaps and generates a personalized **Learning Path**, recommending specific courses (e.g., Coursera, Udemy) and project ideas.
*   **AI Mock Interviewer**: A distinguishing feature where students can participate in voice-enabled mock interviews. The AI adapts its questions based on the student's previous answers, simulating real HR or Technical rounds.
*   **Gamified Coding Arena**: An integrated coding environment where students solve LeetCode-style problems, earning points and badges to climb the peer leaderboard.

### 3.2 For TPOs (The "Administration" Layer)
*   **Drive Management**: Create and manage recruitment drives with customizable eligibility criteria (CGPA, Department, Backlogs).
*   **Automated Filtering**: One-click filtering of eligible students for specific drives.
*   **Analytics Dashboard**: Visual charts displaying placement trends, package distributions, and department-wise performance.
*   **Communication Hub**: Send automated notifications and emails to students regarding drive updates.

### 3.3 For HODs (The "Verification" Layer)
*   **Student Verification**: Simple workflow to approve or verify student profiles and academic records.
*   **Departmental Insights**: Exclusive view of their department's placement ratio and top performers.

## 4. Technology Stack
The project is built on a robust, modern stack ensuring performance and security:
*   **Frontend**: HTML5, CSS3 (Glassmorphism UI), JavaScript.
*   **Backend**: Python (Flask Framework).
*   **Database**: TiDB Cloud (Distributed SQL for high availability) / MySQL.
*   **Artificial Intelligence**: Google Gemini 1.5 Pro & Groq (Llama-3/Mixtral) for fallbacks.
*   **Deployment**: Render (PaaS) with CI/CD integration.

## 5. Potential Impact
This project significantly reduces the administrative burden on college staff while empowering students with self-service tools for career readiness. By democratizing access to high-quality resume critiques and mock interviews—services that usually cost money—the **Smart Campus Placement Portal** ensures that every student, regardless of background, has a fair shot at their dream job.
