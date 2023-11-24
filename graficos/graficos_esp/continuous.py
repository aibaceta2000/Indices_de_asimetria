import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def continuous(df):
    available_columns = df.columns[3:]  # get columns from 3 to end
    selected_column = st.selectbox("Índices seleccionados", available_columns)

    plt.figure(figsize=(8, 6))
    plt.plot(df[selected_column])  # Use the selected_column for plotting
    plt.title(f'Gráfico: {selected_column} Gráfico de columnas')
    plt.xlabel('Índices')
    plt.ylabel(f'Valores {selected_column}')
    st.pyplot(plt)
