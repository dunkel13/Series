#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 06:38:17 2019

@author: sergiocalderonv
"""

#import rpy2 as rpy2# Se debe instalar el paquete rpy2, éste corre
#bajo la versión 2.8.4 de rpy2
import rpy2.robjects as ro
import pandas as pd
#import scipy as sp
import numpy as np
import math

from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri



import statsmodels as sm
import matplotlib.pylab as plt
import statsmodels.api as smapi

Tlength=250
ar = np.array([1, -0.5]) 
ma = np.array([1]) # add zero-lag y maparams tiene los otros parámetros
y = sm.tsa.arima_process.arma_generate_sample(ar, ma,Tlength) 
#plt.plot(y)
y[59]=6
#plt.plot(y)
#import pmdarima as pm
##tzlocal
pandas2ri.activate()

###Análisis de outliers para la serie AirPassengers por medio de la importación de funciones
#de R de las librerías stats, forecast y tsoutliers

# Importar paquete Base de R
base = importr('base')
utils = importr('utils')

utils.chooseCRANmirror(ind=1) 
from rpy2.robjects.vectors import StrVector
names_to_install=['forecast','tsoutliers']
if len(names_to_install)>0:
    utils.install_packages(StrVector(names_to_install))
    

forecastR=importr('forecast')
tsoutlierR=importr('tsoutliers')
lmtestR=importr('lmtest')
statsR=importr('stats')
graphicsR=importr('graphics')
ts=ro.r('ts') ###trae la función ts de R
conca=ro.r('c') ###trae la función c de R
rplot = ro.r('plot')
lista=ro.r('list')
NAS=ro.r('NA')


#########


#plt.plot(y)
rdata=ts(y)
fit=forecastR.auto_arima(rdata)
ajuste=statsR.arima(rdata,order=conca(1,0,1),include_mean=False)
print(ajuste)
print(fit)
print(forecastR.BoxCox_lambda(rdata))
print(fit.rclass)
print(fit.names)
print(fit.rx2('coef'))
print(fit.rx2('fitted'))

##Outliers
outliers=tsoutlierR.tso(rdata)
outliers1=tsoutlierR.tso(rdata,tsmethod = "arima",args_tsmethod = lista(order =conca(1,0,0),seasonal = lista(order = conca(0, 0, 0),period=NAS),include_mean=False))
print(outliers)
print(outliers1)
print(outliers.names)
print(outliers.rx2('outliers'))
print(outliers.rx2('y'))
print(outliers.rx2('fit'))
print(outliers.rx2('effects'))

#####










data = pd.read_csv('AirPassengers.csv')
print(data)
print('\n Data Types:')
print(data.dtypes)
data.columns= ['Mes', 'NPasajeros']   

##Uso de funciones ts y auto.arima              
rdata=ts(data.NPasajeros.values,frequency=12,start=conca(1949,1))
fit=forecastR.auto_arima(rdata)
print(fit)
print(forecastR.BoxCox_lambda(data.NPasajeros.values))
print(fit.rclass)
print(fit.names)
print(fit.rx2('coef'))
print(fit.rx2('fitted'))


##Outliers
outliers=tsoutlierR.tso(rdata)
print(outliers)
print(outliers.names)
print(outliers.rx2('outliers'))
print(outliers.rx2('y'))
print(outliers.rx2('fit'))
print(outliers.rx2('effects'))

ajuste= statsR.arima(base.log(rdata),order=conca(0,1,1),seasonal = base.list(order = conca(0, 1, 1)),include_mean=False)
print(ajuste)
resi= statsR.residuals(ajuste)
#rplot(resi)
coef= tsoutlierR.coefs2poly(ajuste)
outliers1= tsoutlierR.locate_outliers(resi,coef)
print(outliers1)
n=base.length(rdata)
xreg = tsoutlierR.outliers_effects(outliers1,n)
##Convertirlo a un arreglo de Pandas
regoutliers=pandas2ri.ri2py(xreg)
#tso(y=serie2,xreg=xreg,types=c("AO")  )
#arima(serie2,order=c(1,0,0),include.mean = F)

#####Estimación del modelo con variables regresoras#####
import statsmodels.api as smapi
data['Month']=pd.to_datetime(data['Mes'])
pasajeros=data.set_index('Mes')
tsAirP = pasajeros['NPasajeros']

modeloMASPmodel = smapi.tsa.statespace.SARIMAX(tsAirP.apply(math.log),exog=regoutliers,trend='n',order=(0,1,1),seasonal_order=(0,1,1,12))  
results = modeloMASPmodel.fit()
print(results.summary())


