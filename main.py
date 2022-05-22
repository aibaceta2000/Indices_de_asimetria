import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from clases import IndicesDesdeExcel
from io import BytesIO

def xlsdownload(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()    
    return output.getvalue()

def del_sesion_state(st_key):
    if st_key in st.session_state:
        del st.session_state[st_key]


def add_sesion_state(st_key, value):
    if st_key not in st.session_state:
        st.session_state[st_key] = value

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
    **Alstroemeria-UDEC**, una manera sencilla de calcular índices de asimetría del cariotipo a partir de tablas 
    excel generadas con el programa Micromeasure (Reeves, 2001).
    
    Alstroemeria-UDEC, a simple way to calculate karyotype asymmetry indices from excel tables generated 
    by the Micromeasure program (Reeves, 2001).
    
    Álvaro Guzmán Chacón¹, Carlos Baeza Perry² & Pedro Pinacho Davidson³.
     
     ¹Facultad de Ciencias Físicas y Matemáticas, Departamento de Ingeniería Civil Matemática,
      Universidad de Concepción, Concepción, Chile.
      
     ²Facultad de Ciencias Naturales y Oceanográficas, Departamento de Botánica, 
     Universidad de Concepción, Concepción, Chile.
     
     ³Pedro Pinacho Davidson. Facultad de Ingeniería, Departamento de Ingeniería Informática y Ciencias de la 
     Computación, Universidad de Concepción, Concepción, Chile.
    """

elif pag_navegacion_actual == paginas_navegacion[1]:
    st.header('Instrucciones de uso')

    st.subheader('Paso 1:')
    """    
    MicroMeasure es un programa científico de análisis de imágenes, cuya aplicación está destinada a 
    estudios citológicos, citogenéticos y citotaxonómicos. Este programa recibe imágenes en un formato específico y, a 
    través de cálculos internos, retorna un excel con información importante del cariotipo en estudio.
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
    calcular (Ver *Documentación* para revisar cómo se calculan los índices). Seleccione los índices que necesite y haga 
    click en el botón _Calcular índices_. Si se hizo todo de forma correcta, se desplegará una tabla que, por cada 
    archivo excel subido (indicado por su nombre), mostrará hacia la derecha los índices seleccionados. Además, está la 
    opción de descargar la tabla desplegada en formato excel al hacer click en el botón _📥 Descargar Excel con resultados_.
    El archivo se descargará con el nombre Indices_dd-mm-aaaa_hhmmss.xlsx., donde dd-mm-aaaa y hhmmss corresponden, respectivamente,
    a la fecha y hora exacta al momento de calcular los índices.
    """

    st.image("imagenes/paso3.png", caption="Resultado final: Tabla con los índices seleccionados por cada archivo subido y botón de descarga.")
    
    st.subheader('En caso de errores')
    
    """
    En caso de tener errores al momento de calcular los índices, se recomienda reinicar la página. En caso de persistir el problema, escribir un correo
    al autor (alvaroo_98@hotmail.cl) o crear un *Issue* en la página de github.
    """
    st.subheader('Archivo de prueba')
    """
    Puede poner a prueba la aplicación web con el siguiente archivo excel de prueba. Este fue obtenido con MicroMeasure.
    """
    
    st.download_button(
        label='📥 Descargar Excel para probar',
        data=open('elementos_web/excel_ejemplo1.xlsx', 'rb'),
        file_name="A. hookeri subsp. hookeri.xlsx",
        mime="application/vnd.ms-excel"
    )

elif pag_navegacion_actual == paginas_navegacion[2]:
    st.header('Alstroemeria-UDEC.')


    ## Uploades de los excels:
    lista_excels = st.file_uploader('Subir archivos', type=['xls', 'xlsx'], accept_multiple_files=True, on_change=add_sesion_state('uploader_key', 1))

    indices_nombres = [u'A\u2082', 'Ask%', 'CVCI', 'CVCL', 'MCA', 'Syi', 'TF%']

    if ('uploader_key' in st.session_state) & (len(lista_excels) > 0):
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
            add_sesion_state('df_resultado', xlsdownload(df))
        if 'df_resultado' in st.session_state:
            fecha_hoy = datetime.now().strftime(r"%d-%m-%Y_%Hh%Mm%Ss") 
            excel_nombre = f'Indices_{fecha_hoy}.xlsx'
            st.download_button(
                label='📥 Descargar Excel con resultados',
                data=st.session_state['df_resultado'],
                file_name=excel_nombre,
                mime="application/vnd.ms-excel",
                on_click=del_sesion_state('df_resultado')
            )

elif pag_navegacion_actual == paginas_navegacion[3]:
    st.header('Documentación')

    st.markdown('A continuación se presenta un resumen de los índices incluidos en Alstroemeria-UDEC. Cabe destacar que en lo \
    que sigue, _n_ representa la cantidad total de cromosomas y la desviación estándar corresponde a la desviación\
    estándar muestral.', unsafe_allow_html=True)

    #st.markdown("<h4>A<sub>1</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    #st.markdown("El índice __A<sub>1</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    #st.latex(r'A_1 = 1 - \frac{\sum_{i=1}^n\frac{b_i}{B_i}}{n_p}.')
    #st.markdown('Donde ___b_<sub>i</sub>__ y ___B_<sub>i</sub>__ corresponden, respectivamente, al largo promedio de los brazos\
    # cortos y al largo promedio de los brazos largos del _i_-ésimo par de cromosomas homólgos. Y ___n<sub>p</sub>___ es la \
    # cantidad de pares de cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>A<sub>2</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __A<sub>2</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'A_2 = \frac{s}{x}.')
    st.markdown('Donde ___s___ y ___x___ son, respectivamente, la desviación estándar y el promedio de los largos \
    de los cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>Ask% (Arano y Saito, 1980)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __Ask%__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'Ask\% = \frac{\sum_{i=1}^n L_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown('Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son, respectivamente, el largo del brazo más largo y el largo\
    del brazo más corto del cromosoma _i_-ésimo. Es decir, este índice se calcula como la suma de las longitudes de \
    los brazos largos dividio en la suma de los largos de todos los cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CI</sub> (Paszko, 2006)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __CV<sub>CI</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'CV_{CI} = \frac{s_{CI}}{x_{CI}}\times 100.')
    st.markdown('Donde ___s<sub>CI</sub>___ y ___x<sub>CI</sub>___ son, respectivamente, la desviación estándar y la media de\
    los índices centroméricos.', unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CL</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
    st.markdown("El índice __CV<sub>CL</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    st.latex(r'CV_{CL}= A_2 \times 100.')
    st.markdown('Donde ___A<sub>2</sub>___ corresponde al índices propuesto por Romero Zarco ya expuesto.', unsafe_allow_html=True)

    st.markdown("<h4>M<sub>CA</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
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
    los brazos cortos dividido en la suma del largo de todos los cromosomas. Notar que Ask%+TF%=1 para cualquier conjunto\
    de cromosomas.', unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")
    st.write("\n")

    st.caption("<h10>Greilhuber, J., Speta. F. 1976. C-banded karyotypes in the Scilla hohenackeri group, S. persica, \
    and Puschkinia (Liliaceae). Plant Systematics and Evolution 126: 149-188.</h10>", unsafe_allow_html=True)    
    st.caption("<h10>Huziwara, Y. 1962. Karyotype analysis in some genera of Compositae. VIII. Further studies on \
    the chromosomes of Aster. American Journal of Botany 49:116-119.</h10>", unsafe_allow_html=True)
    st.caption("<h10>Paszko, B. 2006. A critical review and a new proposal of karyotype asymmetry indices. \
    Plant Systematics and Evolution 258: 39-48.</h10>", unsafe_allow_html=True)
    st.caption("<h10>Peruzzi, L., Eroglu. H. 2013. Karyotype asymmetry: ¿again, how to measure and what \
    to measure?  Comparative Cytogenetics 7: 1-9.</h10>", unsafe_allow_html=True)
    st.caption("<h10>Romero Zarco, C. 1986. A new method for estimating Karyotype asymmetry. \
    Taxon 36: 526-530.</h10>", unsafe_allow_html=True) 



elif pag_navegacion_actual == paginas_navegacion[4]:
    st.header('Conoce Alstroemeria-UDEC')
