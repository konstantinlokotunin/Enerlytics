import pandas as pd

def extract_data():
    df = pd.read_excel(
        "data/Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx",
        header=[0,1,2]
    )
<<<<<<< HEAD
    return df
=======
    return df

df = extract_data()

print(df.columns.tolist())
>>>>>>> c1cb5c3261f5dd09bfb191177f6ac01d56feb379
