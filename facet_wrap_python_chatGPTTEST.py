import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# --- 1. Load the data ---
df = pd.read_csv(
    "~/Desktop/1-Sandbox/Random_values_table.tsv",
    sep="\t"
)

#print(df)

# --- 2. Convert to long format (like pivot_longer) ---
longdata = df.melt(
    value_vars=[col for col in df.columns if col.startswith("Sample")],
    var_name="Sample",
    value_name="Value"
)
#longdata.to_csv("longdata_output.tsv", sep="\t", index=False)

# --- 3. Define facet colors ---
facet_colors = {
    "Sample_1": "seagreen",
    "Sample_2": "skyblue",
    "Sample_3": "orange",
    "Sample_4": "purple",
    "Sample_5": "pink",
    "Sample_6": "gold",
    "Sample_7": "turquoise",
    "Sample_8": "brown"
}

# --- 4. Create FacetGrid ---
g = sns.FacetGrid(
    longdata, 
    col="Sample", 
    col_wrap=4, 
    sharey=False, 
    height=3
)

# --- 5. Plot boxplots + jitter points ---
def plot_box_jitter(data, color, **kwargs):
    sns.boxplot(
        data=data, 
        y="Value", 
        color="#96bddd", 
        width=0.5, 
        fliersize=0, 
        ax=plt.gca()
    )
    sns.stripplot(
        data=data, 
        y="Value", 
        color="#99bee8", 
        size=4, 
        jitter=0.15, 
        edgecolor="black", 
        linewidth=0.5,
        ax=plt.gca()
    )

g.map_dataframe(plot_box_jitter, color=None)

# --- 6. Style facet titles (strip backgrounds) ---
for ax in g.axes.flatten():
    sample_name = ax.get_title().split(" = ")[-1]
    color = facet_colors.get(sample_name, "gray")

    # Set facet title background color
    ax.set_title(sample_name, fontsize=11, color="white", weight="bold")
    ax.title.set_backgroundcolor(color)

    # Remove x-axis ticks/labels
    ax.set_xticks([])
    ax.set_xlabel("")

# --- 7. Final layout ---
g.fig.tight_layout()
plt.savefig("facet_wrap_python_chatGPTTEST.png", dpi=300)
