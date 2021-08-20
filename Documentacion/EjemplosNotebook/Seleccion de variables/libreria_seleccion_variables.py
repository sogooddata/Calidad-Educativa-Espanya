# Librería desarrollada por Manuel Sánchez-Montañés

from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.model_selection import KFold

import numpy as np
from matplotlib import pyplot as plt


def ranking_variables_clasificacion(X, y, nombres, metodo, draw=False):
    
    nvars = np.shape(X)[1]
    if metodo == "mutual_info":
        scores = []
        for i in range(nvars):
            scores.append(mutual_info_classif(X[:,i].reshape(-1,1),y,random_state=1)[0])
        scores = np.array(scores)
        
    elif metodo == "f_classif": # f de ANOVA
        selector = SelectPercentile(f_classif, percentile=10)
        selector.fit(X, y)
        scores = selector.scores_
    
    elif metodo == "corr":
        scores = []
        aux = y.T
        for i in np.arange(0,nvars):
#            scores.append(np.corrcoef(X[:,i].T,aux)[0][1]) #MAL
            scores.append(np.corrcoef(X[:,i].T,aux)[0][1] ** 2) #BIEN
        scores = np.array(scores)
    
    inds = np.argsort(scores)[::-1] # indices de scores de mayor a menor
                          
    for ind in inds:
        print("%s \t score=%f \t" % (nombres[ind], scores[ind]))
    
    if draw:
        plt.figure(figsize=(10,5))
        plt.bar(range(X.shape[1]),scores[inds], width=.2, color='lightgreen')
        plt.xticks(range(X.shape[1]), np.array(nombres)[inds], rotation=80)
        plt.ylabel("Score")
        plt.show()
    
    return inds


def ranking_variables_regresion(X, y, nombres, metodo, draw=False):
    
    nvars = np.shape(X)[1]
    if metodo == "mutual_info":
        scores = []
        for i in range(nvars):
            scores.append(mutual_info_regression(X[:,i].reshape(-1,1),y,random_state=1)[0])
        scores = np.array(scores)
        
    elif metodo == "corr":
        scores = []
        aux = y.T
        for i in np.arange(0,nvars):
#            scores.append(np.corrcoef(X[:,i].T,aux)[0][1]) #MAL
            scores.append(np.corrcoef(X[:,i].T,aux)[0][1] ** 2) #BIEN
        scores = np.array(scores)
    
    inds = np.argsort(scores)[::-1] # indices de scores de mayor a menor
                          
    for ind in inds:
        print("%s \t score=%f \t" % (nombres[ind], scores[ind]))
    
    if draw:
        plt.figure(figsize=(10,5))
        plt.bar(range(X.shape[1]),scores[inds], width=.2, color='lightgreen')
        plt.xticks(range(X.shape[1]), np.array(nombres)[inds], rotation=80)
        plt.ylabel("Score")
        plt.show()
    
    return inds



def calcula_score_crossval(X, y, model, particiones):
    scores = []
    for p in particiones:
        inds_train, inds_val = p
        model.fit(X[inds_train], y[inds_train])
        score = model.score(X[inds_val], y[inds_val])
        scores.append(score)
    return np.mean(scores)



# X: matriz de n filas (ejemplos) por m columnas (variables)
# y: array de n componentes (etiquetas)
def mi_RFECV(X, y, model, nfolds=5, verbose=False):
    # elegidos contiene la lista de atributos que tenemos
    # empieza conteniendo a todos los atributos:
    elegidos = list(range(X.shape[1])) # X.shape[1] es el número de columnas

    # Ahora, en vez de usar 1 partición training-validación,
    # usamos nfolds particiones. La idea es estimar el score de manera
    # robusta, intentar que no dependa de fluctuaciones estadísticas
    # Cuanto nfolds mayor mejor, pero más lento    
    particiones = list(KFold(n_splits=nfolds).split(X))
    
    # inicializamos el mejor score hasta el momento es el score
    # calculado con todas las variables:
    score = calcula_score_crossval(X, y, model, particiones)
    
    scores = [score]
    l_elegidos = [elegidos.copy()]
    
    while len(elegidos) > 1: # si solo tenemos un atributo no tiene sentido seguir.
        
        if verbose:
            print("Modelo con {} atributos. Score: {}".format(len(elegidos), scores[-1]))
        
        # Ahora vemos qué pasa si quitamos uno de los atributos que
        # nos quedan. Como tenemos len(elegidos) atributos, tenemos
        # len(elegidos) atributos que probar a quitar. Eso se controla en el for:
        best_score_aux = -1.e10
        worst_att = -1 # 
        for e in elegidos:
            elegidos_aux = elegidos.copy()
            elegidos_aux.remove(e)
            score_aux = calcula_score_crossval(X[:,elegidos_aux], y,
                                               model,
                                               particiones)
            if score_aux > best_score_aux:
                best_score_aux = score_aux
                worst_att = e
                
        elegidos.remove(worst_att)
        
        scores.append(best_score_aux)
        l_elegidos.append(elegidos.copy())
    
    if verbose:
            print("Modelo con 1 atributo. Score: {}".format(scores[-1])) # el último que se ha añadido
    
    scores = scores[::-1]
    l_elegidos = l_elegidos[::-1]
    mejor = np.argmax(scores) # si hay empate se queda con el primero (solución con menos atributos)
        
    return l_elegidos[mejor]
