import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd

sns.set_theme(style="white", context="talk")

def style_ax(axs):
    # Background
    axs.set_facecolor("#ffffff")  # bright snow

    # Grid (subtle, vertical only)
    axs.grid(True, axis="y", color="#9ca3af", linestyle="--", alpha=0.4)

    # Customize spines
    sns.despine(ax=axs, left=False, bottom=False)

    for spine in ["left", "bottom", "right", "top"]:
        axs.spines[spine].set_linewidth(1.25)
        axs.spines[spine].set_color("#9ca3af")

    # Tick styling
    axs.tick_params(axis='x', labelsize=11, rotation=30)
    axs.tick_params(axis='y', labelsize=12)

    # Labels
    axs.yaxis.label.set_color("#242424")
    axs.xaxis.label.set_color("#242424")
    axs.set_ylabel("€/L", fontsize=14)

    # Title
    axs.title.set_color("#242424")
    
    # Grid
    axs.legend(
        frameon=False,
        ncol=2,
        fontsize=10,
        loc="upper left"
    )

def visualize_data(df, window=4):

    fig, axs = plt.subplots(4, 1, figsize=(16, 14), sharex=True)

    # --- COLOR SYSTEM (by country) ---
    COLORS = {
        "EU": "#2563EB",   # blue
        "AT": "#FF3366",   # red
        "DE": "#011627"    # black
    }

    # --- PLOT (grouped logic) ---
    for col in df.columns:
        if col == "Date" or "EU" not in col:
            continue

        if "EU" in col:
            country = col.split("_")[0]   # EU, AT

        if "Gasoline" in col:
            linestyle = "-"
            alpha = 1
        else:
            linestyle = "--"
            alpha = 0.9

        axs[0].plot(
            df["Date"],
            df[col],
            label=col,
            color=COLORS[country],
            linestyle=linestyle,
            alpha=0.2
        )

        axs[0].plot(
            df["Date"],
            df[col].rolling(window).mean(),
            label=f"{col} '- Rolling Average'",
            color=COLORS[country],
            linewidth=2.2,
            linestyle=linestyle,
            alpha=alpha
        )

    # --- TITLE ---
    axs[0].set_title(
        "EU Fuel Prices (Raw vs Smoothed)",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    # --- Y RANGE ---
    for col in df.columns:
        
        if col == "Date" or "EU" not in col:    

            numeric_df = df.drop(columns=col)

    y_min = numeric_df.min().min()
    y_max = numeric_df.max().max()

    axs[0].set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    axs.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    axs.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    axs.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    axs.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(axs)

    plt.tight_layout()

    return fig
