import cv2
import numpy as np
import json
import os


#Imagen a introducir en un nuevo
directorioActual = os.path.abspath("")

carpetaImagen = "imagenes"
nombreImagen = "arucoCalb"
extensionImagen = ".png"

nombreImagenNueva = "javi"
extensionImagenNueva = ".jpg"

imagenAJson=os.path.join(directorioActual, carpetaImagen, nombreImagen + extensionImagen)
imgLigada=os.path.join(directorioActual, carpetaImagen, nombreImagenNueva + extensionImagenNueva)

img = cv2.imread(imagenAJson)

imggris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgh, imgw, _ = img.shape


F = cv2.SIFT_create()

kpimg, descimg = F.detectAndCompute(imggris, None)

temp = [{'point0':k.pt[0],'point1':k.pt[1],'size':k.size,'angle': k.angle, 'response': k.response, "octave":k.octave,
     "id":k.class_id} for k in kpimg]
data = {
    "kpimg":temp,
    "descimg": descimg.tolist(),
    "imgh": imgh,
    "imgw": imgw ,
    "imagenLigada": imgLigada
}

carpetaJson = "KPJsons"
jsonExt =  ".json"

archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)


with open(archivoIntroducir, 'w') as archivo:
    json.dump(data, archivo)

