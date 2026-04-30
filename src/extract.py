import pandas as pd

def extract_data():

    url = "https://energy.ec.europa.eu/document/download/906e60ca-8b6a-44e7-8589-652854d2fd3f_en?" \
    "filename=Weekly_Oil_Bulletin_Prices_History_maticni_4web.xlsx"

    df = pd.read_excel(url, header=[0,1,2])

    return df