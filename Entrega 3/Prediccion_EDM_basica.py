# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 09:25:54 2020

@author: Matias
"""

import numpy as np
from scipy.integrate import odeint

#PARAMETROS
#Radio tierra:
r= 7071000 #[m]
#Constante de gravitacion universal:
G=6.674*10**-11 #[N*m/kg^2]
#Masa Tierra:
MT=5.972*10**24 #[Kg]
#Rotacion Tierra:
W=7.27*10**-5 #[rad/s]


def Satelite(z,t):
    zp=np.zeros(6)
    #Matriz rotacion:
    RT = np.array([
         [np.cos(W*t), np.sin(W*t), 0],
         [-np.sin(W*t), np.cos(W*t), 0],
         [0, 0, 1]
         ])
    R1 = W*np.array([
         [-np.sin(W*t), -np.cos(W*t), 0],
         [np.cos(W*t), -np.sin(W*t), 0],
         [0, 0, 0]
         ])
    R2 = W**2*np.array([
         [-np.cos(W*t), np.sin(W*t), 0],
         [-np.sin(W*t), -np.cos(W*t), 0],
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


from datetime import datetime
ti = "2020-07-28T22:59:42.000000"
ti = ti.split("T")
ti = "{} {}".format(ti[0], ti[1])
ti = datetime.strptime(ti, "%Y-%m-%d %H:%M:%S.%f")
tf = "2020-07-30T00:59:42.000000"
tf = tf.split("T")
tf = "{} {}".format(tf[0], tf[1])
tf = datetime.strptime(tf, "%Y-%m-%d %H:%M:%S.%f")

deltaT = (tf - ti).total_seconds()

#PUNTO INICIAL S1B_OPER_AUX
#<TAI>TAI=2020-07-28T23:00:19.000000</TAI>
##<UTC>UTC=2020-07-28T22:59:42.000000</UTC>
#<UT1>UT1=2020-07-28T22:59:41.788840</UT1>
#<Absolute_Orbit>+22677</Absolute_Orbit>
##<X unit="m">2057735.247194</X>
##<Y unit="m">-6459802.571744</Y>
##<Z unit="m">-2037501.319184</Z>
##<VX unit="m/s">-886.585360</VX>
##<VY unit="m/s">-2517.114487</VY>
##<VZ unit="m/s">7108.167902</VZ>

xi= 2057735.247194
yi=-6459802.571744
zi=-2037501.319184
vx_i=-886.585360
vy_i=-2517.114487 #m/s #Velocidad Exacta= 7507,798
vz_i=7108.167902 #m/s

z0 = np.array([xi,yi,zi,vx_i,vy_i,vz_i])

#PUNTO FINAL S1B_OPER_AUX:
#<TAI>TAI=2020-07-30T01:00:19.000000</TAI>
##<UTC>UTC=2020-07-30T00:59:42.000000</UTC>
#<UT1>UT1=2020-07-30T00:59:41.789813</UT1>
#<Absolute_Orbit>+22693</Absolute_Orbit>
##<X unit="m">952282.661396</X>
##<Y unit="m">-343181.132340</Y>
##<Z unit="m">-7009676.903991</Z>
##<VX unit="m/s">-1952.284695</VX>
##<VY unit="m/s">-7307.849847</VY>
##<VZ unit="m/s">92.723677</VZ>
xf= 952282.661396
yf=-343181.132340
zf=-7009676.903991
vx_f= -1952.284695
vy_f= -7307.849847
vz_f= 92.723677

#Vector tiempo
t = np.linspace(0,deltaT,9361)
sol = odeint(Satelite,z0,t)  
x=sol[:,:]

#Norma_i = np.sqrt(sol[-1,0]**2+sol[-1,1]**2+sol[-1,2]**2)
#Norma_f = np.sqrt(xf**2+yf**2+zf**2)
#delta_Norma = Norma_f - Norma_i
Norma= np.sqrt((xf-sol[-1,0])**2 + (yf-sol[-1,1])**2 + (zf-sol[-1,2])**2)
#y=sol[:,1]
#z=sol[:,2]
pos_final= np.array([xf,yf,zf,vx_f,vy_f,vz_f]) - sol[-1]
Norma1= np.sqrt((pos_final[0])**2 + (pos_final[1])**2 + (pos_final[2])**2)
for en in pos_final:
    print(f"{en} [metros]")
print("")
print(f"Deriva en metros: {Norma1} [metros]")
