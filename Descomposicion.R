####Vamos a hacer un análisis Inicial a la serie de pasajeros#####
####Un análisis similar deberá hacerse para las series ISE y ACC de la
####Base de datos Base_Accidentes.xlsx

######Base de Pasajeros###
data("AirPassengers")
plot(AirPassengers)
#####Transformación Box-Cox
library(FitAR)
library(forecast)
forecast::BoxCox.lambda(AirPassengers, method = "guerrero", lower = 0, upper = 2)  
##method="loglik"
FitAR::BoxCox(AirPassengers)

air.arima<-arima(AirPassengers, c(0,1,1), seasonal=list(order=c(0,1,1), period=12))
FitAR::BoxCox(air.arima)
lAirPass=log(AirPassengers)
par(mfrow=c(2,1))
plot(AirPassengers)
plot(lAirPass)


######Descomposición usando promedios Móviles
deslAirPass=decompose(lAirPass)
plot(deslAirPass)
deslAirPass


####Descompoisición usando suavizamiento exponencial
HWAP=HoltWinters(lAirPass,seasonal="additive")
plot(HWAP)
ajustados=fitted(HWAP)
plot(ajustados)
ajustados


####Diferenciación
ldAirPass=diff(lAirPass,lag=1,differences = 1)###Differences indica número de diferencia
