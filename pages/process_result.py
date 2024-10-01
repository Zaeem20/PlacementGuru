import streamlit as st
from core.speech_to_text import recognize_speech_to_text
import google.generativeai as genai
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["gemini"])

# Set up the Streamlit app
st.title('Analysis Report')

# File name for the audio to be transcribed
file_name = st.session_state['stream_ended_and_file_saved']

# Define filler words
filler_words = ["um", "uh", "like", "you know", "so", "basically", "actually", "literally", "mhmm"]

def check_filler_words(transcript):
    transcript_lower = transcript.lower()  # Convert transcript to lowercase
    words = transcript_lower.split()  # Split the transcript into words
    total_words = len(words)  # Get total word count
    
    filler_count = {word: words.count(word) for word in filler_words if word in words}  # Count occurrences of filler words
    total_filler_words = sum(filler_count.values())  # Total filler word count
    
    # Calculate percentage of filler words
    filler_percentage = (total_filler_words / total_words) * 100 if total_words > 0 else 0
    return filler_count, total_words, filler_percentage, total_filler_words

def get_gemini_suggestions(transcript):
    prompt = (
        f"Give me suggestions on how to avoid using filler words like 'you know' during a conversation in an interview in 5-6 lines."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if response else "No suggestions found."

# Transcribing Audio
section_1, section_2 = st.columns([3, 1])

with section_1.container(height=700):
    with st.spinner('Transcribing Audio, it would take a few minutes.'):
        result = recognize_speech_to_text(str(file_name))
        st.success('Transcription Completed', icon='🗒️')

        # Collect all segments into a single transcript string
        transcript = ""
        for i, segment in enumerate(result['segments']):
            start, end = segment['start'], segment['end']
            segment_text = segment['text'].strip()
            st.markdown(f":blue[00:00:{str(int(start)).replace('.', ',')} --> 00:00:{str(int(end)).replace('.', ',')}] *{segment_text}*", unsafe_allow_html=True)
            st.divider()
            transcript += segment_text + " "  # Append the segment to the transcript

# Section 2 for Filler Words Analysis and Suggestions
with section_2:
    if transcript.strip():  # Check if transcript is not empty
        # Check for filler words and get statistics
        filler_count, total_words, filler_percentage, total_filler_words = check_filler_words(transcript)

        # Display pie chart for filler vs non-filler words
        non_filler_words = total_words - total_filler_words
        labels = ['Filler Words', 'Non-Filler Words']
        sizes = [total_filler_words, non_filler_words]
        colors = ['#ff9999', '#66b3ff']

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(5, 3))  # Smaller size
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.gca().set_facecolor('black')  # Set the background color to black
            plt.title("Filler vs Non-Filler Words", color='white')  # Title in white for contrast
            
            # Show pie chart in Streamlit
            st.pyplot(fig)

        # Display filler word analysis
        with col2:
            suggestions = get_gemini_suggestions(transcript)
            st.write("### Suggestions to Avoid Filler Words:")
            st.write(suggestions)

    else:
        st.warning("Please enter a transcript before checking.")
