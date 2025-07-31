import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        disease TEXT NOT NULL,
        occupation TEXT NOT NULL,
        password TEXT NOT NULL
        
    )
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS daily (
        user_id INTEGER NOT NULL,
        email TEXT NOT NULL,
        weight INTEGER NOT NULL,
        sleep_duration INTEGER NOT NULL,
        quality_of_sleep INTEGER NOT NULL,
        physical_activity_level INTEGER NOT NULL,
        stress_level INTEGER NOT NULL,
        bmi_category TEXT NOT NULL,
        blood_pressure INTEGER NOT NULL,
        heart_rate INTEGER NOT NULL,
        daily_steps INTEGER NOT NULL,
        respiratory_rate INTEGER NOT NULL,
        blood_volume INTEGER NOT NULL,
        calories_burned INTEGER NOT NULL,
        body_temperature INTEGER NOT NULL,
        drinking_water INTEGER NOT NULL,
        daily_usage_of_smartphone INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
""")
conn.commit()
conn.close()

def add_user(name,email,age,gender,disease,occupation,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name,email,age,gender,disease,occupation,password) VALUES (?, ?, ?,?,?,?,?)", (name,email,age,gender,disease,occupation,password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user
def fetch_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user
def fetch_user_by_id(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user
def add_daily(user_id,email, weight, sleep_duration, quality_of_sleep, physical_activity_level, stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, respiratory_rate, blood_volume, calories_burned, body_temperature, drinking_water, daily_usage_of_smartphone):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO daily (
            user_id,email, weight, sleep_duration, quality_of_sleep, physical_activity_level, 
            stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, 
            respiratory_rate, blood_volume, calories_burned, body_temperature, 
            drinking_water, daily_usage_of_smartphone
        ) 
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, email, weight, sleep_duration, quality_of_sleep, physical_activity_level, 
          stress_level, bmi_category, blood_pressure, heart_rate, daily_steps, 
          respiratory_rate, blood_volume, calories_burned, body_temperature, 
          drinking_water, daily_usage_of_smartphone))
    conn.commit()
    conn.close()
     

def fetch_daily(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM daily WHERE user_id = ?", (user_id,))
    daily = c.fetchall()
    conn.close()
    return daily
def fetch_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return users
def fetch_all_daily(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM daily WHERE email = ?", (email,))
    daily = c.fetchall()
    conn.close()
    return daily
