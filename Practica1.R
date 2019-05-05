####Importación base de datos 
####y creación de un objeto de serie de tiempo.

library(readr)
library(readxl)

###Importaci?n de diferentes bases de datos
#as? como su conversi?n a un objeto de series de tiempo
#por medio de la funci?n "ts" 

AirPassengers <- read_csv("/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/AirPassengers.csv", 
                               col_types = cols(Month = col_date(format = "%Y-%m")))
AirPassengers
## Serie mensual
seriesAP=ts(AirPassengers$NPassengers,start=c(1949,1),frequency=12)
seriesAP
plot(seriesAP, main="Air Passengers", xlab="Fecha")
monthplot(seriesAP)

## Serie Trimestral
seriesAP_tri=ts(AirPassengers$NPassengers,start=c(1949,1),frequency=4)
seriesAP_tri
plot(seriesAP_tri, main="Air Passengers")
## Serie Trimestral indicando fecha final 
seriesAP_tri=ts(AirPassengers$NPassengers,start=c(1949,1), end=c(1960,12),frequency=12)
seriesAP_tri
plot(seriesAP_tri, main="Air Passengers")
## Estad?sticas descriptivas
summary(seriesAP)


## Importaci?n de base de datos con varias variables
Datos2 <- read_excel("/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/Base_Accidentes.xlsx")
View(Datos2)
## Serie con frecuencia mensual
HER=ts(Datos2$HER,start=c(2005,1),end=c(2018,7),frequency=12)
HER
IC=ts(Datos2$IC,start=c(2005,1),end=c(2018,7),frequency=12)
IC
ISE=ts(Datos2$ISE,start=c(2005,1),end=c(2018,7),frequency=12)
ISE
plot(HER, main="Número de heridos")
## Graficar varias series al tiempo
plot(ISE, main="",ylab="",xlab="Fecha", ylim=c(60,300))
lines(IC, main="", col="red",ylab="IC",xlab="Fecha")
## Empleando varias ventanas
par(mfrow=c(2,1))
plot(ISE, main="",ylab="ISE",xlab="Fecha")
plot(IC, main="", col="red",ylab="IC",xlab="Fecha")

## Estad?sticas descriptivas
summary(HER)
summary(Datos2[,c(3:21)])

Colcap <- read_excel("/Documentos Mac Book Sergio/Time Series/Series de Tiempo Univariadas 2019-I/Bases/Colcap.xlsx", 
                       sheet = "Colcap", col_types = c("date","numeric"))
fechas=as.Date(Colcap$Fecha)
colcap=xts(Colcap$ValorCOLCAP,order.by = fechas)
plot(colcap)
retornos=diff(log(colcap))[2:length(colcap)]
retornos
plot(retornos)
########

#########Descomposición#####
descomposicionSeriesAP=decompose(seriesAP)   ###Usando Filtros de promedios móviles###

plot(descomposicionSeriesAP)

HWAP=HoltWinters(seriesAP,seasonal="additive")
plot(HWAP)
ajustadosSeriesAP=fitted(HWAP)
ajustadosSeriesAP
plot(ajustadosSeriesAP)

SerieAPd=diff(seriesAP,lag=1)###Diferencia Ordinaria
plot(SerieAPd)
SerieAPdD=diff(SerieAPd,lag=12) #####Diferencia Estacional
plot(SerieAPdD)
