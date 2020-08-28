# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 09:25:54 2020

@author: Matias
"""

import scipy as sp
from scipy.integrate import odeint
import matplotlib.pylab as plt 
from mpl_toolkits import  mplot3d
#PARAMETROS
#Radio tierra:
r= 6371000 #[m]
#Constante de gravitacion universal:
G=6.674*10**-11 #[N*m/kg^2]
#Masa Tierra:
MT=5.972*10**24 #[Kg]
#Rotacion Tierra:
W=7.27*10**-5 #[rad/s]


def Satelite(z,t):
    zp=sp.zeros(6)
    #Matriz rotacion:
    RT = sp.array([
         [sp.cos(W*t), sp.sin(W*t), 0],
         [-sp.sin(W*t), sp.cos(W*t), 0],
         [0, 0, 1]
         ])
    R1 = sp.array([
         [-sp.sin(W*t)*W, -sp.cos(W*t)*W, 0],
         [sp.cos(W*t)*W, -sp.sin(W*t)*W, 0],
         [0, 0, 0]
         ])
    R2 = sp.array([
         [-sp.cos(W*t)*W**2, sp.sin(W*t)*W**2, 0],
         [-sp.sin(W*t)*W**2, -sp.cos(W*t)*W**2, 0],
         [0, 0, 0]
         ])
    
    #       [      ]
    #       [  z2  ]
    #dZ/dt= [      ]
    #       [z2'[x]]
    #       [z2'[y]]
    #       [z2'[z]]
    
    zp[0:3] = z[3:6]
    zp[3:6] = -G*MT*z[0:3]/r**3 - RT@(R2@z[0:3] + 2*R1@z[3:6])
        
    return zp

#Vector tiempo
t = sp.linspace(0,10775,1001)

#Parte en el orogen con misma velocodad en x e y
x= r+700*1000
y=0
z=0
vx=0
vy=7510 #m/s #Velocidad Exacta= 7507,798
vz=0 #m/s
z0 = sp.array([x,y,z,vx,vy,vz])

sol = odeint(Satelite,z0,t)  

x=sol[:,0]
y=sol[:,1]
z=sol[:,2]


#ploteo 3D
figure, ax = plt.subplots()
#ax = plt.axes(projection="3d")
#ax.plot3D(x1,y1,z1)

plt.figure(1)
Superficie = plt.Circle((0,0),6371000, color="#A6CAE0", alpha = 0.5, label = "Sup. Terrestre")
Atmosfera = plt.Circle((0,0),6451000, color= "r", alpha = 0.5, fill= False, label= "Atmosfera")
plt.xlim(-8500000,8000000)
plt.ylim(-8500000,8000000)
Leyenda_T= ax.legend(handles=[Atmosfera], loc= "lower left")
Leyenda_A= ax.legend(handles=[Superficie], loc= "upper left")
ax.add_artist(Atmosfera)
ax.add_artist(Superficie)
ax.add_artist(Leyenda_T)
ax.add_artist(Leyenda_A)

Y2=[-8*10**6,-6*10**6,-4*10**6,-2*10**6,0,2*10**6,4*10**6,6*10**6,8*10**6]
y2=["-8000","-6000","-4000","-2000","0","2000","4000","6000","8000"]

X2=[-8*10**6,-6*10**6,-4*10**6,-2*10**6,0,2*10**6,4*10**6,6*10**6,8*10**6]
x2=["-8000","-6000","-4000","-2000","0","2000","4000","6000","8000"]

plt.grid()
plt.title("Trayectoria de Satelite: 2 Orbitas")
plt.xlabel("X [Miles de Km]")
plt.yticks(Y2,y2)
plt.xticks(Y2,y2)
plt.ylabel("Y [Miles de Km]")
plt.plot(x,y, color= "b",label= "Orbita Satelite")
plt.plot(x,y)
plt.legend()
plt.savefig("2 ORBITAS SATELITE")


plt.figure(2)
Y2=[-8*10**6,-6*10**6,-4*10**6,-2*10**6,0,2*10**6,4*10**6,6*10**6,8*10**6]
y2=["-8000","-6000","-4000","-2000","0","2000","4000","6000","8000"]
plt.title("Historias de Tiempo: X(t) / Y(t) / Z(t)")
plt.plot(t,x, label= "X(t)")
plt.plot(t,y, label= "Y(t)")
plt.plot(t,z, label= "Z(t)")
plt.legend()
plt.yticks(Y2,y2)
plt.xlabel("X [Miles de Km]")
plt.ylabel("Y [Miles de Km]")
plt.grid()
plt.savefig("Grafico_XYZ")
