import cv2
import numpy as np
import json
import os

def mezcla(edificio, frame):

    bg = frame
    hbg, wbg, _ = bg.shape
    fg = edificio[:, :, 0:3]
    hfg, wfg, _ = fg.shape 
    #alfa -> opacidad pixxeles primeros
    # afla -> opacidad pixeles del fondo
    alfa = edificio[:, :, 3]
    afla = 255 - alfa

    #BGR-
    #GRAY TO BGR pq las operaciones con matrices tienen q ser
    # de tres canales pero seran el mismo valor para las 3
    alfa = cv2.cvtColor(alfa, cv2.COLOR_GRAY2BGR) / 255
    afla = cv2.cvtColor(afla, cv2.COLOR_GRAY2BGR) / 255


    x = wbg//2 - wfg//2
    y = hbg//2 - hfg//2

    mezcla = bg
    mezcla[y:y+hfg, x:x+wfg] = mezcla[y:y+hfg, x:x+wfg]*afla + fg*alfa

    
    return mezcla


#tamaño en metros



F = cv2.SIFT_create()
directorioActual = os.path.abspath("")

carpetaJson = "KPJsons"
nombreImagen = "arucoCalb"
jsonExt =  ".json"

archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)
with open(archivoIntroducir, 'r') as archivo:
    data2 = json.load(archivo)

kpimg = []

for kp in data2['kpimg']:
    p = cv2.KeyPoint(x=kp["point0"],y=kp["point1"],size=kp["size"], angle=kp["angle"], response=kp["response"], octave=int(kp["octave"]), class_id=int(kp["id"]))
    kpimg.append(p)
    
    
descimg = np.array(data2['descimg'],dtype=np.float32)

nuevoEdificio = cv2.imread(data2["imagenLigada"])
#aqui reestrucutramos como queremos que sea el nuevo 
imgw = data2["imgw"]
imgh = data2["imgh"]
nuevoEdificio = cv2.resize(nuevoEdificio, (imgw,imgh))

#emparejamiento por fuerza bruta
bf_matcher = cv2.BFMatcher()


#FLANN para SIFT
# Fast Library for Approximate Nearest Neighbors
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=100)

#FFLANN para ORB
flann = cv2.FlannBasedMatcher(index_params,search_params)

flags = \
cv2.DRAW_MATCHES_FLAGS_DEFAULT

cap = cv2.VideoCapture(0)
if cap.isOpened():
    final = False
    framew = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    while not final:
        ret, frame = cap.read()
        if not ret:
            final = True
        else:
            #Procesar el frame
            gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Realiza la deteccion y descripcion de caracteristicas en la imagen
            # en escala de grises
            kp, desc = F.detectAndCompute(gris, None)

            #k es el numero de vecinos más creacnos para la caracteristica
            coincidencias = bf_matcher.knnMatch(descimg, desc, k=2)
                     #coincidencias = flann.knnMatch(descimg, desc, k=2)
                        #coincidencias = bf_matcher.match(descimg, desc)

            good = []
            for m, n in coincidencias:
                if m.distance < 0.5*n.distance:
                    good.append([m])
            #print(good,", ", len(good))
            nuevo = frame
            
            if len(good)>8 :
                origenes = []
                destinos = []
                
                origen = np.float32([kpimg[m[0].queryIdx].pt for m in good]).reshape(-1,1,2)
                destino = np.float32([kp[m[0].trainIdx].pt for m in good]).reshape(-1,1,2)

                mascaraa = []
                matriz, mascara = cv2.findHomography(origen, destino, cv2.RANSAC, 5.0)
 
                if (matriz is not None):
                    matches_mask = mascara.ravel().tolist() 
 
                    edificio = cv2.cvtColor(nuevoEdificio,cv2.COLOR_BGR2BGRA)

                    nuevoFrame = cv2.warpPerspective(edificio,matriz,(framew,frameh))
                    
                    nuevo = mezcla(nuevoFrame, frame)
                else  :  
                    print("malo")

            cv2.imshow("Frame con ", frame)
            cv2.imshow("Frame con Cuadrado", nuevo)

            if cv2.waitKey(1) == ord(' '):
                final = True
    cap.release()
    cv2.destroyAllWindows()
else:
    print("No puedo acceder a la cámara")

 
