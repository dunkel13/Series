#library(tis)
data("AirPassengers")
plot(AirPassengers)
monthplot(AirPassengers)
#tierChart(AirPassengers)
lAirP=log(AirPassengers)
plot(lAirP)
acf(lAirP)
dlAirp=diff(lAirP)
plot(dlAirp)
acf(dlAirp,lag.max=48)
monthplot(dlAirp)
sdlAirp=diff(dlAirp,lag=12)
plot(sdlAirp)
monthplot(sdlAirp)
acf(sdlAirp,lag.max=48)
pacf(sdlAirp,lag.max=48)
salidaAR12=arima(sdlAirp,order=c(12,0,0))
salidaMA12=arima(sdlAirp,order=c(0,0,12))
salidaAR12
salidaMA12
library(lmtest)
coeftest(salidaAR12)
salidaAR12fixed=arima(sdlAirp,order=c(12,0,0),include.mean = FALSE,fixed=c(NA,0,0,0,0,0,0,0,0,0,0,NA),method = c("CSS-ML"))
coeftest(salidaAR12fixed)
salidaAR12fixed
attributes(salidaAR12fixed)

#####Pronosticos
library(forecast)
salidaMA12fixed=Arima(sdlAirp,order=c(0,0,12),include.mean = FALSE,fixed=c(NA,0,0,0,0,0,0,0,0,0,0,NA),method = c("CSS-ML"))
coeftest(salidaMA12fixed)

PronosticosAR12=forecast(salidaAR12fixed,h=12,level=0.95)
PronosticosMA12=forecast(salidaMA12fixed,h=12,level=0.95)
plot(PronosticosAR12)
plot(PronosticosMA12)



####Simulación de modelos ARMA####
Tlength=200
arimaej=arima.sim(list(order = c(1,0,1),ar = c(0.7),ma=c(0.6)), n = Tlength)
plot(arimaej,main='ARMA(1,1)')
library(forecast)
library(lmtest)
acf(arimaej,ci.type="ma")
pacf(arimaej)
salidaest=Arima(arimaej,order=c(1,0,1),include.mean = FALSE)
salidaest
coeftest(salidaest)
auto.arima(arimaej,max.p = 3,max.q = 3, start.p = 0, start.q = 0, ic="bic")
###Residuales####
residuales=salidaest$residuals
acf(residuales)
pacf(residuales)
jarque.bera.test(residuales)
#Box.test(x, lag = 1, type = c("Box-Pierce", "Ljung-Box"), fitdf = 0)
Box.test(residuales, lag = (length(residuales)/4), type = "Ljung-Box", fitdf = 2)


#####Estadísticas Cusum####
res=residuales
cum=cumsum(res)/sd(res)
N=length(res)
cumq=cumsum(res^2)/sum(res^2)
Af=0.948 ###Cuantil del 95% para la estadística cusum
co=0.14422####Valor del cuantil aproximado para cusumsq para n/2=200
LS=Af*sqrt(N)+2*Af*c(1:length(res))/sqrt(N)
LI=-LS
LQS=co+(1:length(res))/N
LQI=-co+(1:length(res))/N
plot(cum,type="l",ylim=c(min(LI),max(LS)),xlab="t",ylab="",main="CUSUM")
lines(LS,type="S",col="red")
lines(LI,type="S",col="red")
plot(cumq,type="l",xlab="t",ylab="",main="CUSUMSQ")                      
lines(LQS,type="S",col="red")                                                                           
lines(LQI,type="S",col="red")

