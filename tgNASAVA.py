# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 21:35:57 2019

@author: Viviana
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.arima_model import ARIMA
#from sm.tsa.statespace import SARIMAX
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

#Usamos Pandas para manejar las bases de Datos
tg_NASA=pd.read_csv('C:/Users/Viviana/Desktop/Materias/Series de tiempo/serieTrabajo/tgNASA.txt', delimiter=r"\s+", header=None, names=('Year', 'No_Smoothing', 'Lowess(5)'))
tg_NASA.tail(10)
tg_NASA.min()
########################################################
### Serie original
########################################################
ind = pd.date_range(start='1880', end='2019', freq='Y')
df_tgN = pd.DataFrame(tg_NASA['No_Smoothing'])
df_tgN = df_tgN.set_index(ind)
ts = pd.Series(df_tgN['No_Smoothing'],index=ind)
plt.plot(ts)
plt.show()
acf(ts,nlags=50,unbiased=False)
Grafico_acf_ts = plot_acf(ts,lags=50,unbiased=False)
########################################################
### Serie transformada para que los datos sean positivos
########################################################
dftrans= pd.DataFrame(tg_NASA['No_Smoothing'] + 0.73)
# MIN (No_Smoothing) = -0.48, EN [R]: minimum data value <= 0 so -min+0.25 added to all values, LUEGO -(-0.48)+0.25=0.73
print(dftrans)
dftrans = dftrans.set_index(ind)
tsbox = pd.Series(dftrans['No_Smoothing'],index=ind)
print(tsbox) 
plt.plot(tsbox)
plt.show()
graf_acf_ts=plot_acf(dftrans, lags=50, unbiased=False)
########################################################
### BoxCox
########################################################
import scipy as sp
import scipy.stats 
import pandas as pd
#sp.stats.boxcox(tsbox,alpha=0.05)

import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri
pandas2ri.activate()
base = importr('base')
utils = importr('utils')

utils.chooseCRANmirror(ind=1) 
from rpy2.robjects.vectors import StrVector
names_to_install=['forecast','tsoutliers', 'FitAR']
if len(names_to_install)>0:
    utils.install_packages(StrVector(names_to_install))
forecastR=importr('forecast')
graphicsR=importr('graphics')
fitarR=importr('FitAR')
ts=ro.r('ts') ###trae la función ts de R
rplot = ro.r('plot')

tg_NASA=pd.read_csv('C:/Users/Viviana/Desktop/Materias/Series de tiempo/serieTrabajo/tgNASA.txt', delimiter=r"\s+", header=None, names=('Year', 'No_Smoothing', 'Lowess(5)'))
dftrans= pd.DataFrame(tg_NASA['No_Smoothing'] + 0.73)
ind = pd.date_range(start='1880', end='2019', freq='Y')
dftrans = dftrans.set_index(ind)
tsbox = pd.Series(dftrans['No_Smoothing'],index=ind)
box=fitarR.BoxCox(tsbox)#import scipy as sp
#import scipy.stats 
#sp.stats.boxcox(tsbox,alpha=0.05) 
########################################################
### Descomposición
########################################################
d1ts=ts.diff(periods=1)[1:] #diferencia ordinaria
plt.plot(d1ts)
########################################################
### Identificación
########################################################
acf(d1ts,nlags=50,unbiased=False)
acf_ts=plot_acf(d1ts,lags=50, unbiased=False) # MA(2)
pacf(d1ts,nlags=50) 
Pacf_ts=plot_pacf(d1ts,lags=50) #Ar(5)
########################################################
### Estimación
########################################################
modeloAR=ARIMA(d1ts,order=(5,0,0)) ####Ajuste de un AR(5)
ajusteAR=modeloAR.fit(trend='c')
print(ajusteAR.summary()) #Primer, segundo, tercer y quinto coef son significativos

modeloMA=ARIMA(d1ts,order=(0,0,2)) ####Ajuste de un MA(2)
ajusteMA=modeloMA.fit(trend='c')
print(ajusteMA.summary())  #Ambos coeficientes son significativos
#ajusteMA.resid
import statsmodels.api as smapi
#modeloMASPmodel = smapi.tsa.statespace.SARIMAX(d1ts, trend='n', order=(5,0,2))
#results = modeloMASPmodel.fit()
#print(results.summary()) 
########################################################
### Especificando las entradas de los parámetros
########################################################
ar_orden=[1,1,1,0,0]
#Dejamos este orden porque al intentarlo con [1,1,1,0,1], el quinto coef
#resultó no ser significativo.
ARfinal= smapi.tsa.statespace.SARIMAX(d1ts, trend='n', order=(ar_orden,0,0))  
resultsARfinal = ARfinal.fit()

