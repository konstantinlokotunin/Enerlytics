import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd

sns.set_theme(style="white", context="talk")

def style_ax(ax):
    # Background
    ax.set_facecolor("#f2f7fb")  # bright snow

    # Grid (subtle, vertical only)
    ax.grid(True, axis="y", color="#9ca3af", linestyle="--", alpha=0.4)

    # Customize spines
    sns.despine(ax=ax, left=False, bottom=False)

    for spine in ["left", "bottom", "right", "top"]:
        ax.spines[spine].set_linewidth(1.25)
        ax.spines[spine].set_color("#9ca3af")

    # Tick styling
    ax.tick_params(axis='x', labelsize=11, rotation=30)
    ax.tick_params(axis='y', labelsize=12)

    # Labels
    ax.yaxis.label.set_color("#242424")
    ax.xaxis.label.set_color("#242424")
    ax.set_ylabel("€/L", fontsize=14)

    # Title
    ax.title.set_color("#242424")
    
    # Grid
    ax.legend(
        frameon=False,
        ncol=2,
        fontsize=10,
        loc="upper left"
    )

def visualize_data(df, window=4):

    fig, ax = plt.subplots(figsize=(16, 14), sharex=True)

    # --- COLOR SYSTEM (by country) ---
    COLORS = {
        "EU": "#2563EB",   # blue
        "AT": "#FF3366",   # red
        "DE": "#011627"    # black
    }

    # --- PLOT (grouped logic) ---
    relevant_columns = [col for col in df.columns if "EU" in col and col != "Date"]

    if "Gasoline" in relevant_columns:
        linestyle = "-"
        alpha = 1
    else:
        linestyle = "--"
        alpha = 0.9

    ax.plot(
        df["Date"],
        df[relevant_columns],
        label=relevant_columns,
        color=COLORS["EU"],
        linestyle=linestyle,
        alpha=0.2
    )

    ax.plot(
        df["Date"],
        df[relevant_columns].rolling(window).mean(),
        label=f"{relevant_columns} '- Rolling Average'",
        color=COLORS["EU"],
        linewidth=2.2,
        linestyle=linestyle,
        alpha=alpha
    )

    # --- TITLE ---
    ax.set_title(
        "EU Fuel Prices (Raw vs Smoothed)",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    # --- Y RANGE ---
    relevant_columns = [col for col in df.columns if "EU" in col and col != "Date"]

    numeric_df = df[relevant_columns]       

    y_min = numeric_df.min().min()
    y_max = numeric_df.max().max()

    ax.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    ax.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(ax)

    plt.tight_layout()

    return fig
