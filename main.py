import os
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import string
from clases import IndicesDesdeExcel
import base64

def xldownload(excel_writer, name):
    ## Función para descargar la clase "writer" como excel.
    data = open(excel_writer, 'rb').read()
    b64 = base64.b64encode(data).decode('UTF-8')
    href = f'<a href="data:file/xls;base64,{b64}" download="{name}.xlsx">Descargar {name}</a>'
    return href
st.set_page_config(layout="wide")


paginas_navegacion = ['Home', 'Instrucciones', 'Cálculo de indices', 'Documentación', 'Conoce Alstroemeria-UDEC']

st.image('imagenes/udec.png')

with st.sidebar:
    st.image('imagenes/marca_udec2.png')
    st.text('')
    st.text('')
    pag_navegacion_actual = st.radio('Navegar', paginas_navegacion)


if pag_navegacion_actual == paginas_navegacion[0]:
    st.header('Alstroemeria-UDEC')

    """
    **Alstroemeria-UDEC** es una aplicación web que permite calcular, de una manera sencilla, índices de
     asimetría de cariotipos a partir de tablas excel generadas con el programa *Micromeasure*(Reeves, 2001). 
     **Alstroemeria-UDEC** es el resultado del trabajo en conjunto de la Unidad de Data Science¹ y la 
     Facultad de Ciencias Naturales y Oceanográficas².     
     
     ¹Álvaro Guzmán Chacón. Facultad de Ciencias Físicas y Matemáticas, Departamento de Ingeniería Civil Matemática,
      Universidad de Concepción, Concepción, Chile.
      
     ²Carlos Baeza Perry. Facultad de Ciencias Naturales y Oceanográficas, departamento de Botánica, 
     Universidad de Concepción, Concepción, Chile.
     
     ¹Pedro Pinacho Davidson. Facultad de Ingeniería, Departamento de Ingeniería Informática y Ciencias de la 
     Computación, Universidad de Concepción, Concepción, Chile.
    """

elif pag_navegacion_actual == paginas_navegacion[1]:
    st.header('Instrucciones de uso')

    st.subheader('Paso 1:')
    """    
    MicroMeasure es un programa científico de análisis de imágenes, cuya aplicación está destinada a 
    estudios citológicos, citogenéticos y citotaxonómicos. Este programa recibe imágenes en un formato específico y, a 
    través de cálculos internos, retorna un excel con información importante del careotipo en estudio.
    """

    st.image("imagenes/paso1.png", caption="Ejemplo de excel obtenido de MicroMeasure.")

    st.subheader('Paso 2:')
    """
    Ir al menú _Cálculo de índices_ y hacer click en el botón para subir archivos. Elegir el archivo excel obtenido con 
    MicroMeasure.
    """

    st.image("imagenes/paso2.png", caption="Menú y botón correspondientes para subir el excel.")

    st.subheader('Paso 3:')
    """
    Una vez cargado el archivo excel a la aplicación web, aparecerá un menú para seleccionar los índices que se deseen 
    calcular (Ver documentación para revisar cómo se calculan los índices). Selecciones los índices que necesite y haga 
    click en el botón _Calcular índices_. Si se hizo todo de forma correcta, se desplegará una tabla que, por cada 
    archivo excel subido (indicado por su nombre), mostrará hacia la derecha los índices seleccionados. 
    """

    st.image("imagenes/paso3.png", caption="Resultado final: Tabla con los índices seleccionados por cada archivo subido.")

    st.subheader('Archivos de prueba')
    """
    Puede poner a prueba la aplicación web con los siguientes archivos excel de prueba. Esto fueron obtenidos con 
    MicroMeasure.
    """

    st.markdown(xldownload('elementos_web/excel_ejemplo1.xlsx', 'Excel para probar - 1'), unsafe_allow_html=True)
    st.markdown(xldownload('elementos_web/excel_ejemplo2.xlsx', 'Excel para probar - 2'), unsafe_allow_html=True)
    st.markdown(xldownload('elementos_web/excel_ejemplo3.xlsx', 'Excel para probar - 3'), unsafe_allow_html=True)

