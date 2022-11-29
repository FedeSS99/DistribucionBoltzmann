# cython: language_level=3

cimport cython
from openmp cimport omp_get_max_threads, omp_set_num_threads
from cython.parallel import prange
import numpy as np
cimport numpy as np

ctypedef np.float64_t Dtype_t

cdef extern from "math.h":
    Dtype_t cos(Dtype_t ang) nogil
    Dtype_t sin(Dtype_t ang) nogil

from libc.stdlib cimport rand
from libc.stdio cimport printf
cdef extern from 'limits.h':
    int RAND_MAX

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
@cython.nonecheck(False)
def GenerarPartsAleatoriasCuadrado(Dtype_t r,np.ndarray[Dtype_t,ndim=2] PosParts, Dtype_t xMin,Dtype_t xMax,Dtype_t yMin,Dtype_t yMax):
    cdef:
        int Part_i = 0
        int numParts = <int>PosParts.shape[1]
        int n,cont
        Dtype_t x,y,difX2,difY2
    
    PosParts[0,Part_i] = xMin + (xMax-xMin)*<Dtype_t>rand()/<Dtype_t>RAND_MAX
    PosParts[1,Part_i] = yMin + (yMax-yMin)*<Dtype_t>rand()/<Dtype_t>RAND_MAX
    Part_i += 1

    while Part_i!=numParts:
        x = xMin + (xMax-xMin)*<Dtype_t>rand()/<Dtype_t>RAND_MAX
        y = yMin + (yMax-yMin)*<Dtype_t>rand()/<Dtype_t>RAND_MAX

        cont = 0
        for n in range(Part_i):
            difX2 = (x-PosParts[0,n])*(x-PosParts[0,n])
            difY2 = (y-PosParts[1,n])*(y-PosParts[1,n])

            if difX2+difY2 > 4.0*r*r:
                cont += 1

        if cont == Part_i:
            PosParts[0,Part_i] = x
            PosParts[1,Part_i] = y
            Part_i += 1


@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
@cython.nonecheck(False)
cdef DetectarColisionParticulas(np.ndarray[Dtype_t,ndim=2]PosP,np.ndarray[Dtype_t,ndim=2]VelP,Dtype_t r):
    cdef:
        int N = <int> PosP.shape[1]
        int i,j
        Dtype_t DifVx, DifVy, DifX, DifY
        Dtype_t C_colision, colVx, colVy
        int maxThreads
        
    maxThreads = <int>omp_get_max_threads()
    omp_set_num_threads(maxThreads)

    for i in prange(N-1,nogil=True,chunksize=1,num_threads=maxThreads,schedule="static"):
        for j in range(i+1, N):
            DifX = PosP[0,j] - PosP[0,i]
            DifY = PosP[1,j] - PosP[1,i]
            if j!=i and DifX*DifX + DifY*DifY < 4.0*r*r:                    
                DifVx = VelP[0,i] - VelP[0,j]
                DifVy = VelP[1,i] - VelP[1,j]

                C_colision = (DifX*DifVx+DifY*DifVy)/(DifX*DifX+DifY*DifY)
                colVx = C_colision*DifX
                colVy = C_colision*DifY

                VelP[0,i] -= colVx
                VelP[1,i] -= colVy
                VelP[0,j] += colVx
                VelP[1,j] += colVy

                

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
@cython.nonecheck(False)
cdef DetectarColisionFronteraCuadrado(np.ndarray[Dtype_t,ndim=2]PosP,np.ndarray[Dtype_t,ndim=2]VelP,Dtype_t r,Dtype_t L,Dtype_t dt):
    cdef:
        int N = <int> PosP.shape[1]
        int i, maxThreads
        Dtype_t x,y
        
    maxThreads = <int>omp_get_max_threads()
    omp_set_num_threads(maxThreads)

    for i in prange(N,nogil=True,chunksize=1,num_threads=maxThreads,schedule="static"):
        x = PosP[0,i]
        y = PosP[1,i]

        if x - r <= 0 or x + r >= L:
            VelP[0,i] *= -1.0
        if y - r <= 0 or y + r >= L:
            VelP[1,i] *= -1.0
                
        PosP[0,i] += VelP[0,i]*dt
        PosP[1,i] += VelP[1,i]*dt
        

@cython.nonecheck(False)
def AvanceSimulacion(np.ndarray[Dtype_t,ndim=2]PosP,np.ndarray[Dtype_t,ndim=2]VelP,Dtype_t r,Dtype_t L, Dtype_t dt, int PasosFrame):
    cdef int paso
    
    for paso in range(PasosFrame):
        DetectarColisionParticulas(PosP,VelP,r)
        DetectarColisionFronteraCuadrado(PosP,VelP,r,L,dt)
