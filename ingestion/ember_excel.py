import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def load_raw_ember(path: str) -> pd.DataFrame:
    logging.info("Loading raw Ember dataset...")

    try:
        df = pd.read_csv(path)  
    except Exception as e:
        logging.error(f"Failed to load dataset: {e}")
        raise

    logging.info(f"Raw shape: {df.shape}")
    return df

def inspect(df: pd.DataFrame):
    print(df.head())
    print(df.columns)

df = load_raw_ember("https://files.ember-energy.org/public-downloads/price/outputs/european_wholesale_electricity_price_data_daily.csv")

inspect(df)