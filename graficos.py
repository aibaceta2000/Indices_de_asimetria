import plotly.express as px
import streamlit as st


def heatmap(matriz, color="blues"):
    fig = px.imshow(matriz, color_continuous_scale=color)
    st.plotly_chart(fig)