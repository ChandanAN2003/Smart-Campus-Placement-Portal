USE placement_portal;

-- Insert sample TPO/Admin (password: admin123)
INSERT INTO users (name, email, password_hash, role, department, is_approved) VALUES
('Admin TPO', 'tpo@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'tpo', 'Placement', TRUE);

-- Insert HODs (password: hod123)
INSERT INTO users (name, email, password_hash, role, department, is_approved) VALUES
('HOD CS', 'hod.cs@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'CS', TRUE),
('HOD EC', 'hod.ec@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'EC', TRUE),
('HOD EEE', 'hod.eee@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'EEE', TRUE),
('HOD IS', 'hod.is@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'IS', TRUE),
('HOD MCA', 'hod.mca@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'MCA', TRUE),
('HOD MBA', 'hod.mba@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'MBA', TRUE),
('HOD MTECH', 'hod.mtech@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'hod', 'MTECH', TRUE);

-- Insert sample students (password: student123)
INSERT INTO users (name, email, password_hash, role, department, is_approved) VALUES
('Alice CS', 'alice@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'student', 'CS', TRUE),
('Bob EC', 'bob@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'student', 'EC', TRUE),
('Carol MCA', 'carol@college.edu', 'pbkdf2:sha256:600000$XxXxXxXx$hash_here', 'student', 'MCA', TRUE);

-- Insert sample placement drives
INSERT INTO drives (company_name, job_role, job_description, eligibility, last_date, status, created_by) VALUES
('Tech Corp', 'Software Engineer', 'Looking for skilled software engineers with experience in Python and web development.', 'CGPA >= 7.5, No backlogs', '2024-12-31', 'active', 1),
('Data Systems', 'Data Analyst', 'Seeking data analysts proficient in SQL, Python, and data visualization.', 'CGPA >= 7.0, No backlogs', '2024-12-25', 'active', 1),

