import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
import face_recognition as face
import time
import os
import json

########## HA RELLENAR SEGUN EL ARCHIVO
imagenJPG = "adriana.jpg"
nombreUsuario = "Adriana"
colorUsuarioFavorito = "#fffa7f"
nombreJson = "Adriana"


directorioActual = os.path.abspath("")
carpeta = "database\\"

imagenAJson=os.path.join(directorioActual, carpeta+imagenJPG)

imagen = cv2.imread(imagenAJson)

imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
locs = face.face_locations(imagenrgb, model='hog')
cod_imagen = face.face_encodings(imagenrgb, locs, model='large')[0]

carpetaJson = "CodJson"
nombreImagen = nombreJson
jsonExt =  ".json"
archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)

data = {
    "nombre": nombreUsuario,
    "cod": cod_imagen.tolist(),
    "background": colorUsuarioFavorito
}

archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)

with open(archivoIntroducir, 'w') as archivo:
    json.dump(data, archivo)





