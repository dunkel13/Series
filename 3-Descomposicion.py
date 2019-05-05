#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:16:31 2019

@author: sergiocalderonv
"""


import pandas as pd
from pandas import Series
import numpy as np
import scipy as sp
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
from pydataset import data
#data('AirPassengers')
#Usamos Pandas para manejar las bases de Datos

data = pd.read_csv('AirPassengers.csv')
print(data)
print('\n Data Types:')
print(data.dtypes)


######Convertir el conjunto de datos en una serie de Tiempo#####


con=data['Month']
data['Month']=pd.to_datetime(data['Month'])
##data.set_index('Month', inplace=True)
pasajeros=data.set_index('Month')
#check datatype of index

#convert to time series:
ts = pasajeros['NPassengers']
ts.head(10)

####Graficar la Serie#####
plt.plot(ts)
plt.title('AirPassengers') 

#####Tranformación Box-Cox
import scipy.stats ####En ocasiones puede funcionar la línea 46 sin ésta línea.
sp.stats.boxcox(ts,alpha=0.05)
sp.stats.boxcox(data['NPassengers'],alpha=0.05)
logAirp=sp.stats.boxcox(data['NPassengers'],lmbda=0)
data = data.assign(logAirp=logAirp)   

logpasajeros=data.set_index('Month')   
logAirPass=  logpasajeros['logAirp'] 
plt.plot(logAirPass)

####Descomposición usando filtros
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot


result = seasonal_decompose(logAirPass, model='additive')
print(result.trend)
print(result.seasonal)
print(result.resid)
print(result.observed)
result.plot()
pyplot.show()

####Holt-Winters
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
print(ts)
print(pd.infer_freq(data['Month'], warn=True))
fit1 = ExponentialSmoothing(ts, seasonal_periods=12, trend='add', seasonal='add').fit(use_boxcox=True)
####ejecutar desde la línea 74 hasta la 88
plt.subplot(5, 1, 1)
plt.plot(ts)
plt.ylabel('AirPassengers') 
plt.subplot(5, 1, 2)
plt.plot(fit1.level)
plt.ylabel('level') 
plt.subplot(5, 1, 3)
plt.plot(fit1.slope)
plt.ylabel('slope') 
plt.subplot(5, 1, 4)
plt.plot(fit1.season)
plt.ylabel('sesaon') 
plt.subplot(5, 1, 5)
plt.plot(fit1.resid)
plt.ylabel('resid') 

#####Aplicado diferenciación
diff1logAirPass=logAirPass.diff(periods=1)####Diferencia Ordinaria
plt.plot(diff1logAirPass)
diffs1diff1logAirPass=diff1logAirPass.diff(periods=12) ###Diferencia Estacional
print(diffs1diff1logAirPass)
plt.plot(diffs1diff1logAirPass)




