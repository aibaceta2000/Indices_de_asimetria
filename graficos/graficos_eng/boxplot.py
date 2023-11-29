import streamlit as st
from utilidades import *
from clases import *
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

def boxplot(df):
    #Primero creamos un dataframe con los datos
    df_data = pd.DataFrame(df, columns=df.columns)
    #Creamos un diccionario donde almacenaremos las infrataxas
    infrataxas = dict()
    for index, value in enumerate(df_data['Infrataxa']):
        if value not in infrataxas:
            infrataxas[value] = index
    #infrataxas_graph_data = dict()
    indexes = df_data.iloc[:, 3:]
    #En la siguiente parte se almacenan los datos de los indices por cada infrataxa en caso de que sea necesarias 
    #para una futura implementacion
    #for index, (keys, values) in enumerate(infrataxas.items()):
    #    if index >=0 and index < len(infrataxas) - 1:
    #        infrataxas_graph_data[keys] = df_data.iloc[values:list(infrataxas.values())[index + 1], 3:]
    #    else:
    #        infrataxas_graph_data[keys] = df_data.iloc[values:len(df_data), 3:]
    figs = []
    #Creamos un arreglo para almacenar las secuencias de colores disponibles
    aviable_colors = ['Plotly', 'D3', 'G10','T10','Alphabet','Dark24','Light24','Set1','Pastel1'
                      ,'Dark2','Set2','Pastel2','Set3','Antique','Bold','Pastel','Prism','Safe','Vivid']
    #Creamos un selectbox para permitirle al usuario elegir la secuencia de colores que desee
    selected_color = st.selectbox("Select a Color Sequence", aviable_colors)
    #Almacenamos el color seleccionado
    graph_color = getattr(px.colors.qualitative, selected_color)
    #Creamos un slider para permitirle al usuario modificar el ancho de las cajas del boxplot
    distance = st.slider("width of the boxes", value=0.5, min_value=0.0, step=0.1, max_value=1.0)
    #Almacenamos los indices disponibles para que el usuario pueda seleccionar sobre que indice comparar las infrataxas
    indicesDisponibles = list(df.columns[3:])
    #Creamos en la multiseleccion para que los usuarios seleccionen los indices para los que desean generar los graficos,
    #Sobre estos indices se compararan las infrataxas 
    indicesSeleccionados = st.multiselect("Selected indexes", indicesDisponibles, default=indicesDisponibles)
    #A continuacion se se generan los graficos con las opciones de personalizacion seleccionadas y se muestran por pantalla
    for (columnName) in indexes.columns:
        if columnName in indicesSeleccionados:
            fig = px.box(df_data, y=columnName, boxmode='group', x="Infrataxa", color="Infrataxa", color_discrete_sequence=graph_color)
            fig.update_layout(height=600, width=800)
            fig.update_traces(width=distance)
            figs.append(fig)
    for index, figure in enumerate(figs):
        st.plotly_chart(figure)   
    return figs