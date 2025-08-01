import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL") or "postgresql://postgres:Malleswari%401@db.qgprneayibukmvbbkfnz.supabase.co:5432/postgres"


try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Users table
    print("👤 Users:\n")
    cur.execute("SELECT * FROM users")
    for row in cur.fetchall():
        print(row)

    # Daily table
    print("\n📅 Daily Health Data:\n")
    cur.execute("SELECT * FROM daily")
    for row in cur.fetchall():
        print(row)

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals():
        conn.close()
