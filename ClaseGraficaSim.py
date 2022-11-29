import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from numpy import histogram

class PyQtSim:
    def __init__(self, Sim):
        self.ventana = pg.GraphicsLayoutWidget(title="Distribución de Maxwell-Boltzmann",size=(1200,700))

        self.PlotParticulas = self.ventana.addPlot(col=0,row=0,labels={"bottom":"Posición X (pm)", "left":"Posición Y (pm)"})
        self.PlotHistograma = self.ventana.addPlot(col=1,row=0,labels={"bottom":"Velocidad (pm/ps)","left":"Densidad de frecuencia"})
        self.PlotHistograma.addLegend(offset=(350,30))

        L = Sim.L
        self.T = 0.0
        self.PlotParticulas.setXRange(0, L)
        self.PlotParticulas.setYRange(0, L)
        self.PlotParticulas.setAspectLocked(True, ratio=1)
        self.PlotParticulas.setMouseEnabled(x=False, y=False)
        self.PlotParticulas.hideButtons()
        self.PlotHistograma.setMouseEnabled(x=False, y=False)
        self.PlotHistograma.hideButtons()

        rectaCaja = pg.mkPen(color="w",width=1)
        self.PlotParticulas.plot([0,L],[0,0], pen=rectaCaja)
        self.PlotParticulas.plot([0,L],[L,L], pen=rectaCaja)
        self.PlotParticulas.plot([0,0],[0,L], pen=rectaCaja)
        self.PlotParticulas.plot([L,L],[0,L], pen=rectaCaja)

        self.Particulas = self.PlotParticulas.plot(Sim.Pos[0,:],Sim.Pos[1,:],pxMode=False,
        symbolSize=2.0*Sim.r,symbol="o",pen=pg.mkPen(None),
        symbolBrush=Sim.Colores.tolist(),symbolPen=pg.mkPen(None))

        self.cm = pg.colormap.get("jet", source="matplotlib")
        self.Histograma = self.PlotHistograma.plot([],[],stepMode=True,fillLevel=0,pen=pg.mkPen(None))

        self.CurvaDistTeo = self.PlotHistograma.plot([],[],pen=pg.mkPen((0,255,0),width=2), name="Teórico")
        self.PlotParticulas.setTitle(title=f"Tiempo = {self.T:.2f}s")

        self.ventana.show()


    def IniciarSimulacion(self, Sim):
        timer = QtCore.QTimer()
        timer.setSingleShot(True)

        def ActualizarSistema():
            Sim.PasosSimulacion()
            self.T += Sim.PasosFrame*Sim.dt
            if self.T < Sim.Tf:
                Sim.ObtencionColores()
                HistDatos = histogram(Sim.magVel,bins=30,density=True)

                self.Particulas.setData(Sim.Pos[0,:],Sim.Pos[1,:],pxMode=False,
                symbolSize=2.0*Sim.r,symbol="o",pen=pg.mkPen(None),
                symbolBrush=Sim.Colores.tolist(),symbolPen=pg.mkPen(None))

                brush = self.cm.getBrush(span=(0,HistDatos[0].max()))
                self.Histograma.setData(HistDatos[1],HistDatos[0])
                self.Histograma.setBrush(brush)

                DistribucionTeo, Temp = Sim.DistMaxBoltz_Teorico()

                self.CurvaDistTeo.setData(x=Sim.magVel,y=DistribucionTeo)

                self.PlotParticulas.setTitle(title=f"Tiempo = {self.T:.2f}ps")
                if Temp < 1.0 or Temp > 1e3:
                    self.PlotHistograma.setTitle(title=f"Temperatura= {Temp:.3e} K")
                else:
                    self.PlotHistograma.setTitle(title=f"Temperatura= {Temp:.3f} K")
                timer.start()
    
            else:
                timer.stop()


        timer.timeout.connect(ActualizarSistema)
        ActualizarSistema()

        pg.exec()