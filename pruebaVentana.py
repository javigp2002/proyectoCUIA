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

#funciones
myBuilding = Edificio()
myDetectFaces = DetectaCaras()

#coger frame de la camara y mostrar en el frame de 600x700
def video_stream():
    global video

    video = cv2.VideoCapture(0)

    myBuilding.framew = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    myBuilding.frameh = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    myBuilding.extraerDatosNuevoEdificio()

    procesar_stream()

#procesar el frame de la camara cada 10 ms
def procesar_stream():
    global video
    ret, frame = video.read()
    if ret:
        copiaFrame = frame.copy()
        #LADO DERECHO (MENU), cada 5 segundos
        threading.Thread(target=myDetectFaces.detectarCaras, args=(copiaFrame,)).start()



        #LADO IZQUIERDO (FRAME PRINCIPAL)
        frame = myBuilding.cambiarFrame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        #pasamos la imagen a formato tkinter
        image = ImageTk.PhotoImage(image=img)
        video_label.configure(image=image)
        video_label.image = image
        #llamamos a la funcion cada 10 milisegundos
        video_label.after(10, procesar_stream)


#variables
ventana = tkinter.Tk()
video = None

#MAIN

# crear una ventana dividida en dos partes con un menu a la derecha de 200x700 y un frame a la izquierda
ventana.title("Ventana")
ventana.geometry("840x480")
ventana.resizable(False, False)

#Etiquetas

video_label = tkinter.Label(ventana, bg="black")
video_stream()
video_label.pack(side=tkinter.LEFT)

ventana.mainloop()
