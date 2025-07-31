import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
from streamlit_option_menu import option_menu
import requests 
import seaborn as sns
from streamlit_lottie import st_lottie
import streamlit as st
import speech_recognition as sr
from streamlit_option_menu import option_menu
import requests
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
from googleapiclient.discovery import build
import pandas as pd
import random
from bs4 import BeautifulSoup  
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# Function to create database connection
def create_connection():
    conn = sqlite3.connect('health_app.db')
    return conn
API_KEY = 'AIzaSyBd4yGXZXraYFkwyZosssBQ6u7ckrxfTTs'
BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
VIDEO_DETAILS_URL = 'https://www.googleapis.com/youtube/v3/videos'
youtube = build("youtube", "v3", developerKey=API_KEY)
nltk.download('stopwords')
nltk.download('punkt')
def parse_duration(duration_str):
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration_str)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0 if match.group(1) is not None else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0 if match.group(2) is not None else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0 if match.group(3) is not None else 0
    return hours * 3600 + minutes * 60 + seconds
def search_videos(query):
    params = {
        'part': 'snippet',
        'q': query,
        'key': API_KEY,
        'type': 'video',
        'maxResults': 5,  # Adjust as needed
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    videos = []
    for item in data.get('items', []):
        video_id = item['id']['videoId']
        video_params = {
            'part': 'snippet,statistics,contentDetails',
            'id': video_id,
            'key': API_KEY,
        }
        video_response = requests.get(VIDEO_DETAILS_URL, params=video_params)
        video_data = video_response.json()
        video_statistics = video_data['items'][0].get('statistics', {})
        like_count = int(video_statistics.get('likeCount', 0))
        video = {
            'title': video_data['items'][0]['snippet']['title'],
            'video_id': video_id,
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'views': int(video_statistics.get('viewCount', 0)),
            'likes': like_count,
            'comments': int(video_statistics.get('commentCount', 0)),
            'length': parse_duration(video_data['items'][0]['contentDetails']['duration']),
            'channel_name': video_data['items'][0]['snippet']['channelTitle'],
            'date_posted': video_data['items'][0]['snippet']['publishedAt'],
        }
        videos.append(video)
    return videos# Function to create user table
def create_user_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
    ''')
    conn.commit()

# Function to insert user data into user table
def insert_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?);
    ''', (username, pbkdf2_sha256.hash(password)))
    conn.commit()

# Function to check if user exists in user table
def check_user(conn, username, password):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password FROM users WHERE username = ?;
    ''', (username,))
    user = cursor.fetchone()
    if user:
        return pbkdf2_sha256.verify(password, user[0])
    return False

# Function to create daily updates table
def create_daily_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_updates (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            occupation TEXT NOT NULL,
            sleep_duration INTEGER NOT NULL,
            quality_of_sleep INTEGER NOT NULL,
            physical_activity_level INTEGER NOT NULL,
            stress_level INTEGER NOT NULL,
            BMI_category TEXT NOT NULL,
            blood_pressure INTEGER NOT NULL,
            heart_rate INTEGER NOT NULL,
            daily_steps INTEGER NOT NULL,
            respiratory_rate INTEGER NOT NULL,
            blood_volume INTEGER NOT NULL,
            calories_burned INTEGER NOT NULL,
            body_temperature INTEGER NOT NULL,
            drinking_water INTEGER NOT NULL,
            daily_usage_of_smart_phone INTEGER NOT NULL
        );
    ''')
    conn.commit()

