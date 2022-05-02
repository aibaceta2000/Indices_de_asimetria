import os
import pandas as pd
import streamlit as st
#import xlsxwriter
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

paginas_navegacion = ['Home', 'Instrucciones', 'Cálculo de indices', 'Documentación', 'About Us']

st.image('imagenes/udec.png')

with st.sidebar:
    st.image('imagenes/marca_udec2.png')
    st.text('')
    st.text('')
    pag_navegacion_actual = st.radio('Navegar', paginas_navegacion)


if pag_navegacion_actual == paginas_navegacion[0]:
    st.header('BIENVENIDOS')

    """
    Bienvenidos a **Alstroemeria-UDEC**, una aplicación web que permite calcular, de una manera sencilla, índices de
     asimetría de cariotipos a partir de tablas excel generadas con el programa *Micromeasure*(Reeves, 2001). 
     **Alstroemeria-UDEC** es el resultado del trabajo en conjunto de la Unidad de Data Science¹ y la 
     Facultad de Ciencias Naturales y Oceanográficas².
     
     ¹Pedro Pinacho Davidson. Facultad de Ingeniería, Departamento de Ingeniería Informática y Ciencias de la 
     Computación, Universidad de Concepción, Concepción, Chile.
     
     ¹Álvaro Guzmán Chacón. Facultad de Ciencias Físicas y Matemáticas, Departamento de Ingeniería Civil Matemática,
      Universidad de Concepción, Concepción, Chile.
      
     ²Carlos Baeza Perry. Facultad de Ciencias Naturales y Oceanográficas, departamento de Botánica, 
     Universidad de Concepción, Concepción, Chile
    """

elif pag_navegacion_actual == paginas_navegacion[1]:
    st.header('INSTRUCCIONES DE USO')

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
    st.header('BIENVENIDO A LA WEBAPP PARA CÁLCULO DE ÍNDICES.')


    ## Uploades de los excels:
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    lista_excels = st.file_uploader('Subir archivos', type=['xls', 'xlsx'], accept_multiple_files=True, key=st.session_state.uploader_key)

    indices_nombres = ['CV꜀ₗ', 'CV꜀ᵢ', 'Mca', 'Ask%', 'TF%', 'Syi', u'A\u2081', u'A\u2082']

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

    """
    Especificación respecto al cálculo de índices:
    """
    st.subheader('CV꜀ₗ')

    st.subheader('CV꜀ᵢₗ')

    st.subheader("...")

    st.subheader(u'A\u2082')

    """
    **NO OLVIDAR CITAR PAPERS CORRESPONDIENTES**
    """



elif pag_navegacion_actual == paginas_navegacion[4]:
    st.header('Acerca de nosotros')
