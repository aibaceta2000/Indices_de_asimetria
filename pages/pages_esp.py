import streamlit as st
from utilidades import *
from clases import *


def inicio():
    st.header('Chromindex-UdeC')
    st.write(
    """
    **Chromindex-UdeC**, un método simple para calcular índices de asimetría
    cariotípica a partir de tablas Excel generadas por el programa MicroMeasure.

    Álvaro Guzmán Chacón¹, Carlos Baeza Perry² & Pedro Pinacho Davidson³.

    ¹Facultad de Ciencias Físicas y Matemáticas, Departamento de Ingeniería Civil Matemática,
    Universidad de Concepción, Concepción, Chile.

    ²Facultad de Ciencias Naturales y Oceanográficas, Departamento de Botánica,
    Universidad de Concepción, Concepción, Chile.

    ³Facultad de Ingeniería, Departamento de Ingeniería Informática y Ciencias de la
    Computación, Universidad de Concepción, Concepción, Chile.
    """
    )
    write_espacios(6)

def instrucciones():
    st.header('Instrucciones de Uso')

    st.subheader('Paso 1:')
    st.write(
    """
    Tener una tabla excel generada por MicroMeasure del cariotipo a estudiar.
    MicroMeasure un programa científico de análisis de imágenes, cuya aplicación está destinada a estudios citológicos, citogenéticos y
    estudios citotaxonómicos. Este programa recibe imágenes en un formato específico y, a través de cálculos internos, devuelve
    un excel con información importante sobre el cariotipo en estudio.
    """
    )

    st.image("imagenes/paso1.png", caption="Ejemplo de Excel obtenido con MicroMeasure.")

    st.subheader('Paso 2:')
    st.write(
    """
    Vaya al menú 🥀**Calculo de índices** y haga clic en el botón para cargar archivos. Elija el archivo Excel obtenido con
    MicroMeasure.
    """
    )

    st.image("imagenes/paso2_esp.png", caption="Menú correspondiente y botón para cargar archivo excel..")

    st.subheader('Paso 3:')
    st.write(
    """
    Una vez subido el archivo excel a la aplicación web, aparecerá un menú para seleccionar los índices a
    calcular (Ver 📃**Documentación** para revisar cómo se calculan los índices). Seleccione los índices que necesita y haga clic en
    en el botón _Calcular Indices_. Si todo se hizo correctamente, se mostrará una tabla que, por cada excel
    cargado (indicado por su nombre), mostrará el valor de los índices seleccionados hacia la derecha. Además, está
    la opción de descargar la tabla mostrada en formato excel haciendo clic en el botón 📥 _Descargar como Excel_.
    El archivo será descargado con el nombre Indices_dd-mm-yyyy_hhmmss.xlsx, donde dd-mm-yyyy y hhmmss corresponden,
    respectivamente, a la fecha y hora exacta al momento en que se calcularon los indices.
    """
    )

    st.image("imagenes/paso3_esp.png",
             caption="Resultado final: Tabla con los índices seleccionados por cada archivo subido, además del botón de descarga.")

    st.subheader('En caso de errores')

    st.markdown("""En caso de tener errores al usar la aplicación, se recomienda recargar la página. \
    Si el problema persiste, puede escribir un correo al autor (alvaroo.g98@gmail.com) o crear un *Issue* \
    en la página de <a href="https://github.com/Zekess/Indices_de_asimetria">**GitHub**</a> (Ver 📃**Documentación**),\
    detallando el problema y adjuntando imágenes de ser necesario.""", unsafe_allow_html=True)

    st.subheader('Archivo de prueba')
    st.write(
    """
    Puede probar Chromindex-Udec con el siguiente archivo excel de prueba. Fue obtenido con MicroMeasure-
    """
    )

    st.download_button(
        label='📥 Descargar archvo Excel de prueba',
        data=open('elementos_web/excel_ejemplo1.xlsx', 'rb'),
        file_name="A. hookeri subsp. hookeri.xlsx",
        mime="application/vnd.ms-excel"
    )

