# MCOC2020-P1

# Entrega 1
![Balistica_1](https://user-images.githubusercontent.com/43649125/91117356-64c17080-e65c-11ea-8a24-811a1405d748.png)

# Entrega 2

### Ecuacion de espacio del sistema:
![CodeCogsEqn](https://user-images.githubusercontent.com/43649125/91514637-41453280-e8b5-11ea-902c-76adefc0a3c4.gif)

Suponiendo que el satelite Sentinel 1-A esta orbitando a 700 Km sobre la superficie terrestre, utilice la formula de velocidad orbital `Vorb = (GMT/r^2)^1/2` para encontrar la velocidad minima que debia poseer el satelite para mantenerse en orbita. 
Siendo G la constante de gravitacion universal, MT la masa de la Tierra y r el radio de la orbita. Cnosiderando lo anterior, el satelite Sentinel 1-A debe poseer una velocidad minima `Vt = 7507,798 [m/s]` para mantenerse en orbita. A modo de poseen un margen de error y no trabajar al limite, definí la velocidad de orbita del satelite en `Vt'= 7510 [m/s]`.
Dado que la fuerza de gravedad es una fuerza de aceleración centripeta, esta actua sobre cuerpos en movimiento en trayectorias curvilineas con paradero final el centro de la circunferencia. Para poder hacer gravitar un objeto, se debe tomar en cuenta este tipo de fuerzas y aplicar la ecuacion anterior para mantenerlo orbitando.

A continuacion se presenta un grafico que muestra 2 orbitas realizadas por el satelite Sentinel 1-A, en un tiempo de 10.775 [s] y a una velocidad Vt':

![2 ORBITAS SATELITE](https://user-images.githubusercontent.com/43649125/91513009-4e602280-e8b1-11ea-962d-6a1ee6c847f7.png)

A continuación se presenta un grafico de historias de tiempo para las variables X, Y, Z correspondientes a 2 orbitas completas:

![Historias de tiempo](https://user-images.githubusercontent.com/43649125/91513017-51f3a980-e8b1-11ea-9eda-02b8b710c39a.png)

# Entrega 5

## P1
![P1 Posicion Real](https://user-images.githubusercontent.com/43649125/92336207-a696e180-f074-11ea-8d1a-38d80b2cff21.png)

## P2
![REAL](https://user-images.githubusercontent.com/43649125/92341206-5e3aec00-f093-11ea-98e8-d79daa0593bc.png)


El grafico anterior corresponde a la deriva de Eulerint y Odeint en funcion del tiempo, utilizando `Nsubdiviciones = 1`.

Vemos que tanto Odeint como Eulerint comienzan desde el mismo punto, sin embargo su deriva cambia bastante desde el inicio hasta el termino del tiempo. Eulerint deriva de Odeint en `19.187,2 Kilometros`. Aplicando un `perf_counter()` para ambas funciones obtenemos que Odeint se demora `1,3171 [s]` en generar los resultados, v/s Eulerint que tarda `3,7098 [s]` en producir los resultados.

## P3

Para esta pregunta generé 500 subdivisiones y el tiempo de ejecucion fue de 1687,0518 segundos en mi PC. Se adjunta grafico con los resultados.

![Deriva Nsub_500](https://user-images.githubusercontent.com/43649125/92339255-92aaaa00-f08b-11ea-8b02-ef9f1a069550.png)

La distancia maxima que aparece en el grafico esta errada. Eulerint alcanzo una distancia de `2515,042 Kilometros`. Al calcular el error restando la distancia de Euelerint con la distancia de Oilerint y dividiendo esto por la distancia de Oilerint, me dio que el `error fue de 816,28%`.Dado que la capacidad de mi computador no me permite iterar hasta encontrar la solucion requerida es que pregunte a distintos compañeros de clase que valores obtuvieron ellos. Llegue a la conclusion de que para poder llegar a un error menor al 1% hace falta hacer mas de 10.000 subdivisiones. De hecho, con 10.000 iteraciones recien se llega a un error aproximado de 5%

## P4

### Corrección J2
![Posicion J2](https://user-images.githubusercontent.com/43649125/92340143-a0fac500-f08f-11ea-99a0-c4a8236ecc60.png)

![P2 DIstancia real J2](https://user-images.githubusercontent.com/43649125/92340173-b839b280-f08f-11ea-9388-e5b9ce04fea8.png)

![REAL+J2](https://user-images.githubusercontent.com/43649125/92341204-5d09bf00-f093-11ea-9b0b-f37de286666b.png)

En este grafico se aprecia la deriva entre Odeint y Eulerint con la correccion J2. El tiempo de ejecución fue de `12,592 [s]`. La deriva es de `19392.2 Kilometros`

### Corrección J2 + J3
![Posicion J2+J3](https://user-images.githubusercontent.com/43649125/92340148-a3f5b580-f08f-11ea-9b18-093ffcd40598.png)

![P2 DIstancia real J2+J3](https://user-images.githubusercontent.com/43649125/92340177-ba9c0c80-f08f-11ea-8d62-4aa6fbb9cb25.png)

![REAL+J2+J3](https://user-images.githubusercontent.com/43649125/92341205-5e3aec00-f093-11ea-8b70-fe9ff5838b65.png)

En este grafico se aprecia la deriva entre Odeint y Eulerint con las correcciones J2 + J3. EL tiempo de ejecución fue de `7.915 [s]`. La deriva es de `19395.6 Kilometros`.
