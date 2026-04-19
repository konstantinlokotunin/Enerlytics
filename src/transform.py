import pandas as pd

def clean_oil_data(df):

    df.columns = [
        "_".join([str(level).strip() for level in col if "Unnamed" not in str(level)])
        for col in df.columns
]

    df = df.rename(columns={df.columns[0]: "date"})
    df = df.dropna(subset=["date"])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["date_str"] = df["date"].dt.strftime("%Y-%m-%d")

    df_filtered = df[df["date"].between("2020-01-01", "2026-12-31")]

    cols = ["date", "date_str", "EU_price_with_tax_euro95_Euro-super 95  (I)_1000 l",
        "EU_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l",
        "AT_price_with_tax_euro95_Euro-super 95  (I)_1000 l",
        "AT_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l",
        "DE_price_with_tax_euro95_Euro-super 95  (I)_1000 l",
        "DE_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l"]

    df = df_filtered[cols]

    df = df.rename(columns={
        "EU_price_with_tax_euro95_Euro-super 95  (I)_1000 l": "EU_Price_Super95",
        "EU_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l": "EU_Price_Diesel",
        "AT_price_with_tax_euro95_Euro-super 95  (I)_1000 l": "AT_Price_Super95",
        "AT_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l": "AT_Price_Diesel",
        "DE_price_with_tax_euro95_Euro-super 95  (I)_1000 l": "DE_Price_Super95",
        "DE_price_with_tax_diesel_Gas oil automobile Automotive gas oil Dieselkraftstoff (I)_1000 l": "DE_Price_Diesel"
    })

    return df
