## Entrega 5

### P1
![P1 Posicion Real](https://user-images.githubusercontent.com/43649125/92336207-a696e180-f074-11ea-8d1a-38d80b2cff21.png)

### P2
![Deriva odeint_eulerint](https://user-images.githubusercontent.com/43649125/92336706-cb418800-f079-11ea-94ec-f38cc2d5e018.png)

El grafico anterior corresponde a la deriva de Eulerint y Odeint en funcion del tiempo, utilizando `Nsubdiviciones = 1`.

Vemos que tanto Odeint como Eulerint comienzan desde el mismo punto, sin embargo su deriva cambia bastante desde el inicio hasta el termino del tiempo. Eulerint deriva de Odeint en `19.127,2 Kilometros`. Aplicando un `perf_counter()` para ambas funciones obtenemos que Odeint se demora `1.3171 [s]` en generar los resultados, v/s Eulerint que tarda `3.7098 [s]` en producir los resultados.

### P3

Para esta pregunta generé 500 subdivisiones y el tiempo de ejecucion fue de 57:36 segundos en mi PC. Se adjunta grafico con los resultados.
![Deriva Nsub_500](https://user-images.githubusercontent.com/43649125/92339255-92aaaa00-f08b-11ea-8b02-ef9f1a069550.png)

Dado que la capacidad de mi computador no me permite iterar hasta encontrar la solucion requerida es que pregunte a distintos compañeros de clase que valores obtuvieron ellos. Llegue a la conclusion de que para poder llegar a un error menor al 1% hace falta hacer mas de 10000 subdivisiones.
