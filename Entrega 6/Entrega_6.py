# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 23:23:53 2020

@author: Matias
"""

import numpy as np
from scipy.integrate import odeint
from EOF import utc2time, leer_eof
import matplotlib.pylab as plt
from time import perf_counter
t1 = perf_counter()
from datetime import datetime, timedelta
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

##
m = 1 #Kg
f = 1 #Hz
eps = 0.2 #Epsilon
w = 2*np.pi*f
k = m*w**2
c = 2*eps*w*m
##

mejora = 2

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
    if mejora == 0:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2-(2*R1@xpt + R2@x))
    elif mejora == 1:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2 + F_J2 -(2*R1@xpt + R2@x))
    elif mejora == 2:
        zp[3:6] = RT.T@(-GMT*Norma_r/r**2 + F_J2 + F_J3 -(2*R1@xpt + R2@x))
        
            
    return zp


from sys import argv
archivo = argv[1]
t_D, x_D, y_D, z_D, vx_D, vy_D, vz_D = leer_eof(archivo)
z0 = np.array([x_D[0],y_D[0],z_D[0],vx_D[0],vy_D[0],vz_D[0]])

eof_out = archivo.replace(".EOF",".PRED")

t = t_D

sol = odeint(Satelite,z0,t)  
x=sol[:,0]
y = sol[:,1]
z = sol[:,2]
vx = sol[:,3]
vy = sol[:,3]
vz = sol[:,3]

with open(eof_out, "w") as fout:
    
    Nt = len(t)
    fout.write("<?xml version=1.0 ?>\n")
    fout.write("<Earth_Explorer_File>\n")
    fout.write("    <Earth_Explorer_Header>\n")
    fout.write("        <Fixed_Header>\n")
    fout.write("            <File_Name>S1B_OPER_AUX_POEORB_OPOD_20200818T110748_V20200728T225942_20200730T005942</File_Name>\n")
    fout.write("            <File_Description>Precise Orbit Ephemerides (POE) Orbit File</File_Description>\n")
    fout.write("            <Notes></Notes>\n")
    fout.write("            <Mission>Sentinel-1B</Mission>\n")
    fout.write("            <File_Class>OPER</File_Class>\n")
    fout.write("            <File_Type>AUX_POEORB</File_Type>\n")
    fout.write("            <Validity_Period>\n")
    fout.write("                <Validity_Start>UTC=2020-07-28T22:59:42</Validity_Start>\n")
    fout.write("                <Validity_Stop>UTC=2020-07-30T00:59:42</Validity_Stop>\n")
    fout.write("            </Validity_Period>\n")
    fout.write("            <File_Version>0001</File_Version>\n")
    fout.write("            <Source>\n")
    fout.write("                <System>OPOD</System>\n")
    fout.write("                <Creator>OPOD</Creator>\n")
    fout.write("                <Creator_Version>0.0</Creator_Version>\n")
    fout.write("                <Creation_Date>UTC=2020-08-18T11:07:48</Creation_Date>\n")
    fout.write("            </Source>\n")
    fout.write("        </Fixed_Header>\n")
    fout.write("        <Variable_Header>\n")
    fout.write("            <Ref_Frame>EARTH_FIXED</Ref_Frame>\n")
    fout.write("            <Time_Reference>UTC</Time_Reference>\n")
    fout.write("        </Variable_Header>\n")
    fout.write("    </Earth_Explorer_Header>\n")
    fout.write("<Data_Block type=xml>\n")
    fout.write("    <List_of_OSVs count=9361>\n")
    for i in range(Nt):
        obj = datetime(2020,7,28,22,59,42,000000)
        fecha = (obj + timedelta(seconds=t[i])).strftime("%Y-%m-%dT%H:%M:%S.%f")
        fout.write("        <OSV>\n")
        fout.write(f"            <TAI>TAI={fecha}</TAI>\n")
        fout.write(f"            <UTC>UTC={fecha}</UTC>\n")
        fout.write(f"            <UT1>UT1={fecha}</UT1>\n")
        fout.write("            <Absolute_Orbit>+22677</Absolute_Orbit>\n")
        fout.write(f"            <X unit=\"m\">{x[i]}</X>\n")
        fout.write(f"            <Y unit=\"m\">{y[i]}</X>\n")
        fout.write(f"            <Z unit=\"m\">{z[i]}</X>\n")
        fout.write(f"            <VX unit=\"m/s\">{vx[i]}</X>\n")
        fout.write(f"            <VY unit=\"m/s\">{vy[i]}</X>\n")
        fout.write(f"            <VZ unit=\"m/s\">{vz[i]}</X>\n")
        fout.write("            <Quality>NOMINAL</Quality>\n")
        fout.write("        </OSV>\n")
    fout.write("    </List_of_OSVs>\n")
    fout.write("</Data_Block>\n")
    fout.write("</Earth_Explorer_File>\n")


