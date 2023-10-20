import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial import ConvexHull
import streamlit as st


def plot_convex_hull(
    a, selected_palette, show_legend, show_labels, show_ticks, show_point_values
):
    combinations = [("CVCL", "MCA"), ("CVCL", "LTC"), ("MCA", "LTC")]

    # Initialize an empty DataFrame for convex hull points
    hulls = pd.DataFrame(columns=a.columns)

    # Find convex hull for each 'Infrataxa' group
    for x_var, y_var in combinations:
        for group, data in a.groupby("Infrataxa"):
            hull = ConvexHull(data[[x_var, y_var]].values)  # Compute convex hull
            hull_points = data.iloc[hull.vertices]  # Get hull points
            hulls = pd.concat([hulls, hull_points])  # Concatenate hull points

        palette = sns.color_palette(selected_palette, len(hulls["Infrataxa"].unique()))

        # Plot with convex hull
        fig = plt.figure(figsize=(12, 6))

        # Define positions for the main scatter plot and boxplot axes
        startx, starty, w, h = 0.1, 0.1, 0.75, 0.75
        scatter_ax = plt.axes([startx, starty, w, h])
        boxplot_ax = plt.axes([w + 0.11, starty, 0.1, h])
        boxplot_ax2 = plt.axes([startx, h + 0.11, w, 0.1])

        # Scatter plot with convex hull
        for i, (group, data) in enumerate(hulls.groupby("Infrataxa")):
            scatter_ax.scatter(
                data[x_var], data[y_var], label=group, s=30, c=[palette[i]]
            )
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

            if show_point_values:
                for x, y in zip(data[x_var], data[y_var]):
                    scatter_ax.annotate(
                        f"({x:.1f}, {y:.1f})",
                        xy=(x, y),
                        xytext=(-10, 5),
                        textcoords="offset points",
                        fontsize=8,
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
            scatter_ax.legend().set_visible(False)  # Hide legend if not required

        # x and y ticks
        if not show_ticks:
            scatter_ax.set_xticks([])
            scatter_ax.set_yticks([])

        # Boxplots
        ax = sns.boxplot(
            x="Infrataxa",
            y=y_var,
            data=a,
            ax=boxplot_ax,
            palette=palette,
            whis=float("inf"),
        )
        ax2 = sns.boxplot(
            y="Infrataxa",
            x=x_var,
            data=a,
            ax=boxplot_ax2,
            palette=palette,
            whis=float("inf"),
        )

        # Hide boxplots details
        for ax in [boxplot_ax, boxplot_ax2]:
            ax.set(xlabel=None, ylabel=None)
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)

        st.pyplot(fig)
