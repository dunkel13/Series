#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 04:53:51 2019

@author: sergiocalderonv
"""

#####Llama algunas librerías de Python y sublibrerías
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6

#Usamos Pandas para manejar las bases de Datos
# Importación de los datos
data = pd.read_csv('/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/AirPassengers.csv')
print(data)
print('\n Data Types:')
print(data.dtypes)
Npasajeros=data["NPassengers"]
print(Npasajeros)
ind = pd.date_range(start='1/1949', end='1/1961', freq='M')
print(ind)
SerieAP =pd.Series(data["NPassengers"].values,index=ind)
SerieAP
plt.plot(SerieAP)
plt.ylabel('Número de Pasajeros')
plt.xlabel('Fecha')
plt.title('AirPassengers') 

############
########## Importación datos con base de varias variables
data2=pd.ExcelFile('/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/Base_Accidentes.xlsx')
#Nombres de las hojas de la base
print(data2.sheet_names)
#Data Frame de la hoja "Datos"
data2=data2.parse('DATA2005')
print(data2)

# Conversión de la fecha
data2["Fecha"] = data2.iloc[:,0].map(str) +'-'+ data2.iloc[:,1].map(str)
data2['Fecha'] = pd.to_datetime(data2['Fecha'])
accidentes = data2.set_index('Fecha')
# Otra forma
ind = pd.date_range(start='1/1/2005', end='8/1/2018', freq='M')
accidentes2 = data2.set_index(ind)
ind1 = pd.date_range(start='1/1/2005', end='8/1/2018', freq='Q')
accidentes2 = data2.set_index(ind1) #No son compatibles

# Eliminar columnas
accidentes = accidentes.drop(['PERIODO','MES'], axis=1)
ts2 = accidentes['HER']
ts2.head(10)
ts21 = accidentes2['ISE']
ts21.head(10)

#### Seleccionar fechas específicas
accidentes['2005-01-01':'2006-02-01']
#### Valores de una fecha específica
accidentes.loc['2016-02-01']
# Valores dependiendo de la frecuencia
accidentes.asfreq(freq='A',how="S")['HER']
accidentes2.asfreq(freq='Q', method='ffill')['HER']
# Valor de la columna HER el 2016-02-01
accidentes['HER']['2016-02']

#### Gráfico de la Serie#####
plt.plot(ts2)
plt.title('Serie de heridos')

#### Estadísticas descriptivas
print(ts2.describe())
print(accidentes.describe()) #Para todas las variables

#### Graficando dos o más series al tiempo
accidentes[['ISE', 'IC', 'IPI']].plot(figsize=(10, 8), fontsize=12)
accidentes[['ISE', 'HER']].plot(figsize=(10, 8), fontsize=12)
## Otra forma
plt.plot(accidentes["IC"])
plt.plot(ts21, color='red')

### Ejemplos de cambio de fecha
pd.date_range(start='1/1/2018', end='1/08/2018')
pd.date_range(start='1/1/2018', periods=8)
pd.date_range(end='1/1/2018', periods=8)
pd.date_range(start='2018-04-24', end='2018-04-27', periods=3)
pd.date_range(start='1/1/2018', periods=5, freq='3M')
pd.date_range(start='2017-01-01', end='2017-01-04', closed='left')
pd.date_range(start='2017-01-01', end='2017-01-04', closed='right')



#########

colcapdata=data = pd.ExcelFile('/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/Colcap.xlsx')
print(colcapdata.sheet_names)
colcapdata=colcapdata.parse('Colcap')
retornos=np.log(colcapdata['ValorCOLCAP']).diff().dropna()
print(colcapdata)
colcapdata['Fecha']=pd.to_datetime(colcapdata['Fecha'])
print(colcapdata)
colcap=colcapdata.set_index('Fecha')
print(colcap)
plt.plot(colcap)
plt.title('Indice COLCAP')

