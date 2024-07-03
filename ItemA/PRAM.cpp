#include <imp.h>
#include <iostream>

using namespace std;

//Sea n_body = n = número total de partículas (tamaño del problema)

int main(int argc, char *argv[]){
    //Paso 1: Inicialización

    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    double n_body;
    //se lee el balor de n_body de un archivo de entrada
    //...
    Particle ptcl[n_body];

    if(rank==0){
        //inicialización de n_body leyendo el archivo de entrada (O(1))
        //...

        ifstream inp("input.dat");
        //Lectura de las partículas
        for(int i=0;i<n_body;i++){ //O(n)
            Particle &p = ptcl[i];
			inp >> p.id >> p.mass >> p.pos >> p.vel;
        }
    }

    //Envío de n_body a todos los procesos
    //O(logp*(alpha+beta))
    MPI_Bcast(&n_body, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    //Envío de todas las partículas a los procesos
    //O(logp*(alpha+n*beta))
    MPI_Bcast(ptcl, nbody*sizeof(Particle), MPI_CHAR, 0, MPI_COMM_WORLD);

    // Paso 2: se divide el dominio del problema. Cada proceso tomará una porción distinta de ptcl utilizando jstart y jend
    jstart = (myRank * nbody) / n_proc; 
	jend   = ((1+myRank) * nbody) / n_proc; 
	n_loc = jend - jstart; 
	int nj = n_loc; //número de partículas por proceso
	int ni = nbody;

    // Paso 3: Cálculo de objetos predictores
    Predictor *jpred = Predictor::allocate(N_MAX_loc); //tamaño máximo de partículas por proceso
	Predictor *ipred = Predictor::allocate(N_MAX); //tamaño máximo de partículas total

		for(int j=0; j<nj; j++){ //O(n/p)
			jpred[j] = Predictor(time_cur, Jparticle(ptcl[j+jstart])); //cada proceso toma una porción distinta de ptcl
		}
		for(int i=0; i<ni; i++){ //O(n)
			ipred[i] = Predictor(time_cur, Jparticle(ptcl[i])); //todos los procesos toman la totalidad de ptcl
		}
    
    //en este punto cada proceso tiene distinto jpred y el mismo ipred

    // Paso 4: cada proceso calcula fuerza para sus partículas y la guarda en force_tmp
    calc_force(ni, nj, eps2, ipred, jpred, force_tmp); //O(n^2/p)

    //Paso 5: todos los procesos suman sus fuerzas y lo guardan en el array force
    //O(log(p)*(alpha+(7n)*beta)). OJO: n'=7n porque nword=7 en la clase Force
    MPI_Allreduce(force_tmp, force, ni*Force::nword, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    //Paso 6: todos los procesos actualizan sus partículas con la fuerza calculada
    for(int i=0; i<ni; i++) //O(n)
        ptcl[i].init(time_cur, force[i]);

    // Paso 7: Calcula la energía hasta que se acabe el tiempo del experimento

    //imprime solo primera fila del resultado
	energy(myRank); //O(n)

    //imprime el resto de filas del resultado
    while(time_cur <= t_end){ //O(dt)
        //hallar particulas se deben actualizar en este paso
        n_act = hallar_num_particulas_a_actualizar(); //O(n)
    

        int ni = n_act;

        //actualizar objetos predictores
        for(int i=0; i<ni; i++){ //itera el # de partículas que se van a actualizar en este paso. O(n)
            ipred[i] = Predictor(min_t, ptcl[active_list[i]])
        }

        //recalcular fuera local de las partículas considerando los nuevos predictores
        calc_force(ni, nj, eps2, ipred, jpred, force_tmp); //O(n^2/p)

        //nuevamente se suman las fuerzas de cada proceso
        //O(log(p)*(alpha+(7n)*beta)). OJO: n'=7n porque nword=7 en la clase Force
        MPI_Allreduce(force_tmp, force, ni*Force::nword, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

        //actualizar las partículas con la nueva fuerza calculada
        for(int i=0; i<ni; i++){ //O(n)
            Particle &p = ptcl[active_list[i]];
            p.correct(dt_min, dt_max, eta, force[i]); //O(1)
        }

        //Impresión de resultados de esta iteración
        energy(myRank); //O(n)

        //actualizar tiempo
        time_cur += dt_min; 
    }

    //Paso 8: Liberar memoria
    delete[] jpred;
    delete[] ipred;

    MPI_Finalize();
    return 0;
}