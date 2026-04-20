import pandas as pd

def transform_data(df):

    # --- Flatten MultiIndex columns ---
    df.columns = [
        "_".join(
            str(level).strip()
            for level in col
            if "Unnamed" not in str(level)
        )
        for col in df.columns
    ]

    # --- Rename first column to date ---
    df = df.rename(columns={df.columns[0]: "Date"})

    # --- Clean date ---
    df = df.dropna(subset=["Date"])
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # --- Filter time range ---
    df = df[df["Date"].between("2020-01-01", "2026-12-31")]

    # --- Select relevant columns (pattern-based instead of hardcoding) ---
    relevant_cols = [col for col in df.columns if any(
        key in col for key in [
            "EU_price_with_tax_euro95",
            "EU_price_with_tax_diesel",
            "AT_price_with_tax_euro95",
            "AT_price_with_tax_diesel"]
    )]

    df = df[["Date"] + relevant_cols]

    df[relevant_cols] = df[relevant_cols] / 1000

    # --- Rename columns cleanly ---
    rename_col = {
        col: col.split("_")[0] + "_" + ("Diesel Price (€/L)" if "diesel" in col.lower() else "Gasoline Price (€/L)")
        for col in relevant_cols
    }

    df = df.rename(columns=rename_col)

    return df