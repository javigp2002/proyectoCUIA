import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
import face_recognition as face
import os
import json
import threading
import time

class DetectaCaras:
    directorioCodigos = ""
    cods = []
    estaDetectando = False
    haEncontrado= False
    nombreUsuario = ""
    backGround = ""

    def __init__(self):
        directorioActual = os.path.abspath("")
        carpetaJson = "CodJson"

        self.directorioCodigos= os.path.join(directorioActual, carpetaJson)
        self.cods = []
        self.nameCods =[]
        self.backGrounds = []
        self.codificarImagenes()
        self.estaDetectando = False
        self.haEncontrado = False
        self.nombreUsuario = ""
        self.backGround = ""


    #codificamos las imagenes en CODS
    def codificarImagenes(self):
        for path in os.listdir(self.directorioCodigos):    
            archivoIntroducir=os.path.join(self.directorioCodigos,path)
            with open(archivoIntroducir, 'r') as archivo:
                data2 = json.load(archivo)
            codificacionActual = np.array(data2['cod'],dtype=np.float32)
            nombreActual =data2['nombre']

            self.cods.append(codificacionActual)
            self.nameCods.append(nombreActual)
            self.backGrounds.append(data2['background'])


    def runDetectCaras(self, frame):
        #print ("hebra detectarCaras: ",threading.get_ident())

        imagenrgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        caras = face.face_locations(imagenrgb, model='hog')
        codificacionesFrameActual = face.face_encodings(imagenrgb, caras, model='large')

        if caras is not None:
            comparando = True

            for i in range (len(caras)) :
                codificaciones = face.compare_faces(self.cods, codificacionesFrameActual[i], tolerance=0.5)
                if (comparando == False):
                    break

                #por cada cara buscamos en las codificaciones que tenemos almacenadas
                for j in range (len(codificaciones)):
                    if codificaciones[j]:
                        self.nombreUsuario = self.nameCods[j]
                        comparando = False
                        self.haEncontrado = True
                        self.backGround = self.backGrounds[j]
                        break
        self.estaDetectando = False

    #pasado un frame, devuelve las caras que detecta
    def detectarCaras(self, frame):
        if self.estaDetectando or self.haEncontrado:
            return 
        self.estaDetectando = True
        
        #rendimiento Lento -> threading
        threading.Thread(target=self.runDetectCaras, args=(frame,), name = "detectarCaras").start()        





