import speech_recognition as sr
import pyaudio
from playsound import playsound
import pyttsx3
import wikipedia

global nameBuilding

class MySpeechRecognition:
    rec = None
    mic = None
    palabraClave=''
    engine = None

    def __init__(self):
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.palabraClave = "información"
        self.engine = pyttsx3.init()
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')
        

    def escucha(self):
        with self.mic as source:
            self.rec.adjust_for_ambient_noise(source, duration=0.5)
            #timeout none para que no se corte la escucha
            audio = self.rec.listen(source, timeout=None)
            return audio

    #dado un audio quiero comprobar si se ha dicho una palabra concreta
    def speech_recognition(self, audio):
        if (audio == None):
            print("No se ha escuchado nada")

        try:
            audioEscuchado = self.rec.recognize_google(audio, language="es-ES")
        except sr.UnknownValueError:
            print("No se ha entendido nada")
            return False
        
        print ("audio:", audioEscuchado)
        if self.palabraClave in audioEscuchado:
            return True
        else:
            return False   
    
    def textToSpeech(self, text):
        self.engine.save_to_file(text , 'audio.wav')
        self.engine.runAndWait()       


def wikipediaSearch(name):
        wikipedia.set_lang("es")
        return wikipedia.summary(name, sentences=3)
        