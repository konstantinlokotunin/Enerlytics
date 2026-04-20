import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd

sns.set_theme(style="white", context="talk")

def style_ax(ax):
    # Background
    ax.set_facecolor("#EDF3FD")  # white smoke

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

def visualize_data(df):

    fig, ax = plt.subplots(figsize=(12, 6))

    # --- COLOR SYSTEM (by country) ---
    COLORS = {
        "EU": "#2563EB",   # blue
        "AT": "#FF3366",   # red
        "DE": "#011627"    # black
    }

    # --- PLOT (grouped logic) ---
    for col in df.columns:
        if col == "Date":
            continue

        country = col.split("_")[0]   # EU, AT

        if "Gasoline" in col:
            linestyle = "-"
            alpha = 1
        else:
            linestyle = "--"
            alpha = 0.9

        ax.plot(
            df["Date"],
            df[col].rolling(4).mean(),
            label=col.replace("_", " "),
            color=COLORS[country],
            linewidth=2.2,
            linestyle=linestyle,
            alpha=alpha
        )

    # --- TITLE ---
    ax.set_title(
        "Fuel Prices in Europe (EU vs Austria)",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    # --- Y RANGE ---
    y_min = df.drop(columns=["Date"]).min().min()
    y_max = df.drop(columns=["Date"]).max().max()
    ax.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS (CLEANER) ---
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#535C65", alpha=0.1, label="Ukraine war")
    
    ax.axvspan(pd.Timestamp("2026-02-28"), pd.Timestamp("2026-04-13"),
        color="#535C65", alpha=0.1, label="2026 Iran war")

    style_ax(ax)

    plt.tight_layout()
    plt.savefig("outputs/fuel_prices.png", dpi=300)
    plt.close(fig)