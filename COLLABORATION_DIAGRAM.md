# 5.6 Collaboration Diagram

The **Collaboration Diagram** (also known as a Communication Diagram) emphasizes the structural organization of the objects that send and receive messages. Unlike the Sequence Diagram which focuses on time ordering, this diagram focuses on the relationships and potential message pathways between objects.

## 5.6.1 Objects and Links
The system consists of the following key participating objects interacting in the "Smart Placement" environment:

1.  **User Interface (VIEW)**: The Student or TPO Dashboard.
2.  **Main Controller (CTRL)**: The Flask backend handling logic.
3.  **Database (DB)**: TiDB storing permanent records.
4.  **AI Service (EXT)**: The Google Gemini API for intelligence.

## 5.6.2 Scenario A: AI Resume Scoring Interaction
This scenario illustrates how the objects collaborate to process a student's resume.

**Interaction Flow:**
1.  **Student** sends `1: upload_resume(file)` to **User Interface**.
2.  **User Interface** forwards `2: submit_request(file)` to **Main Controller**.
3.  **Main Controller** parses the file and sends `3: analyze_text(content)` straight to **AI Service**.
    *   *Note: This shows direct coupling between Controller and AI Service.*
4.  **AI Service** calculates and returns `4: return_score(json)` to **Main Controller**.
5.  **Main Controller** triggers `5: save_record(score)` to the **Database**.
6.  **Database** acknowledges with `6: confirm_save()` to **Main Controller**.
7.  **Main Controller** pushes `7: display_dashboard(data)` back to **User Interface**.

**Structural Insight:**
*   The **Main Controller** acts as the central hub (star topology).
*   The **AI Service** and **Database** never interact directly; they are decoupled by the Controller.

## 5.6.3 Scenario B: Drive & Notification Flow
This scenario shows the collaboration when a TPO launches a new placement drive.

**Interaction Flow:**
1.  **TPO** sends `1: create_drive(details)` to **User Interface**.
2.  **User Interface** invokes `2: validate_and_post()` on **Main Controller**.
3.  **Main Controller** sends `3: insert_drive()` to **Database**.
4.  **Main Controller** (simultaneously) triggers `4: fetch_eligible_students()` from **Database**.
5.  **Database** returns `5: student_list[]` to **Main Controller**.
6.  **Main Controller** iterates and sends `6: send_email_alert()` to **Notification Service** (Internal Object).

**Structural Insight:**
*   This flow highlights the **Controller's** role in orchestrating two separate downstream actions (Storage and Notification) based on a single upstream event.
