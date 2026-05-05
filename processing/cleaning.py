import pandas as pd
import logging

from ingestion.ember_excel import load_raw_ember

def clean_ember_data(df: pd.DataFrame) -> pd.DataFrame:

    df = df.drop(columns=["ISO3 Code"])
    df = df.rename(columns={"Price (EUR/MWhe)": "Price"})

    df["Date"] = pd.to_datetime(df["Date"])
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    df = df.dropna()

    logging.info(f"Cleaned shape: {df.shape}")
    return df

df = load_raw_ember("https://files.ember-energy.org/public-downloads/price/outputs/european_wholesale_electricity_price_data_daily.csv")

df = clean_ember_data(df)