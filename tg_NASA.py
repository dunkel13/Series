# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 20:35:45 2019

@author: FM
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
tg_NASA=pd.read_csv('C:/Users/FAMILIA MORENO/Documents/FMpy/tgNASA.txt', delimiter=r"\s+", header=None, names=('Year', 'No_Smoothing', 'Lowess(5)'))
tg_NASA.head(10)
tg_NASA.tail(10)

ind = pd.date_range(start='1880', end='2019', freq='Y')
print(ind)
###########################
### TRANSFORMACIÓN BOX COX
###########################
tg_NASA.min()
bc_tg_NASA = pd.DataFrame(tg_NASA['No_Smoothing'] + 0.73) 
# MIN (No_Smoothing) = -0.48, EN [R]: minimum data value <= 0 so -min+0.25 added to all values, LUEGO -(-0.48)+0.25=0.73
print(bc_tg_NASA)
bc_tg_NASA = bc_tg_NASA.set_index(ind)
bc_ts_tgN = pd.Series(bc_tg_NASA['No_Smoothing'],index=ind)
print(bc_ts_tgN) 
plt.plot(bc_ts_tgN)
plt.show()
import scipy as sp
import scipy.stats ####En ocasiones puede funcionar la línea 46 sin ésta línea.
sp.stats.boxcox(bc_tg_NASA['No_Smoothing'],alpha=0.05) 
print(sp.stats.boxcox(bc_tg_NASA['No_Smoothing'],alpha=0.05))

###



tg_NASA = tg_NASA.set_index(ind)
ts_tgN = pd.Series(tg_NASA['No_Smoothing'],index=ind)
print(ts_tgN) 
plt.plot(ts_tgN)
plt.show()
#import statsmodels.api as smapi
#smapi.graphics.tsa.month_plot(tsAirP)
acf(ts_tgN,nlags=50,unbiased=False)
Grafico_acf_tgN = plot_acf(ts_tgN,lags=50,unbiased=False)
import scipy as sp
import scipy.stats ####En ocasiones puede funcionar la línea 46 sin ésta línea.
sp.stats.boxcox(tg_NASA['No_Smoothing'],alpha=0.05) 
print(sp.stats.boxcox(ts_tgN['No_Smoothing'],alpha=0.05))
np.minimum(tg_NASA['No_Smoothing'])
print(tg_NASA['No_Smoothing'])

print(ts_tgN)
