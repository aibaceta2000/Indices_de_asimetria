import os
import pandas as pd
import streamlit as st
#import xlsxwriter
import numpy as np
from datetime import datetime
import string
from clases import IndicesDesdeExcel




paginas_navegacion = ['Home', 'Instrucciones', 'Cálculo de indices', 'About Us']

with st.sidebar:
    st.image('imagenes/marca_udec2.png')
    st.text('')
    st.text('')
    pag_navegacion_actual = st.radio('Navegar', paginas_navegacion)


if pag_navegacion_actual == paginas_navegacion[0]:
    st.header('BIENVENIDOS')

elif pag_navegacion_actual == paginas_navegacion[1]:
    st.header('INSTRUCCIONES DE USO (VIDEO)')

elif pag_navegacion_actual == paginas_navegacion[2]:
    st.header('BIENVENIDO A LA WEBAPP PARA CÁLCULO DE ÍNDICES.')


    ## Uploades de los excels:
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    lista_excels = st.file_uploader('Subir archivos', type=['xls', 'xlsx'], accept_multiple_files=True, key=st.session_state.uploader_key)

    indices_nombres = ['CVcl', 'CVci', 'Mca', 'Ask%', 'TF%', 'Syi', 'A', 'A1', 'A2']

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
    st.header('CRÉDITOS, INFO CONTACTO')
