from speech_utils import text_to_speech, speech_to_text

print("🔹 Testing text-to-speech...")
text_to_speech("Hello! This is a test.")

print("🔹 Testing speech-to-text...")
recognized_text = speech_to_text()
print(f"✅ Recognized Speech: {recognized_text}")
