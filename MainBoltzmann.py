from ClaseBoltzmann import SimBoltzmann
from ClaseGraficaSim import PyQtSim

if __name__ == "__main__":
    #Todas las magnitudes física en unidades del SI
    N = 512
    Vmax = 250.0 #en picometros por picosegundo (pm/ps)
    dt = 1e-4 # en segundos (ps)
    PasosFrame = 1000
    Tf = 30.0 # en segundos (ps)
    L = 15000.0 # en nanometros (pm)
    #Radio y masa del Xenon
    r = 216.0 # en nanometros (pm)
    m = 131.293*(1.66053886e-27)

    Simulacion = SimBoltzmann(N, Vmax, dt, PasosFrame, Tf, r, m, L)
    GraficaSimulacion = PyQtSim(Simulacion)
    GraficaSimulacion.IniciarSimulacion(Simulacion)