# UI for registration page
def register_page(conn):
    st.header("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_username and new_password and new_password == confirm_password:
            insert_user(conn, new_username, new_password)
            st.success("Registered successfully! You can now login.")
        else:
            st.error("Please fill out all fields and ensure passwords match.")

# UI for login page
def login_page(conn):
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            if check_user(conn, username, password):
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")
def daily_updates_values(conn):
    st.header("Daily Updates")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=0, max_value=150)
    weight = st.number_input("Weight", min_value=0)
    occupation = st.text_input("Occupation")
    sleep_duration = st.number_input("Sleep Duration", min_value=0)
    quality_of_sleep = st.slider("Quality of Sleep", min_value=0, max_value=10)
    physical_activity_level = st.slider("Physical Activity Level", min_value=0, max_value=10)
    stress_level = st.slider("Stress Level", min_value=0, max_value=10)
    BMI_category = st.selectbox(
        'Select BMI Category',
        ('Obese', 'Overweight', 'Normal', 'Underweight'))
    blood_pressure = st.number_input("Blood Pressure", min_value=0)
    heart_rate = st.number_input("Heart Rate", min_value=0)
    daily_steps = st.number_input("Daily Steps", min_value=0)
    respiratory_rate = st.number_input("Respiratory Rate", min_value=0)
    blood_volume = st.number_input("Blood Volume", min_value=0)
    calories_burned = st.number_input("Calories Burned", min_value=0)
    body_temperature = st.number_input("Body Temperature", min_value=0)
    drinking_water = st.number_input("Drinking Water", min_value=0)
    daily_usage_of_smart_phone = st.number_input("Daily Usage of Smart Phone", min_value=0)
    # Add more input fields as needed
    if st.button("Submit"):
        if username:
            if check_user(conn, username, password):
                insert_daily_updates(conn, username, gender, age, weight, occupation, sleep_duration, quality_of_sleep,
                                 physical_activity_level, stress_level, BMI_category, blood_pressure, heart_rate,
                                 daily_steps, respiratory_rate, blood_volume, calories_burned, body_temperature,
                                 drinking_water, daily_usage_of_smart_phone)
                st.success("Daily updates submitted successfully!")
            else:
                st.error(f"User '{username}' does not exist in the database.")
        else:
            st.error("Please enter a username.")

# Function to insert daily updates data into database
def insert_daily_updates(conn, username, gender, age, weight, occupation, sleep_duration, quality_of_sleep,
                         physical_activity_level, stress_level, BMI_category, blood_pressure, heart_rate,
                         daily_steps, respiratory_rate, blood_volume, calories_burned, body_temperature,
                         drinking_water, daily_usage_of_smart_phone):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_updates (username, gender, age, weight, occupation, sleep_duration, quality_of_sleep,
                                  physical_activity_level, stress_level, BMI_category, blood_pressure, heart_rate,
                                  daily_steps, respiratory_rate, blood_volume, calories_burned, body_temperature,
                                  drinking_water, daily_usage_of_smart_phone) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', (username, gender, age, weight, occupation, sleep_duration, quality_of_sleep, physical_activity_level,
          stress_level, BMI_category, blood_pressure, heart_rate, daily_steps, respiratory_rate, blood_volume,
          calories_burned, body_temperature, drinking_water, daily_usage_of_smart_phone))
    conn.commit()

