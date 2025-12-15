"""
Database connection and utility functions
"""
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env (local development)
load_dotenv()


class Database:
    def __init__(self):

        # ---------- LOCAL DEFAULTS (XAMPP MySQL) ----------
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DB", "placement_portal")
        self.port = int(os.getenv("MYSQL_PORT", 3306))

        # ---------- OVERRIDE: RENDER / TiDB CLOUD ----------
        # If DB_HOST exists, we use TiDB config
        if os.getenv("DB_HOST"):
            self.host = os.getenv("DB_HOST")
            self.user = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASS")
            self.database = os.getenv("DB_NAME")
            self.port = int(os.getenv("DB_PORT", 4000))

            # SSL required for TiDB Cloud
            self.ssl = {
                "ca": os.getenv("SSL_CA", "/etc/ssl/certs/ca-certificates.crt")
            }
        else:
            # Local MySQL has NO SSL
            self.ssl = None

    def connect(self):
        """Establish DB connection"""
        try:
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
            print(f"[ERROR] DB Connection Failed: {e}")
            raise

    def get_connection(self):
        return self.connect()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute SQL query safely"""
        conn = None
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)

                if fetch_one:
                    return cursor.fetchone()
                if fetch_all:
                    return cursor.fetchall()

                conn.commit()
                return cursor.rowcount

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Query Execution Failed: {e}")
            raise

        finally:
            if conn:
                conn.close()


# Global DB instance
db = Database()
