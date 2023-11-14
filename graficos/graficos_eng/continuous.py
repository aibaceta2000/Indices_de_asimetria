import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def continuous(df):
    available_columns = df.columns[3:]  # get columns from 3 to end
    selected_column = st.selectbox("Select an index", available_columns)

    plt.figure(figsize=(8, 6))
    plt.plot(df[selected_column])  # Use the selected_column for plotting
    plt.title(f'Graph: {selected_column} Column Plot')
    plt.xlabel('Index')
    plt.ylabel(f'{selected_column} Values')
    st.pyplot(plt)
