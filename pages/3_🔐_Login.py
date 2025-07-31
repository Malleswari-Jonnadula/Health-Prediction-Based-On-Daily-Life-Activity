import streamlit as st
import os
import json
from database import authenticate_user
import json
import os
def save_login_status(logged_in, current_user):
    with open("login_status.json", "w") as f:
        json.dump({"logged_in": logged_in, "current_user": current_user}, f)


st.set_page_config(page_title="Login", layout="wide")
if st.session_state.get("logged_in") and st.session_state.get("current_user"):
    st.switch_page("pages/4_🏥_User_Home.py")

# ✅ Styling - Background + Centered Form
st.markdown("""
    <style>
    [data-testid="stSidebar"], header, footer {
        display: none !important;
    }
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        background-image: url("https://img.freepik.com/free-vector/medical-banner-with-healthcare-icons_1017-26805.jpg");
        overflow: hidden;
    }

    [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        overflow: hidden;
        background-image: url("https://img.freepik.com/free-vector/medical-banner-with-healthcare-icons_1017-26805.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    .block-container {
        padding: 2rem 3rem;
        border-radius: 20px;
        max-width: 550px;
        margin: auto;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
    }
    .login-box {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 3rem 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
        width: 100%;
        max-width: 480px;
    }
    .login-title {
        font-size: 32px;
        font-weight: bold;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    </style>
""", unsafe_allow_html=True)


st.markdown('<div class="login-title">🔐 Login to Your Health Tracker</div>', unsafe_allow_html=True)
with st.form(key="login_form"):
    email = st.text_input("📧 Email", placeholder="Enter your email")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

    col1, col2 = st.columns([3,2])
    login_btn = col1.form_submit_button("🔓 Login", type="primary")
    signup_btn = col2.form_submit_button("👤 Create Account", type="primary")

    if login_btn:
        if authenticate_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = email
            save_login_status(True, email)
            st.success("✅ Login successful!")
            st.switch_page("pages/4_🏥_User_Home.py")  
        else:
            st.error("❌ Invalid email or password.")

    if signup_btn:
        st.switch_page("pages/2_👤_Signup.py")
st.markdown("</div>", unsafe_allow_html=True)
