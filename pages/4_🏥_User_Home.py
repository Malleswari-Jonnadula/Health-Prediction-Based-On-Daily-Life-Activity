import streamlit as st
import pickle
from streamlit_option_menu import option_menu
from database import fetch_user, add_daily, fetch_all_daily
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import json
def load_login_status():
    if os.path.exists("login_status.json"):
        with open("login_status.json", "r") as f:
            return json.load(f)
    return {"logged_in": False, "current_user": None}
def save_login_status(logged_in, current_user):
    with open("login_status.json", "w") as f:
        json.dump({"logged_in": logged_in, "current_user": current_user}, f)

# --- On App Start ---
if "logged_in" not in st.session_state:
    status = load_login_status()
    st.session_state["logged_in"] = status["logged_in"]
    st.session_state["current_user"] =  status["current_user"]
if not st.session_state["logged_in"] or not st.session_state["current_user"]:
    st.warning("⚠️ You must log in to access this page.")
    st.stop()
model = joblib.load('kmeans_model.pkl')
st.set_page_config(page_title="User Home", page_icon="🩺", layout="wide")

def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

def user_home_page():
    if "current_user" not in st.session_state or not st.session_state["current_user"]:
        st.warning("⚠️ Session expired. Please log in again.")
        st.stop()

    user = fetch_user(st.session_state["current_user"])
    if not user:
        st.error("User not found. Please log in again.")
        st.stop()
    
    with st.sidebar:
        st.markdown(f"""
        <style>
        .welcome-text {{
            text-align: center;
            padding: 0 10px;
            font-size: 22px;
            font-weight: bold;
            margin-top: -70px;
            margin-bottom: 8px;
            color: white;
        }}
        .welcome-image {{
            display: block;
            margin: 10px auto 20px auto;
            border-radius: 10px;
        }}
        header, footer {{
            visibility: hidden;
        }}
        [data-testid="stSidebarNav"] {{
            display: none !important;
        }}
        [data-testid="stSidebar"] {{
            overflow-y: hidden !important;
            overflow-x: hidden !important;
            height: 100vh !important;
            padding-right: 0 !important;
        }}
        [data-testid="stSidebar"]::-webkit-scrollbar {{
            display: none;
        }}
        </style>
        <div class="welcome-text">Hello👋🏼 {user[1]}!</div>
        <img class="welcome-image" src="https://cdni.iconscout.com/illustration/premium/thumb/doctor-welcoming-with-namaste-hand-gesture-illustration-download-in-svg-png-gif-file-formats--pack-healthcare-medical-illustrations-2215045.png" width="100%">
        """, unsafe_allow_html=True)

        select = option_menu(
            "",
            ["User Profile", "Daily Updates", "Analytics", "Statistics", "Logout"],
            icons=['person-circle', 'calendar', 'bar-chart-line', 'file-medical', 'box-arrow-right'],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0", "background-color": "#d6d6d6"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "margin": "0px",
                    "color": "black",
                },
                "nav-link-selected": {
                    "background-color": "#10bec4",
                },
            },
        )

    if select == 'User Profile':
        st.markdown(
    """
    <style>
    /* Remove extra space at top and bottom */
    .main > div:first-child {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }

    /* Optional: reduce Streamlit's default margins */
    [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        padding-bottom: 1 !important;
    }

    /* Optional: prevent main scroll from misaligning layout */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

        st.markdown(
            """
            <style>
            .custom-main {
                background-image: url('https://img.freepik.com/free-vector/watercolor-medical-background_52683-162142.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                padding: 2rem;    
                border-radius: 15px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        if user:
            name, age, gender, disease, occupation = user[1], user[3], user[4], user[5], user[6]
            if gender == 'Male👦🏻':
                image_link = "https://t4.ftcdn.net/jpg/05/19/88/15/360_F_519881596_pBc2tSugR7oaxJxhSykB5uIw2WhWQl5K.jpg"
            else:
                image_link = "https://t4.ftcdn.net/jpg/09/70/98/03/360_F_970980315_5VYmD4c0BrqX77veKiFsc2J6ksMN5zsh.jpg"
        # CSS Styling for vertical container
            profile_css = """
            <style>
                .profile-container {
                    background-color: #10bec4;
                    padding:50px;
                    border-radius: 50px;
                    box-shadow: 10px 8px 12px rgba(0, 0, 0, 0.15);
                    max-width: 400px;
                    border: 2px solid black;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                .profile-header {
                    font-size: 25px;
                    font-weight: bold;
                    margin-bottom: 1px;
                    color: #333;
                }
                .profile-item {
                    font-size: 19px;
                    margin-bottom: 10px;
                    color: #555;
                    font-weight:bold;
                }
                .profile-image img {
                    border-radius: 50%;
                    max-width: 250px;
                    max-height: 250px;
                    margin-bottom: 0px;
                }
            </style>
            """

            profile_html = f"""
            <div class="custom-main">
                <div class="profile-container">
                    <div class="profile-image">
                        <img src="{image_link}" alt="User Image">
                    </div>
                    <div class="profile-details">
                        <div class="profile-header">User Report</div>
                        <div class="profile-item"><strong>Name:</strong> {name}</div>
                        <div class="profile-item"><strong>Age:</strong> {age}</div>
                        <div class="profile-item"><strong>Gender:</strong> {gender}</div>
                        <div class="profile-item"><strong>Disease:</strong> {disease}</div>
                        <div class="profile-item"><strong>Occupation:</strong> {occupation}</div>
                    </div>
                </div>
            </div>
            """

            st.markdown(profile_css + profile_html, unsafe_allow_html=True)
    elif select == 'Daily Updates':
        st.markdown("<h1 style='text-align: center;'>Daily Updates of User</h1>", unsafe_allow_html=True)
    
        username = user[1]
        gender = user[3]
        age = user[4]
        daily_data = fetch_all_daily(user[2])

        if daily_data:
            daily_data_df = pd.DataFrame(daily_data)
            wt, slp, qslp, pal, sl, bmi, bp, hr, ds, rr, bv, cb, bt, dw, dus = daily_data_df.tail(1).values[0][2:]
        else:
            wt, slp, qslp, pal, sl, bmi, bp, hr, ds, rr, bv, cb, bt, dw, dus = 0, 0, 0, 0, 0, 'Normal', 0, 0, 0, 0, 0, 0, 0, 0, 0
        wt = float(wt) if isinstance(wt, (int, float)) and 3 <= wt <= 200 else 60.0
        slp = int(slp) if isinstance(slp, (int, float)) and 1 <= slp <= 24 else 7
        qslp = int(qslp) if isinstance(qslp, int) and 0 <= qslp <= 10 else 5
        pal = int(pal) if isinstance(pal, int) and 0 <= pal <= 10 else 5
        sl = int(sl) if isinstance(sl, int)  and 0 <= sl <= 10 else 5
        bp = int(bp) if isinstance(bp, int) and 80 <= bp <= 200 else 120
        hr = int(hr) if isinstance(hr, int) and 40 <= hr <= 200 else 75
        ds = int(ds) if isinstance(ds, int) and ds >= 0 else 5000
        rr = int(rr) if isinstance(rr, int) and 5 <= rr <= 30 else 14
        bv = float(bv) if isinstance(bv, (int, float)) and 3.5 <= bv <= 6.0 else 5.0
        cb = int(cb) if isinstance(cb, int) and 1000 <= cb <= 4000 else 2200
        bt = float(bt) if isinstance(bt, (int, float)) and 35.0 <= bt <= 40.0 else 36.8
        dw = float(dw) if isinstance(dw, (int, float)) and 0.5 <= dw <= 10.0 else 5.0
        dus = int(dus) if isinstance(dus, int) and 0 <= dus <= 24 else 4

        with st.form('Daily Updates'):
            
            st.markdown('<div class="custom-card"><h4>📊 Physical & Lifestyle Details</h4>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            weight = col1.number_input("🏋️Weight (kg)",min_value=3.0, max_value=635.0, value=wt ,help="Your body weight in kilograms.")
            sleep_duration = col2.number_input("🛏️Sleep Duration (hours)", min_value=1, max_value=24 ,value=slp, help="How many hours you slept today.")

            quality_of_sleep = col1.slider("🌙Quality of Sleep", 0, 10, qslp , help="Rate your sleep quality from 0 to 10.")
            
            physical_activity_options = {"Low": 2, "Moderate": 5, "High": 8}
            physical_activity_level_label = col2.selectbox("🏃Physical Activity Level", list(physical_activity_options.keys()),
                                                   help="How active you were today.")
            physical_activity_level = physical_activity_options[physical_activity_level_label]
           
            col1, col2 = st.columns(2)
            stress_options = {"Low": 2, "Moderate": 5, "High": 8}
            stress_label = col1.selectbox("😫Stress Level", list(stress_options.keys()),
                                            help="How stressed you felt today.")
            stress_level = stress_options[stress_label]
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="custom-card"><h4>🧬 Vitals</h4>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            BMI_category = col1.selectbox("📈BMI Category", ['Normal', 'Overweight', 'Obese', 'Underweight'],index=0, help="Select your BMI group.")
            bp_options = {
                'Normal (~120/80) 💓': 120,
                'Elevated (~130/80)': 130,
                'Stage 1 (~140/90)': 140,
                'Stage 2 (~160/100)': 160
            }
            bp_choice = col2.selectbox("💓Blood Pressure", list(bp_options.keys()),
                                    help="Select BP status, Ideal: ~120/80 mm Hg")
            blood_pressure = bp_options[bp_choice]
            hr_options = {
                "60-100 bpm (Normal)": 75,
                "<60 bpm (Low)": 55,
                ">100 bpm (High)": 110
            }
            hr_choice = col1.selectbox("❤️Heart Rate", list(hr_options.keys()),
                                    help="Normal heart rate is 60–100 bpm.")
            heart_rate = hr_options[hr_choice]

            daily_steps = col2.number_input("👣Daily Steps", min_value=0, value=ds, help="Number of steps you walked today.")
            resp_options = {
                "Normal (12–16 breaths/min)": 14,
                "Low (<12)": 10,
                "High (>16)": 18
            }
            resp_choice = col1.selectbox("🫁Respiratory Rate", list(resp_options.keys()),
                                        help="Typical breathing rate.")
            respiratory_rate = resp_options[resp_choice]
            blood_volume = col2.slider("🩸Blood Volume (liters)", min_value=3.5, max_value=6.0,
                               value=bv, step=0.1, help="Average adult has ~5L of blood.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<h4>🔥 Body Stats</h4>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            cal_options = {
                "Sedentary (~1800 kcal)": 1800,
                "Active (~2200 kcal)": 2200,
                "Very Active (~2700 kcal)": 2700
            }
            cal_choice = col1.selectbox("Calories Burned (kcal)", list(cal_options.keys()),
                                        help="Roughly based on your activity.")
            calories_burned = cal_options[cal_choice]
            body_temperature = col2.slider("🌡️Body Temperature (°C)", min_value=35.0, max_value=40.0, value=bt, step=0.1, help="Normal: ~36.5–37.5 °C")

            drinking_water = col1.number_input("💧Drinking Water (liters)", min_value=0.5, max_value=10.0, value=dw, step=0.1, help="2–3 Liters/day is generally recommended.")


            daily_usage_of_smart_phone = col2.slider("📱Smartphone Usage (hours)", min_value=0, max_value=24, value=dus, help="Total hours spent on phone.")
            st.markdown('</div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 1, 2])            
            if col2.form_submit_button("Submit", type='primary'):
                required = [weight, sleep_duration, daily_steps, drinking_water, daily_usage_of_smart_phone]
                if username and all(required):
                    add_daily(user[0], user[2], weight, sleep_duration, quality_of_sleep,
                            physical_activity_level, stress_level, BMI_category, blood_pressure,
                            heart_rate, daily_steps, respiratory_rate, blood_volume, calories_burned,
                            body_temperature, drinking_water, daily_usage_of_smart_phone)
                    st.success("✅Daily updates submitted successfully!")
                else:
                    st.error("❗Please fill in all fields before submitting.")

            
    elif select == 'Analytics':
        st.markdown(
        """
        <style>
        /* Apply background image to the main content area */
        .main {
            background-image: url("https://images.rawpixel.com/image_800/czNmcy1wcml2YXRlL3Jhd3BpeGVsX2ltYWdlcy93ZWJzaXRlX2NvbnRlbnQvbHIvcm0zNzNiYXRjaDE1LWJnLTExLmpwZw.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-color: rgba(255, 255, 255, 0.8);
            background-blend-mode: overlay;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        st.markdown("<h1 style='text-align: center;color:#d65804;'>Analytics of User</h1>", unsafe_allow_html=True)
        daily_data = fetch_all_daily(user[2])
        if daily_data:
            daily_data_df = pd.DataFrame(daily_data)
            columns = ['ID','mail', 'weight', 'sleep_duration', 'quality_of_sleep',
                        'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                        'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                        'drinking_water', 'daily_usage_of_smart_phone']
            #make a dataframe with column names
            daily_data_df.columns=columns
            df=daily_data_df.drop(['ID','mail'],axis=1)
            st.write(df)
            if st.checkbox('Show Analytics'):
                col1, col2 = st.columns(2)
                # Unique usage times and their counts
                unique_times = df['daily_usage_of_smart_phone'].unique()
                counts = df['daily_usage_of_smart_phone'].value_counts()
                colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'orange']

                # Sleep Duration Distribution
                fig, ax = plt.subplots()
                ax.hist(df['sleep_duration'], bins=10, edgecolor='black')
                ax.set_xlabel('Sleep Duration (hours)')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: red; text-align: center;">Sleep Duration Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)
        
                # Weight Distribution
                fig, ax = plt.subplots()
                ax.hist(df['weight'], bins=10, edgecolor='black', color='orange')
                ax.set_xlabel('Weight')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: green; text-align: center;">Weight Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)

                # Physical Activity Level Distribution
                fig, ax = plt.subplots()
                ax.hist(df['physical_activity_level'], bins=10, edgecolor='black', color='green')
                ax.set_xlabel('Physical Activity Level')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: blue; text-align: center;">Physical Activity Level Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                fig, ax = plt.subplots()
                ax.hist(df['stress_level'], bins=10, edgecolor='black', color='red')
                ax.set_xlabel('Stress Level')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: magenta; text-align: center;">Stress Level Distribution</h3>', unsafe_allow_html=True)    
                col2.pyplot(fig)
                col1,col2=st.columns(2)
                fig, ax = plt.subplots()
                ax.hist(df['heart_rate'], bins=10, edgecolor='black', color='cyan')
                ax.set_xlabel('Heart Rate')
                ax.set_ylabel('Frequency')
                col1.markdown(f'<h3 style="color: yellow; text-align: center;">Heart Rate Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                fig, ax = plt.subplots()
                ax.hist(df['daily_steps'], bins=10, edgecolor='black', color='magenta')
                ax.set_xlabel('Daily Steps')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: orange; text-align: center;">Daily Steps Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)

                fig, ax = plt.subplots()
                ax.bar(unique_times, counts, color=colors)
                ax.set_xlabel('Usage Time (hours)')
                ax.set_ylabel('Frequency')
                ax.tick_params(axis='x', rotation=45)
                col1.markdown(f'<h3 style="color: green; text-align: center;">Smartphone Usage Time Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                # Plotting Drinking Water (liters)
                fig, ax = plt.subplots()
                ax.hist(df['drinking_water'], bins=10, edgecolor='black')
                ax.set_xlabel('Drinking Water Intake (liters)')
                ax.set_ylabel('Frequency')
                col2.markdown(f'<h3 style="color: red; text-align: center;">Drinking Water Intake Distribution</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
                col1,col2=st.columns(2)
                bmi_plot = df['BMI_category'].value_counts().plot(kind='bar', color=['#FF9999', '#66B2FF'], figsize=(6, 4))
                col1.markdown(f'<h3 style="color: blue; text-align: center;">BMI Category Distribution</h3>', unsafe_allow_html=True)
                col1.pyplot(bmi_plot.figure)

                fig = plt.figure(figsize=(6, 4))
                sns.scatterplot(x=df['weight'], y=df['heart_rate'], hue=df['BMI_category'], palette='viridis')
                col2.markdown(f'<h3 style="color: yellow; text-align: center;">Weight vs Heart Rate</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
                col1, col2 = st.columns(2)

                line_chart = pd.DataFrame({
                    'Daily Steps': df['daily_steps'],
                    'Calories Burned': df['calories_burned']
                })
                col1.markdown(f'<h3 style="color: maroon; text-align: center;">Daily Steps vs Calories Burned</h3>', unsafe_allow_html=True)  
                col1.line_chart(line_chart)

                fig = plt.figure(figsize=(6, 4))
                col2.markdown(f'<h3 style="color: green; text-align: center;">Blood Pressure Distribution</h3>', unsafe_allow_html=True)
                sns.histplot(df['blood_pressure'], kde=True, color='purple')
                col2.pyplot(fig)
                categories = ['sleep_duration', 'quality_of_sleep', 'stress_level', 'blood_pressure', 'heart_rate']
                values = df[categories].iloc[0].values.tolist()
                col1, col2=st.columns(2)
                # Append the first value to the end of the list to close the radar chart
                values += values[:1]

                # Append an empty string to categories to match the number of angles and values
                categories += [categories[0]]

                # Calculate the angles for the radar chart
                angles = [n / float(len(values)) * 2 * 3.14 for n in range(len(values))]

                        # Create the radar chart
                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, polar=True)

                # Set the angle for the first category at the top
                ax.set_theta_offset(3.14 / 2)
                ax.set_theta_direction(-1)

                # Set the limits for the radial axis
                ax.set_ylim(0, 10)

                # Plot the data on the radar chart
                ax.plot(angles, values, color='blue', linewidth=2, linestyle='solid')

                # Fill the area under the curve
                ax.fill(angles, values, color='blue', alpha=0.4)

                # Set the labels for the categories
                ax.set_xticks(angles)
                ax.set_xticklabels(categories)

                # Display the plot
                col1.markdown(f'<h3 style="color: red; text-align: center;">Health Radar Chart</h3>', unsafe_allow_html=True)
                col1.pyplot(fig)

                numerical_columns = ['weight', 'sleep_duration', 'quality_of_sleep', 'physical_activity_level', 'stress_level', 
                        'blood_pressure', 'heart_rate', 'daily_steps', 'respiratory_rate', 'blood_volume', 
                        'calories_burned', 'body_temperature', 'drinking_water', 'daily_usage_of_smart_phone']

                # Compute the correlation matrix
                correlation_matrix = df[numerical_columns].corr()

                # Generate the heatmap
                fig = plt.figure(figsize=(10, 8))
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
                col2.markdown(f'<h3 style="color: blue; text-align: center;">Correlation Matrix</h3>', unsafe_allow_html=True)
                col2.pyplot(fig)
        else:
            st.error("No data available for analytics.")    
    elif select == 'Statistics':

        alerts=0
        st.markdown("<h1 style='text-align: center; color: #d65804;'>Statistics of User</h1>", unsafe_allow_html=True)
        try:
            
            daily_data = fetch_all_daily(user[2])
            daily_data_df = pd.DataFrame(daily_data)
            if daily_data_df.empty:
                st.error("No data available for statistics.")
            else:
                columns = ['ID','mail', 'weight', 'sleep_duration', 'quality_of_sleep',
                            'physical_activity_level', 'stress_level', 'BMI_category', 'blood_pressure', 'heart_rate',
                            'daily_steps', 'respiratory_rate', 'blood_volume', 'calories_burned', 'body_temperature',
                            'drinking_water', 'daily_usage_of_smart_phone']
                    #make a dataframe with column names

                daily_data_df.columns=columns
                df=daily_data_df.drop(['ID','mail'],axis=1)
                st.write(df)
                weight_diff = df['weight'].diff()
                if max(diff < 0 for diff in weight_diff):
                    st.error("Alert: Weight is gradually decreasing!")
                    alerts+=1
                    st.divider()
                # If all differences are positive, weight is increasing
                elif max(diff > 0 for diff in weight_diff):
                    st.error("Alert: Weight is gradually increasing!")
                    alerts+=1
                    st.divider()
                duration_diff = df['sleep_duration'].diff()
                # If all differences are negative, sleep duration is decreasing
                if max(diff < 0 for diff in duration_diff):
                    st.error("Alert: Sleep duration is decreasing. Consider regulating sleep for 6 hours regularly.")
                    alerts+=1
                    st.divider()
                quality_diff = df['quality_of_sleep'].diff()
                    # If all differences are negative, quality of sleep is decreasing
                if max(diff < 0 for diff in quality_diff):
                    st.error("Alert: Quality of sleep is consistently decreasing. Consider consulting a healthcare professional.")
                    alerts+=1
                    st.success("Suggestion: Keep a consistent sleep schedule, create a relaxing bedtime routine, and avoid caffeine and electronics before bed.")
                    st.divider()
                activity_diff = df['physical_activity_level'].diff()
                    # If all differences are negative, physical activity level is decreasing
                if max(diff < 0 for diff in activity_diff):
                    st.error("Alert: Physical activity level is consistently decreasing. Consider incorporating more exercise into your routine.")
                    alerts+=1
                    st.success("Suggestion: Aim for at least 150 minutes of moderate-intensity aerobic activity or 75 minutes of vigorous-intensity activity per week, along with muscle-strengthening activities on two or more days per week.")
                    st.divider()
                stress_diff = df['stress_level'].diff()
                    # If all differences are positive, stress level is consistently increasing
                if max(diff > 0 for diff in stress_diff):
                    st.error("Alert: Stress level is consistently increasing. It's important to take steps to manage stress.")
                    alerts+=1
                    st.success("Suggestion: Practice stress-reduction techniques such as deep breathing, meditation, exercise, and maintaining a healthy lifestyle. Consider seeking support from a therapist or counselor if needed.")
                    st.divider()
                systolic_diff = df['blood_pressure'].diff()
                if max(diff > 0 for diff in systolic_diff):
                    alerts+=1
                    st.error("Alert: Blood pressure is consistently increasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                    st.success("Suggestion: Implement lifestyle changes such as reducing sodium intake, increasing physical activity, maintaining a healthy weight, and managing stress.")
                    st.divider()
                # If all differences are negative for systolic and diastolic, blood pressure is consistently decreasing
                elif max(diff < 0 for diff in systolic_diff):
                    alerts+=1
                    st.error("Alert: Blood pressure is consistently decreasing. Monitor your blood pressure regularly and consider consulting a healthcare professional.")
                    st.success("Suggestion: Monitor your blood pressure closely and consult with a healthcare provider to ensure it's within a healthy range.")
                    st.divider()
                rate_diff = df['heart_rate'].diff()
                # If all differences are negative, heart rate is consistently decreasing
                if max(diff < 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Heart rate is consistently decreasing. Monitor your heart rate and consider consulting a healthcare professional.")
                    st.success("Suggestion: Focus on cardiovascular exercises, maintain a healthy diet, and manage stress levels to improve heart health.")
                    st.divider()
                # If all differences are positive, heart rate is consistently increasing
                elif max(diff > 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Heart rate is consistently increasing. Monitor your heart rate and consider consulting a healthcare professional.")
                    st.success("Suggestion: Check for factors such as physical exertion, stress, or caffeine intake that might be causing the increase. Consider consulting with a healthcare provider for further evaluation.")
                    st.divider()
                if df['daily_steps'].sum() == 0:
                    alerts+=1
                    st.error("Alert: No steps recorded. It's important to stay active throughout the day.")
                    st.success("Suggestion: Aim to incorporate physical activity into your daily routine. Start with small, achievable goals and gradually increase your activity level.")
                    st.divider()
                # If steps are consistently decreasing
                elif len(df) >= 2:
                    decreasing=all(df['daily_steps'].iloc[i] >= df['daily_steps'].iloc[i + 1] for i in range(len(df) - 1))
                    if decreasing:
                        alerts+=1
                        st.error("Alert: Daily steps are consistently decreasing. It's important to maintain physical activity levels.")
                        st.success("Suggestion: Find activities you enjoy and set specific goals to increase your daily step count. Consider walking meetings, taking the stairs, or going for a walk during breaks.")
                        st.divider()               
                    else:
                        alerts+=1
                        st.error("Alert: Daily steps are not consistently maintained. It's important to strive for regular physical activity.")
                        st.success("Suggestion: Set a daily step goal and track your progress using a pedometer or smartphone app. Try to incorporate walking into your daily routine, such as walking instead of driving for short trips.")
                        st.divider()
                else:
                    st.info("Not enough data to analyze trends yet. Keep updating daily!")
                rate_diff = df['respiratory_rate'].diff()
                # If all differences are negative, respiration rate is consistently decreasing
                if max(diff < 0 for diff in rate_diff):
                    alerts+=1
                    st.error("Alert: Respiration rate is consistently decreasing. Monitor your respiratory health and consider consulting a healthcare professional.")
                    st.success("Suggestion: Practice deep breathing exercises, maintain good posture, and ensure proper hydration and ventilation in your environment.")
                    st.divider()
                avg_blood_volume = df['blood_volume'].mean()
                # Define thresholds for low and high blood volume levels
                low_threshold = avg_blood_volume * 0.9
                high_threshold = avg_blood_volume * 1.1
                # Check blood volume levels and provide recommendations
                if df['blood_volume'].min() < low_threshold:
                    alerts+=1
                    st.error("Alert: Blood volume is low. Consult with a healthcare professional for further evaluation.")
                    st.success("Suggestion: Ensure adequate hydration and consider consuming iron-rich foods to support healthy blood volume levels.")
                    st.divider()
                avg_calories_burned = df['calories_burned'].mean()
                # Define thresholds for low and high calories burned levels
                low_threshold = avg_calories_burned * 0.9
                high_threshold = avg_calories_burned * 1.1

                # Check calories burned levels and provide recommendations
                if df['calories_burned'].min() < low_threshold:
                    alerts+=1
                    st.error("Alert: Calories burned are low. Consider increasing physical activity.")
                    st.success("Suggestion: Incorporate more exercise into your routine, such as brisk walking, jogging, or cycling. Set achievable goals and track your progress.")
                    st.divider()
                elif df['calories_burned'].max() > high_threshold:
                    alerts+=1
                    st.error("Alert: Calories burned are high. Ensure a balanced approach to exercise and nutrition.")
                    st.success("Suggestion: Maintain a well-rounded diet with plenty of fruits, vegetables, lean proteins, and whole grains. Avoid overexertion and ensure adequate rest and recovery.")
                    st.divider()
                normal_low = 35.0
                normal_high = 38.0
                # Check if any temperature readings are outside the normal range
                if max(temp < normal_low or temp > normal_high for temp in df['body_temperature']):
                    alerts+=1
                    st.error("Alert: Body temperature is outside the normal range.")
                    st.success("Suggestion: If you have a fever (temperature above 100.4°F or 38°C), consult a healthcare professional. Otherwise, monitor your temperature and consider rest and hydration if you feel unwell.")
                    st.divider()
                # Define recommended water intake levels
                recommended_low = 2.0  # liters
                recommended_high = 4  # liters
                # Check if any water intake readings are below the recommended range
                if max(water < recommended_low for water in df['drinking_water']):
                    alerts+=1
                    st.error("Alert: Drinking water intake is below the recommended range.")
                    st.success("Suggestion: Increase your water intake to ensure proper hydration. Aim to drink at least 8 glasses (approximately 2 liters) of water per day.")
                    st.divider()
                # Define recommended smartphone usage range
                recommended_low = 2  # hours (minimum)
                recommended_high = 8  # hours (maximum for healthy usage)
                # Check if any usage time readings are above the recommended maximum
                if max(usage > recommended_high for usage in df['daily_usage_of_smart_phone']):
                    alerts+=1
                    st.error("Alert: Daily usage time of smartphone is above the recommended range.")
                    st.success("Suggestion: Limit screen time and take breaks from smartphone use. Consider setting usage limits or using apps that track and manage screen time.")
                    st.divider()
                # ✅ Final Risk Result Based on Alerts
                if alerts <= 3:
                    st.markdown('<h1 style="color: green; text-align: center;">🟢 Low Risk — Stay Healthy!</h1>', unsafe_allow_html=True)
                elif alerts <= 7:
                    st.markdown('<h1 style="color: orange; text-align: center;">🟠 Moderate Risk — Keep Monitoring</h1>', unsafe_allow_html=True)
                else:
                    st.markdown('<h1 style="color: red; text-align: center;">🔴 High Risk — Please Consult a Doctor</h1>', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    col2.image("https://png.pngtree.com/png-clipart/20230816/original/pngtree-doctor-consultation-icon-visit-vector-consultation-vector-picture-image_10832751.png", use_column_width=True)

                try:
                    gender = user[3] if isinstance(user[3], str) else 'Male'
                    age = user[4] if isinstance(user[4], (int, float)) else 22
                    df.columns = ['weight', 'sleep_duration', 'quality_of_sleep',
                        'physical_activity_level', 'stress_level', 'BMI_category',
                        'blood_pressure', 'heart_rate', 'daily_steps', 'respiratory_rate',
                        'blood_volume', 'calories_burned', 'body_temperature',
                        'drinking_water', 'daily_usage_of_smart_phone']
                    df_kmeans = df.copy()
                    df_kmeans['Gender'] = 1 if gender.lower().startswith('female') else 0
                    df_kmeans['Age'] = age
                    df_kmeans.rename(columns={
                        'weight': 'Weight',
                        'sleep_duration': 'Sleep Duration',
                        'quality_of_sleep': 'Quality of Sleep',
                        'physical_activity_level': 'Physical Activity Level',
                        'stress_level': 'Stress Level',
                        'BMI_category': 'BMI Category',
                        'blood_pressure': 'Blood Pressure',
                        'heart_rate': 'Heart Rate',
                        'daily_steps': 'Daily Steps',
                        'respiratory_rate': 'Respiration Rate',
                        'blood_volume': 'Blood Volume',
                        'body_temperature': 'Body Temperature',
                        'drinking_water': 'Drinking Water (lts)',
                        'daily_usage_of_smart_phone': 'Daily Usage Time of Smart Phone'
                    }, inplace=True)

                    # Step 4: Encode 'BMI Category'
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    df_kmeans['BMI Category'] = le.fit_transform(df_kmeans['BMI Category'])

                    # Step 5: Arrange columns in exact training order
                    prediction_features = [
                        'Gender', 'Age', 'Weight', 'Sleep Duration', 'Quality of Sleep',
                        'Physical Activity Level', 'Stress Level', 'BMI Category', 'Heart Rate',
                        'Daily Steps', 'Respiration Rate', 'Blood Volume', 'Body Temperature',
                        'Drinking Water (lts)', 'Daily Usage Time of Smart Phone'
                    ]

                    # Step 6: Predict risk cluster
                    prediction_input = df_kmeans[prediction_features]

                except Exception as e:
                        st.warning(f"⚠️ Something went wrong while predicting risk cluster: {e}")                

                

        except Exception as e:
            st.info('Only few data points available for statistics. Try again Tomorrow 📆')
            st.write(e)
    elif select == 'Logout': 
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        save_login_status(False, None)
        st.success("Logged Out!")
        st.switch_page("pages/3_🔐_Login.py")

user_home_page()