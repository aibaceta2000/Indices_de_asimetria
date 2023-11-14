import seaborn as sns
import streamlit as st
from scipy.cluster.hierarchy import linkage
from scipy.stats import zscore


# personalizacion del heatmap
def heatmap(df):
    # seleccion indices
    indicesDisponibles = list(df.columns[3:])
    indicesSeleccionados = st.multiselect("Índices seleccionados", indicesDisponibles, default=indicesDisponibles)
    indices = [df.columns.get_loc(indice) for indice in indicesSeleccionados]

    fila = st.columns([0.15, 0.85])
    
    with fila[0]:
        st.write(' ')
        discrete_palette = st.checkbox("Paleta de colores discreta", True)
        scaled_data = st.checkbox("Escalar data", True)
        annotations = st.checkbox("Mostrar valores de celdas", False)

    available_palettes = ["Spectral", "plasma", 'RdBu']
    available_palettes += ["Set1", "Set2", "Set3", "pastel", "dark", "Paired", "Accent"] if discrete_palette else []
    
    with fila[1]:
        selected_palette = st.selectbox("Paleta de colores seleccionada:", available_palettes)  
        n_colors = st.slider("Number of colors:", value=9, min_value=3, step=1, max_value=15, disabled= not discrete_palette)
        

    if len(indicesSeleccionados) < 2:
        st.warning("Select at least 2 indexes")
    else:
        heatmapGraph(df, 
                    indices=indices,
                    color=selected_palette, 
                    n_colors=n_colors, 
                    discrete_palette=discrete_palette,
                    annot=annotations,
                    scaled_data=scaled_data)


# funcion del heatmap
def heatmapGraph(df, indices, color="Spectral", n_colors=9, discrete_palette=True, annot=False, scaled_data=True):
    col = sns.color_palette(color, n_colors=n_colors) if discrete_palette else color
    

    # atrocidad para que el clustermap use jerarquia con los datos originales y no con los datos escalados
    linkage_matrix_row = linkage(df.iloc[:, indices], method='average', metric='euclidean')
    linkage_matrix_col = linkage(df.iloc[:, indices].T, method='average', metric='euclidean')


    # clustermap
    clustermap = sns.clustermap(data        = df.iloc[:, indices], 
                                method      = 'average', 
                                metric      = 'euclidean', 
                                cmap        = col, 
                                row_linkage = linkage_matrix_row, 
                                col_linkage = linkage_matrix_col, 
                                z_score     = 1 if scaled_data else None,
                                annot       = annot,
                                cbar        = not discrete_palette)
    
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
    if discrete_palette:
        clustermap.cax.set_position([0.0, 0.85, 0.18, 0.18])
        
        datosHistograma = zscore(df.iloc[:, indices]) if scaled_data else df.iloc[:, indices]

        hist = sns.histplot(datosHistograma.to_numpy().reshape(-1), #clustermap.data2d.values.ravel(), #clustermap.data2d.to_numpy().reshape(-1), 
                            ax=clustermap.cax,
                            bins=n_colors)
        
        for bin, i in zip(hist.patches, col):
            bin.set_facecolor(i)

        hist.set_title("Color Key and Histogram")
        if scaled_data: 
            hist.set_xticks([-1, 0, 1])

        hist.set_xlabel("z-score" if scaled_data else "Value")

    st.pyplot(clustermap)

