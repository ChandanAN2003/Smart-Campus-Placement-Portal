import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("MYSQL_HOST", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "")
port = int(os.getenv("MYSQL_PORT", 3306))
dbname = os.getenv("MYSQL_DB", "placement_portal")

print(f"Connecting to MySQL at {host}:{port} as {user}...")

try:
    conn = pymysql.connect(host=host, user=user, password=password, port=port)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
    print(f"Database '{dbname}' created or already exists.")
    conn.close()
except Exception as e:
    print(f"Error creating DB: {e}")
