import streamlit as st
from graficos.graficos_esp.boxplot import boxplot
from graficos.graficos_esp.continuous import continuous
from graficos.graficos_esp.heatmap import heatmap
from graficos.graficos_esp.plot_hull_boxplot import *
from utilidades import *
from clases import *
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_pdf import PdfPages
from bd import *

#Traduccion pendiente

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
    Vaya al menú 🥀**Cálculo de índices** y haga clic en el botón para cargar archivos. Elija el archivo Excel obtenido con
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
    st.markdown(""" A continuación se detallan los índices que **Chromindex-UdeC** incluye. Notar que
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
    st.header('Documentación de gráficos')
    st.markdown("""Para utilizar la generacion de graficos, es necesario que el archivo tenga un formato de .XLS, .XLSX o .CSV. 
                Además, las columnas deben seguir el siguiente orden: Taxa, Infrataxa, Población e Índices. Cada columna debe 
                tener su encabezado correspondiente en la primera fila, y los índices pueden ser de cualquier tipo y estar 
                dispuestos en cualquier orden. A continuacion, se muestra un ejemplo:""", unsafe_allow_html=True)    

    ejemplo = pd.read_csv("./ejemplo/Baeza_Werdermannii.csv")
    st.dataframe(ejemplo.set_index(ejemplo.columns[0])[:10], width=1400)

    st.download_button(
        label="Descargar Ejemplo CSV",
        data=ejemplo.to_csv().encode('utf-8'),
        file_name="ejemplo.csv",
        key='download_button'
    )

    st.markdown("<h4>Heatmap</h4>", unsafe_allow_html=True)
    st.markdown("""Su implementación es mediante la función __clustermap__ y el histograma mostrado 
                en su esquina superior izquierda es mediante la función __histplot__, ambos pertenecientes a la librería __seaborn__. 
                El escalado de datos se realiza utilizando la puntuación Z, que se aplica de forma independiente a cada columna. 
                Los dendrogramas se crean utilizando el método de enlace promedio con datos sin estandarizar, y se utiliza 
                la métrica euclidiana para calcular las distancias entre los puntos.""", unsafe_allow_html=True)

    st.markdown("<h4>Scatter plot with Convex Hull and Boxplots</h4>", unsafe_allow_html=True)
    st.markdown("""Su implementación es mediante la función __spatial.ConvexHull__ de la librería __scipy__. Los boxplots utilizados 
                son de la libreria __seaborn__, generados con la función __boxplot__.""", unsafe_allow_html=True)
    
    st.markdown("<h4>Boxplot</h4>", unsafe_allow_html=True)
    st.markdown("""Su implementación es mediante la función __express.box__ de la librería __plotly__.""", unsafe_allow_html=True)
    
    st.markdown("<h4>graf 1 2</h4>", unsafe_allow_html=True)
    st.markdown("""Su implementación es mediante la función __pyplot__ de la librería __matplotlib__.""", unsafe_allow_html=True)
    
    
    
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

def selectorGraficos():
    st.header("Selector de graficos")
    upload = st.file_uploader(
        'Subir archivo(s)', 
        type=['xls', 'xlsx','csv'], 
        accept_multiple_files=True,
        on_change=add_sesion_state('uploader_key', 1)
    )
    """ check_cvcl=st.checkbox("CVCL Column Plot")
    check_ltc=st.checkbox("LTC Column Plot")
    check_heat=st.checkbox("Heatmap")
    check_scatter=st.checkbox("Scatter plot with Convex Hull and Boxplots")
    check_boxplot=st.checkbox("Boxplot") """
    
    if upload:
        st.markdown('---')
        
        for uploaded_file in upload:
            # Check the file extension to determine the file type for each uploaded file
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                # Read an Excel file
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            elif uploaded_file.name.endswith('.csv'):
                # Read a CSV file
                df = pd.read_csv(uploaded_file)
            else:
                st.error(f'Formato de archivo no soportado {uploaded_file.name}. Porfavor suba un Excel (.xlsx or .xls) o CSV (.csv) file.')
                continue  # Skip processing this file and continue with the next
        
            # Display the DataFrame for each uploaded file
            st.subheader(f'Data from {uploaded_file.name}:')
            st.dataframe(df)
            selectgraphtype = st.selectbox(
                'Seleccionar tipo de gráfico:',
                ("CVCL Column Plot", "LTC Column Plot", "Heatmap", "Scatter plot with Convex Hull and Boxplots", "Boxplot"),
            )
            if selectgraphtype == "CVCL Column Plot":
                # Plot 'CVCL' column
                plt.figure(figsize=(8, 6))
                plt.plot(df['CVCL'])
                plt.title('Gráfico 1: CVCL Column Plot')
                plt.xlabel('Index')
                plt.ylabel('CVCL Values')
                st.pyplot(plt)

            elif selectgraphtype == "LTC Column Plot":
                # Plot 'LTC' column
                plt.figure(figsize=(8, 6))
                plt.plot(df['LTC'])
                plt.title('Gráfico 2: LTC Column Plot')
                plt.xlabel('Index')
                plt.ylabel('LTC Values')
                st.pyplot(plt)
            
            elif selectgraphtype == "Heatmap":
                heatmap(df)
            
            elif selectgraphtype == 'Scatter plot with Convex Hull and Boxplots':
                plot_convex_hull(df)

            elif selectgraphtype == "Boxplot":
                st.header("Test Graph")
                df_data = pd.DataFrame(df, columns=df.columns)
                infrataxas = dict()
                for index, value in enumerate(df_data['Infrataxa']):
                    if value not in infrataxas:
                        infrataxas[value] = index
                infrataxas_graph_data = dict()
                indexes = df_data.iloc[:, 3:]
                for index, (keys, values) in enumerate(infrataxas.items()):
                    if index >=0 and index < len(infrataxas) - 1:
                        infrataxas_graph_data[keys] = df_data.iloc[values:list(infrataxas.values())[index + 1], 3:]
                    else:
                        infrataxas_graph_data[keys] = df_data.iloc[values:len(df_data), 3:]
                    
                figs = []
                for (columnName) in indexes.columns:
                    fig = px.box(df_data, y=columnName, boxmode='group', x="Infrataxa", color="Infrataxa")
                    fig.update_layout(height=600, width=800)
                    fig.update_traces(width=0.5)
                    #fig.update_layout(hovermode=False)
                    figs.append(fig)
                for index, figure in enumerate(figs):
                    st.plotly_chart(figure)   

            formato = st.selectbox("Formato de exportación:", ["PNG", "JPEG", "PDF"])

            if st.button("Exportar gráfico"):
                # Save Graph
                buffer = io.BytesIO()
                if formato == "PNG":
                    plt.savefig(buffer, format="png")
                    extension = "png"
                elif formato == "JPEG":
                    plt.savefig(buffer, format="jpeg")
                    extension = "jpg"
                elif formato == "PDF":
                    plt.savefig(buffer, format="pdf")
                    extension = "pdf"
    
                # Download graph
                st.markdown(get_binary_file_downloader_html(buffer, f"gráfico.{extension}", "Descargar Gráfico"), unsafe_allow_html=True)
    
    st.subheader("¿Cómo usar?")
    st.write(
        """
        Desarrolladores web usan con frecuencia Chrom-Index como un punto de referencia para optimizar sus 
        paginas y aplicaciones web para la mejor experiencia de usuario posible en el navegador Chrome. 
        Provee visiones valiosas sobre que tan eficiente un sitio corre en Chrome y ayuda a 
        identificar áreas para mejorar. Solo sube tu archivo .xls con el formato correcto y procesaremos 
        el archivo y generaremos los gráficos.
        """
    )
    st.subheader("¿Qué es Chrom-Index?")
    st.write(
        """
        En el mundo de navegadores web, Chrom-Index es un término que ha estado ganando popularidad 
        entre tanto entusiastas de tecnología como desarrolladores. Representa una métrica única diseñada 
        para medir la eficiencia y rendimiento del navegador a través de varias plataformas y dispositivos.
        """
    )

def get_binary_file_downloader_html(bin_data, file_label, button_text):
    data = base64.b64encode(bin_data.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{data}" download="{file_label}">{button_text}</a>'
    return href

def bd():

    st.header('Chromindex-UdeC')
    
    create_user()
    if not 'logeado' in st.session_state:
        login()
    ## Uploades de los excels:
    lista_excels = st.file_uploader('Upload files', type=['xls', 'xlsx'], accept_multiple_files=True,
                                    on_change=add_sesion_state('uploader_key', 1))

    indices_nombres = [u'A\u2082', 'Ask%', 'CVCI', 'CVCL', 'MCA', 'Syi', 'TF%']

    if ('uploader_key' in st.session_state) & (len(lista_excels) > 0):
        container_multiselect = st.container()
        check_all = st.checkbox('Select all')
        if check_all:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres, indices_nombres)
        else:
            indices_seleccionados = container_multiselect.multiselect('Multiselect', indices_nombres)
        if st.button('Calculate indices'):
            df = pd.DataFrame(columns=['File'] + indices_seleccionados)

            for uploader in lista_excels:
                indices_clase = IndicesDesdeExcel(uploader)
                indices_dicc = indices_clase.calcular_indices(indices_seleccionados)
                excel_nombre = uploader.name.split('.xls')[0]
                df.loc[len(df) + 1] = [excel_nombre] + list(indices_dicc.values())
            st.dataframe(df)
            
            add_sesion_state('db_data', df.to_dict(orient='records'))
            add_sesion_state('df_resultado', xlsdownload(df))

        if 'df_resultado' in st.session_state:
            fecha_hoy = datetime.now().strftime(r"%d-%m-%Y_%Hh%Mm%Ss")
            excel_nombre = f'Indices_{fecha_hoy}.xlsx'
            st.download_button(
                label='📥 Download as Excel',
                data=st.session_state['df_resultado'],
                file_name=excel_nombre,
                mime="application/vnd.ms-excel",
            )

        if 'db_data' in st.session_state and 'logeado' in st.session_state:
            if st.button('Save to my account'):
                print(st.session_state['db_data'])
                guardar(st.session_state['db_data'])  
    