import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
import face_recognition as face
import time
import os
import json

    
directorioActual = os.path.abspath("")
carpeta = "database\\"

imagenAJson=os.path.join(directorioActual, carpeta+"pitt.jpg")
#res = DeepFace.verify(oscars, pitt)
javi = cv2.imread(imagenAJson)
cv2.imshow("javi", javi)


javirgb = cv2.cvtColor(javi, cv2.COLOR_BGR2RGB)
locs = face.face_locations(javirgb, model='hog')
cod_javi = face.face_encodings(javirgb, locs, model='large')[0]

carpetaJson = "CodJson"
nombreImagen = "Pitt"
jsonExt =  ".json"
archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)

data = {
    "nombre": "Brad Pitt",
    "cod": cod_javi.tolist()
}

archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)


with open(archivoIntroducir, 'w') as archivo:
    json.dump(data, archivo)





