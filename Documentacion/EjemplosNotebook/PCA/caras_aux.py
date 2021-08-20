import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix

# defino algunas funciones auxiliares para la carga de imágenes y su representación

def loadImages(root, factor=1, nimages=False):
    files = os.listdir(root)
    if not nimages:
        nimages = len(files)
    X = np.zeros((nimages, int(factor*250)*int(factor*250)))
    for i in range(nimages):
        f = os.path.join(root, files[i])
        img = Image.open(f).convert('L')
        dims = np.shape(img)
        if i==0:
            h = int(factor*dims[0])
            w = int(factor*dims[1])
        img = img.resize((h, w))
        X[i,:] = np.ravel(img)
    return X, h, w


def plot_gallery(images, titles, nrows=3, ncols=4, cmap=plt.cm.gray):
    plt.figure(figsize=(1.8*ncols, 2.4*nrows))
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(nrows*ncols):
        plt.subplot(nrows, ncols, i+1)
        plt.imshow(images[i], cmap=cmap)
        plt.title(titles[i], size=12)
        plt.xticks(()); plt.yticks(())
    plt.show()
    

def report_base_error(X_train, y_train, X_test, y_test):    
    clases, counts_clases = np.unique(y_train, return_counts=True) # valores unicos de las clases
    prioris_tr = counts_clases / len(X_train)
    for c,p in zip(clases, prioris_tr):
        print('- Priori de la clase %d en training: %.3f' % (c, p))
    ind_clase_mayoritaria_train = prioris_tr.argmax()
    print('- Clase mayoritaria en training: %d\n' % clases[ind_clase_mayoritaria_train])

    for c in clases:
        print('- Priori de la clase %d en test: %.3f' % (c, y_test.count(c)/len(y_test)))            
    print('- Score de la clasificacion por mayoria en test: %.3f' %
          (y_test.count(ind_clase_mayoritaria_train)/len(y_test)))


def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicho: %s\nreal:      %s' % (pred_name, true_name)


def representa_algunas_predicciones(X_test, y_test, clf, target_names,
                                    h, w, show_only_errors=True):

    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=target_names))
    print('Matriz de Confusion:')
    print(confusion_matrix(y_test, y_pred))
    print('\nScore en test: %.3f' % clf.score(X_test, y_test))
    
    titulos = [title(y_pred, y_test, target_names, i) for i in range(len(y_pred))]
    if show_only_errors == True:
        inds = np.where(y_pred != y_test)[0]
        plot_gallery(X_test[inds,:].reshape((len(inds), h, w)), (np.array(titulos))[inds])
    else:
        plot_gallery(X_test.reshape((len(X_test), h, w)), titulos)
                     
    plt.show()


def entrena_e_imprime_scores(clf, X_tr, y_tr, X_te, y_te):
    clf.fit(X_tr, y_tr)
    print('Score en training: %.3f' % clf.score(X_tr, y_tr))
    print('Score en test: %.3f' % clf.score(X_te, y_te))