MAfinal= smapi.tsa.statespace.SARIMAX(d1ts, trend='n', order=(0,0,2))  
resultsMAfinal = MAfinal.fit()
########################################################
### Pronósticos
########################################################

#### AR ####
pronosticosAR=resultsARfinal.forecast(steps=5)
resultsARfinal.resid
plt.plot(resultsARfinal.resid)
salforecastAR=resultsARfinal.get_prediction(start=139, end=144,full_results=True,alpha=0.05,dynamic=False)
salforecastAR.conf_int(alpha=0.05) #Intervalos de predicción 
salforecastARotro=resultsARfinal.get_forecast(steps=5)
ICforecastAR95=salforecastARotro.conf_int(alpha=0.05)
pronosticosAR=salforecastARotro.predicted_mean
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#Actual data
ax.plot(d1ts.astype('float64'), '--', color="blue", label='data')
# Means
ax.fill_between(pronosticosAR.index, ICforecastAR95.iloc[:, 0], ICforecastAR95.iloc[:, 1], alpha=0.05)
ax.plot(pronosticosAR, lw=1, color="black", alpha=0.5, label='SARIMAX')
ax.legend(loc='upper right')
plt.draw()

#### MA ####
pronosticosMA=resultsMAfinal.forecast(steps=5)
salforecastMA=resultsMAfinal.get_prediction(start=139, end=144,full_results=True,alpha=0.05,dynamic=False)
salforecastMA.conf_int(alpha=0.05) #Intervalos de predicción 
salforecastMAotro=resultsMAfinal.get_forecast(steps=5)
ICforecastMA95=salforecastMAotro.conf_int(alpha=0.05)
pronosticosMA=salforecastMAotro.predicted_mean
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#Actual data
ax.plot(d1ts.astype('float64'), '--', color="blue", label='data')
# Means
ax.fill_between(pronosticosMA.index, ICforecastMA95.iloc[:, 0], ICforecastMA95.iloc[:, 1], alpha=0.05)
ax.plot(pronosticosMA, lw=1, color="black", alpha=0.5, label='SARIMAX')
ax.legend(loc='upper right')
plt.draw()

#### ARMA ####


########################################################
### Auto.Arima
########################################################
import pmdarima as pm
ajuste=pm.auto_arima(d1ts,start_p=0,start_q=0, max_p=5, max_q=2, d=0, D=0, seasonal=False)
ajuste.summary()
#modeloest=ARIMA(d1ts,order=(2,0,1))
#resultsmodeloest=modeloest.fit()
#print(resultsmodeloest.summary())
#resultsmodeloest.aic

modeloARMAmodelfinal = smapi.tsa.statespace.SARIMAX(d1ts, trend='n', order=(2,0,1))  
resultsARMAfinal = modeloARMAmodelfinal.fit()
print(resultsARMAfinal.summary())

###Pronóstico
pronosticosARMA=resultsARMAfinal.forecast(steps=5)
resultsARMAfinal.resid
plt.plot(resultsARMAfinal.resid)
salforecastARMA=resultsARMAfinal.get_prediction(start=139, end=144,full_results=True,alpha=0.05,dynamic=False)
salforecastARMA.conf_int(alpha=0.05) #Intervalos de predicción
salforecastARMAotro=resultsARMAfinal.get_forecast(steps=5)
ICforecastARMA95=salforecastARMAotro.conf_int(alpha=0.05)
pronosticosARMA=salforecastARMAotro.predicted_mean
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#Actual data
ax.plot(d1ts.astype('float64'), '--', color="blue", label='data')
# Means
ax.fill_between(pronosticosARMA.index, ICforecastARMA95.iloc[:, 0], ICforecastARMA95.iloc[:, 1], alpha=0.05)
ax.plot(pronosticosARMA, lw=1, color="black", alpha=0.5, label='SARIMAX')
ax.legend(loc='upper right')
plt.draw()

###análisis de residuales
residuales=resultsARMAfinal.resid
acf(residuales,nlags=50,unbiased=False)
plot_acf(residuales,lags=50,unbiased=False)
pacf(residuales,nlags=50)
plot_pacf(residuales,lags=50)

#breakvar: h0: No hay heterocedasticidad
resultsARMAfinal.test_heteroskedasticity(method='breakvar') #No rechaza H0, no hay heteroced.
#jarquebera: h0: hay normalidad
resultsARMAfinal.test_normality(method='jarquebera') #No se rechaza H0, hay normalidad
#ljungbox: h0: no hay autocorrelación
resultsARMAfinal.test_serial_correlation(method='ljungbox') #No se rechaza, no hay autocorr.


