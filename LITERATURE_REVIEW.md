# 2. Literature Review
The literature review explores the evolution of campus recruitment systems, moving from data-centric prediction models to modern AI-driven solutions. It analyzes key research in the domains of predictive analytics, Natural Language Processing (NLP), and Generative AI to understand existing methodologies and their limitations. This analysis establishes the theoretical foundation for this project, highlighting how the **AI-Integrated Smart Campus Placement Portal** addresses specific gaps in transparency, context-awareness, and student mentorship found in current technologies.

## 2.1 Campus Placement Prediction
**Paper 1: Chakraborty et al. (2020) - "Campus Placement Prediction using Supervised Machine Learning"**
*   **Core Research**: This study proposed using Logistic Regression and Decision Trees to predict student employability based strictly on quantitative academic history (10th/12th marks, CGPA). They achieved decent accuracy but noted the system's inability to assess actual technical skills.
*   **Included in My Project**:
    > My project incorporates the **eligibility filtering logic** proposed here but extends it significantly. Instead of relying solely on CGPA, my system uses AI to parse the "Projects" and "Skills" sections of a resume. This allows the platform to predict placement success based on **practical skills** (e.g., "Full Stack Development"), not just academic grades.

## 2.2 Resume Parsing and NLP
**Paper 2: Sharma & Kumar (2021) - "Resume Parsing using NLP techniques"**
*   **Core Research**: Explored the use of TF-IDF (Term Frequency-Inverse Document Frequency) to extract keywords from resumes. Their system could identify skills but failed to understand context (e.g., distinguishing between "Java" the programming language and "Java" coffee).
*   **Included in My Project**:
    > My project overcomes the limitations of their keyword-based approach by implementing **Semantic Resume Analysis using Google Gemini AI**. Unlike their TF-IDF model, my system understands context—recognizing that a student who "built a microservice using Spring Boot" implicitly possesses "Java" proficiency, even if the word "Java" is not explicitly mentioned.

## 2.3 AI-Driven Interview Preparation
**Paper 3: Zhang et al. (2022) - "Reducing Interview Anxiety with Voice-based AI Agents"**
*   **Core Research**: conducted experiments showing that students who practiced with AI-based conversational agents demonstrated significantly reduced anxiety and improved performance in real human interviews.
*   **Included in My Project**:
    > Drawing directly from this research, I have implemented an **Interactive AI Mock Interviewer**. The system uses Web Speech API for Speech-to-Text and Gemini for response generation, allowing students to have real, voice-based technical conversations. This provides the "low-stakes practice environment" recommended by Zhang et al.

## 2.4 Generative AI in Education
**Paper 4: Google AI Research (2023) - "Capabilities of Large Language Models in Unstructured Text Analysis"**
*   **Core Research**: Demonstrated the efficacy of models like PaLM and Gemini in performing complex reasoning tasks on unstructured text data without specific model training (Zero-shot learning).
*   **Included in My Project**:
    > This is the foundational technology of my project. I have integrated **Google Gemini 1.5 Pro** as the core engine to power the **Resume Scoring** and **Automated Email Drafting** features. This allows the application to function without needing a massive, pre-labeled dataset for training, making it lightweight and efficient.

## 2.5 Skill Gap Analysis
**Paper 5: Wang et al. (2021) - "Deep Learning for Personalized Skill Gap Analysis"**
*   **Core Research**: Proposed a complex Deep Learning recommender system to map student skills to industry requirements and suggest courses.
*   **Included in My Project**:
    > I have implemented a **Personalized Skill Gap Analyzer** that achieves the same goal but with greater flexibility. By feeding the specific "Job Description" to the AI, my system dynamically identifies missing skills and generates a **customized learning path** with links to Coursera/Udemy, simplifying the complex architecture proposed by Wang into a real-time API call.

## 2.6 Ethics and Transparency
**Paper 6: Smith & Jones (2023) - "Transparency and Bias in AI Recruitment Systems"**
*   **Core Research**: Highlighted the ethical risks of "Black Box" AI algorithms that reject candidates without explanation, leading to mistrust among applicants.
*   **Included in My Project**:
    > To address this, my system relies on **Explainable AI (XAI)** principles. When a student's resume typically scores low, the system does not just say "Rejected." It explicitly lists **"Missing Keywords"** and provides **"Improvement Suggestions,"** ensuring the process is transparent and educational rather than punitive.

## 2.7 System Scalability
**Paper 7: Kumar (2024) - "Comparative Analysis of Distributed Databases for Academic ERPs"**
*   **Core Research**: Concluded that Distributed SQL databases (like TiDB) offer superior reliability over traditional MySQL for academic events where traffic spikes occur suddenly (e.g., during exam results or placement drives).
*   **Included in My Project**:
    > I have architected the backend using **TiDB Cloud (Distributed MySQL)**. This ensures that the placement portal remains stable and responsive even during "Drive Days" when hundreds of students might be accessing the "Apply" feature simultaneously, preventing the system crashes common in traditional college ERPs.
