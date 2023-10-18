import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


def heatmap(df, color="Spectral"):
    data = df.iloc[:, 3:6].values
    data = (data - data.mean()) / data.std()

    # Etiquetas
    row_labels = df.iloc[:, 1].values
    row_labels = [ row_labels[i] + " " + str(i+1) for i in range(len(row_labels)) ]
    column_labels = df.columns[3:6]


    fig, ax = plt.subplots(2, 2, width_ratios=[1, 4], height_ratios=[1, 4])
    fig.tight_layout()

    sns.heatmap(data, cmap=color, ax=ax[1, 1], cbar_ax=ax[0, 0])


    # Etiquetas
    ax[1, 1].set_yticklabels(row_labels, rotation=0, fontsize=5)
    ax[1, 1].yaxis.tick_right()
    ax[1, 1].set_xticklabels(column_labels, rotation=90, fontweight='light')
    ax[1, 1].tick_params(axis="both", which="both", length=0)

    st.pyplot(fig)