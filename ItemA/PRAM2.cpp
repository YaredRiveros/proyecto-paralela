//PRAM para calcular la fuerza entre partículas, considerando
// que el número de procesos p es menor que la cantidad de
//elementos n

//Input: arreglo de objetos Particle ptcl, número de partículas n,
//número de procesos p

//Output: arreglo de partículas ptcl modificadas durante la simulación

//Algoritmo para un proceso p_i, tal que 0 <= i < p

//sea jpred un arreglo de objetos Predictor de tamaño n/p

//sea ipred un arreglo de objetos Predictor de tamaño n

//se define inicio y fin del dominio para el proceso actual
jstart = (p_i * n) / p; 
jend   = ((1+p_i) * n) / p; 

double dt = 0.125;
double time_cur = 0.0;
double t_end = 1;

while(time_cur <= t_end) do
    for 1 <= i <= n/p do    //O(n/p)
        jpred[i] = Predictor(ptcl[i+jstart])

    for 1 <= i <= n do    //O(n)
        ipred[i] = Predictor(ptcl[i])


    // sea force un arreglo de objetos Force de tamaño n
    // sea force_tmp un arreglo de objetos Force de tamaño n/p

    //O(n^2/p)
    for 1 <= i <= n do
        for 1 <= j <= n/p do
            double dx = jpred[j].pos.x - ipred[i].pos.x;
            double dy = jpred[j].pos.y - ipred[i].pos.y;
            double dz = jpred[j].pos.z - ipred[i].pos.z;
            double dvx = jpred[j].vel.x - ipred[i].vel.x;
            double dvy = jpred[j].vel.y - ipred[i].vel.y;
            double dvz = jpred[j].vel.z - ipred[i].vel.z;

            double r2 = eps2 + dx*dx + dy*dy + dz*dz;
            double rv = dx*dvx + dy*dvy + dz*dvz;
            
            if(r2 == eps2) continue;
            double rinv2 = 1.0 / r2;
            double rinv1 = sqrt(rinv2);
            rv *= -3.0 * rinv2;
            rinv1 *= jpred[j].mass;
            double rinv3 = rinv1 * rinv2;

            pot += rinv1;
            ax += rinv3 * dx;
            ay += rinv3 * dy;
            az += rinv3 * dz;
            jx += rinv3 * (dvx + rv * dx);
            jy += rinv3 * (dvy + rv * dy);
            jz += rinv3 * (dvz + rv * dz);

        force_tmp[i].acc.x = ax;
        force_tmp[i].acc.y = ay;
        force_tmp[i].acc.z = az;
        force_tmp[i].jrk.x = jx;
        force_tmp[i].jrk.y = jy;
        force_tmp[i].jrk.z = jz;
        force_tmp[i].pot = -pot;

    //O(log(p)*(alpha+(7n)*beta))
    Allreduce(force_tmp, force, n*7, DOUBLE, SUM, COMM_WORLD); //O(log(p)*(alpha+(7n)*beta)

    //O(n)
    for 1 <= i <= n do
        ptcl[i].acc = force[i].acc;
        ptcl[i].jrk = force[i].jrk;
        ptcl[i].pot = force[i].pot;

    time_cur += dt;

endwhile

return ptcl;



