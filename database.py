import psycopg2
import streamlit as st

# Connect using secrets
def get_connection():
    return psycopg2.connect(st.secrets["DB_URL"])

# Create tables (if not exists)
def create_tables():
    conn = get_connection()
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            disease TEXT NOT NULL,
            occupation TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Daily table
    c.execute("""
        CREATE TABLE IF NOT EXISTS daily (
            id SERIAL PRIMARY KEY,
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
    c.close()
    conn.close()

# Add a user
def add_user(name, email, age, gender, disease, occupation, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO users (name, email, age, gender, disease, occupation, password)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, email, age, gender, disease, occupation, password))
    conn.commit()
    c.close()
    conn.close()

# Authenticate user
def authenticate_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = c.fetchone()
    c.close()
    conn.close()
    return user

# Fetch user by email
def fetch_user(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = c.fetchone()
    c.close()
    conn.close()
    return user

# Fetch user by ID
def fetch_user_by_id(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = c.fetchone()
    c.close()
    conn.close()
    return user

# Add daily data
def add_daily(user_id, email, weight, sleep_duration, quality_of_sleep, physical_activity_level, stress_level,
              bmi_category, blood_pressure, heart_rate, daily_steps, respiratory_rate, blood_volume,
              calories_burned, body_temperature, drinking_water, daily_usage_of_smartphone):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO daily (
            user_id, email, weight, sleep_duration, quality_of_sleep, physical_activity_level,
            stress_level, bmi_category, blood_pressure, heart_rate, daily_steps,
            respiratory_rate, blood_volume, calories_burned, body_temperature,
            drinking_water, daily_usage_of_smartphone
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, email, weight, sleep_duration, quality_of_sleep, physical_activity_level, stress_level,
          bmi_category, blood_pressure, heart_rate, daily_steps, respiratory_rate, blood_volume,
          calories_burned, body_temperature, drinking_water, daily_usage_of_smartphone))
    conn.commit()
    c.close()
    conn.close()

# Fetch all daily data by user_id
def fetch_daily(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM daily WHERE user_id = %s", (user_id,))
    daily = c.fetchall()
    c.close()
    conn.close()
    return daily

# Fetch all users
def fetch_all_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    c.close()
    conn.close()
    return users

# Fetch all daily entries by email
def fetch_all_daily(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM daily WHERE email = %s", (email,))
    daily = c.fetchall()
    c.close()
    conn.close()
    return daily
