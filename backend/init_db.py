"""
Database initialization script
"""
import os
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from database import db
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with schema and seed data"""
    try:
        schema_path = Path(__file__).parent.parent / 'database' / 'schema.sql'
        if not schema_path.exists():
            schema_path = Path(__file__).parent.parent.parent / 'database' / 'schema.sql'

        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()

            statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
            
            # SQLite compatibility translations
            if db.is_sqlite:
                import re
                translated_statements = []
                for statement in statements:
                    # Convert INT AUTO_INCREMENT PRIMARY KEY to INTEGER PRIMARY KEY AUTOINCREMENT
                    statement = re.sub(r'INT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', statement, flags=re.IGNORECASE)
                    # Convert ENUM(...) to VARCHAR(100)
                    statement = re.sub(r'ENUM\([^)]+\)', 'VARCHAR(100)', statement, flags=re.IGNORECASE)
                    # Remove ON UPDATE CURRENT_TIMESTAMP
                    statement = re.sub(r'ON\s+UPDATE\s+CURRENT_TIMESTAMP', '', statement, flags=re.IGNORECASE)
                    # Convert UNIQUE KEY name (cols) to UNIQUE(cols)
                    statement = re.sub(r'UNIQUE\s+KEY\s+\w+\s+\(([^)]+)\)', r'UNIQUE (\1)', statement, flags=re.IGNORECASE)
                    
                    translated_statements.append(statement)
                statements = translated_statements

            conn = db.connect()
            try:
                if db.is_sqlite:
                    try:
                        raw_conn = conn.driver_connection
                    except AttributeError:
                        raw_conn = conn.connection
                    cursor = raw_conn.cursor()
                else:
                    cursor = conn.cursor()
                    
                for statement in statements:
                    if statement:
                        cursor.execute(statement)
                conn.commit()
                print("[OK] Database schema created successfully")
            finally:
                conn.close()

        create_default_users()
        print("[OK] Database initialized successfully")

    except Exception as e:
        print(f"[WARN] Database schema initialization note (ignoring): {e}")
        # Proceed to create users even if schema exists
        try:
            create_default_users()
        except Exception as e2:
             print(f"[ERROR] Could not create users: {e2}")

def create_default_users():
    """Create default admin, HOD, and student users"""
    conn = db.get_connection()
    try:
        # Helper to create a user safely if not exists
        def create_user_if_not_exists(name, email, plain_password, role, department, is_approved):
            exists = db.execute_query(
                "SELECT id FROM users WHERE email = %s",
                (email,),
                fetch_one=True
            )
            if not exists:
                password_hash = generate_password_hash(plain_password)
                db.execute_query(
                    "INSERT INTO users (name, email, password_hash, role, department, is_approved) VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, email, password_hash, role, department, is_approved)
                )
                print(f"[OK] Created default user: {email} ({role} - {department})")
            else:
                # Update department short-code if needed (e.g. Computer Science -> CS)
                db.execute_query(
                    "UPDATE users SET department = %s WHERE email = %s",
                    (department, email)
                )
                print(f"[INFO] User already exists: {email} (updated department to {department})")

        # 1. Create TPO
        create_user_if_not_exists('Admin TPO', 'tpo@college.edu', 'admin123', 'tpo', 'Placement', True)

        # 2. Create Student
        create_user_if_not_exists('Alice Johnson', 'alice@college.edu', 'student123', 'student', 'CS', True)

        # 3. Create HODs for all departments
        hods = [
            ('HOD CS', 'hod.cs@college.edu', 'hod123', 'hod', 'CS', True),
            ('HOD EC', 'hod.ec@college.edu', 'hod123', 'hod', 'EC', True),
            ('HOD EEE', 'hod.eee@college.edu', 'hod123', 'hod', 'EEE', True),
            ('HOD IS', 'hod.is@college.edu', 'hod123', 'hod', 'IS', True),
            ('HOD MCA', 'hod.mca@college.edu', 'hod123', 'hod', 'MCA', True),
            ('HOD MBA', 'hod.mba@college.edu', 'hod123', 'hod', 'MBA', True),
            ('HOD MTECH', 'hod.mtech@college.edu', 'hod123', 'hod', 'MTECH', True)
        ]

        for name, email, pwd, role, dept, approved in hods:
            create_user_if_not_exists(name, email, pwd, role, dept, approved)

    except Exception as e:
        print(f"[ERROR] Error creating default users: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # 🔥 Important: Don’t reset DB on Render!
    if os.getenv("RENDER") == "True":
        print("⚠️ Skipping database initialization on Render (production).")
    else:
        print("Initializing database locally...")
        init_database()
