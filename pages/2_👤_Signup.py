import streamlit as st
from database import add_user
import re

st.set_page_config(page_title="Signup", layout="wide")

# ✅ Styling
st.markdown("""
    <style>
    [data-testid="stSidebar"], header, footer {
        display: none !important;
    }
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden;
    }
    [data-testid="stAppViewContainer"]{
        background-image: url("https://img.freepik.com/free-vector/medical-banner-with-healthcare-icons_1017-26805.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    .block-container {
        padding: 2rem 3rem;
        border-radius: 20px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ✅ Email validator
def validate_mail(mail):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail)

# ✅ Signup Form
with st.form(key="signup_form"):
    st.markdown("### 👤 Sign Up Here", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    name = col1.text_input("Name")
    email = col2.text_input("Email")

    col1, col2 = st.columns(2)
    age = col1.slider("Age", 1, 100, 18)
    gender = col2.selectbox("Gender", ["Male👦🏻", "Female👩🏻", "Others"])

    col1, col2 = st.columns(2)
    disease = col1.selectbox("Disease", ["Lung", "Heart", "Diabetes", "Eye", "Kidney", "Brain", "Muscle", "Skin", "Migraine", "Blood Cancer", "Breast Cancer", "Others", "None"])
    occupation = col2.selectbox("Occupation", ["Student", "Doctor", "Engineer", "Teacher", "Businessman", "Others"])

    col1, col2 = st.columns(2)
    password = col1.text_input("Create Password", type="password")
    confirm = col2.text_input("Retype Password", type="password")

    col1, col2 = st.columns([2,1])
    signup_btn = col1.form_submit_button("🔏 Sign Up", type="primary")
    home_btn = col2.form_submit_button("🏠 Go to Home", type="primary")

    if signup_btn:
        if not validate_mail(email):
            st.error("❌ Invalid email format")
        elif len(password) < 6:
            st.error("❌ Password must be at least 6 characters")
        elif password != confirm:
            st.error("❌ Passwords do not match")
        elif not all([name, email, age, gender, disease, occupation]):
            st.error("❌ Please fill all fields")
        else:
            try:
                add_user(name, email, age, gender, disease, occupation, password)
                st.success("✅ Account created!Please login.")
                st.switch_page("pages/3_🔐_Login.py")

                # ✅ SET session state so that login state is preserved
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = email

            except Exception as e:
                st.error(f"Error: {e}")

    if home_btn:
        st.switch_page("app.py")
