from ClaseBoltzmann import SimBoltzmann
from ClaseGraficaSim import PyQtSim
"""
Código principal que solicita las cantidades físicas enlistadas como
el número de particulas, la velocidad máxima, el paso de tiempo, dimensiones
de la caja así como la masa y el radio de las partículas para simular un gas
ideal y demostrar la distribución de Maxwell-Boltzmann

Propietario : Federico Salinas Samaniego
"""

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
