import streamlit as st
from graficos.graficos_eng.boxplot import boxplot
from graficos.graficos_eng.continuous import continuous
from graficos.graficos_eng.heatmap import heatmap
from graficos.graficos_eng.plot_hull_boxplot import *
from utilidades import *
from clases import *
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_pdf import PdfPages
from bd import *
import plotly.io as pio

def home():
    st.header('Chromindex-UdeC')
    st.write("""
    **Chromindex-UdeC**, a simple method for calculating karyotypic asymmetry
    indices from excel tables generated by the MicroMeasure program.

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

def howToUse():
    st.header('How to use')

    st.subheader('Step 1:')
    st.write(
    """
    Have an excel table generated by MicroMeasure of the karyotype to study.
    MicroMeasure is a scientific image analysis program, whose application is intended for cytological, cytogenetic and
    cytotaxonomic studies. This program receives images in a specific format and, through internal calculations, returns
    an excel with important information on the karyotype under study.
    """
    )

    st.image("imagenes/paso1.png", caption="Example of Excel obtained from MicroMeasure.")

    st.subheader('Step 2:')
    st.write(
    """
    Go to the 🥀**Index calculation** menu and click on the button to upload files. Choose the excel file obtained with
    MicroMeasure.
    """
    )

    st.image("imagenes/paso2_eng.png", caption="Corresponding menu and button to upload excel file.")

    st.subheader('Step 3:')
    st.write(
    """
    Once the excel file has been uploaded to the web application, a menu will appear to select the indices to be
    calculated (See 📃**Documentation** to revise how the indices are calculated). Select the indices you need and click
    on the button _Calculate Indices_. If everything was done correctly, a table will be displayed that, for each excel
    file uploaded (indicated by its name), will show the value of the selected indices to the right. In addition, there
    is the option to download the displayed table in excel format by clicking on the button 📥 _Download as Excel_.
    The file will be downloaded with the name Indices_dd-mm-yyyy_hhmmss.xlsx, where dd-mm-yyyy and hhmmss correspond,
    respectively, to the exact date and time at the time of calculating the indices.
    """
    )

    st.image("imagenes/paso3_eng.png",
             caption="Final result: Table with the indices selected for each uploaded file, and download button.")

    st.subheader('In case of errors')

    st.markdown("""In case of having errors when using the app, it is recommended to refresh the page. If the problem persists, write\
    an email to the author (alvaroo.g98@gmail.com) or create an *Issue* on the \
    <a href="https://github.com/Zekess/Indices_de_asimetria">**GitHub**</a>  page (See 📃**Documentation**), \
    detailing the problem and attaching images if necessary.""", unsafe_allow_html=True)

    st.subheader('Test file')
    st.write(
    """
    You can try Chromindex-UdeC with the following test excel file. It was obtained with MicroMeasure.
    """
    )

    st.download_button(
        label='📥 Download test Excel file',
        data=open('elementos_web/excel_ejemplo1.xlsx', 'rb'),
        file_name="A. hookeri subsp. hookeri.xlsx",
        mime="application/vnd.ms-excel"
    )

def indexCalc():
    st.header('Chromindex-UdeC')

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
                on_click=del_sesion_state('df_resultado')
            )

        if 'db_data' in st.session_state and 'logeado' in st.session_state:
            if st.button('Save to my account'):
                guardar(st.session_state['db_data']) 
        if 'db_data' in st.session_state and 'logeado' not in st.session_state:
            st.write("If you want to save the data to your account, log in to the Account tab")

def docs():
    st.header('Documentation')

    st.markdown("""The source code is aviable at the following GitHub repository:
    <a href="https://github.com/Zekess/Indices_de_asimetria">**Chromindex-UdeC Repository**</a>.\n""",
                unsafe_allow_html=True)
    st.markdown(""" Below there is a summary of the indices that **Chromindex-UdeC** includes. Note that in what
    follows, _n_ represents the total number of chromosomes. Also the standard deviation corresponds to the sample
    standard deviation (unbiased).""", unsafe_allow_html=True)

    # st.markdown("<h4>A<sub>1</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    # st.markdown("El índice __A<sub>1</sub>__ es calculado de la siguiente forma:", unsafe_allow_html=True)
    # st.latex(r'A_1 = 1 - \frac{\sum_{i=1}^n\frac{b_i}{B_i}}{n_p}.')
    # st.markdown('Donde ___b_<sub>i</sub>__ y ___B_<sub>i</sub>__ corresponden, respectivamente, al largo promedio de los brazos\
    # cortos y al largo promedio de los brazos largos del _i_-ésimo par de cromosomas homólgos. Y ___n<sub>p</sub>___ es la \
    # cantidad de pares de cromosomas.', unsafe_allow_html=True)

    st.markdown("<h4>A<sub>2</sub> (Romero Zarco, 1986)</h4>", unsafe_allow_html=True)
    st.markdown("The index __A<sub>2</sub>__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'A_2 = \frac{s}{x}.')
    st.markdown("""Where ___s___ and ___x___ are the standard deviation and the mean of the length of
    chromosomes.""", unsafe_allow_html=True)

    st.markdown("<h4>Ask% (Arano y Saito, 1980)</h4>", unsafe_allow_html=True)
    st.markdown("The index __Ask%__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'Ask\% = \frac{\sum_{i=1}^n L_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown("""Where ___L<sub>i</sub>___ and ___l<sub>i</sub>___ are the length of the longest arm and the length of
     the shortest arm of the _i_-th chromosome, respectively. That is, this index is calculated as the sum of the lengths
     of the long arms divided by the sum of the lengths of all the chromosomes.""", unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CI</sub> (Paszko, 2006)</h4>", unsafe_allow_html=True)
    st.markdown("The index __CV<sub>CI</sub>__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'CV_{CI} = \frac{s_{CI}}{x_{CI}}\times 100.')
    st.markdown("""Where ___s<sub>CI</sub>___ and ___x<sub>CI</sub>___ are the standard deviation and the mean of the
    centromeric indices, respectively.""", unsafe_allow_html=True)

    st.markdown("<h4>CV<sub>CL</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
    st.markdown("The index __CV<sub>CL</sub>__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'CV_{CL}= A_2 \times 100.')
    st.markdown("""Where ___A<sub>2</sub>___ corresponds to the index proposed by Romero Zarco, previously shown.""",
                unsafe_allow_html=True)

    st.markdown("<h4>M<sub>CA</sub>  (Peruzzi y Eroglu, 2013)</h4>", unsafe_allow_html=True)
    st.markdown("The index __M<sub>CA</sub>__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'M_{CA} = \frac{\sum_{i=1}^n \frac{L_i-l_i}{L_i+l_i}}{n} \times 100.')
    st.markdown("""Where ___L<sub>i</sub>___ and ___l<sub>i</sub>___ are the length of the longest arm and the length of
    the shortest arm of the _i_-th chromosome, respectively.""", unsafe_allow_html=True)

    st.markdown("<h4>Sy<sub>i</sub>  (Greihuber y Speta, 1976)</h4>", unsafe_allow_html=True)
    st.markdown("The index __Sy<sub>i</sub>__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'Sy_i = \frac{x_l}{x_L} \times 100.')
    st.markdown("""Where ___x<sub>l</sub>___ and ___x<sub>L</sub>___ are the mean length of the short arms and the
    mean length of the long arms, respectively.""", unsafe_allow_html=True)

    st.markdown("<h4>TF% (Huziwara, 1962)</h4>", unsafe_allow_html=True)
    st.markdown("The index __TF%__ is calculated in the following way:", unsafe_allow_html=True)
    st.latex(r'TF\% = \frac{\sum_{i=1}^n l_i}{\sum_{i=1}^n L_i+l_i}.')
    st.markdown("""Where ___L<sub>i</sub>___ and ___l<sub>i</sub>___ are the length of the longest arm and the length
    of the shortest arm of the _i_-th chromosome, respectively. That is, this index is calculated as the sum of the
    lengths of the short arms divided by the sum of the lengths of all the chromosomes. Note that Ask%+TF%=1 for any
    set of chromosomes.""", unsafe_allow_html=True)



    write_espacios(2)
    st.header('Graphics Documentation')
    st.markdown("""To generate graphics, the file must be in .XLS, .XLSX, or .CSV format. 
                Additionally, the columns should follow the following order: Taxa, Infrataxa, Population, and Indices. Each column should 
                have its corresponding header in the first row, and the indices can be of any type and arranged in any 
                order. Below is an example:""", unsafe_allow_html=True)

    example = pd.read_csv("./ejemplo/Baeza_Werdermannii.csv")
    st.dataframe(example.set_index(example.columns[0])[:10], width=1400)

    st.download_button(
        label="Download CSV Example",
        data=example.to_csv().encode('utf-8'),
        file_name="example.csv",
        key='download_button'
    )

    st.markdown("<h4>Heatmap</h4>", unsafe_allow_html=True)
    st.markdown("""Its implementation is done using the __clustermap__ function and the histogram shown 
                in the upper left corner is created using the __histplot__ function, both belonging to the __seaborn__ library. 
                Data scaling is performed using Z-scores, applied independently to each column. 
                Dendrograms are created using the average linkage method with unstandardized data, and 
                the Euclidean metric is used to calculate distances between points.""", unsafe_allow_html=True)

    st.markdown("<h4>Scatter plot with Convex Hull and Boxplots</h4>", unsafe_allow_html=True)
    st.markdown("""Its implementation is done using the __spatial.ConvexHull__ function from the __scipy__ library. The boxplots used 
                are from the __seaborn__ library, generated with the __boxplot__ function.""", unsafe_allow_html=True)

    st.markdown("<h4>Boxplot</h4>", unsafe_allow_html=True)
    st.markdown("""Its implementation is done using the __express.box__ function from the __plotly__ library.""", unsafe_allow_html=True)

    st.markdown("<h4>Graph 1 2</h4>", unsafe_allow_html=True)
    st.markdown("""Its implementation is done using the __pyplot__ function from the __matplotlib__ library.""", unsafe_allow_html=True)
        


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

def about():
    st.header('About Chromindex-UdeC')

    st.markdown(
    """
    Cytotaxonomy is a branch of cytogenetics, dedicated to the comparative study of karyological traits for
    systematic and evolutionary purposes (Siljak-Yakovlev & Peruzzi 2012). It has been very important in recent
    years because its contribution to the knowledge of the evolution and phylogeny of vascular plants has allowed a
    clearer and more precise understanding of the mechanisms involved in plant diversification.

    Currently, the use of karyotype asymmetry indices, both intra- and interchromosomal, is widely used in plant
    systematics (Paszko 2006; Peruzzi & Eroglu 2013). One of the daily difficulties is the tabular use of the
    generated data. Normally, these data are very numerous and complex to use, which can generate unintentional
    errors that can generate noise in the interpretation of the results. For this reason, the contribution of the
    Chromindex-UdeC program can help to remedy this situation.

    **Chromindex-UdeC** was born from the motivation to create a tool to facilitate the calculation of karyotype
    asymmetry indices, with the idea of speeding up research and avoiding the complex calculations behind these
    indices. Chromindex-UdeC was conceived in the context of the internship of the Data Science Unit of the
    University of Concepción. This internship was a cooperation between the collaborators presented on the home
    page.

    To develop the **Chromindex-UdeC** program, the first step was to create a **Python** script (Rossum & Drake
    2009) capable of reading Excel tables and retrieving values of the different indexes. However, a user-friendly
    interface was also needed so that any researcher could use this tool, without the need to understand
    programming. For this purpose, the **Streamlit** library (https://streamlit.io/) was used. This library allows
    the creation of a web application from Python code without major difficulties. Once the code was obtained, it
    was uploaded to **GitHub** (https://github.com/) to use a server for mounting the application on the web.
    """,
    unsafe_allow_html=True
    )
    write_espacios(2)

    st.caption("<h10>Van Rossum, G. & Drake, F.L., 2009. Python 3 Reference Manual, Scotts Valley, CA: \
               CreateSpace.</h10>", unsafe_allow_html=True)

def graphSelector():
    st.header("Graph selector")
    upload = st.file_uploader(
        'Upload file(s)', 
        type=['xls', 'xlsx','csv'], 
        accept_multiple_files=True,
        on_change=add_sesion_state('uploader_key', 1)
    )
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
                st.error(f'Unsupported file format for {uploaded_file.name}. Please upload an Excel (.xlsx or .xls) or CSV (.csv) file.')
                continue  # Skip processing this file and continue with the next
        
            # Display the DataFrame for each uploaded file
            st.subheader(f'Data from {uploaded_file.name}:')
            st.dataframe(df)
            selectgraphtype = st.selectbox(
                'Select the type of graph:',
                ('Continuous graph', "Heatmap", "Scatter plot with Convex Hull and Boxplots", "Boxplot"),
            )
            #we store the boxplot in case the user want to download them
            boxplot_figs = []
            if selectgraphtype == 'Continuous graph':
                continuous(df)

            elif selectgraphtype == "Heatmap":
                heatmap(df)

            elif selectgraphtype == 'Scatter plot with Convex Hull and Boxplots':
                plot_convex_hull(df)

            elif selectgraphtype == "Boxplot":
                boxplot_figs = boxplot(df)

                
            formato = st.selectbox("Exportation format:", ["PNG", "JPEG", "PDF"])

            if st.button("Export Graph"):
                buffer = io.BytesIO()
                extension = formato.lower()
                #to generate the boxplots a different library of graphs is used therefore the boxplots are saved in a different way
                if selectgraphtype == "Boxplot":
                    print("")
                    for index, figure in enumerate(boxplot_figs):
                        buffer = io.BytesIO()
                        pio.write_image(figure, buffer, format=extension)

                        # Download graph
                        st.markdown(get_binary_file_downloader_html(buffer, f"graph_{index + 1}.{extension}", f"Download Graph {index + 1}"), unsafe_allow_html=True)
                else:
                    plt.savefig(buffer, format = formato.lower())
                    # Download graph
                    st.markdown(get_binary_file_downloader_html(buffer, f"graph.{extension}", "Download Graph"), unsafe_allow_html=True)


    st.subheader("How to use?")
    st.write(
        """
        Web developers often use the Chrom-Index as a reference point to optimize their 
        websites and web applications for the best possible user experience on the Chrome browser.
        It provides valuable insights into how efficiently a site runs on Chrome and helps 
        identify areas for improvement. Just upload your .xls file with the correct format and we 
        will process the file and generate the graphs.
        """
    )
    st.subheader("What is Chrom-Index?")
    st.write(
        """
        In the world of web browsers, the Chrom-Index is a term that has been gaining popularity 
        among tech enthusiasts and developers alike. It represents a unique metric designed to 
        measure the efficiency and performance of the browser across various platforms and devices.
        """
    )

def get_binary_file_downloader_html(bin_data, file_label, button_text):
    data = base64.b64encode(bin_data.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{data}" download="{file_label}">{button_text}</a>'
    return href

def db():
    if not 'logeado' in st.session_state:
        create_user()
        login()
    else:
        username = st.session_state["logeado"]
        st.header(f"Welcome {username}")
        ver()