# Function to retrieve daily updates by username
def retrieve_daily_updates(conn, username):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM daily_updates WHERE username = ?;
    ''', (username,))
    return cursor.fetchall()

# UI for Daily Updates History page
def daily_updates_history_page(conn):
    username = st.text_input("Enter Username")
    if st.button("Retrieve"):
        if username:
            records = retrieve_daily_updates(conn, username)
            if records:
                columns = ['ID', 'username', 'gender', 'age', 'weight', 'occupation', 'sleep_duration', 'quality_of_sleep',
                    'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                    'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                    'drinking_water', 'daily_usage_of_smart_phone']

                df = pd.DataFrame(records, columns=columns)
                # Unique usage times and their counts
                unique_times = df['daily_usage_of_smart_phone'].unique()
                counts = df['daily_usage_of_smart_phone'].value_counts()
                colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange']

                # Sleep Duration Distribution
                st.subheader("Sleep Duration (hours)")
                fig, ax = plt.subplots()
                ax.hist(df['sleep_duration'], bins=10, edgecolor='black')
                ax.set_xlabel('Sleep Duration (hours)')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
                
                st.subheader("Weight Distribution")
                # Weight Distribution
                fig, ax = plt.subplots()
                ax.hist(df['weight'], bins=10, edgecolor='black', color='orange')
                ax.set_xlabel('Weight')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                st.subheader("Physical Activity Level Distribution")
                # Physical Activity Level Distribution
                fig, ax = plt.subplots()
                ax.hist(df['physical_activity_level'], bins=10, edgecolor='black', color='green')
                ax.set_xlabel('Physical Activity Level')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                # Stress Level Distribution
                st.subheader("Stress Level Distribution")
                fig, ax = plt.subplots()
                ax.hist(df['stress_level'], bins=10, edgecolor='black', color='red')
                ax.set_xlabel('Stress Level')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                # Heart Rate Distribution
                st.subheader("Heart Rate Distribution")
                fig, ax = plt.subplots()
                ax.hist(df['heart_rate'], bins=10, edgecolor='black', color='cyan')
                ax.set_xlabel('Heart Rate')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)


                # Daily Steps Distribution
                st.subheader("Daily Steps Distribution")
                fig, ax = plt.subplots()
                ax.hist(df['daily_steps'], bins=10, edgecolor='black', color='magenta')
                ax.set_xlabel('Daily Steps')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                # Plotting
                st.subheader("Daily Usage Time of Smart Phone")
                fig, ax = plt.subplots()
                ax.bar(unique_times, counts, color=colors)
                ax.set_xlabel('Usage Time (hours)')
                ax.set_ylabel('Frequency')
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)

                st.subheader("Drinking Water (liters)")
                # Plotting Drinking Water (liters)
                fig, ax = plt.subplots()
                ax.hist(df['drinking_water'], bins=10, edgecolor='black')
                ax.set_xlabel('Drinking Water Intake (liters)')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)

                st.subheader("Body Temperature")
                fig, ax = plt.subplots()
                sns.kdeplot(df['body_temperature'], shade=True, ax=ax)
                ax.set_xlabel('Body Temperature')
                ax.set_ylabel('Density')
                st.pyplot(fig)

            else:
                st.warning("No records found for the username.")

def statistics_page(conn):
    st.header("Statistics")
    username = st.text_input("Enter Username")
    if st.button("Retrieve"):
        if username:
            records = retrieve_daily_updates(conn, username)
            if records:
                columns = ['ID', 'username', 'gender', 'age', 'weight', 'occupation', 'sleep_duration', 'quality_of_sleep',
                    'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                    'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                    'drinking_water', 'daily_usage_of_smart_phone']

                df = pd.DataFrame(records, columns=columns)
                try:
                    weight_diff = df['weight'].diff()
                    if max(diff < 0 for diff in weight_diff):
                        st.write("Alert: Weight is gradually decreasing!")
                        st.divider()
                    # If all differences are positive, weight is increasing
                    elif max(diff > 0 for diff in weight_diff):
                        st.write("Alert: Weight is gradually increasing!")
                        st.divider()
                    duration_diff = df['sleep_duration'].diff()
                    # If all differences are negative, sleep duration is decreasing
                    if max(diff < 0 for diff in duration_diff):
                        st.write("Alert: Sleep duration is decreasing. Consider regulating sleep for 6 hours regularly.")
                        st.divider()
                    quality_diff = df['quality_of_sleep'].diff()
                        # If all differences are negative, quality of sleep is decreasing
                    if max(diff < 0 for diff in quality_diff):
                        st.write("Alert: Quality of sleep is consistently decreasing. Consider consulting a healthcare professional.")
                        st.write("Suggestion: Keep a consistent sleep schedule, create a relaxing bedtime routine, and avoid caffeine and electronics before bed.")
                        st.divider()
                    activity_diff = df['physical_activity_level'].diff()
                        # If all differences are negative, physical activity level is decreasing
                    if max(diff < 0 for diff in activity_diff):
                        st.write("Alert: Physical activity level is consistently decreasing. Consider incorporating more exercise into your routine.")
                        st.write("Suggestion: Aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity per week, along with muscle-strengthening activities on two or more days per week.")
                        st.divider()
                    stress_diff = df['stress_level'].diff()
                        # If all differences are positive, stress level is consistently increasing
                    if max(diff > 0 for diff in stress_diff):
                        st.write("Alert: Stress level is consistently increasing. It's important to take steps to manage stress.")
                        st.write("Suggestion: Practice stress-reduction techniques such as deep breathing, meditation, exercise, and maintaining a healthy lifestyle. Consider seeking support from a therapist or counselor if needed.")
                        st.divider()
                    systolic_diastolic = df['blood_pressure'].str.split('/', expand=True).astype(int)
                    # Calculate differences between consecutive systolic and diastolic values
                    systolic_diff = systolic_diastolic[0].diff()
                    diastolic_diff = systolic_diastolic[1].diff()
                    # If all differences are positive for systolic and diastolic, blood pressure is consistently increasing
                    if max(diff > 0 for diff in systolic_diff) and all(diff > 0 for diff in diastolic_diff):
                        st.write("Alert: Blood pressure is consistently increasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                        st.write("Suggestion: Implement lifestyle changes such as reducing sodium intake, increasing physical activity, maintaining a healthy weight, and managing stress.")
                        st.divider()
                    # If all differences are negative for systolic and diastolic, blood pressure is consistently decreasing
                    elif max(diff < 0 for diff in systolic_diff) and all(diff < 0 for diff in diastolic_diff):
                        st.write("Alert: Blood pressure is consistently decreasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                        st.write("Suggestion: Monitor your blood pressure closely and consult with a healthcare provider to ensure it's within a healthy range.")
                        st.divider()
                    rate_diff = df['heart_rate'].diff()
                    # If all differences are negative, heart rate is consistently decreasing
                    if max(diff < 0 for diff in rate_diff):
                        st.write("Alert: Heart rate is consistently decreasing. Monitor your heart rate and consider consulting a healthcare professional.")
                        st.write("Suggestion: Focus on cardiovascular exercises, maintain a healthy diet, and manage stress levels to improve heart health.")
                        st.divider()
                    # If all differences are positive, heart rate is consistently increasing
                    elif max(diff > 0 for diff in rate_diff):
                        st.write("Alert: Heart rate is consistently increasing. Monitor your heart rate and consider consulting a healthcare professional.")
                        st.write("Suggestion: Check for factors such as physical exertion, stress, or caffeine intake that might be causing the increase. Consider consulting with a healthcare provider for further evaluation.")
                        st.divider()
                    if df['daily_steps'].sum() == 0:
                        st.write("Alert: No steps recorded. It's important to stay active throughout the day.")
                        st.write("Suggestion: Aim to incorporate physical activity into your daily routine. Start with small, achievable goals and gradually increase your activity level.")
                        st.divider()
                    # If steps are consistently decreasing
                    elif max(df['daily_steps'].iloc[i] >= df['daily_steps'].iloc[i + 1] for i in range(len(df) - 1)):
                        st.write("Alert: Daily steps are consistently decreasing. It's important to maintain physical activity levels.")
                        st.write("Suggestion: Find activities you enjoy and set specific goals to increase your daily step count. Consider walking meetings, taking the stairs, or going for a walk during breaks.")
                        st.divider()
                    # If steps are not consistently maintained
                    else:
                        st.write("Alert: Daily steps are not consistently maintained. It's important to strive for regular physical activity.")
                        st.write("Suggestion: Set a daily step goal and track your progress using a pedometer or smartphone app. Try to incorporate walking into your daily routine, such as walking instead of driving for short trips.")
                        st.divider()
                    rate_diff = df['respiratory_rate'].diff()
                    # If all differences are negative, respiration rate is consistently decreasing
                    if max(diff < 0 for diff in rate_diff):
                        st.write("Alert: Respiration rate is consistently decreasing. Monitor your respiratory health and consider consulting a healthcare professional.")
                        st.write("Suggestion: Practice deep breathing exercises, maintain good posture, and ensure proper hydration and ventilation in your environment.")
                        st.divider()
                    avg_blood_volume = df['blood_volume'].mean()
                    # Define thresholds for low and high blood volume levels
                    low_threshold = avg_blood_volume * 0.9
                    high_threshold = avg_blood_volume * 1.1
                    # Check blood volume levels and provide recommendations
                    if df['blood_volume'].min() < low_threshold:
                        st.write("Alert: Blood volume is low. Consult with a healthcare professional for further evaluation.")
                        st.write("Suggestion: Ensure adequate hydration and consider consuming iron-rich foods to support healthy blood volume levels.")
                        st.divider()
                    elif df['blood_volume'].max() > high_threshold:
                        st.write("Alert: Blood volume is high. Consult with a healthcare professional for further evaluation.")
                        st.write("Suggestion: Monitor blood pressure and cholesterol levels, and consider lifestyle changes such as maintaining a healthy weight and reducing sodium intake.")
                        st.divider()
                    avg_calories_burned = df['calories_burned'].mean()
                    # Define thresholds for low and high calories burned levels
                    low_threshold = avg_calories_burned * 0.9
                    high_threshold = avg_calories_burned * 1.1

                    # Check calories burned levels and provide recommendations
                    if df['calories_burned'].min() < low_threshold:
                        st.write("Alert: Calories burned are low. Consider increasing physical activity.")
                        st.write("Suggestion: Incorporate more exercise into your routine, such as brisk walking, jogging, or cycling. Set achievable goals and track your progress.")
                        st.divider()
                    elif df['calories_burned'].max() > high_threshold:
                        st.write("Alert: Calories burned are high. Ensure a balanced approach to exercise and nutrition.")
                        st.write("Suggestion: Maintain a well-rounded diet with plenty of fruits, vegetables, lean proteins, and whole grains. Avoid overexertion and ensure adequate rest and recovery.")
                        st.divider()
                    normal_low = 97.0
                    normal_high = 99.0
                    # Check if any temperature readings are outside the normal range
                    if max(temp < normal_low or temp > normal_high for temp in df['body_temperature']):
                        st.write("Alert: Body temperature is outside the normal range.")
                        st.write("Suggestion: If you have a fever (temperature above 100.4°F or 38°C), consult a healthcare professional. Otherwise, monitor your temperature and consider rest and hydration if you feel unwell.")
                        st.divider()
                    # Define recommended water intake levels
                    recommended_low = 2.0  # liters
                    recommended_high = 4  # liters
                    st.write(df['drinking_water'].tolist())
                    # Check if any water intake readings are below the recommended range
                    if max(water < recommended_low for water in df['drinking_water']):
                        st.write("Alert: Drinking water intake is below the recommended range.")
                        st.write("Suggestion: Increase your water intake to ensure proper hydration. Aim to drink at least 8 glasses (approximately 2 liters) of water per day.")
                        st.divider()
                    # Define recommended smartphone usage range
                    recommended_low = 0  # hours (minimum)
                    recommended_high = 2  # hours (maximum for healthy usage)
                    st.write(df['daily_usage_of_smart_phone'].tolist())
                    # Check if any usage time readings are above the recommended maximum
                    if max(usage > recommended_high for usage in df['daily_usage_of_smart_phone']):
                        st.write("Alert: Daily usage time of smartphone is above the recommended range.")
                        st.write("Suggestion: Limit screen time and take breaks from smartphone use. Consider setting usage limits or using apps that track and manage screen time.")
                        st.divider()

                except:
                    pass

# Main UI
st.set_page_config(page_title="Health Application", page_icon=":hospital:")


with st.sidebar:
    page = option_menu("DashBoard", ["Home",'Login','Register','Daily Updates','Analytics','Statistics'], 
        icons=['house','unlock-fill','lock-fill','hospital','graph-up','bar-chart'], menu_icon="cast", default_index=0,
        styles={
        "nav-link-selected": {"background-color": "green", "color": "white", "border-radius": "5px"},
})

conn = create_connection()
create_user_table(conn)
create_daily_table(conn)
if page == "Home":
    st.write("<h1 style='color: green;'>PUBLIC HEALTHCARE CENTER</h1>", unsafe_allow_html=True)
    st.image('https://www.epfitnesstrainer.com/wp-content/uploads/2021/03/health-and-wellbeing-blog.jpg', use_column_width=True)

if page == "Login":
    login_page(conn)
elif page == "Register":
    register_page(conn)
elif page == "Daily Updates":
    daily_updates_values(conn)  # Assuming you want this page to have the same functionalities as login
elif page == "Analytics":
    daily_updates_history_page(conn)
elif page == "Statistics":
    statistics_page(conn)