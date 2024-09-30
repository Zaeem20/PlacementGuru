from click import option
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import google.generativeai as genai
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import pprint

load_dotenv()
genai.configure(api_key = os.environ["gemini"])
def search_on_gemini(role, company, interviewer_type):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        f"You are interviewer and you are interviewing a candidate for '{role} and diffculty level is {difficulty_level}' "
        f"interview at {company} with a {interviewer_type} interviewer and what kind of {company_type} he is selecting . list 4 interview related questions don't add unnecessary information."
    )
    response = model.generate_content(prompt)
    results = response.text.strip().split("\n")
    return results if results else ["No results found. Please try again."]

st.set_page_config(page_title='PlacementGuru', layout='wide')

st.title('Placement Guru')

# Columns for input
col1, col2 = st.columns(2)

with col1:
    role = st.text_input('Role', placeholder='What role are you seeking for!')
    sec1, sec2 = st.columns(2)
    with sec1:
        company = st.selectbox('Company', options=('Google', 'Meta', 'Wipro', 'Accenture', 'Other'))
    with sec2:
        interviewer_type = st.selectbox('Interviewer', options=('Professional', 'Technical', 'Behaviour','Friendly'))
    

col3,col4 = st.columns(2)

with col3:
    sec3,sec4 = st.columns(2)
    with sec3:
     difficulty_level = st.selectbox('Difficulty',options=('Beginner','Intermediate','Expert'))
    with sec4:
        company_type = st.text_input("Company Type")
# WebRTC stream for recording interviews
with st.container(height=50):
    with col2:
        webrtc_streamer('record interview')

with st.sidebar.container():
    st.page_link("main.py",label="Home")
    st.page_link("pages\\about.py",label="About")
    st.page_link("pages\\contact.py",label="Contact")
    st.page_link("pages\\result.py",label="Result")

# Create a button for search functionality
if st.button("Search"):
    if role:
        # Call the search function with user input
        results = search_on_gemini(role, company, interviewer_type)
        # Display the results
        # st.container(border=True,height=300)  
        for result in results:
            st.write(result)
          # End of result container
    else:
        st.warning("Please enter a role to search.")