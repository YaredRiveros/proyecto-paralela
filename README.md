# proyecto-paralela

## Compilación y ejecución
Como indica en el enunciado, en este proyecto trabajaremos sin gpu. Para ello, el código proporcionado se utilizará del siguiente modo:
- Compilar: make cpu-4th
- Ejecutar: mpirun -np=<num_procesos> ./cpu-4th

Para cambiar el tamaño del problema, se debe de ejecutar el siguiente comando: 
./gen-plum.exe <n> <np>

, de tal manera que el tamaño del problema sera N = n*np(kb/np), donde kb=1024.

## Item A: PRAM y complejidad teórica

### PRAM
El PRAM lo puede encontrar en ItemA/PRAM.cpp. En éste comentamos la compleijidad de cada operación a detalle.

### Complejidad teórica

OJO: a pesar de que el código contenga directiva pragma omp, el código no es híbrido (solo tiene MPI).

Utilizando el PRAM realizado, la complejidad teórica a la que llegamos es 
T_p(n,p) = O(n/p) + O(n) + O(n^2/p) + O(log(p)*(alpha+n*beta)) + O(n)

= O(n^2/p) + O(nlog(p))


## Item B: Medición de tiempo y comparación con curva teórica

 Realizamos la medición de tiempos y anotamos los resultados en el achivo ItemB/experimentacion.xlsx. Luego, graficamos las curvas en ItemB/graficos.py. Al finalizar, obtuvimos los siguientes resultados:

![comparacion_8k](ItemB/sinConstante/comparacion_8k.png)

![comparacion_9k](ItemB/sinConstante/comparacion_9k.png)

![comparacion_16k](ItemB/sinConstante/comparacion_16k.png)

Se valida la relación entre las curvas teórica y experimental obtenidas, pues se observa que una siempre es proporcional a otra. Para suporponer la curva teórica sobre la experimental lo más posible utilizamos mínimos cuadrados para hallar la constante de proporcionalidad y obtuvimos los siguientes resultados:

![comparacion_8k](ItemB/conConstante/comparacion_8k.png)

![comparacion_9k](ItemB/conConstante/comparacion_9k.png)

![comparacion_16k](ItemB/conConstante/comparacion_16k.png)

Note que aún existe una ligera diferencia entre las curvas teóricas y experimentales. Esto puede deberse a que en la complejidad teórica no consideramos varios bucles lineales presentes en el código original, lo que provoca que la curva teórica disminuya más rápidamente con p que la experimental.

## Item C: Medición de velocidad para distintos valores de n y p

Se utilizó el cálculo de la velocidad en Flops/s que ya estaba implementada en el código (se calcula como la división del número de flops entre el tiempo de ejecución total del algoritmo) para medir las curvas de velocidad para distintos números de procesos dado un tamaño del problema n.

Además, en cada gráfica se incluye la curva de velocidad ideal, que se calcula como la velocidad para un n cualquiera y p=1 multiplicada por el número de procesos utilizados. Esto asegura que estemos asumiendo que la velocidad escala directamente proporcional a p y se genere una recta.

- Sin escala logarítmica:

![itemc_sinEscala](Itemc/comparacion.png)

- Con escala logarítimica:

![itemc_conEscala](Itemc/comparacion_escalaLog.png)
