import seaborn as sns
import streamlit as st
from scipy.cluster.hierarchy import linkage
import matplotlib.pyplot as plt
import numpy as np


def heatmap(df, color="Spectral"):
    # color
    colores = 9
    col = sns.color_palette(color, n_colors=colores)

    # atrocidad para que el clustermap use jerarquia con los datos originales y no con los datos escalados
    linkage_matrix_row = linkage(df.iloc[:, 3:6], method='average', metric='euclidean')
    linkage_matrix_col = linkage(df.iloc[:, 3:6].T, method='average', metric='euclidean')

    # clustermap
    clustermap = sns.clustermap(df.iloc[:, 3:6], 
                                method='average', 
                                metric='euclidean', 
                                cmap=col, 
                                row_linkage=linkage_matrix_row, 
                                col_linkage=linkage_matrix_col, 
                                z_score=1,
                                cbar=0
                                )
    
    # etiquetas especies
    row_labels = df.iloc[:, 1].values
    row_labels = [ row_labels[i] + " " + str(i+1) for i in range(len(row_labels)) ]

    row_order = clustermap.dendrogram_row.reordered_ind
    clustermap.ax_heatmap.set_yticklabels([row_labels[i] for i in row_order], fontsize=10, rotation = 0)
    


    # rotacion dendogramas
    clustermap.ax_heatmap.invert_xaxis()
    clustermap.ax_col_dendrogram.invert_xaxis()

    clustermap.ax_heatmap.invert_yaxis()
    clustermap.ax_row_dendrogram.invert_yaxis()


    # histograma
    clustermap.cax.set_position([0.0, 0.85, 0.18, 0.18])

    hist = sns.histplot(clustermap.data2d.to_numpy().reshape(-1), 
                 ax=clustermap.cax,
                 bins=colores
                 )
    
    for bin, i in zip(hist.patches, col):
        bin.set_facecolor(i)


    hist.set_title("Color Key and Histogram")
    hist.set_xticks([-1, 0, 1])
    hist.set_xlabel("z-score")





    st.pyplot(clustermap)

