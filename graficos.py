import plotly.express as px
import streamlit as st

def heatmap(matriz):
    fig = px.imshow(matriz)
    st.plotly_chart(fig, theme="streamlit")