import pandas as pd

def extract_data():
    df = pd.read_excel(
        "data/Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx",
        header=[0,1,2]
    )
    return df

df = extract_data()

print(df.columns.tolist())
