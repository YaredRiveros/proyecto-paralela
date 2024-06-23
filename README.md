# proyecto-paralela

## Compilación y ejecución
Como indica en el enunciado, en este proyecto trabajaremos sin gpu. Para ello, el código proporcionado se utilizará del siguiente modo:
- Compilar: make cpu-4th
- Ejecutar: mpirun -np=<num_procesos> ./cpu-4th

Para cambiar el tamaño del problema, se debe de ejecutar el siguiente comando: 
./gen-plum.exe <n> <np>

, de tal manera que el tamaño del problema sera N = n*np(kb/np), donde kb=1024.
