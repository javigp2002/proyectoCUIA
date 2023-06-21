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

class Edificio:
    nuevoEdificio = None
    kpimg = None
    descimg = None
    frameh = None
    framew = None
    F = None


    def extraerDatosNuevoEdificio(self):
        
        directorioActual = os.path.abspath("")

        carpetaJson = "KPJsons"
        nombreImagen = "arucoCalb"
        jsonExt =  ".json"

        archivoIntroducir=os.path.join(directorioActual, carpetaJson, nombreImagen + jsonExt)
        with open(archivoIntroducir, 'r') as archivo:
            data2 = json.load(archivo)

        self.kpimg = []

        for kp in data2['kpimg']:
            p = cv2.KeyPoint(x=kp["point0"],y=kp["point1"],size=kp["size"], angle=kp["angle"], response=kp["response"], octave=int(kp["octave"]), class_id=int(kp["id"]))
            self.kpimg.append(p)
            
            
        self.descimg = np.array(data2['descimg'],dtype=np.float32)

        self.nuevoEdificio = cv2.imread(data2["imagenLigada"])
        #aqui reestrucutramos como queremos que sea el nuevo 
        imgw = data2["imgw"]
        imgh = data2["imgh"]
        self.nuevoEdificio = cv2.resize(self.nuevoEdificio, (imgw,imgh))

    # tiene que ejecutarse previamente la funcion ExtraerDatosself.nuevoEdificio
    def cambiarFrame(self, frame):
        F = cv2.SIFT_create()
        
        bf_matcher = cv2.BFMatcher()

        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Realiza la deteccion y descripcion de caracteristicas en la imagen
        # en escala de grises
        kp, desc = F.detectAndCompute(gris, None)

        #k es el numero de vecinos más creacnos para la caracteristica
        coincidencias = bf_matcher.knnMatch(self.descimg, desc, k=2)

        good = []
        for m, n in coincidencias:
            if m.distance < 0.5*n.distance:
                good.append([m])
        nuevo = frame
        
        if len(good)>8 :
            origenes = []
            destinos = []
            
            origen = np.float32([self.kpimg[m[0].queryIdx].pt for m in good]).reshape(-1,1,2)
            destino = np.float32([kp[m[0].trainIdx].pt for m in good]).reshape(-1,1,2)

            mascaraa = []
            matriz, mascara = cv2.findHomography(origen, destino, cv2.RANSAC, 5.0)

            if (matriz is not None):
                matches_mask = mascara.ravel().tolist() 
                edificio = cv2.cvtColor(self.nuevoEdificio,cv2.COLOR_BGR2BGRA)
                nuevoFrame = cv2.warpPerspective(edificio,matriz,(self.framew,self.frameh))
                nuevo = mezcla(nuevoFrame, frame)

            
        return nuevo

