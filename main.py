import streamlit as st
from utilidades import *
from pages.pages_eng import *
from pages.pages_esp import *

st.set_page_config(
page_title="Chromindex-UdeC",
page_icon="imagenes/logoAPP.jpeg",
layout="wide"
)

# Cabezera
col1, _, col2 = st.columns([1, 3, 2])
col1.image('imagenes/logoAPP.jpeg')
col2.image('imagenes/udec.gif', use_column_width='always')

# Selector del lenguaje (en la sidebar)
leng = lenguaje_selectbox()

# Cargar página en inglés
if leng == lenguajes[0]:
    # Menú y contenido de la sidebar
    pag_actual = page_radio_eng()
    write_espacios_sbar(32)
    st.sidebar.image("imagenes/marca_udec2.png")

    if pag_actual == paginas_navegacion_eng[0]:#inicio
        home()

    elif pag_actual == paginas_navegacion_eng[1]:#instrucciones
        howToUse()

    elif pag_actual == paginas_navegacion_eng[2]:#calculo de indices
        indexCalc()

    elif pag_actual == paginas_navegacion_eng[3]:#documentacion
        docs()

    elif pag_actual == paginas_navegacion_eng[4]:#selector de graficos
        graphSelector()

    elif pag_actual == paginas_navegacion_eng[5]:#about
        about()

    elif pag_actual == paginas_navegacion_eng[6]:#about
        db()


# Cargar página en español
else:
    # Menú y contenido de la sidebar
    pag_actual = page_radio_esp()
    write_espacios_sbar(32)
    st.sidebar.image("imagenes/marca_udec2.png")

    if pag_actual == paginas_navegacion_esp[0]:#inicio
        inicio()

    elif pag_actual == paginas_navegacion_esp[1]:#instrucciones
        instrucciones()

    elif pag_actual == paginas_navegacion_esp[2]:#calculo de indices
        calculoIndices()

    elif pag_actual == paginas_navegacion_esp[3]:#documentacion
        docu()

    elif pag_actual == paginas_navegacion_esp[4]:#selector de graficos
        selectorGraficos()

    elif pag_actual == paginas_navegacion_esp[5]:#about
        acerca()

    elif pag_actual == paginas_navegacion_esp[6]:#about
        bd()

#Pie de página
write_espacios(6)
st.image('imagenes/banner.png')
