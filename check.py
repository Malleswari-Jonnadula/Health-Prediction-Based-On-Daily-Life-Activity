import psycopg2
conn = psycopg2.connect("postgresql://postgres.qgprneayibukmvbbkfnz:Malleswari%401@aws-0-ap-south-1.pooler.supabase.com:6543/postgres")
print("✅ Connected successfully")
conn.close()
