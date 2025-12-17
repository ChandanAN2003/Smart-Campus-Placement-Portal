# 1.5 Database Design

The database design provides a structured repository for the Smart Placement Portal, ensuring data integrity, minimal redundancy, and efficient retrieval. The system uses **MySQL** (or TiDB Cloud in production) as the relational database management system.

## 1.5.1 Schema Diagram Description
The database consists of **6 primary tables** linked via foreign keys to maintain referential integrity.

### 1. **Users Table** (`users`)
Stores profile information for all system actors (Students, HODs, TPOs).
*   **Primary Key**: `id`
*   **Key Fields**: `name`, `email` (Unique), `password_hash`, `role` (Enum: Student/HOD/TPO), `department`, `is_approved`.
*   **Security**: Passwords are hashed using Scrypt/PBKDF2.

### 2. **Drives Table** (`drives`)
Stores information about recruitment drives posted by the TPO.
*   **Primary Key**: `id`
*   **Foreign Key**: `created_by` -> `users.id`
*   **Key Fields**: `company_name`, `job_role`, `salary_package`, `eligibility_criteria`, `last_date`, `status` (Active/Closed).

### 3. **Applications Table** (`applications`)
Tracks which student has applied for which drive and their current status.
*   **Primary Key**: `id`
*   **Foreign Keys**: `student_id` -> `users.id`, `drive_id` -> `drives.id`
*   **Key Fields**: `status` (Applied/Shortlisted/Selected), `applied_at`.
*   **Constraint**: Unique composite key (`student_id`, `drive_id`) prevents duplicate applications.

### 4. **Resumes Table** (`resumes`)
Stores the path to uploaded resumes and their AI analysis results.
*   **Primary Key**: `id`
*   **Foreign Key**: `user_id` -> `users.id`
*   **Key Fields**: `file_path`, `job_fit_score` (0-100), `ai_feedback` (Text).

### 5. **Notifications Table** (`notifications`)
Stores alerts and messages for users.
*   **Primary Key**: `id`
*   **Foreign Key**: `user_id` -> `users.id`
*   **Key Fields**: `message`, `is_read`, `type`.

### 6. **Offer Letters Table** (`offer_letters`)
Stores the proof of placement.
*   **Primary Key**: `id`
*   **Foreign Key**: `application_id` -> `applications.id`
*   **Key Fields**: `file_path`, `issued_date`.

## 1.5.2 Data Integrity & Security
*   **Normalization**: The schema is normalized to **3NF** to reduce data redundancy.
*   **Cascading Deletes**: If a user is deleted, their applications and notifications are automatically removed to prevent orphaned records.
*   **Indexing**: Critical fields like `email`, `drive_id`, and `student_id` are indexed for fast search performance.
