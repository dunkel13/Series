##########################################################
### pUNTO 3
##########################################################
{
  n=200 #Tamaño de la serie
  l=50 #condiciones iniciales
  theta=-0.5 
  phi=0.5
  sigma=2
  ###Simulación IID####
  set.seed(114)
  serieIID=as.ts(rnorm(n,0,2))
  plot(serieIID,main='IID')
  acf(serieIID)
  ### Descomposición usando filtros de promedios móviles
  FitAR::BoxCox(serieIID) 
  forecast::BoxCox.lambda(serieIID, method="guerrero", lower=0, upper=2)
  # como lambda es muy cercano a uno, no se hace la transformación de los datos
  tIID<-ts(serieIID, frequency=10)
  ### Descomposición usando filtros de promedios móviles
  desIID=decompose(tIID)
  plot(desIID)
  tsIID<- as.ts(as.vector(desIID$random))
  acf(serieIID, type="correlation", na.action = na.pass)
  acf(tsIID, type="correlation", na.action = na.pass)
  # como sabemos que la serieIID es estacionaria, en este ejercicio se visualiza que a pesar que no hay una componente estacional, se estima y por lo tanto se altera la componente estacionaria de la serie
  ### Descomposición usando suavizamiento exponencial
  HWtIID=HoltWinters(tIID,seasonal="additive")
  plot(HWtIID)
  ajustadostIID=fitted(HWtIID)
  head(ajustadostIID)
  Yt<-tIID-ajustadostIID[,2]-ajustadostIID[,3]-ajustadostIID[,4]
  tIID_Est<-as.ts(as.vector(Yt))
  # la componente Yt es la componente "estacionaria" serie 
  par(mfrow=c(1,1))
  #plot(tIID)
  plot(tIID_Est)
  acf(tIID_Est, type="correlation")
  # como sabemos que la serieIID es estacionaria, en este ejercicio se visualiza que a pesar que no hay una componente estacional, se estima y por lo tanto se altera la componente estacionaria de la serie
}
