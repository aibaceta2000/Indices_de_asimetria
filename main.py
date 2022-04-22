import os
import pandas as pd
import streamlit as st
#import xlsxwriter
import numpy as np
from datetime import datetime
import string
from clases import IndicesDesdeExcel

st.header('BIENVENIDO A LA WEBAPP PARA CÁLCULO DE ÍNDICES.')


## Uploades de los excels:
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0
lista_excels = st.file_uploader('Subir archivos', type=['xls', 'xlsx'], accept_multiple_files=True, key=st.session_state.uploader_key)

indices_nombres = ['CVcl', 'Mca', 'Ask%', 'TF%', 'Syi', 'A1', 'A']

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
