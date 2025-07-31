import streamlit as st

# Navigation function
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()
def home_page():
    #add info about the eye disease detection system in the sidebar
    st.markdown(
    """
    <style>
    html, body,[data-testid="stAppViewContainer"]{
    overflow: hidden !important;
        height: 100vh !important;
        background-image: url("https://img.freepik.com/free-vector/healthcare-blue-banner-with-doctor_1017-26807.jpg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
     .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        overflow: hidden !important;
        height: 100vh !important;
    }

    ::-webkit-scrollbar {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    col1,col2,col3 = st.columns([1,3,1])
    col2.markdown(
        """
        <div style="text-align: center; padding: 3px; background-color: #b3a2a2 ; border: 2px solid black;">
            <p style="color: black; font-size: 30px;"><b>Health Prediction Based On Daily Life Activity</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    #add image
    st.write("")
    st.write("")
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://cdn4.iconfinder.com/data/icons/medical-and-healthcare-pasteline-series/64/Preventive_Healthcare-512.png" alt="Health" width="400" height="350">
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1.5, 2, 2])
    with col2:
        if st.button("Login",type="primary"):
            navigate_to_page("login")
    with col3:
        if st.button("Sign Up",type="primary"):
            navigate_to_page("signup")
