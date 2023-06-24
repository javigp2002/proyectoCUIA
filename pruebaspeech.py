from SpeechRecognitionJavi import MySpeechRecognition
import speech_recognition as sr
import pyttsx3
import IPython.display as ipd
from playsound import playsound
import os
import SpeechRecognitionJavi

mySpeechRecognition = MySpeechRecognition()

mySpeechRecognition.textToSpeech(
    SpeechRecognitionJavi.wikipediaSearch("Templo de Saturno")
)

playsound("audio.wav")
#da un exception al cerrarlo pero no corta la ejecucion