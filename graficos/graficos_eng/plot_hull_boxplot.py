import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import streamlit as st
import itertools

available_palettes = [
    "Set1",
    "Set2",
    "Set3",
    "deep",
    "muted",
    "bright",
    "pastel",
    "dark",
    "colorblind",
    "Paired",
    "Accent",
    "husl",
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "coolwarm",
    "RdYlGn",
    "PiYG",
    "PRGn",
    "BrBG",
    "RdGy",
    "PuOr",
    "RdBu",
    "RdBu_r",
    "bwr",
    "seismic",
]


def plot_convex_hull(a):
    popu_flag = a.columns[2].lower() in ["population", "poblacion", "población"]
    # if there is a population column
    if popu_flag:
        available_columns = a.columns[3:]  # get columns from 3 to end
    else:
        available_columns = a.columns[2:]
    selected_columns = st.multiselect("Select the indexes", available_columns)

    if len(selected_columns) < 2:
        st.warning("Select at least 2 indexes")
    else:
        # get the permutations
        permutations = list(itertools.permutations(selected_columns, 2))
        # select desired permutations
        combination = st.selectbox("Select a combination", permutations)

        selected_palette = st.selectbox("Select palette:", available_palettes)

        col1, col2, col3 = st.columns(3)
        with col1:
            topboxplots = st.checkbox("Show Top Boxplots", True)
            rightboxplots = st.checkbox("Show Right Boxplots", True)
            show_hulls = st.checkbox("Show Convex Hulls", True)

        with col2:
            show_legend = st.checkbox("Show Legend", True)
            show_labels = st.checkbox("Show Labels", True)
            show_ticks = st.checkbox("Show Ticks", True)

        with col3:
            if popu_flag:
                show_population = st.checkbox("Show Population", True)
            show_coordinates = st.checkbox("Show Coordinates", False)

        # Initialize an empty DataFrame for convex hull points
        hulls = pd.DataFrame(columns=a.columns)

        # Find convex hull for each 'Infrataxa' group
        x_var, y_var = combination
        for group, data in a.groupby("Infrataxa"):
            hull = ConvexHull(data[[x_var, y_var]].values)  # Compute convex hull
            hull_points = data.iloc[hull.vertices]  # Get hull points
            hulls = pd.concat([hulls, hull_points])  # Concatenate hull points

        st.header(f"{x_var} vs {y_var}")

        palette = sns.color_palette(selected_palette, len(hulls["Infrataxa"].unique()))

        # Plot with convex hull
        fig = plt.figure(figsize=(12, 6))

        # Define positions for the main scatter plot and boxplot axes
        startx, starty, w, h = 0.1, 0.1, 0.75, 0.75
        scatter_ax = plt.axes([startx, starty, w, h])
        if rightboxplots:
            boxplot_ax = plt.axes([w + 0.11, starty, 0.1, h])
        if topboxplots:
            boxplot_ax2 = plt.axes([startx, h + 0.11, w, 0.1])

        # Plot Scatter plot
        for i, (group, data) in enumerate(a.groupby("Infrataxa")):
            scatter_ax.scatter(
                data[x_var], data[y_var], label=group, s=30, c=[palette[i]]
            )

            # show point coordinates
            if show_coordinates:
                for x, y in zip(data[x_var], data[y_var]):
                    scatter_ax.annotate(
                        f"({x:.1f}, {y:.1f})",
                        xy=(x, y),
                        xytext=(-10, 5),
                        textcoords="offset points",
                        fontsize=8,
                    )
            # show the point value (population column)
            if popu_flag:
                if show_population:
                    for x, y, population in zip(
                        data[x_var], data[y_var], data["Population"]
                    ):
                        scatter_ax.annotate(
                            f"{population}",
                            xy=(x, y),
                            xytext=(-10, 5),
                            textcoords="offset points",
                            fontsize=8,
                        )

        # Plot Convex hull
        if show_hulls:
            for i, (group, data) in enumerate(hulls.groupby("Infrataxa")):
                hull = ConvexHull(data[[x_var, y_var]].values)
                for simplex in hull.simplices:
                    scatter_ax.plot(
                        data[x_var].values[simplex],
                        data[y_var].values[simplex],
                        color=palette[i],
                    )

                scatter_ax.fill(
                    data[x_var].values[hull.vertices],
                    data[y_var].values[hull.vertices],
                    alpha=0.2,
                    color=palette[i],
                )

        # x and y labels
        if show_labels:
            scatter_ax.set_xlabel(x_var)
            scatter_ax.set_ylabel(y_var)
        else:
            scatter_ax.set(xlabel=None, ylabel=None)

        # legend
        if show_legend:
            scatter_ax.legend()
        else:
            scatter_ax.legend().set_visible(False)

        # x and y ticks
        if not show_ticks:
            scatter_ax.set_xticks([])
            scatter_ax.set_yticks([])

        # Boxplots
        def plot_boxplot(ax, data, x, y, palette):
            sns.boxplot(
                x=x,
                y=y,
                data=data,
                ax=ax,
                palette=palette,
                whis=float("inf"),
            )

            ax.set(xlabel=None, ylabel=None)
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

        if rightboxplots:
            plot_boxplot(boxplot_ax, a, "Infrataxa", y_var, palette)
        if topboxplots:
            plot_boxplot(boxplot_ax2, a, x_var, "Infrataxa", palette)

        st.pyplot(fig)
