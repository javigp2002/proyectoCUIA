import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
import face_recognition as face
import os
import json

class DetectaCaras:
    directorioCodigos = ""
    cods = []

    def __init__(self):
        directorioActual = os.path.abspath("")
        carpetaJson = "CodJson"

        self.directorioCodigos= os.path.join(directorioActual, carpetaJson)
        self.cods = []
        self.nameCods =[]
        self.codificarImagenes()


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


    #pasado un frame, devuelve las caras que detecta
    def detectarCaras(self, frame):
        imagen = frame.copy()
        imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        caras = face.face_locations(imagenrgb, model='hog')
        codificacionesFrameActual = face.face_encodings(imagenrgb, caras, model='large')

        if caras is not None:
            for i in range (len(caras)):
                codificaciones = face.compare_faces(self.cods, codificacionesFrameActual[i], tolerance=0.5)
                
                #por cada cara buscamos en las codificaciones que tenemos almacenadas
                for j in range (len(codificaciones)):
                    if codificaciones[j]:
                        print(self.nameCods[j])
                        return True
        





