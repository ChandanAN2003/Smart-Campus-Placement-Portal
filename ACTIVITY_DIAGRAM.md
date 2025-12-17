# 1.4 Activity Diagram

An **Activity Diagram** is a behavioral diagram that portrays the control flow of activities in the system. It describes the dynamic aspects of the system by showing the sequence of activities from start to finish, including decisions, branches, and parallel processing.

## 1.4.1 Key Activities and Flows

The Smart Placement Portal involves several complex workflows. The Activity Diagram visualizes these processes to ensure logic correctness.

### Activity 1: Student Placement Application Process
This flow describes the lifecycle of a student applying for a job.
1.  **Start**: Student logs into the portal.
2.  **View Dashboard**: User sees list of active placement drives.
3.  **Select Drive**: User clicks on a specific job opening.
4.  **Decision Node (Eligible?)**:
    *   *If No*: Display "Not Eligible" message. End Activity.
    *   *If Yes*: Proceed to "Apply" options.
5.  **AI Analysis (Optional)**:
    *   User opts for "Analyze Resume".
    *   System sends Resume + Job Description to AI.
    *   Display "Fit Score" and "Missing Skills".
6.  **Apply**: User clicks "Apply Now".
7.  **System Action**: Record application in Database.
8.  **Confirmation**: Show success message.
9.  **End**.

### Activity 2: TPO Drive Management
This flow details how a Training & Placement Officer manages recruitment.
1.  **Start**: TPO logs in.
2.  **Create Drive**: TPO inputs Company Name, Criteria, Package, etc.
3.  **Post Drive**: System validates and saves the drive.
4.  **Fork (Parallel)**:
    *   *Action A*: Drive appears on all Student Dashboards.
    *   *Action B*: Notification service emails eligible students.
5.  **Monitor**: TPO views "Track Applications" analytics.
6.  **End**.

## 1.4.2 Symbols Used
*   **Rounded Rectangle**: Represents an Activity or Action state.
*   **Diamond**: Represents a Decision (branching) or Merge.
*   **Solid Bar**: Represents a Fork (splitting into parallel flows) or Join (synchronizing).
*   **Solid Circle**: Start State.
*   **Bullseye Circle**: End State.
