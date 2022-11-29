# DistribucionBoltzmann
El repositorio cuenta con tres scripts: 
- ClaseBoltzmann.py : Recibe cantidades físicas del sistema a simular, crea arreglos de posiciones y velocidades de
particulas para despues poder calcular su dinámica en el tiempo.
- ClaseGraficaSim.py : Genera el entorno gráfico para visualizar la simulación a partir de los datos provenientes de la
clase en ClaseBoltzmann.py
- MainBoltzmann.py : Se declaran las cantidades físicas para poder ser utilizadas en los códigos anteriores e iniciar la
simulacion


En MainBoltzmann.py se solicitan las siguientes cantidades para generar la simulación de un gas ideal bajo la distribución de Maxwell-Boltzmann e iniciarla:
- N : Número de partículas
- VMax : Velocidad máxima para las componentes de velocidad X y Y
- dt : Paso de tiempo para la simulación
- PasosFrame : Número de pasos de tiempo que se ejecutaran por cuadro
- Tf : Tiempo final de simulación
- r : Radio de las partículas
- L : Longitud de arista de la caja 

Tras tenerlas todas declaradas, ejecutar el mismo archivo dará inicio a la dinámica de partículas así como la distribución de velocidades además de la temperatura del sistema.
