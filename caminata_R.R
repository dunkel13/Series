##########################################################################
####################### Tarea 1: Caminata aleatoria ######################
##########################################################################


######### Usando for #########
set.seed(0)
muestra<-rnorm(200, mean=0, sd=1)
st=matrix(data=NA, nrow=200, ncol=1)
st[1]=muestra[1]
for(i in 2:200){
  st[i]=muestra[i]+st[i-1]
}
st
#View(cbind(muestra, st))
tiempo=seq(from=1, to=200, by=1)
plot(tiempo, st, type="l", xlab="t", ylab="St", main="Caminata aleatoria")

######### Usando funci�n ###########

caminata<-function(t, muestra){
  st=matrix(data=NA, nrow=t, ncol=1)
  st[1]=muestra[1]
  for(i in 2:t){
    st[i]=muestra[i]+st[i-1]
  }
  return(st)
}
caminata(200, muestra)

