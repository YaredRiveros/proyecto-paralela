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
El PRAM lo puede encontrar en PRAM/PRAM.cpp. En éste comentamos la compleijidad de cada operación a detalle.

### Complejidad teórica

OJO: a pesar de que el código contenga directiva pragma omp, el código no es híbrido (solo tiene MPI).

Utilizando el PRAM realizado, la complejidad teórica a la que llegamos es 
T_p(n,p) = O(n) + O(logp*(alpha+beta)) + O(logp*(alpha+n*beta)) +   O(n/p) + O(n) + O(n^2/p) + O(log(p)*(alpha+n*beta)) + O(n) + O(n) + #_intervalos_tiempo*( O(n) + O(n) + O(n^2/p) + O(log(p)*(alpha+n*beta)) + O(n) + O(n) )

= O(p*(alpha+n*beta)) + + O(n^2/p) + #_intervalos_tiempo( O(n^2/p) + O(log(p)*(alpha+n*beta))) 


## Item B: Medición de tiempo y comparación con curva teórica
OJO: el programa calcula el tiempo total del algoritmo dentro del while principal, es decir, debemos usar la curva teórica que considera solamente lo que está dentro de dicho bucle para la comparación. Entonces, considerando #_intervalos_tiempo como una constante, tenemos que:

T_p = #_intervalos_tiempo( O(n^2/p) + O(log(p)*(alpha+n*beta))) 
 = O(n^2/p) + O(log(p)*(alpha+n*beta)) = O(n^2/p) + O(logp+nlogp) = O(n^2/p) + O(nlogp) = O(n^2/p + nlogp)

 Realizamos la medición de tiempos y anotamos los resultados en el achivo ItemB/experimentacion.xlsx. Luego, graficamos las curvas en ItemB/graficos.py. Al finalizar, obtuvimos los siguientes resultados:

![comparacion_8k](ItemB/comparacion_8k.png)

![comparacion_9k](ItemB/comparacion_9k.png)

![comparacion_16k](ItemB/comparacion_16k.png)

Se valida la relación entre las curvas teórica y experimental obtenidas, pues se observa que una siempre es proporcional a otra.

## Item C: Medición de velocidad para distintos valores de n y p

Se utilizó el cálculo de la velocidad en Flops/s que ya estaba implementada en el código para medir las curvas de velocidad para distintos números de procesos dado un tamaño del problema n.

Sin escala logarítmica:

![itemc_sinEscala](ItemC/comparacion.png)

Con escala logarítimica:

![itemc_conEscala](ItemC/comparacion_escalaLog.png)