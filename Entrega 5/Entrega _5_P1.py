# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 09:22:49 2020

@author: Matias
"""

#J3 corrige la forma de "pera" de la tierra que tiene por debajo.
#J2 corrige el atachamiento de los polos.
#ARRASTRE ATMOSFERICO.

import numpy as np
from scipy.integrate import odeint
from EOF import utc2time, leer_eof
import matplotlib.pylab as plt

#PARAMETROS
#Radio tierra:
radio_tierra= 6371000 #[m]
H = 700000 #[m]
r0 = radio_tierra + H
#Constante de gravitacion universal:
G=6.674*10**-11 #[N*m/kg^2]
#Masa Tierra:
MT=5.972*10**24 #[Kg]
GMT = 3.986e14
#Rotacion Tierra:
W=-7.2921150e-5 #[rad/s]
J2 = 1.75553*10**10*1000**5
J3 = -2.61913*10**11*1000**6

mejora = 0 #Aqui corro las prediciones reales, con J2 y con J2+J3.

def Satelite(z,t):
    #Matriz rotacion:
    RT = np.array([
         [np.cos(W*t), np.sin(W*t), 0],
         [-np.sin(W*t), np.cos(W*t), 0],
         [0, 0, 1]
         ])
    R1 = W*np.array([
         [-np.sin(W*t), np.cos(W*t), 0],
         [-np.cos(W*t), -np.sin(W*t), 0],
         [0, 0, 0]
         ])
    R2 = W**2*np.array([
         [-np.cos(W*t), -np.sin(W*t), 0],
         [np.sin(W*t), -np.cos(W*t), 0],
         [0, 0, 0]
         ])
   
    
    #Empezamos a armar correcciones
    x = z[0:3]
    xpt = z[3:6]
    r = np.sqrt(np.dot(x,x))
    
    #Para trabajar ecuaciones de J2 y J3
    xvar = RT@x
    Norma_r = xvar/r
    
    #Simplificaciones:
    z2 = xvar[2]**2
    cuacs = xvar[0]**2 + xvar[1]**2
    F_J2 = J2*xvar/r**7
    #J2:
    F_J2 = J2*xvar/r**7   
    F_J2[0] = F_J2[0]*(6*z2 - 3/2*cuacs)
    F_J2[1] = F_J2[1]*(6*z2 - 3/2*cuacs)
    F_J2[2] = F_J2[2]*(3*z2 - 9/2*cuacs)
    #J3
    F_J3 = np.zeros(3)
    F_J3 = J3*xvar[0]*xvar[2]/r**9*(10*z2 - 15/2*cuacs)
    F_J3 = J3*xvar[1]*xvar[2]/r**9*(10*z2 - 15/2*cuacs)
    F_J3 = J3/r**9*(4*z2*(z2 - 3*cuacs) + 3/2*cuacs**2)
             
    zp=np.zeros(6)     
    zp[0:3] = xpt
    #Para no generar 3 archivos, creo un bloque if para evaluar
    #acorde voy sumando mejoras.
    if mejora == 0:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2-(2*R1@xpt + R2@x))
    elif mejora == 1:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2 + F_J2 -(2*R1@xpt + R2@x))
    elif mejora == 2:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2 + F_J2 + F_J3 -(2*R1@xpt + R2@x))
        
            
    return zp


archivo = "S1B_OPER_AUX_POEORB_OPOD_20200818T110748_V20200728T225942_20200730T005942.EOF"
t_D, x_D, y_D, z_D, vx_D, vy_D, vz_D = leer_eof(archivo)
z0 = np.array([x_D[0],y_D[0],z_D[0],vx_D[0],vy_D[0],vz_D[0]])
Tmax = max(t_D)
t = t_D

sol = odeint(Satelite,z0,t)  
xg=sol[:,0]
yg=sol[:,1]
zg=sol[:,2]

plt.figure()
plt.subplot(3,1,1)
plt.plot(t/3600,x_D/1000)
plt.plot(t/3600,xg/1000)
plt.ylabel("$X$ (Km)")
plt.subplot(3,1,2)
plt.plot(t/3600,y_D/1000)
plt.plot(t/3600,yg/1000)
plt.ylabel("$Y$ (Km)")
plt.subplot(3,1,3)
plt.plot(t/3600,z_D/1000,label= "real")
plt.plot(t/3600,zg/1000,label="predicha")
plt.tight_layout(rect=[0,0.03,1,0.97])
plt.ylabel("$Z$ (Km)")
plt.suptitle("Posición")
plt.xlabel("Tiempo, $t$ (horas)")
#plt.savefig("Posicion Real")
plt.show()

