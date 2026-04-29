import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import pandas as pd

sns.set_theme(style="white", context="talk")

def style_ax(ax):
    # Background
    ax.set_facecolor("#fbfbfb")  # bright snow

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

def create_individual_fig(figsize=(10, 7)):
    """Helper to create a standard figure and axis"""
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def visualize_data(df, window=4):

    # --- COLOR SYSTEM (by country) ---
    COLORS = {
        "EU": "#2563EB",   # blue
        "AT": "#FF3366",   # red
        "DE": "#011627"    # black
    }

     # --- FIGURE 1: EU Prices ---
    fig1, ax1 = create_individual_fig()

    relevant_columns = [col for col in df.columns if "EU" in col and col != "Date"]

    if any("Gasoline" in col for col in relevant_columns):
        linestyle = "-"
        alpha = 1
    else:
        linestyle = "--"
        alpha = 0.9

    ax1.plot(
        df["Date"],
        df[relevant_columns],
        label=relevant_columns,
        color=COLORS["EU"],
        linestyle=linestyle,
        alpha=0.2
    )

    ax1.plot(
        df["Date"],
        df[relevant_columns].rolling(window).mean(),
        label=[f"{col} - Rolling Average" for col in relevant_columns],
        color=COLORS["EU"],
        linewidth=2.2,
        linestyle=linestyle,
        alpha=alpha
    )

    # --- TITLE ---
    ax1.set_title(
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

    ax1.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax1.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    ax1.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(ax1)


     # --- FIGURE 2: Volatility ---
    fig2, ax2 = create_individual_fig()

    relevant_columns = [col for col in df.columns if "EU" in col and col != "Date"]

    if any("Gasoline" in col for col in relevant_columns):
        linestyle = "-"
        alpha = 1
    else:
        linestyle = "--"
        alpha = 0.9

    ax2.plot(
        df["Date"],
        df[relevant_columns].rolling(window).std(),
        label=f"{relevant_columns} Volatility",
        color=COLORS["EU"],
        linewidth=2.2,
        linestyle=linestyle,
        alpha=alpha
    )

    # --- TITLE ---
    ax2.set_title(
        "Price Volatility (Rolling Std)",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    # --- Y RANGE ---
    relevant_columns = [col for col in df.columns if "EU" in col and col != "Date"]

    numeric_df = df[relevant_columns]       

    y_min = numeric_df.std().min()
    y_max = numeric_df.std().max()

    ax2.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax2.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    ax2.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(ax2)


     # --- FIGURE 3: AT vs EU Spread ---
    fig3, ax3 = create_individual_fig()

    EU_Petrol = [col for col in df.columns if "EU" in col and "Gasoline" in col]
    EU_Diesel = [col for col in df.columns if "EU" in col and "Diesel" in col]

    AT_Petrol = [col for col in df.columns if "AT" in col and "Gasoline" in col]
    AT_Diesel = [col for col in df.columns if "AT" in col and "Diesel" in col]

    petrol_spread = df[EU_Petrol].values - df[AT_Petrol].values
    diesel_spread = df[EU_Diesel].values - df[AT_Diesel].values

    ax3.plot(
        df["Date"],
        petrol_spread,
        label="Gasoline Spread (€/L)",
        linestyle="-",
        alpha=1
    )

    ax3.plot(
        df["Date"],
        diesel_spread,
        label="Diesel Spread (€/L)",
        linestyle="--",
        alpha=0.9
    )

    # --- TITLE ---
    ax3.set_title(
        "Austria vs EU Price Spread",
        fontsize=18,
        pad=15,
        weight="bold"
    )

    # --- Y RANGE ---
    y_min = min(petrol_spread.min(), diesel_spread.min())
    y_max = max(petrol_spread.max(), diesel_spread.max())

    ax3.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax3.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    ax3.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(ax3)


     # --- FIGURE 4: Product Spread ---
    fig4, ax4 = create_individual_fig()

    EU_Petrol = [col for col in df.columns if "EU" in col and "Gasoline" in col]
    EU_Diesel = [col for col in df.columns if "EU" in col and "Diesel" in col]

    eu_spread = df[EU_Petrol].values - df[EU_Diesel].values

    ax4.plot(
        df["Date"],
        eu_spread,
        label="EU Petrol vs Diesel Spread (€/L)",
        linestyle="-",
        alpha=1
    )

    # --- TITLE ---
    ax4.set_title(
        "EU Petrol vs Diesel Spread",
        fontsize=18,
        pad=15,
        weight="bold"
    )

        # --- Y RANGE ---
    y_min = eu_spread.min()
    y_max = eu_spread.max()

    ax4.set_ylim(y_min - 0.05, y_max + 0.05)

    # --- X AXIS ---
    ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    ax4.axvspan(pd.Timestamp("2022-02-24"), pd.Timestamp("2023-01-01"),
        color="#9ca3af", alpha=0.1, label="Ukraine war")
    
    ax4.axvspan(pd.Timestamp("2026-02-28"), df["Date"].max(),
        color="#9ca3af", alpha=0.1, label="2026 Iran war")

    style_ax(ax4)

    plt.tight_layout()

    return fig1, fig2, fig3, fig4