import streamlit as st
from core.speech_to_text import recognize_speech_to_text

# st.set_page_config('Analysis Report', layout="wide")
st.title('Analysis Report')

file_name = st.session_state['stream_ended_and_file_saved']

# Performinng TTS, 
section_1, section_2 = st.columns([3, 1])


with section_1.container(height=700):
    with st.spinner('Transcribing Audio, it would take few minutes.'):
        result = recognize_speech_to_text(str(file_name))
        st.success('Transcription Completed', icon='🗒️')
        for i, segment in enumerate(result['segments']):
            start, end = segment['start'], segment['end']
            st.markdown(
                f":blue[00:00:{str(int(start)).replace('.', ',')} --> 00:00:{str(int(end)).replace('.', ',')}] *{segment['text'].strip()}*", unsafe_allow_html=True)
            # st.markdown(">" + segment['text'].strip())
            st.divider()

        ...

with section_2:
    st.write('hello')