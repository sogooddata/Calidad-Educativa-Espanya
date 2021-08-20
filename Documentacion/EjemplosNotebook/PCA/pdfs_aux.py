# por Manuel Sanchez-Montanes

import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.colors import ListedColormap

#from scipy.stats import gaussian_kde
#import mpl_toolkits.mplot3d.axes3d as axes3d


#--------------------------------------------------------------------------------
# genera_puntos_gaussiana2D(Npuntos, media, var1, var2, angulo)
#
# Npuntos: numero de puntos a generar
# media:   media de la Gaussiana (2 dimensiones)
# var1:    varianza en el eje principal 1
# var2:    varianza en el eje principal 2
# angulo:  angulo a rotar (en grados) en el sentido contrario a las
#          agujas del reloj
#--------------------------------------------------------------------------------
def genera_puntos_gausiana2D(Npuntos, media, var1, var2, angulo):
    
    X = np.random.randn(2, Npuntos)
    X[0,:] = X[0,:] * np.sqrt(var1) # se multiplica cada atributo por la
    X[1,:] = X[1,:] * np.sqrt(var2) # raiz cuadrada de la varianza deseada

    X = rota_datos_alrededor_origen(X, angulo)

    X[0,:] = media[0] + X[0,:]
    X[1,:] = media[1] + X[1,:]

    return X.transpose()


#--------------------------------------------------------------------------------
# genera_puntos_circulo(Npuntos, media, radiomin, radiomax)
#
# Npuntos: numero de puntos a generar
# media:   media de la Gaussiana (2 dimensiones)
#--------------------------------------------------------------------------------
def genera_puntos_circulo(Npuntos, media, radiomin, radiomax):

    radios = radiomin + (radiomax-radiomin)*np.random.rand(1, Npuntos)
    angulos = 2*3.1415*np.random.rand(1, Npuntos)
    
    X = np.concatenate((media[0] + np.multiply(radios, np.cos(angulos)), media[1] + np.multiply(radios, np.sin(angulos))), axis=0)
    
    return X.transpose()


#--------------------------------------------------------------------------------
# genera_puntos_cuadrado2D(Npuntos, media, ancho, alto, angulo)
#
# Npuntos: numero de puntos a generar
# media:   media del cuadrado (2 dimensiones)
# angulo:  angulo a rotar (en grados) en el sentido contrario a las
#          agujas del reloj
#--------------------------------------------------------------------------------
def genera_puntos_cuadrado2D(Npuntos, media, ancho, alto, angulo):
    
    X = np.random.rand(2, Npuntos) - 0.5
    X[0,:] = X[0,:] * ancho
    X[1,:] = X[1,:] * alto

    X = rota_datos_alrededor_origen(X, angulo)

    X[0,:] = media[0] + X[0,:]
    X[1,:] = media[1] + X[1,:]

    return X.transpose()


#--------------------------------------------------------------------------------
# function X_rotados = rota_datos_alrededor_origen(X, angulo)
#
# esta funcion rota datos 2D en torno al origen
# angulo: en grados, y en contra de las agujas del reloj
#--------------------------------------------------------------------------------
def rota_datos_alrededor_origen(X, angulo):
    
    angle_rad = angulo*2.0*np.pi/360.0

    s = np.sin(angle_rad)
    c = np.cos(angle_rad)
    matriz_rotacion = np.matrix([[c,-s],[s,c]])
    X_rotados = matriz_rotacion*X # se rotan los puntos generados

    return X_rotados


def visualiza_nube2D(X_original):
    
    X = X_original.transpose()
    
    print("--------------------------------------------------------")
    print("Datos experimentales: ")
    print("--------------------------------------------------------")
    media = np.mean(X, axis = 1)
    media = np.asarray(media).reshape(-1)
    print("Media:")
    print(media)
    print("--------------------------------------------------------")
    covar = np.cov(X)
    print("Matriz de covarianzas:")
    print(covar)
    print("--------------------------------------------------------")
    
    autovalores, autovectores = np.linalg.eig(covar)
    if autovalores[0] < autovalores[1]:
        autovalores = autovalores[[1,0]]
        autovectores = autovectores[:,[1,0]]

    print("Autovalores: ")
    print(autovalores)
    print("--------------------------------------------------------")
    print("Matriz de autovectores (en columnas): ")
    print(autovectores)
    print("--------------------------------------------------------")

    plt.figure(1)
    
    plt.plot(X[0,:],X[1,:],'b.',zorder=1) 
    hl =  np.sqrt(autovalores[0])*0.3
    hw =  np.sqrt(autovalores[0])*0.15
    aw =  np.sqrt(autovalores[0])*0.03

    dx1 = 3*np.sqrt(autovalores[0])*autovectores[0,0]
    dy1 = 3*np.sqrt(autovalores[0])*autovectores[1,0]
    dx2 = 3*np.sqrt(autovalores[1])*autovectores[0,1]
    dy2 = 3*np.sqrt(autovalores[1])*autovectores[1,1]
    
    plt.plot([media[0]-dx1, media[0]+dx1], [media[1]-dy1, media[1]+dy1], 'r', zorder=1, linewidth=2)
    plt.plot([media[0]-dx2, media[0]+dx2], [media[1]-dy2, media[1]+dy2], 'r', zorder=1, linewidth=2)
    
     
    plt.grid(True)
    plt.axis('equal')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
    
    return
