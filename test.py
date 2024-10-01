import streamlit as st
import time

# Define the exam levels and their corresponding questions
exam_levels = {
    'Beginner': [
        {'text': 'What is the capital of France?', 'options': ['Paris', 'London', 'Berlin']},
        {'text': 'What is the largest planet in our solar system?', 'options': ['Earth', 'Saturn', 'Jupiter']}
    ],
    'Intermediate': [
        {'text': 'What is the process of converting plaintext into ciphertext?', 'options': ['Encryption', 'Decryption', 'Hashing']},
        {'text': 'What is the most popular programming language in the world?', 'options': ['Python', 'Java', 'C++']}
    ],
    'Expert': [
        {'text': 'What is the concept of dependency injection in software development?', 'options': ['Loose Coupling', 'Tight Coupling', 'Inheritance']},
        {'text': 'What is the difference between monolithic architecture and microservices architecture?', 'options': ['Scalability', 'Flexibility', 'Security']}
    ]
}

# Define the time limits for each exam level
time_limits = {
    'Beginner': 30,  # 30 minutes
    'Intermediate': 45,  # 45 minutes
    'Expert': 60  # 60 minutes
}

# Create a Streamlit app
st.title("Aptitude Test Page")
st.header("Choose Your Exam Level:")

# Create a dropdown menu to select the exam level
exam_level = st.selectbox("Select your exam level:", ['Beginner', 'Intermediate', 'Expert'])

# Create a button to start the exam
start_exam_button = st.button("Start Exam")

if start_exam_button:
    # Start the exam
    st.header("Exam Started!")
    st.write(f"Time remaining: {time_limits[exam_level]} minutes")

    # Create a timer
    timer = time.time() + time_limits[exam_level] * 60

    # Display the questions
    for question in exam_levels[exam_level]:
        st.write(question['text'])
        options = st.radio("Select an option:", question['options'])
        st.write("")  # Add a blank line between questions

    # Calculate the score
    score = 0
    for question in exam_levels[exam_level]:
        # Check if the user answered correctly
        if st.session_state[question['text']] == question['options'][0]:
            score += 1

    # Display the score
    st.header("Exam Finished!")
    st.write(f"Your score: {score}/{len(exam_levels[exam_level])}")

    # Stop the timer
    st.write(f"Time taken: {time.time() - timer:.2f} seconds")