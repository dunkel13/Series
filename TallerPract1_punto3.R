##########################################################
### PUNTO 3
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
{
#####Simulación MA(1)#####
  set.seed(151)
  ruido=rnorm(n+l,0,sigma)
  MA1aux=rep(0,n+l)
  MA1aux
  for(j in 2:(n+l))
  {
    MA1aux[j]=theta*ruido[j-1]+ruido[j]
  }
  MA1=as.ts(MA1aux[l+1:n])
  plot(MA1)
  acf(MA1)
  ###
  FitAR::BoxCox(MA1) 
  forecast::BoxCox.lambda(MA1, method="guerrero", lower=0, upper=2)
  # como lambda es muy cercano a uno, no se hace la transformación de los datos
  ### Descomposición usando filtros de promedios móviles
  tMA1<-ts(MA1, frequency=9)
  desMA1=decompose(tMA1)
  plot(desMA1)
  tsMA1<- as.ts(as.vector(desMA1$random))
  #acf(MA1, type="correlation", na.action = na.pass)
  acf(tsMA1, type="correlation", na.action = na.pass)
  # como sabemos que la MA1 es estacionaria, en este ejercicio se visualiza que a pesar que no hay una componente estacional, se estima y por lo tanto se altera la componente estacionaria de la serie haciendo que se vaya a cero en un rezago superior a la serie MA1 original
  ### Descomposición usando suavizamiento exponencial
  HWtMA1=HoltWinters(tMA1,seasonal="additive")
  plot(HWtMA1)
  ajustadostMA1=fitted(HWtMA1)
  head(ajustadostMA1)
  Yt<-tMA1-ajustadostMA1[,2]-ajustadostMA1[,3]-ajustadostMA1[,4]
  tMA1_Est<-as.ts(as.vector(Yt))
  # la componente Yt es la componente "estacionaria" serie 
  par(mfrow=c(1,1))
  #plot(tMA1)
  plot(tMA1_Est)
  acf(tMA1_Est, type="correlation")
  }
