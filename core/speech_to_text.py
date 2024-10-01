import speech_recognition as sr

def recognize_speech_to_text(file_path: str):
    recognizer = sr.Recognizer()
    with  sr.AudioFile(file_path) as source:
        recognizer.adjust_for_ambient_noise(source=source, duration=1)
        audio = recognizer.record(source)

        prediction = recognizer.recognize_whisper(audio, model='medium.en', show_dict=True)
        # predicted_text=recognizer.recognize_google(audio)
        return prediction