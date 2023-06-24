import tkinter
import cv2
from PIL import Image, ImageTk
import imutils
import os
import numpy as np
import json
from building import Edificio
from detectFaces import DetectaCaras
import threading
import time
import SpeechRecognitionJavi
from SpeechRecognitionJavi import MySpeechRecognition
from playsound import playsound



#funciones
def detectaCaraYCambiaLabel(frame):
    myDetectFaces.detectarCaras(frame)

    if (myDetectFaces.haEncontrado == True):
        usuario.configure(text="Hola, " + myDetectFaces.nombreUsuario, fg=myDetectFaces.backGround)


#coger frame de la camara y mostrar en el frame de 600x700
def video_stream():
    global video

    video = cv2.VideoCapture(0)

    myBuilding.framew = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    myBuilding.frameh = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    myBuilding.extraerDatosNuevoEdificio()

    #t = threading.Thread(target=procesar_stream)
    #t.start()
    procesar_stream()

#procesar el frame de la camara cada 10 ms
def procesar_stream():
    global video
    #print ("hebra Procesar: ",threading.get_ident())

    ret, frame = video.read()
    if ret:
        copiaFrame = frame.copy()
        #LADO DERECHO (MENU)
        detectaCaraYCambiaLabel(copiaFrame)

        #LADO IZQUIERDO (FRAME PRINCIPAL)
        #requiere el mayor tiempo de ejecucion
        frame = myBuilding.cambiarFrame(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        #pasamos la imagen a formato tkinter
        image = ImageTk.PhotoImage(image=img)
        video_label.configure(image=image)
        video_label.image = image
        
        #llamamos a la funcion cada 10 milisegundos
        # para que se actualice el frame en la ventana (necesitamos le video) 
        video_label.after(10, procesar_stream)



def buscaInformacion():
    #print ("hebrainfo: ",threading.get_ident())
    while True:
        mySpeechRecognition = MySpeechRecognition()
        print("Diga 'Información' si desea información del monumento: ")

        # escuchamos hasta que diga alguien información
        audio = mySpeechRecognition.escucha()
        while not mySpeechRecognition.speech_recognition(audio):
            audio = mySpeechRecognition.escucha()
        
        print("Ha dicho información ", myBuilding.nombreEdificioWikipedia)
        # si ha dicho información, buscamos en wikipedia
        if myBuilding.nombreEdificioWikipedia != "":
            textoWikipedia = SpeechRecognitionJavi.wikipediaSearch(myBuilding.nombreEdificioWikipedia)
            print(textoWikipedia)
            mySpeechRecognition.textToSpeech(textoWikipedia)
            var.set(textoWikipedia)
            playsound("audio.wav")
        




#objetos
myBuilding = Edificio()
myDetectFaces = DetectaCaras()

#variables
ventana = tkinter.Tk()
video = None
bgTotal = "#414141"


#MAIN
#print ("hebra Main: ",threading.get_ident())

# crear una ventana dividida en dos partes con un menu a la derecha de 200x700 y un frame a la izquierda
ventana.title("Ventana")
ventana.geometry("840x480")
ventana.resizable(False, False)
ventana.configure(bg=bgTotal)

#Etiquetas

video_label = tkinter.Label(ventana, bg="black")
video_label.pack(side=tkinter.LEFT)

#Zona derecha
contenedor_menu = tkinter.Frame(ventana, bg=bgTotal, width=200, height=480)
contenedor_menu.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

    # Usuario
usuario = tkinter.Label(contenedor_menu,text="Usuario Desconocido", bg=bgTotal, fg="white", height="1", font=("Times New Roman", 15))
usuario.pack(side=tkinter.TOP)

#threading.Thread(target=video_stream()).start()
video_stream()

#Informacion
#text = tkinter.Message(contenedor_menu, height=16, width=20,bg=bgTotal, fg="white", font=("Times New Roman", 13))
var = tkinter.StringVar()
text = tkinter.Message(contenedor_menu, textvariable=var, relief=tkinter.RAISED, bg=bgTotal, fg="white", font=("Times New Roman", 13),
                       justify="center", width=200)
var.set("")
text.pack(side=tkinter.BOTTOM, fill=tkinter.X)

#necesidad de daemon para que no espere a que termine y finalice cuando el programa acabe
threading.Thread(target=buscaInformacion,name="t2",daemon = True).start()

ventana.mainloop()
