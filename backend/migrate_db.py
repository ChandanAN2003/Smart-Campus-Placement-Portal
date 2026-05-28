from database import db

def migrate():
    print("Migrating database...")
    try:
        # Add reset_otp column
        try:
            db.execute_query("ALTER TABLE users ADD COLUMN reset_otp VARCHAR(6)")
            print("Added reset_otp column.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("reset_otp column already exists.")
            else:
                print(f"Error adding reset_otp: {e}")

        # Add reset_otp_expiry column
        try:
            db.execute_query("ALTER TABLE users ADD COLUMN reset_otp_expiry DATETIME")
            print("Added reset_otp_expiry column.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("reset_otp_expiry column already exists.")
            else:
                print(f"Error adding reset_otp_expiry: {e}")

        # Add mock_test_score column to applications
        try:
            db.execute_query("ALTER TABLE applications ADD COLUMN mock_test_score VARCHAR(50)")
            print("Added mock_test_score column.")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("mock_test_score column already exists.")
            else:
                print(f"Error adding mock_test_score: {e}")

        # Create badges table
        try:
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS badges (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    icon VARCHAR(50) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    min_score INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Created badges table.")
            
            # Seed default badges if table is empty
            count = db.execute_query("SELECT COUNT(*) as count FROM badges", fetch_one=True)
            if count and count['count'] == 0:
                db.execute_query("""
                    INSERT INTO badges (name, icon, description, min_score) VALUES
                    ('Warm Up', '🥉', 'First steps! Earned 50 points by participating in tests.', 50),
                    ('Consistent Learner', '🥈', 'On the right track! Reached 150 points through practice.', 150),
                    ('Placement Ready', '🥇', 'Excellent work! Scored 300 points. You are fully prepared.', 300),
                    ('Elite Code Ninja', '💻', 'God mode! Scored 500+ points by mastering tests and coding arenas.', 500)
                """)
                print("Seeded default badges.")
        except Exception as e:
            print(f"Error creating/seeding badges table: {e}")

        # Create user_badges table
        try:
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS user_badges (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    badge_id INT NOT NULL,
                    awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(badge_id) REFERENCES badges(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_badge (user_id, badge_id)
                )
            """)
            print("Created user_badges table.")
        except Exception as e:
            print(f"Error creating user_badges table: {e}")

        # Create coding_submissions table
        try:
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS coding_submissions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    problem_title VARCHAR(255) NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    code TEXT NOT NULL,
                    status VARCHAR(50) DEFAULT 'failed',
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Created coding_submissions table.")
        except Exception as e:
            print(f"Error creating coding_submissions table: {e}")

        print("Migration complete.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()

