import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

sns.set_theme(style="white", context="talk")

def visualize_data(df):

    fig, ax = plt.subplots(figsize=(12, 6))

    # --- COLOR SYSTEM (by country) ---
    COLORS = {
        "EU": "#2563eb",   # blue
        "AT": "#16a34a",   # green
        "DE": "#dc2626"    # red
    }

    # --- PLOT (grouped logic) ---
    for col in df.columns:
        if col == "Date":
            continue

        country = col.split("_")[0]   # EU, AT, DE

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
        "Fuel Prices in Europe (EU vs Austria vs Germany)",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    ax.set_ylabel("€/L", fontsize=12)

    # --- Y RANGE ---
    y_min = df.drop(columns=["Date"]).min().min()
    y_max = df.drop(columns=["Date"]).max().max()
    ax.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS (CLEANER) ---
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # --- GRID (ONLY HORIZONTAL!) ---
    ax.grid(True, axis="y", linestyle="--", alpha=0.25)
    ax.grid(False, axis="x")

    # --- SPINES ---
    sns.despine(ax=ax)

    # --- LEGEND (clean & readable) ---
    ax.legend(
        frameon=False,
        ncol=2,
        fontsize=10,
        loc="upper left"
    )

    plt.tight_layout()
    plt.savefig("outputs/fuel_prices.png", dpi=300)
    plt.close(fig)