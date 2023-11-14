import streamlit as st
from io import BytesIO
from datetime import datetime
import pandas as pd
#from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
#from htbuilder.units import percent, px
#from htbuilder.funcs import rgba, rgb


lenguajes = ["🇺🇸 Eng (USA)", "🇨🇱 Esp (Chile)"]
paginas_navegacion_eng = [
    '🏠Home',
    '📖How to use', 
    '🥀Index calculation', 
    '📃Documentation', 
    '📊Graph selector',
    '❓About Chromindex-UdeC',
    '🌱Account'
    
]
paginas_navegacion_esp = [
    '🏠Inicio', 
    '📖Instrucciones', 
    '🥀Cálculo de índices', 
    '📃Documentación', 
    '📊Selector de graficos',
    '❓Acerca de Chromindex-UdeC',
    '🌱Cuenta'
]

def lenguaje_selectbox():
    check_sstate = ("idioma" in st.session_state)
    if check_sstate:
        lenguaje = st.sidebar.selectbox("Language - Idioma: ", lenguajes, index=st.session_state.idioma)
    else:
        lenguaje = st.sidebar.selectbox("Language - Idioma: ", lenguajes)

    if lenguaje == lenguajes[0]:
        st.session_state.idioma = 0
    else:
        st.session_state.idioma = 1
    return lenguaje

def page_radio_eng():
    pagina = st.sidebar.radio("Menu", paginas_navegacion_eng)
    return pagina

def page_radio_esp():
    pagina = st.sidebar.radio("Menú", paginas_navegacion_esp)
    return pagina

def write_espacios_sbar(n=1):
    for i in range(n):
        st.sidebar.write("\n")

def write_espacios(n=1):
    for i in range(n):
        st.write("\n")

def xlsdownload(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.close()
    return output.getvalue()


def del_sesion_state(st_key):
    if st_key in st.session_state:
        del st.session_state[st_key]


def add_sesion_state(st_key, value):
    if st_key not in st.session_state:
        st.session_state[st_key] = value

################################################################################
############ TODAVÍA EN PRUEBA EL SIGUIENTE CÓDIGO #############################
################################################################################

# def image(src_as_string, **style):
#     return img(src=src_as_string, style=styles(**style))
#
#
# def link(link, text, **style):
#     return a(_href=link, _target="_blank", style=styles(**style))(text)
#
#
# def layout(*args):
#
#     style = """
#     <style>
#       # MainMenu {visibility: hidden;}
#       footer {visibility: hidden;}
#      .stApp { bottom: 105px; }
#     </style>
#     """
#
#     style_div = styles(
#         position="fixed",
#         left=0,
#         bottom=0,
#         margin=px(0, 0, 0, 0),
#         width=percent(100),
#         color="black",
#         text_align="center",
#         height="auto",
#         opacity=1
#     )
#
#     style_hr = styles(
#         display="block",
#         margin=px(8, 8, "auto", "auto"),
#         border_style="inset",
#         border_width=px(2)
#     )
#
#     body = p()
#     foot = div(
#         style=style_div
#     )(
#         hr(
#             style=style_hr
#         ),
#         body
#     )
#
#     st.markdown(style, unsafe_allow_html=True)
#
#     for arg in args:
#         if isinstance(arg, str):
#             body(arg)
#
#         elif isinstance(arg, HtmlElement):
#             body(arg)
#
#     st.markdown(str(foot), unsafe_allow_html=True)
#
#
# def footer():
#     myargs = [
#         image("https://raw.githubusercontent.com/Zekess/Indices_de_asimetria/main/imagenes/banner.png", width=px(1080)),
#     ]
#     layout(*myargs)
