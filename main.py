import streamlit as st
from streamlit_webrtc import webrtc_streamer
import google.generativeai as genai

st.set_page_config(page_title='PlacementGuru', layout='wide')



st.write('Hello world')
webrtc_streamer('record interview') 