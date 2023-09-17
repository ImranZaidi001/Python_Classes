import pyaudio
import wave
import os
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame

# Constants for audio recording
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
OUTPUT_FILENAME = "SpeechToSpeechBYImranHaider.wav"

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream for recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record audio
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording done.")

# Stop and close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio to a WAV file
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

# Speech recognition using the Google Web Speech API
recognizer = sr.Recognizer()
with sr.AudioFile(OUTPUT_FILENAME) as source:
    audio_data = recognizer.record(source)
    try:
        # Use the Google Web Speech API for speech recognition
        text = recognizer.recognize_google(audio_data)
        print("Recognized text:", text)
        
        # Translate the recognized text (for example, from English to Spanish)
        translator = Translator()
        translated_text = translator.translate(text, src='en', dest='ur').text
        print("Translated text:", translated_text)
        
        # Generate text-to-speech output in the translated language
        tts = gTTS(text=translated_text, lang='ur')
        tts.save("SpeechToSpeech_output.mp3")
        
        # Play the generated audio
        pygame.mixer.init()
        pygame.mixer.music.load("SpeechToSpeech_output.mp3")
        pygame.mixer.music.play()
        pygame.mixer.music.wait()
        
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")

# Clean up: Remove the temporary WAV file
os.remove(OUTPUT_FILENAME)
