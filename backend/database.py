import pymysql
import os
from dotenv import load_dotenv
import certifi
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Load environment variables from .env (local development)
load_dotenv()

def dict_factory(cursor, row):
    """Convert SQLite row to dictionary to mimic PyMySQL DictCursor"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

import datetime
def curdate_impl():
    """SQLite custom implementation for MySQL CURDATE()"""
    return datetime.date.today().isoformat()

class Database:
    def __init__(self):
        self.is_sqlite = False

        # ---------- LOCAL DEFAULTS (XAMPP MySQL) ----------
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DB", "placement_portal")
        self.port = int(os.getenv("MYSQL_PORT", 3306))

        # ---------- OVERRIDE: RENDER / TiDB CLOUD ----------
        if os.getenv("DB_HOST"):
            self.host = os.getenv("DB_HOST")
            self.user = os.getenv("DB_USER")
            self.password = os.getenv("DB_PASS")
            self.database = os.getenv("DB_NAME")
            self.port = int(os.getenv("DB_PORT", 4000))

            self.ssl = {
                "ca": os.getenv("SSL_CA", certifi.where())
            }
        else:
            self.ssl = None

        # Try connecting with MySQL first
        try:
            db_url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            connect_args = {}
            if self.ssl:
                connect_args['ssl'] = self.ssl
                
            self.engine = create_engine(
                db_url,
                connect_args=connect_args,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_recycle=1800,
                pool_pre_ping=True
            )
            # Test connection
            conn = self.engine.raw_connection()
            conn.close()
            print(f"[OK] Connected successfully to MySQL database '{self.database}' on {self.host}:{self.port}")

        except Exception as mysql_err:
            print(f"[WARN] MySQL/TiDB Connection Failed: {mysql_err}")
            print("[INFO] Falling back to high-performance SQLite Local Database...")
            self.is_sqlite = True
            self.database = "placement_portal.db"
            db_url = "sqlite:///placement_portal.db"
            
            self.engine = create_engine(
                db_url,
                connect_args={"check_same_thread": False}
            )
            print("[OK] SQLite Database engine initialized successfully")

    def connect(self):
        """Get a connection from the pool/engine"""
        try:
            conn = self.engine.raw_connection()
            if self.is_sqlite:
                # Get the underlying sqlite3 connection and set row_factory and functions
                try:
                    raw_conn = conn.driver_connection
                except AttributeError:
                    try:
                        raw_conn = conn.connection
                    except:
                        raw_conn = None
                
                if raw_conn:
                    raw_conn.row_factory = dict_factory
                    raw_conn.create_function("CURDATE", 0, curdate_impl)
            return conn
        except Exception as e:
            print(f"[ERROR] DB Connection Failed: {e}")
            raise

    def get_connection(self):
        return self.connect()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute SQL query safely, with auto-translation for SQLite"""
        conn = None
        cursor = None
        try:
            conn = self.connect()
            
            if self.is_sqlite:
                # Translate parameter placeholder from MySQL (%s) to SQLite (?)
                query = query.replace('%s', '?')
                # Under SQLite, raw connection or driver connection acts as the DBAPI connection
                try:
                    raw_conn = conn.driver_connection
                except AttributeError:
                    raw_conn = conn.connection
                
                raw_conn.row_factory = dict_factory
                raw_conn.create_function("CURDATE", 0, curdate_impl)
                cursor = raw_conn.cursor()
            else:
                cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            if fetch_one:
                res = cursor.fetchone()
                # Ensure it is a standard dict (or dict-like)
                return dict(res) if res else None
            if fetch_all:
                res = cursor.fetchall()
                return [dict(r) for r in res] if res else []

            conn.commit()
            return cursor.rowcount

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Query Execution Failed: {e}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

# Global DB instance
db = Database()
