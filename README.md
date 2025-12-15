# 🎓 AI-Powered Smart Placement & Talent Management Portal

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-Pro-purple.svg)

A next-generation **Campus Placement Automation System** that leverages **Generative AI** to streamline the recruitment process. This platform connects Students, Training & Placement Officers (TPOs), and HODs while providing advanced AI-driven tools for career preparation.

---

## 🚀 Key Features

### 🤖 AI-Powered Student Tools
- **Advanced Resume Analysis (ATS)**: Uses Gemini AI to scan resumes against Job Descriptions, providing a **% Match Score** and specific improvement suggestions.
- **Skill Gap Analysis**: Identifies missing skills for a target role and generates a personalized **Learning Path** with course recommendations (Coursera/Udemy).
- **AI Mock Interviews**: A voice-enabled AI interviewer that conducts domain-specific interviews (HR, Technical, Managerial) and provides instant feedback.
- **Proctored Mock Tests**: Full-screen, webcam-monitored technical assessments generated dynamically based on the student's department (CS, MBA, EEE, etc.).
- **Coding Arena**: Integrated LeetCode-style coding environment with AI code reviews.

### 👥 Role-Based Portals

#### 1. Student Dashboard
- View and Apply for active Placement Drives.
- Track Application Status (Applied -> Shortlisted -> Offer).
- Earn **Badges & Points** (Gamification) for solving problems and taking tests.
- View detailed analytics of performance.

#### 2. TPO (Admin) Dashboard
- **Create & Manage Drives**: Post new job openings with specific departmental eligibility.
- **Analytics**: View placement statistics, department-wise trends, and offer counts.
- Manage student database and approvals.

#### 3. HOD (Head of Dept) Dashboard
- **Verify Students**: Approve or reject student registrations from their department.
- Monitor department-specific placement progress.
- View list of placed/unplaced students.

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3 (Glassmorphism UI), JavaScript, Three.js (3D Backgrounds).
- **Backend**: Python (Flask Framework).
- **Database**: MySQL (Relational Data Management).
- **AI Engine**: Google Gemini 1.5 Pro / Flash.
- **Tools**: SQLAlchemy, Werkzeug Security, Chart.js.

---

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/smart-placement-portal.git
   cd smart-placement-portal
   ```

2. **Set up Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Create a `.env` file in the `backend` folder:
   ```env
   SECRET_KEY=your_secret_key
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost   # Or use TiDB Cloud Host
   DB_NAME=placement_portal
   DB_PORT=3306        # 4000 for TiDB
   GEMINI_API_KEY=your_gemini_api_key
   ```
   *Note: The application supports TiDB Cloud with connection pooling for production performance.*

5. **Initialize Database**
   ```bash
   python init_db.py
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```
   Access the portal at `http://localhost:5000`

---

## 📸 Screenshots

| Student Dashboard | Resume Analysis |
|:---:|:---:|
| *(Add Screenshot)* | *(Add Screenshot)* |

| Mock Test Environment | AI Interview |
|:---:|:---:|
| *(Add Screenshot)* | *(Add Screenshot)* |

---

## 🔮 Future Scope
- **Mobile App**: React Native application for students.
- **Automated Emailing**: SMTP integration for offer letter dispatch.
- **Blockchain**: Verifiable certificates for achievements.

---

**Developed for Final Year Project 2025**