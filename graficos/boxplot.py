import streamlit as st
from utilidades import *
from clases import *
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

def boxplot(df):
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
    aviable_colors = ['Plotly', 'D3', 'G10','T10','Alphabet','Dark24','Light24','Set1','Pastel1'
                      ,'Dark2','Set2','Pastel2','Set3','Antique','Bold','Pastel','Prism','Safe','Vivid']
    selected_color = st.selectbox("Select a Color Sequence", aviable_colors)
    graph_color = getattr(px.colors.qualitative, selected_color)
    distance = st.slider("width of the boxes", value=0.5, min_value=0.0, step=0.1, max_value=1.0)
    indicesDisponibles = list(df.columns[3:])
    indicesSeleccionados = st.multiselect("Selected indexes", indicesDisponibles, default=indicesDisponibles)
    for (columnName) in indexes.columns:
        if columnName in indicesSeleccionados:
            fig = px.box(df_data, y=columnName, boxmode='group', x="Infrataxa", color="Infrataxa", color_discrete_sequence=graph_color)
            #fig = px.box(df_data, y=columnName, boxmode='group', x="Infrataxa", color="Infrataxa", color_discrete_sequence=px.colors.qualitative.Antique)
            fig.update_layout(height=600, width=800)
            fig.update_traces(width=distance)
        
            #fig.update_layout(hovermode=False)
            figs.append(fig)
    for index, figure in enumerate(figs):
        st.plotly_chart(figure)   