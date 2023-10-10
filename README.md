# Chromindex-UDEC

Este repositorio es un proyecto que busca automatizar el cálculo de indices de asimetría para citotaxonomía vegetal. El proyecto consiste en la aplicación web <a href="http://chromindex.udec.cl/">Chromindex-UDEC</a>. Esta aplicación web podrá calcular los índices A<sub>2</sub>, CV<sub>CI</sub>, CV<sub>CL</sub>, Ask%, M<sub>CA</sub>, Sy<sub>i</sub> y TF% a partir de excels generados por la aplicacion *MicroMeasure*, para luego permitir descargar un archivo excel (.xlsx) con el detalle de los resultados.

## Instrucciones

1. Crear y ejecutar un entorno virtual (recomendado):
   dentro de la carpeta Indices_de_asimetria ejecutar
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Instalar dependencias:
   si utiliza un entorno virtual, asegúrese de que se encuentre activado
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar:
   si utiliza un entorno virtual, asegúrese de que se encuentre activado
   ```bash
   streamlit run main.py
   ```
