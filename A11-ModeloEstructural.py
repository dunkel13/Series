# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 12:13:23 2019

@author: acer
"""

### Estimación del modelo estructural para la serie GNP que posee tendencia y ciclo

# Datasets
####Debe instalarse pandas-datareader
#import pandas as pd
from pandas_datareader import DataReader
import numpy as np
import statsmodels.api as sm
import matplotlib.pylab as plt
import pandas as pd

# Obtención de los datos
start = '1948-01'
end = '2008-01'
us_gnp = DataReader('GNPC96', 'fred', start=start, end=end)
plt.plot(us_gnp)
log_gnp = np.log(us_gnp)
dates = us_gnp.index._mpl_repr()
plt.plot(log_gnp)

# Especificación del modelo
unrestricted_model = {
    'level': 'local linear trend', 'cycle': True, 'damped_cycle': True, 'stochastic_cycle': True
}

output_mod = sm.tsa.UnobservedComponents(log_gnp, **unrestricted_model)
output_res = output_mod.fit(method='powell', disp=False)
print(output_res.summary())

##Gráfico
fig = output_res.plot_components(legend_loc='lower right', figsize=(15, 9));

##Pronóstico
output_res.forecast(12)
log_gnp_forecast=output_res.get_prediction(start='2008-04-01', end='2009-01-01')

fig, ax = plt.subplots(figsize=(13, 3), dpi=300)
forecast = log_gnp_forecast.predicted_mean
forecast
ci = log_gnp_forecast.conf_int(alpha=0.5)
ci

arraypronosticosSTIC={'pronostico':forecast.values,'li':ci['lower GNPC96'].values,'ls':ci['upper GNPC96'].values}
indice=pd.date_range(start='2008-04-01',end='2009-01-01',freq='QS')
pronosticosSTIC=pd.DataFrame(data=arraypronosticosSTIC,index=indice)

#####Función inversa Box-Cox######
def inverse_boxcox(y, lambda_):
    return np.exp(y) if lambda_ == 0 else np.exp(np.log(lambda_ * y + 1) / lambda_)



####Se devuelve  a la escala original
for column in ['pronostico', 'li', 'ls']:
    pronosticosSTIC[column] = inverse_boxcox(pronosticosSTIC[column],0)
    
    
#######Gráfica de los pronósticos#####
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#Actual data
ax.plot(us_gnp.astype('float64'), '--', color="blue", label='data')
# Means
ax.plot(pronosticosSTIC['pronostico'], lw=1, color="black", alpha=0.5, label='Structural')
ax.fill_between(pronosticosSTIC['pronostico'].index, pronosticosSTIC.iloc[:, 1], pronosticosSTIC.iloc[:, 2], alpha=0.05)
ax.legend(loc='upper left')
plt.draw()

from sklearn.metrics import mean_squared_error

X = log_gnp.values
size = int(len(X) * 0.8)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predicciones = list()
for t in range(len(test)):
	output_mod = sm.tsa.UnobservedComponents(history, **unrestricted_model)
	modelo_fit = output_mod.fit(method='powell', disp=False)
	output = modelo_fit.forecast()  ####Especificar los pasos adelante
	yhat = output[0]
	predicciones.append(np.exp(yhat))
	obs = test[t]
	history.append(obs)
	print('Predicción=%f, Esperado=%f' % (np.exp(yhat), np.exp(obs)))
error = mean_squared_error(np.exp(test), predicciones)
print('ECM: %.3f' % error)
