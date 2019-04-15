import numpy as np
import matplotlib.pyplot as ptl
FACV=np.zeros(50)
np.random.seed(2)
X=np.random.normal(0, 1, 50)

def cov_auto_samp(X,delta):
    N = len(X)
    Xs = np.average(X)
    autoCov = 0.0
    times = 0.0
    for i in np.arange(0, N-delta):
        autoCov += (X[i+delta]-Xs)*(X[i]-Xs)
        times +=1
    return autoCov/times

for j in range(0, 50):
        FACV[j]=cov_auto_samp(X,j)
        
FACV[0]
h=np.arange(0,50)
h
ptl.plot(h,FACV,'ko--')
ptl.plot(h,X,'ko-')
