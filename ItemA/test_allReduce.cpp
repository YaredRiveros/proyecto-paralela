#include <mpi.h>
#include <iostream>
#include <vector>
#include <cmath>

#define INLINE inline

template <typename REAL> 
struct vector3{
	REAL x, y, z;
	INLINE vector3(){
		x = y = z = REAL(0);
	}
	INLINE vector3(const REAL &r){
		x = y = z = r;
	}
	INLINE vector3(const REAL &_x, const REAL &_y, const REAL &_z){
		x = _x;  y = _y;  z = _z;
	}
	INLINE vector3(const REAL *p){
		x = p[0]; y = p[1]; z = p[2];
	}
	INLINE ~vector3(){}

	INLINE REAL &operator [](int i){
	  return (&x)[i];
	}
	INLINE const REAL &operator [](int i) const{
	  return (&x)[i];
	}
	template <class real> 
		INLINE operator vector3<real> () const {
			return vector3<real> (real(x), real(y), real(z));
		}
	INLINE operator REAL *(){
		return &x;
	}
	INLINE REAL (*toPointer())[3]{
		return (REAL (*)[3])&x;
	}
	typedef REAL (*pArrayOfReal3)[3];
	INLINE operator pArrayOfReal3(){
		return toPointer();
	}

	/*void outv(std::ostream &ofs = std::cout) const{
		ofs << "(" << x << ", " << y << ", " << z << ")" << std::endl;
	}*/
	INLINE bool are_numbers () const{
		// returns false if *this has (a) NaN member(s)
		return (norm2() >= REAL(0));
	}

	INLINE REAL norm2() const{
		return (*this)*(*this);
	}
	INLINE REAL abs() const{
		return std::sqrt(norm2());
	}

	friend std::ostream &operator << (std::ostream &ofs, const vector3<REAL> &v){
		ofs << v.x << " " << v.y << " " << v.z;
		// ofs << str_begin << v.x << str_delim << v.y << str_delim << v.z << str_end;
		return ofs;
	}
	friend std::istream &operator >> (std::istream &ifs, vector3<REAL> &v){
		ifs >> v.x >> v.y >> v.z;
		return ifs;
	}
	INLINE const vector3<REAL> operator + (const vector3<REAL> &v) const{
		return vector3<REAL> (x+v.x, y+v.y, z+v.z);
	}
	INLINE const vector3<REAL> operator - (const vector3<REAL> &v) const{
		return vector3<REAL> (x-v.x, y-v.y, z-v.z);
	}
	INLINE const vector3<REAL> operator * (const REAL &s) const{
		return vector3<REAL> (x*s, y*s, z*s);
	}
	INLINE friend const vector3<REAL> operator * (const REAL &s, const vector3<REAL> &v){
		return v*s;
	}
	// dot product
	INLINE const REAL operator * (const vector3<REAL> &v) const{
		return (x*v.x + y*v.y + z*v.z);
	}
	// vector product
	INLINE const vector3<REAL> operator % (const vector3<REAL> &v) const{
		return vector3<REAL> ( y*v.z - z*v.y, 
				       z*v.x - x*v.z, 
				       x*v.y - y*v.x );
	}
	INLINE const vector3<REAL> operator / (const REAL &s) const{
		REAL r = REAL(1)/s;
		return (*this)*r;
	}
	INLINE const vector3<REAL> &operator = (const vector3<REAL> &v){
		x = v.x; y=v.y; z=v.z;
		return *this;
	}

	INLINE const vector3<REAL> operator - (){
		return vector3<REAL> (-x, -y, -z);
	}
	INLINE const vector3<REAL> &operator += (const vector3<REAL> &v){
		*this = *this + v;
		return *this;
	}
	INLINE const vector3<REAL> &operator -= (const vector3<REAL> &v){
		*this = *this - v;
		return *this;
	}
	INLINE const vector3<REAL> &operator *= (const REAL &s){
		*this = *this * s;
		return *this;
	}
	INLINE const vector3<REAL> &operator /= (const REAL &s){
		*this = *this / s;
		return *this;
	}

	INLINE friend const vector3<REAL> maxeach (const vector3<REAL> &a, const vector3<REAL> &b){
		return vector3<REAL> (std::max(a.x, b.x), std::max(a.y, b.y), std::max(a.z, b.z));
	}
	INLINE friend const vector3<REAL> mineach (const vector3<REAL> &a, const vector3<REAL> &b){
		return vector3<REAL> (std::min(a.x, b.x), std::min(a.y, b.y), std::min(a.z, b.z));
	}
	INLINE const vector3<REAL> abseach(){
		return vector3<REAL> (std::fabs(x), std::fabs(y), std::fabs(z));
	}

	/*
	static std::string str_begin, str_delim, str_end;
	static void set_bracket(const std::string &begin, const std::string &delim, const std::string &end){
		str_begin = begin;
		str_delim = delim;
		str_end   = end;
	}
	*/
#ifdef USE_BOOST
	boost::format format(const char *str){
		return boost::format(str) % x % y % z;
	}
#endif
};

struct Force{
	enum{
		nword = 7,
	};
	vector3<double> acc;
	vector3<double> jrk;
	double pot;
};

// Definición de Force y vector3 según lo proporcionado

//Este archivo se utilizó para comprender el tamaño de envío
//del allReduce con un array de tipo Force

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int ni = 2; // Número de partículas

    std::vector<Force> force_tmp(ni);
    std::vector<Force> force(ni);

    // Inicialización de force_tmp en cada proceso
    if (rank == 0) {
        force_tmp[0] = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}, 7.0};
        force_tmp[1] = {{1.5, 2.5, 3.5}, {4.5, 5.5, 6.5}, 7.5};
    } else if (rank == 1) {
        force_tmp[0] = {{0.5, 1.0, 1.5}, {2.0, 2.5, 3.0}, 3.5};
        force_tmp[1] = {{0.75, 1.25, 1.75}, {2.25, 2.75, 3.25}, 3.75};
    }

    MPI_Allreduce(force_tmp.data(), force.data(), ni * Force::nword, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    // Mostrar resultados
    if (rank == 0) {
        std::cout << "Proceso " << rank << ":" << std::endl;
        for (int i = 0; i < ni; ++i) {
            std::cout << "  Particle " << i << ":" << std::endl;
            std::cout << "    acc: (" << force[i].acc.x << ", " << force[i].acc.y << ", " << force[i].acc.z << ")" << std::endl;
            std::cout << "    jrk: (" << force[i].jrk.x << ", " << force[i].jrk.y << ", " << force[i].jrk.z << ")" << std::endl;
            std::cout << "    pot: " << force[i].pot << std::endl;
        }
    }

    MPI_Barrier(MPI_COMM_WORLD);

    if(rank==1){
        std::cout << "Proceso " << rank << ":" << std::endl;
        for (int i = 0; i < ni; ++i) {
            std::cout << "  Particle " << i << ":" << std::endl;
            std::cout << "    acc: (" << force[i].acc.x << ", " << force[i].acc.y << ", " << force[i].acc.z << ")" << std::endl;
            std::cout << "    jrk: (" << force[i].jrk.x << ", " << force[i].jrk.y << ", " << force[i].jrk.z << ")" << std::endl;
            std::cout << "    pot: " << force[i].pot << std::endl;
        }
    }

    MPI_Finalize();
    return 0;
}
