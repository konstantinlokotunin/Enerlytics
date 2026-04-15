def clean_oil_data(df):
    df = df.rename(columns={
        "period": "date",
        "value": "oil_price"
    })

    df["date"] = pd.to_datetime(df["date"])
    df["oil_price"] = df["oil_price"].astype(float)

    return df[["date", "oil_price"]]