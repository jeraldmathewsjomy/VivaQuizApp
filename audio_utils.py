from gtts import gTTS
import speech_recognition as sr
import os
from playsound import playsound

def text_to_speech(text, lang='en'):
    print(f"Generating speech for: {text}")  # Debugging: Log the text
    tts = gTTS(text=text, lang=lang)
    tts.save("temp_audio.mp3")
    playsound("temp_audio.mp3")
    os.remove("temp_audio.mp3")

def speech_to_text(timeout=5, retries=3):
    print("Starting speech recognition...")  # Debugging: Log the start of recognition
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        for attempt in range(retries):
            try:
                print(f"Attempt {attempt + 1}: Listening for {timeout} seconds...")
                audio = recognizer.listen(source, timeout=timeout)  # Set a timeout
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text
                except sr.UnknownValueError:
                    print("Sorry, I did not understand that.")
                    if attempt < retries - 1:  # Fixed: Removed extra space in "retries"
                        print("Retrying...")
                        timeout += 2  # Increase timeout by 2 seconds for the next attempt
                        continue
                    else:
                        print("Maximum retries reached.")
                        return None
                except sr.RequestError as e:
                    print(f"Sorry, the service is down. Error: {e}")
                    return None
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
                if attempt < retries - 1:  # Fixed: Removed extra space in "retries"
                    print("Retrying...")
                    timeout += 2  # Increase timeout by 2 seconds for the next attempt
                    continue
                else:
                    print("Maximum retries reached.")
                    return None
    return None