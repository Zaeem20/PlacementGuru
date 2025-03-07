import streamlit as st
from core.speech_to_text import recognize_speech_to_text
import google.generativeai as genai
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import re

st.set_page_config(page_icon="🧊")

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Set up the Streamlit app
st.title('Analysis Report')

if 'audio_file_path' not in st.session_state:
    st.error("No recording found! Please complete an interview first.")
    st.stop()

# File name for the audio to be transcribed
file_name = st.session_state['audio_file_path']


def get_gemini_suggestions(transcript):
    prompt = (
        f"Give me suggestions on how to avoid using filler words like from {transcript} 'you know' during a conversation in an interview in 5-6 lines."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if response else "No suggestions found."


# Transcribing Audio
section_1, section_2 = st.columns([2, 1])

with section_1.container(height=500):
    with st.spinner('Transcribing Audio, it would take a few minutes.'):
        result = recognize_speech_to_text(str(file_name))
        st.success('Transcription Completed', icon='🗒️')
        st.write(result['text'])

        def check_filler_words(transcript):
            filler_words = ["um", "uh", "you know", "like", "so", "actually", "basically", "I mean"]
            filler_count = 0

            # Count filler words even within sentences
            for filler in filler_words:
                count = len(re.findall(rf'\b{re.escape(filler)}\b', transcript, re.IGNORECASE))
                filler_count += count
                if count > 0:
                    st.write(f"Count of '{filler}': {count}")

            total_words = len(transcript.split())
            non_filler_count = total_words - filler_count
            filler_percentage = (filler_count / total_words * 100) if total_words > 0 else 0

            st.write(f"The total words in this transcript: {total_words}")
            st.write(f"The total filler count in this transcript: {filler_count}")
            st.write(f"The filler percentage in this transcript: {filler_percentage:.2f}%")
            st.write(f"The non-filler count in this transcript: {non_filler_count}")

            labels = ['Filler Words', 'Non-Filler Words']
            sizes = [filler_count, non_filler_count]
            colors = ['#ff9999', '#66b3ff']

            fig, ax = plt.subplots(figsize=(5, 3))
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            plt.title("Filler vs Non-Filler Words", color='white')
            st.pyplot(fig)

        if "text" in result:
            check_filler_words(result["text"])
        else:
            st.write("Error: Transcription text not found.")


with section_2.container(height=500):
    suggestions = get_gemini_suggestions(result['text'])
    st.write("### Suggestions to Avoid Filler Words:")
    st.write(suggestions)
