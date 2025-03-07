import streamlit as st
import time

# Set page layout
st.set_page_config(page_title="PlacementGuru", layout="wide",page_icon="🧊")

# CSS for styling
st.markdown("""
    <style>
        .container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 5% 10%;
        }
        .text-box {
            font-size: 28px;
            font-weight: bold;
            color: white;
        }
        .image-box  {
            margin-top: 100px;
            width: 100%;
            border-radius: 20px;
            box-shadow: 2px 2px 15px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Layout with two columns
col1, col2 = st.columns([1, 1])


with col1:
    st.markdown(
            """
            <h1 style='font-size: 40px; font-weight: bold;'>Welcome to PlacementGuru! 🚀</h1>
            <p style='font-size: 22px;'>Your AI-driven Interview Preparation Partner.</p>
            <br>
            <h2>How this Works</h2>
            <p>Step 1: Setup your microphone and camera. Then Click on start.</p>
            <p>Step 2: Fill the details of the Form. Click Submit.</p>
            <p>Step 3: Your interview will start. After completing all the questions click stop to submit your stream.</p>
            <i></i>
            <br>
            """,
            unsafe_allow_html=True
        )
    if st.button("Let's get started"):
        st.switch_page("pages/Interview.py")

    st.markdown(
            """
            <br>
            <i>If you are encountering any problem or you have any suggestions, feel free to contact us by sharing your thoughts.<i>
            """,
            unsafe_allow_html=True
        )

# Image on the right
with col2:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image("./assets/interview.jpg", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