elif pag_navegacion_actual == paginas_navegacion[2]:
    st.header('Aplicación Web Alstroemeria-UDEC.')


    ## Uploades de los excels:
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    lista_excels = st.file_uploader('Subir archivos', type=['xls', 'xlsx'], accept_multiple_files=True, key=st.session_state.uploader_key)

    indices_nombres = [u'A\u2081', u'A\u2082', 'Ask%', 'CVCI', 'CVCL', 'MCA', 'Syi', 'TF%']

    if len(lista_excels) > 0:
        container_multiselect = st.container()
        check_all = st.checkbox('Seleccionar todos')
        if check_all:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres, indices_nombres)
        else:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres)
        if st.button('Calcular indices'):
            df = pd.DataFrame(columns=['Nombre'] + indices_seleccionados)
            for uploader in lista_excels:
                indices_clase = IndicesDesdeExcel(uploader)
                indices_dicc = indices_clase.calcular_indices(indices_seleccionados)
                excel_nombre = uploader.name.split('.xls')[0]
                df.loc[len(df) + 1] = [excel_nombre] + list(indices_dicc.values())
            df

elif pag_navegacion_actual == paginas_navegacion[3]:
    st.header('Documentación')

    st.markdown('El cálculo de los índices se hizo según la referencia<sup>1</sup>. A continuación se presenta un resumen \
    de estos cálculos. Cabe destacar que en lo que sigue, _n_ representa la cantidad total de cromosomas y la desviación\
    estándar corresponde a la desviación estándar muestral.', unsafe_allow_html=True)

    st.markdown("<h4>A<sub>1</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __A<sub>1</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'A_1 = 1 - \frac{\sum_{i=1}^n\frac{b_i}{B_i}}{n_p}.')
    st.markdown('Donde ___b_<sub>i</sub>__ y ___B_<sub>i</sub>__ corresponden, respectivamente, al largo promedio de los brazos\
     cortos y al largo promedio de los brazos largos del _i_-ésimo par de cromosomas homólgos. Y ___n<sub>p</sub>___ es la \
     cantidad de pares de cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>A<sub>2</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __A<sub>2</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'A_2 = \frac{s}{x}.')
    st.markdown('Donde ___s___ y ___x___ son, respectivamente, la desviación estándar y el promedio de los largos \
    de los cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>Ask% (Arano, 1963)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __Ask%__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'Ask\% = \frac{\sum_{i=1}^n L_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown('Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son, respectivamente, el largo del brazo más largo y el largo\
    del brazo más corto del cromosoma _i_-ésimo. Es decir, este índice se calcula como la suma de las longitudes de \
    los brazos largos dividio en la suma del largo de todos los cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CI</sub> (Paszko, 2006)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __CV<sub>CI</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'CV_{CI} = \frac{s_{CI}}{x_{CI}}.')
    st.markdown('Donde ___s<sub>CI</sub>___ y ___x<sub>CI</sub>___ son, respectivamente, la desviación estándar y la media de\
    los índices centroméricos.', unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CL</sub>  (Paszko, 2006)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __CV<sub>CL</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'CV_{CL}= A_2 \times 100.')
    st.markdown('Donde ___A<sub>2</sub>___ corresponde al índices propuesto por Romero Zarco ya expuesto.', unsafe_allow_html=True)

    st.markdown("<h4>M<sub>CA</sub>  (Watanabe, 1999???)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __M<sub>CA</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'M_{CA} = \frac{\sum_{i=1}^n \frac{L_i-l_i}{L_i+l_i}}{n} \times 100.')
    st.markdown('Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son, respectivamente, el largo del brazo más largo y el largo\
    del brazo más corto del cromosoma _i_-ésimo.', unsafe_allow_html=True)

    st.markdown("<h4>Sy<sub>i</sub>  (Greihuber y Speta, 1976)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __Sy<sub>i</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'Sy_i = \frac{x_l}{x_L} \times 100.')
    st.markdown('Donde ___x<sub>l</sub>___ y ___x<sub>L</sub>___ son, respectivamente, la media de los largos de los brazos cortos\
    y la media de los largos de los brazo largos.', unsafe_allow_html=True)

    st.markdown("<h4>TF% (Huziwara, 1962)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __TF%__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'TF\% = \frac{\sum_{i=1}^n l_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown('Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son, respectivamente, el largo del brazo más largo y el largo\
    del brazo más corto del cromosoma _i_-ésimo. Es decir, este índice se calcula como la suma de las longitudes de \
    los brazos cortos dividio en la suma del largo de todos los cromosomas.', unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")
    st.write("\n")

    st.caption("<h10> <sup>1</sup>: Zuo, L., & Yuan, Q. (2011). The difference between the heterogeneity of the \
    centromeric index and intrachromosomal asymmetry. Plant systematics and Evolution, 297(1), \
    141-145.</h10>", unsafe_allow_html=True)



elif pag_navegacion_actual == paginas_navegacion[4]:
    st.header('Conoce Alstroemeria-UDEC')