def calculoIndices():
    st.header('Chromindex-UdeC')

    ## Uploades de los excels:
    lista_excels = st.file_uploader('Cargar archivos', type=['xls', 'xlsx'], accept_multiple_files=True,
                                    on_change=add_sesion_state('uploader_key', 1))

    indices_nombres = [u'A\u2082', 'Ask%', 'CVCI', 'CVCL', 'MCA', 'Syi', 'TF%']

    if ('uploader_key' in st.session_state) & (len(lista_excels) > 0):
        container_multiselect = st.container()
        check_all = st.checkbox('Seleccionar todos')
        if check_all:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres, indices_nombres)
        else:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres)
        if st.button('Calcular índices'):
            df = pd.DataFrame(columns=['Archivo'] + indices_seleccionados)
            for uploader in lista_excels:
                indices_clase = IndicesDesdeExcel(uploader)
                indices_dicc = indices_clase.calcular_indices(indices_seleccionados)
                excel_nombre = uploader.name.split('.xls')[0]
                df.loc[len(df) + 1] = [excel_nombre] + list(indices_dicc.values())
            st.dataframe(df)
            add_sesion_state('df_resultado', xlsdownload(df))
        if 'df_resultado' in st.session_state:
            fecha_hoy = datetime.now().strftime(r"%d-%m-%Y_%Hh%Mm%Ss")
            excel_nombre = f'Indices_{fecha_hoy}.xlsx'
            st.download_button(
                label='📥 Descargar como Excel',
                data=st.session_state['df_resultado'],
                file_name=excel_nombre,
                mime="application/vnd.ms-excel",
                on_click=del_sesion_state('df_resultado')
            )

