import cv2
import matplotlib.pyplot as plpt
import numpy as np
import pandas as pd
from deepface import DeepFace
import time
import os


backends = ['opencv', 'ssd', 'mtcnn', 'retinaface', 'dlib']
#imagen = oscars.copy()
#caras = DeepFace.extract_faces(imagen, detector_backend='retinaface')
directorioActual = os.path.abspath("")
carpetaImagen = "database"
carpetaJavi = "javi"

imagenAJson=os.path.join(directorioActual, carpetaImagen+carpetaJavi)
#res = DeepFace.verify(oscars, pitt)

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
            caras = DeepFace.extract_faces(imagen, detector_backend='retinaface', enforce_detection=False)
        
            res = DeepFace.find(imagen, "database\\javi", enforce_detection=False)
            print(res)  
            if (res[0].size > 0 and res[0]['VGG-Face_cosine'][0] < 0.3):
                print ("hola")       


            #if (res[0]['VGG-Face_cosine'][0] < 0.2): # si la mejor relacion q encuentra es menor que ese numero entonces es valido
                #aqui ahora tengo que poner que se cambie la información y que durante un tiempo no este buscando gente y modifique
                # al gusto de la persona que haya encontrado

            #    print("hola javi")

            
            cv2.imshow("frame", frame)
            time.sleep(3);            
            

            if cv2.waitKey(1) == ord(' '):
                final = True
            
            
            #write code that makes a simple interface where the main stream is the cv2.imshow and a button section on its right
            #the buttons should be:
            # - freeze: freezes the frame and allows the user to select a face
            # - add: adds the face to the database
            # - delete: deletes the face from the database
            # - exit: exits the program
            # - save: saves the database
            # - load: loads the database
            # - train: trains the database


            

            

