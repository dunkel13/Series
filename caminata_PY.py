# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:18:45 2019

@author: Viviana
"""

import pandas as pd
import numpy as np
from scipy import stats 
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

### Genreación de la muestra ###
np.random.seed(0)
muestra=np.random.normal(0, 1, 200)
print(muestra)

### Función para las sumas acumualdas ###
muestra

def caminata(t, muestra):  
    suma= []
    for i in range(0,t+1):
        nuevo=sum(muestra[0:i+1])
        suma.append(nuevo)
        print(suma)    
    return(suma)  
datos=caminata(200,muestra)

### Gráfico de la serie de tiempo ###
t = np.arange(1, 201, 1)
datosn=datos[0:200]
Caminata=pd.Series(datosn,index=t)
Caminata
plt.plot(Caminata)
plt.ylabel('St')
plt.xlabel('t')
plt.title('Caminata Aleatoria') 
