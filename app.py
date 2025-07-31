import streamlit as st

# Page setup
st.set_page_config(
    page_title="Healthcare Application",
    page_icon="🩺",
    layout="wide"
)

# Hide sidebar, main menu, footer, etc.
st.markdown(
    """
    <style>
    /* Hide sidebar, header, footer */
    [data-testid="stSidebar"], header, footer {
        display: none !important;
    }

    /* Fullscreen background on main content */
    html, body, [data-testid="stAppViewContainer"] {
        height: 100vh;
        overflow: hidden;
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-vector/medical-banner-with-healthcare-icons_1017-26805.jpg?t=st=1719986881~exp=1719990481~hmac=ee74b68294d95d85742d91e08407b5e6ad5278d3912b96b12922828db62a37f0&w=996");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }

    /* Center all columns vertically */
    .block-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100vh;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Page content
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(
        """
        <div style="text-align: center; padding: 1px;margin-top:60px; background-color: #b3a2a2;font-weight:bold; border: 2px solid black;">
            <p style="color: black; font-size: 32px;"><b>Health Prediction Based On Daily Life Activity</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://cdn4.iconfinder.com/data/icons/medical-and-healthcare-pasteline-series/64/Preventive_Healthcare-512.png"
                 alt="Health" width="350" height="350">
        </div>
        """,
        unsafe_allow_html=True
    )

    col_login, col_signup = st.columns([18,4])
    with col_login:
        if st.button("Login", type="primary"):
            st.switch_page("pages/3_🔐_Login.py")

    with col_signup:
        if st.button("Sign Up", type="primary"):
            st.switch_page("pages/2_👤_Signup.py")
