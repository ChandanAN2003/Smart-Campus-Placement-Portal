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

        print("Migration complete.")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
