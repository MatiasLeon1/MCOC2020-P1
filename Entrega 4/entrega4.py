# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 15:35:26 2020

@author: Matias
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pylab as plt
import sympy as sp

#PARAMETROS
#x(0) = 1
#xp(0) = 1

m = 1 #Kg
f = 1 #Hz
eps = 0.2 #Epsilon
w = 2*np.pi*f
k = m*w**2
c = 2*eps*w*m


#Variables alfa, beta,C1 y C2 de la solucion de la EDO
#Que hay que determinar
x=sp.Function('x')
t=sp.symbols('t')
eq=sp.Eq(x(t).diff(t,2)+c*x(t).diff(t)+k*x(t),0)

#X(t)
sol=sp.dsolve(eq,x(t)).rhs 
#XP(t)
sold=sp.diff(sol,t)

#Viendo Parametros
#x(0)
x0=1
condicion_0 = sp.Eq(sol.subs(t,0),x0)
#xp(0)
xderiv_0=1
condicion_1=sp.Eq(sold.subs(t,0),xderiv_0)

c1c2 = list(sp.linsolve([condicion_0,condicion_1],sp.var('C1,C2')))


def eulerint(harmonic,z0,t,Nsub=1):
    Nt = len(t)
    Ndim = len(z0)
    
    z = np.zeros((Nt,Ndim))
    z[0,:]=z0
    
    #z(i+1)=zp:i*dt+z_i
    for i in range(1,Nt):
        t_anterior = t[i-1]
        dt = (t[i]-t[i-1])/Nsub
        z_temp = z[i-1,:].copy() 
        for k in range(Nsub):
            z_temp+= dt*harmonic(z_temp,t_anterior+k*dt)
        z[i,:]=z_temp
          
    return z

def harmonic(z,t):
    zp = np.zeros(2)
    zp[0] = z[1]
    zp[1] = -(k/m)*z[0] - (c/m)*z[1]
    
    return zp

alpha = -1.2566370614
beta = 6.1562391847
C1 = 1
C2 = 0.3665609788

#Reemplazando para calcular oscilador armonico
z0 = np.array([1,1])
t = np.linspace(0, 4., 100)

z_odeint = odeint(harmonic,z0,t)
ode = z_odeint[:,0]

z_real = np.exp(alpha*t)*(np.cos(beta*t)*C1+np.sin(beta*t)*C2)

z_euler_sd_1 = eulerint(harmonic,z0,t,Nsub=1)
euler1 = z_euler_sd_1[:,0]

z_euler_sd_10 = eulerint(harmonic,z0,t,Nsub=10)
euler10 = z_euler_sd_10[:,0]

z_euler_sd_100 = eulerint(harmonic,z0,t,Nsub=100)
euler100 = z_euler_sd_100[:,0]

plt.figure()
plt.plot(t,z_real,label="real",linewidth=2,color="k")
plt.plot(t,ode,label="odeint",color="b",linewidth=1)
plt.plot(t,euler1,"g--",label="eulerint (Nsub=1)")
plt.plot(t,euler10,"r--",label="eulerint (Nsub=10)")
plt.plot(t,euler100,"--",label="eulerint (Nsub=100)",color="orange")
plt.grid()

plt.title("Estudio convergencia metodo de Euler")
plt.xlabel("Tiempo [s]")
plt.ylabel("Posicion [m]")
plt.legend()
plt.savefig("Entrega_4")