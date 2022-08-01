import streamlit as st
from utilidades import *
from pages.pages_eng import *
from pages.pages_esp import *

st.set_page_config(
page_title="Chromidex-UdeC",
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

    if pag_actual == paginas_navegacion_eng[0]:
        home()

    elif pag_actual == paginas_navegacion_eng[1]:
        howToUse()

    elif pag_actual == paginas_navegacion_eng[2]:
        indexCalc()

    elif pag_actual == paginas_navegacion_eng[3]:
        docs()

    elif pag_actual == paginas_navegacion_eng[4]:
        about()


# Cargar página en español
else:
    # Menú y contenido de la sidebar
    pag_actual = page_radio_esp()
    write_espacios_sbar(32)
    st.sidebar.image("imagenes/marca_udec2.png")

    if pag_actual == paginas_navegacion_esp[0]:
        inicio()

    elif pag_actual == paginas_navegacion_esp[1]:
        instrucciones()

    elif pag_actual == paginas_navegacion_esp[2]:
        calculoIndices()

    elif pag_actual == paginas_navegacion_esp[3]:
        docu()

    elif pag_actual == paginas_navegacion_esp[4]:
        acerca()

#Pie de página
write_espacios(6)
st.image('imagenes/banner.png')
