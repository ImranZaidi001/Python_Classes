
from googletrans import Translator

from gtts import gTTS

import pygame

import pyaudio


english_text =input( "Enter text to translate\t= \t")

translator = Translator()

translated_text = translator.translate(english_text, src='en', dest='ur')

print("Translated text:", translated_text.text)

 

tts = gTTS(translated_text.text, lang='ur')

tts.save("TextToText&SpeechByImranHaider.mp3")

 

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("TextToText&SpeechByImranHaider.mp3")

pygame.mixer.music.play()

 

while pygame.mixer.music.get_busy():

    pygame.time.Clock().tick(10)