def docu():
    st.header('Documentación')

    st.markdown("""El código fuente está disponible en el siguiente repositorio de GitHub:
    <a href="https://github.com/Zekess/Indices_de_asimetria">**Chromindex-UdeC Repository**</a>.\n""",
                unsafe_allow_html=True)
    st.markdown(""" A continuación se detallan los índices que **Chromidex-UdeC** incluye. Notar que
    en lo que sigue, _n_ representa el número total de cromosomas. Además, la desviación estandar corresponde
    a la desviación estandar de la muestra de cromosomas (insesgada).""", unsafe_allow_html=True)

    # st.markdown("<h4>A<sub>1</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    # st.markdown("El índice __A<sub>1</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    # st.latex(r'A_1 = 1 - \frac{\sum_{i=1}^n\frac{b_i}{B_i}}{n_p}.')
    # st.markdown('Donde ___b_<sub>i</sub>__ y ___B_<sub>i</sub>__ corresponden, respectivamente, al largo promedio de los brazos\
    # cortos y al largo promedio de los brazos largos del _i_-ésimo par de cromosomas homólgos. Y ___n<sub>p</sub>___ es la \
    # cantidad de pares de cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>A<sub>2</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __A<sub>2</sub>__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'A_2 = \frac{s}{x}.')
    st.markdown("""Donde ___s___ y ___x___ son la desviación estandar y la meda de las longitudes de los
    cromosomas.""", unsafe_allow_html=True)

    st.markdown("<h4>Ask% (Arano y Saito, 1980)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __Ask%__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'Ask\% = \frac{\sum_{i=1}^n L_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown("""Donde ___L<sub>i</sub>___ and ___l<sub>i</sub>___ son la longitud del brazo más largo y la longitud del
    brazo más corto del cromosoma _i_-ésimo, respectivamente. Es decir, este índice se calcula como la suma de las longitudes
    de los brazos largos dividido por la suma de las longitudes de todos los cromosomas.""", unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CI</sub> (Paszko, 2006)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __CV<sub>CI</sub>__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'CV_{CI} = \frac{s_{CI}}{x_{CI}}\times 100.')
    st.markdown("""Donde ___s<sub>CI</sub>___ y ___x<sub>CI</sub>___ son la desviación estándar y la media de
    los índices centroméricos, respectivamente.""", unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CL</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __CV<sub>CL</sub>__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'CV_{CL}= A_2 \times 100.')
    st.markdown("""Donde ___A<sub>2</sub>___ corresponde al índice propuesto por Romero Zarco, mostrado anteriormente.""",
                unsafe_allow_html=True)

    st.markdown("<h4>M<sub>CA</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __M<sub>CA</sub>__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'M_{CA} = \frac{\sum_{i=1}^n \frac{L_i-l_i}{L_i+l_i}}{n} \times 100.')
    st.markdown("""Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son la longitud del brazo más largo y la longitud del
    brazo más corto del cromosoma _i_-ésimo, respectivamente.""", unsafe_allow_html=True)

    st.markdown("<h4>Sy<sub>i</sub>  (Greihuber y Speta, 1976)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __Sy<sub>i</sub>__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'Sy_i = \frac{x_l}{x_L} \times 100.')
    st.markdown("""Donde ___x<sub>l</sub>___ y ___x<sub>L</sub>___ son la longitud media de los brazos cortos y la
    longitud media de los brazos largos, respectivamente.""", unsafe_allow_html=True)

    st.markdown("<h4>TF% (Huziwara, 1962)</h4>", unsafe_allow_html=True)
    st.markdown("El indice __TF%__ se calcula de la siguiente manera:", unsafe_allow_html=True)
    st.latex(r'TF\% = \frac{\sum_{i=1}^n l_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown("""Donde ___L<sub>i</sub>___ y ___l<sub>i</sub>___ son la longitud del brazo más largo y la longitud
    del brazo más corto del cromosoma _i_-ésimo, respectivamente. Es decir, este índice se calcula como la suma de las
    longitudes de los brazos cortos dividido por la suma de las longitudes de todos los cromosomas. Notar que Ask%+TF%=1
    para cualquier conjunto de cromosomas.""", unsafe_allow_html=True)


    write_espacios(2)

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

def acerca():
    st.header('Acerca de Chromindex-UdeC')

    st.markdown(
        """
        La citotaxonomía es una rama de la citogenética, dedicada al estudio comparativo de los rasgos cariológicos con propósitos
        sistemáticos y evolutivos (Siljak-Yakovlev & Peruzzi 2012). Ha sido muy importante en los últimos
        años porque su contribución al conocimiento de la evolución y filogenia de las plantas vasculares ha permitido
        una comprensión más clara y precisa de los mecanismos implicados en la diversificación de las plantas.

        Actualmente, el uso de índices de asimetría del cariotipo, tanto intra- como intercromosómicos, es ampliamente
        utilizado en sistemática vegetal (Paszko 2006; Peruzzi & Eroglu 2013). Una de las dificultades cotidianas es el uso tabular de los
        datos generados. Normalmente, estos datos son muy numerosos y complejos de manejar, lo cual puede provocar
        errores que pueden generar ruido en la interpretación de los resultados. Por ello, la contribución del
        programa Chromindex-UdeC puede ayudar a solucionar esta situación.

        **Chromindex-UdeC** nació de la motivación de crear una herramienta que facilitara el cálculo de los índices de
        asimetría del cariotipo, con la idea de agilizar la investigación y evitar los cálculos complejos que hay detrás de estos
        índices. Chromindex-UdeC fue concebido en el contexto de las prácticas de la Unidad de Data Science de la
        Universidad de Concepción. Esta práctica fue una cooperación entre los colaboradores presentados en la página
        de inicio.

        Para desarrollar el programa **Chromindex-UdeC**, el primer paso fue crear un script en **Python** (Rossum & Drake
        2009) capaz de leer tablas de Excel y obtener los valores de los diferentes índices. Sin embargo, también se
        necesitaba una interfaz fácil de usar para que cualquier investigador pudiera utilizar esta herramienta, sin necesidad de entender
        programación. Para ello se utilizó la librería **Streamlit** (https://streamlit.io/). Esta biblioteca permite
        la creación de una aplicación web a partir de código Python sin mayores dificultades. Una vez desarrollado el código, se
        se subió a **GitHub** (https://github.com/) para usar un servidor y montar en él la aplicación en la web.
        """,
        unsafe_allow_html=True
    )
    write_espacios(2)

    st.caption("<h10>Van Rossum, G. & Drake, F.L., 2009. Python 3 Reference Manual, Scotts Valley, CA: \
               CreateSpace.</h10>", unsafe_allow_html=True)
