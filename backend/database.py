"""
Database connection and utility functions
"""
import pymysql
import os
from dotenv import load_dotenv
import certifi

# Load environment variables from .env (local development)
load_dotenv()



from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

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
                "ca": os.getenv("SSL_CA", certifi.where())
            }
        else:
            # Local MySQL has NO SSL
            self.ssl = None

        # Create SQLAlchemy Engine
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
            pool_recycle=1800, # Recycle connections every 30 mins
            pool_pre_ping=True # Check connection liveness before checkout
        )

    def connect(self):
        """Get a connection from the pool"""
        try:
            # Get raw DBAPI connection from pool
            # This returns a sqlalchemy.pool.base._ConnectionFairy
            # We need to ensure it behaves like our pymysql connection
            
            # Note: raw_connection() usually returns standard DBAPI connection.
            # However, we need DictCursor behavior which we relied on in pymysql.connect settings.
            # To get DictCursor with generic engine, we might need to rely on the fact 
            # that we can set cursorclass driver arg/options.
            
            # Actually, standard pymysql cursors are tuples.
            # The original code used `cursorclass=pymysql.cursors.DictCursor`.
            # We can pass this in connect_args to create_engine.
            
            return self.engine.raw_connection()

        except Exception as e:
            print(f"[ERROR] DB Connection Pool Failed: {e}")
            raise

    def get_connection(self):
        return self.connect()

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute SQL query safely"""
        conn = None
        cursor = None
        try:
            conn = self.connect()
            # To ensure DictCursor behavior if not set globally:
            # Pymysql raw connection allows creating specific cursors.
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
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
            if cursor:
                cursor.close()
            if conn:
                conn.close() # Returns to pool


# Global DB instance
db = Database()
