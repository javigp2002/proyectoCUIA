import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
import face_recognition as face
import time
import os
import json

    


#imagen = oscars.copy()
#caras = DeepFace.extract_faces(imagen, detector_backend='retinaface')
directorioActual = os.path.abspath("")
carpetaJson = "CodJson"

directorioCodigos= os.path.join(directorioActual, carpetaJson)
#abrir todos los ficheros de una carpeta
cods = []

for path in os.listdir(directorioCodigos):    
    archivoIntroducir=os.path.join(directorioActual, carpetaJson,path)
    with open(archivoIntroducir, 'r') as archivo:
        data2 = json.load(archivo)
    codificacionActual = np.array(data2['cod'],dtype=np.float32)
    cods.append(codificacionActual)




    




final =False
freeze = False
cap = cv2.VideoCapture(0)
if cap.isOpened():
    final = False
    framew = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while not final :
        ret, frame = cap.read()

        if not ret:
            final = True
        else:
            imagen = frame.copy()
            imagenrgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            caras = face.face_locations(imagenrgb, model='hog')
            codificacionesFrameActual = face.face_encodings(imagenrgb, caras, model='large')

            if caras is not None:
                for i in range (len(caras)):
                    print (face.compare_faces(cods, codificacionesFrameActual[i], tolerance=0.5))

                    if (face.compare_faces(cods, codificacionesFrameActual[i], tolerance=0.5)[0]):
                        color = (0,255,0)
                    else:
                        color = (0,0,255)
                    t,r,b,l = caras[i]
                    dist= face.face_distance(cods, codificacionesFrameActual[i])[0]
                    cv2.rectangle(frame, (l,t), (r,b), color, 2)
                    cv2.putText(frame, f"{dist:.2f}", (l,t-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        


            cv2.imshow("frame", frame)

            if cv2.waitKey(1) == ord(' '):
                final = True

print(framew, frameh)




