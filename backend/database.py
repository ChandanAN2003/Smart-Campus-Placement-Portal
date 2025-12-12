"""
Database connection and utility functions
"""
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
load_dotenv()

class Database:
    def __init__(self):
        # Local defaults (for XAMPP)
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DB", "placement_portal")
        self.port = int(os.getenv("MYSQL_PORT", 3306))

        # Render / TiDB Cloud override (if available)
        self.host = os.getenv("DB_HOST", self.host)
        self.user = os.getenv("DB_USER", self.user)
        self.password = os.getenv("DB_PASSWORD", self.password)
        self.database = os.getenv("DB_NAME", self.database)
        self.port = int(os.getenv("DB_PORT", self.port))

        # Enable SSL only for TiDB Cloud (Render)
        self.ssl = {"ssl": {}} if os.getenv("DB_SSL", "False").lower() == "true" else None

    def connect(self):
        """Establish database connection"""
        try:
            # print("--------------------------------------------------")
            # print("[INFO] Connecting to database...")
            # Reduced logging to avoid noise on every query
            
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                ssl=self.ssl,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            return connection
        except Exception as e:
            print(f"[ERROR] Database connection error: {e}")
            raise

    def get_connection(self):
        """Get a new connection"""
        return self.connect()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query and return results"""
        conn = None
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.rowcount
                conn.commit()
                return result
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            print(f"[ERROR] Query execution error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def close(self):
        """Placeholder for backward compatibility"""
        pass

# Global instance
db = Database()
