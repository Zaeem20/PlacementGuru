from click import option
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import google.generativeai as genai

st.set_page_config(page_title='PlacementGuru', layout='wide')


st.title('Placement Guru')
col1, col2 = st.columns(2)
with col1:
    sec1,sec2 = st.columns(2)
    with sec1:
        st.text_input('Role', placeholder='What role your are seeking for!')
        st.selectbox('Company', options=('', 'Google', 'Meta', 'Wipro', 'Accenture'))
    with sec2:
        st.selectbox('Interviewer', options = ('Professional', 'Technical', 'Behaviour'))

with col2:
    webrtc_streamer('record interview') 