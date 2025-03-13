import speech_recognition as sr
from gtts import gTTS
import os
import playsound

def text_to_speech(text):
    """Convert text to speech and play it."""
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp_audio.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
    except Exception as e:
        print(f"Text-to-Speech Error: {e}")

def speech_to_text():
    """Convert spoken audio to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"Recognized Speech: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition request failed: {e}")
            return None
        

