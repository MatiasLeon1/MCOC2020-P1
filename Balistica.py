# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:45:03 2020

@author: Matias
"""

import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt 
#Parametros
ro = 1.225        #kg/m3
cd = 0.47         #coeficiente drag
cm = 0.01
inch = 2.54*cm    #Lo paso a cm
D = 8.5*inch      #Diametro
r = D/2           #Radio
A = sp.pi*r**2    #Area
CD = 0.5*ro*cd*A
g = 9.81          #m/s2
m = 15 #kg
V = 5   #viento en metros x segundo

def Bala(z,t):
    zp=sp.zeros(4)
    
    zp[0] = z[2]
    zp[1] = z[3]
    
    v = z[2:4]  #saca ultimos 2 componentes
    v[0]= v[0]- V
    v2=sp.dot(v,v)
    vnorm = sp.sqrt(v2)
    FD = -CD*v2*v/(vnorm)
    
    zp[2] = FD[0]/m
    zp[3] = FD[1]/m -g
    
    return zp

V_List=[0,10,20]
for V in V_List:
    
    #Vector tiempo
    t = sp.linspace(0,10,1001)

    #Parte en el orogen con misma velocodad en x e y
    vi=100*1000/3600
    z0 = sp.array([0,0,vi,vi])

    sol = odeint(Bala, z0,t)  

    x=sol[:,0]
    y=sol[:,1]
    plt.ylim(0,50)
    plt.xlim(0,150)    
    plt.plot(x,y)
    
plt.title("Trayectoria para distintos vientos")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.grid(True)
plt.legend(["V = 0 m/s", "V = 10 m/s", "V = 20 m/s"])    
plt.figure()
plt.savefig("Balistica_1.png", Bbox_inches = "tight")