###Optimización
require(graphics)

fr <- function(x) {   ## Rosenbrock Banana function
  x1 <- x[1]
  x2 <- x[2]
  100 * (x2 - x1 * x1)^2 + (1 - x1)^2
}
grr <- function(x) { ## Gradient of 'fr'
  x1 <- x[1]
  x2 <- x[2]
  c(-400 * x1 * (x2 - x1 * x1) - 2 * (1 - x1),
    200 *      (x2 - x1 * x1))
}
optim(c(-1.2,1), fr)
(res <- optim(c(-1.2,1), fr, grr, method = "BFGS"))


#####ml estimation for ar(1) model, yt=c+phi*yt-1+et###
c=0
phi=0.7
sigma=1
T=200
inic=50
Tmax=T+inic
xt=rep(0,Tmax)
for(j in 2:Tmax)
   { 
    xt[j]=c+phi*xt[j-1]+rnorm(1,0,sigma)
}
yt=ts(xt[(inic+1):Tmax])
plot.ts(yt)
likelyar=function(x){
         serie=yt
         cest=0
         #cest=x[1]
         phiest=x[1]
         sigma2est=x[2]
         Tlength=length(serie)
        -(-(Tlength-1)*log(2*pi)/2-(Tlength-1)*log(sigma2est)/2-(1/(2*sigma2est))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])^2))
}
#likelyar(c(1,0.5,1))
likelyar(c(phi,sigma^2))
grlikelyar= function(x) { 
  #x=c(0.8,0.3,0.7)
  #x=c(0.3,0.7)
  serie=yt
  #cest=x[1]
  cest=0
  phiest=x[1]
  sigma2est=x[2]
  Tlength=length(serie)
  c(-((1/(sigma2est))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])*serie[1:(Tlength-1)])),-(-(1/2)*(Tlength-1)*(1/sigma2est)+(1/(2*(sigma2est^2)))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])^2)))
  #c((1/(sigma2est))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])),(1/(sigma2est))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])*serie[1:(Tlength-1)]),-(1/2)*(Tlength-1)*(1/sigma2est)+(1/(sigma2est^2))*sum((serie[2:Tlength]-cest-phiest*serie[1:(Tlength-1)])^2))
}
likelyar(c(phi,sigma^2))
grlikelyar(c(phi,sigma^2))

optim(c(0.3,0.7), likelyar,grlikelyar ,method = "BFGS",hessian=TRUE, control=list(trace=TRUE))
#, lower=c(-5,-0.9,0), upper=c(5,0.9,10000)


###Gradiente Descendiente###
library(gradDescent)
