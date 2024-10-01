import os, time
import streamlit as st
import json 
import google.generativeai as genai
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import moviepy.editor as me
import numpy as np                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
import pydub, av, uuid
from pathlib import Path
from core.speech_to_text import speak_text
from aiortc.contrib.media import MediaRecorder
from streamlit_webrtc import webrtc_streamer, WebRtcMode


load_dotenv()
genai.configure(api_key = os.environ["GEMINI_API_KEY"])
def search_on_gemini(role, company, interviewer_type):
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = json.load(open("prompts\prompts.json"))
    response = model.generate_content(prompt.get('interviewer').format(role=role, difficulty_level=difficulty_level, company=company, interviewer_type=interviewer_type, company_type=company_type))

    results = json.loads(response.text)
    # st.write(results)
    return results


st.set_page_config(page_title='PlacementGuru', layout='wide')

st.title('Placement Guru')

# Base Path for Recordings
RECORD_DIR = Path("records")
RECORD_DIR.mkdir(exist_ok=True)


if "prefix" not in st.session_state:
    st.session_state["prefix"] = str(uuid.uuid4())
prefix = st.session_state["prefix"]
in_file = RECORD_DIR / f"{prefix}_input.mp4"

if "stream_ended_and_file_saved" not in st.session_state:
    st.session_state["stream_ended_and_file_saved"] = None


def convert_to_wav():
    ctx = st.session_state.get("Start Interview")
    state = ctx.state
    if ctx and not state.playing and not state.signalling:
        if in_file.exists():
            time.sleep(1)   # wait for the file to be written
            output_wav = RECORD_DIR / f"{prefix}_output.wav"
            try:
                video = me.VideoFileClip(str(in_file))
                video.audio.write_audiofile(str(output_wav), codec='pcm_s16le')
                st.success(f"Audio saved as {output_wav.name}")
                st.session_state['stream_ended_and_file_saved'] = output_wav
            except Exception as e:
                st.error(f"Error converting video to audio: {e}")
                st.session_state['stream_ended_and_file_saved'] = None


def in_recorder_factory() -> MediaRecorder:
    return MediaRecorder(str(in_file), format="mp4")

def process_audio(frame: av.AudioFrame) -> av.AudioFrame:
    raw_samples = frame.to_ndarray()
    sound = pydub.AudioSegment(
        data=raw_samples.tobytes(),
        sample_width=frame.format.bytes,
        frame_rate=frame.sample_rate,
        channels=len(frame.layout.channels),
    )

    sound = sound.apply_gain(gain)

    # Ref: https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentget_array_of_samples  # noqa
    channel_sounds = sound.split_to_mono()
    channel_samples = [s.get_array_of_samples() for s in channel_sounds]
    new_samples: np.ndarray = np.array(channel_samples).T
    new_samples = new_samples.reshape(raw_samples.shape)

    new_frame = av.AudioFrame.from_ndarray(new_samples, layout=frame.layout.name)
    new_frame.sample_rate = frame.sample_rate
    return new_frame




# Columns for input
col1, col2 = st.columns(2)

with col1.container(height=350):
    role = st.text_input('Role', placeholder='What role are you seeking for!')
    sec1, sec2 = st.columns(2)
    with sec1:
        company = st.selectbox('Company', options=('Google', 'Meta', 'Wipro', 'Accenture', 'Other'))
        difficulty_level = st.selectbox('Difficulty',options=('Beginner','Intermediate','Expert'))
        button_click = st.button("Search")
    with sec2:
        interviewer_type = st.selectbox('Interviewer', options=('Professional', 'Technical', 'Behaviour','Friendly'))
        company_type = st.text_input("Company Type")
    

# WebRTC stream for recording interviews
with col2.container(height=350):
    # if st.button('Next Question'):
    #     if st.session_state.get('pending_questions', None):
    #         try:
    #             speak_text(st.session_state['pending_questions'].pop())
    #         except StopIteration:
    #             speak_text("All Questions done")

    webstream=webrtc_streamer(
        key="Start Interview",
        mode=WebRtcMode.SENDRECV,
        media_stream_constraints={'video': {'width': 960, 'height': 440}, "audio": {
            "sampleRate": 16000,
            "sampleSize": 16,
            'echoCancellation': True,
            "noiseSuppression": True,
            "channelCount": 1}},
        on_change=convert_to_wav,
        audio_frame_callback=process_audio,
        in_recorder_factory=in_recorder_factory,
    )

    if st.session_state['stream_ended_and_file_saved']:
        st.switch_page('pages/process_result.py')


    gain = st.slider("Gain", -10.0, +20.0, 1.0, 0.05)



# st.sidebar.image('0')
with st.sidebar:
    st.page_link("main.py",label="Home")
    st.page_link("pages\\about.py",label="About")
    st.page_link("pages\\contact.py", label="Contact")
    st.page_link("pages\\result.py",label="Result")
    st.page_link("pages\\chat.py",label="Chat With our AI")
    st.page_link("pages\\roadmap.py",label="Roadmap")

# Create a button for search functionality
st.divider()
if button_click:
    with st.container(height=300):
        st.markdown("""
        <style>
            div.stSpinner > div{
            text-align:center;
            align-items: center;
            justify-content: center;
            }
        </style>""", unsafe_allow_html=True)

        with st.spinner(text='Generating Questions...', ):
            if role:
                # Call the search function with user input
                result = search_on_gemini(role, company, interviewer_type)
                st.session_state['interview_question'] = result['questions'].copy()
                st.session_state['pending_questions'] = st.session_state['interview_question'][::-1]

                # Display the results
                # st.container(border=True,height=300)
                st.subheader(result["topic-title"])
                for i in result['questions']:
                    st.markdown(f'-  **{i}**')

                    # End of result container
            else:
                st.warning("Please enter a role to search.")

