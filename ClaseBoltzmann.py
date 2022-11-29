import numpy as np
from RutinasBoltzmann import GenerarPartsAleatoriasCuadrado, AvanceSimulacion

class SimBoltzmann:
    def __init__(self, N, Vmax, dt, PasosFrame, Tf, r, m, L):
        """
        Clase que recibe características del sistema aislado para
        simular un gas ideal.
        N : Número de partículas
        VMax : Velocidad máxima para las componentes de velocidad X y Y
        dt : Paso de tiempo para la simulación
        PasosFrame : Número de pasos de tiempo que se ejecutaran por cuadro
        Tf : Tiempo final de simulación
        r : Radio de las partículas
        L : Longitud de arista de la caja 
        """
        self.N = N
        self.Vmax = Vmax
        self.dt = dt
        self.PasosFrame = PasosFrame
        self.Tf = Tf
        self.r = r
        self.L = L
        self.m = m

        self.Pos = np.zeros((2,self.N), dtype=np.float64)
        self.Vel = np.zeros((2,self.N), dtype=np.float64)
        self.Colores = np.zeros((self.N, 3), dtype=np.uint8)

        randAng = np.random.uniform(-np.pi, np.pi, self.N)
        cosAng = np.cos(randAng)
        sinAng = np.sin(randAng)
        randVel = np.random.uniform(0.0, self.Vmax, (2,self.N))
        self.Vel[0,:] = randVel[0,:]*cosAng
        self.Vel[1,:] = randVel[1,:]*sinAng

        GenerarPartsAleatoriasCuadrado(r, self.Pos, 0.01*self.L, 0.99*self.L, 0.01*self.L, 0.99*self.L)

    def ObtencionColores(self):
        self.magVel = np.hypot(self.Vel[0,:], self.Vel[1,:])
        self.magVel.sort()
        minV, maxV = self.magVel.min(), self.magVel.max()
        t = (self.magVel - minV)/(maxV - minV)

        self.Colores[:,0] = np.uint8(255*0.5*(1+np.cos(np.pi*t)))
        self.Colores[:,1] = np.uint8(255*0.5*(1+np.cos(np.pi*(2.0*t+1))))
        self.Colores[:,2] = np.uint8(255*0.5*(1+np.cos(np.pi*(t+1))))

    def DistMaxBoltz_Teorico(self):
        vPromedio2 = self.magVel.mean()**2.0
        self.c = 0.5*np.pi/(vPromedio2)
        Temp = self.m*vPromedio2/(np.pi*(1.380649e-23))

        return self.c*self.magVel*np.exp(-0.5*self.c*(self.magVel**2.0)), Temp

    def PasosSimulacion(self):
        AvanceSimulacion(self.Pos, self.Vel, self.r, self.L, self.dt, self.PasosFrame)