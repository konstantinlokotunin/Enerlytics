import requests
import pandas as pd


def fetch_brent_oil():
    """
    Fetch Brent oil prices from EIA API
    """

    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

    params = {
        "api_key": "YOUR_API_KEY",
        "frequency": "daily",
        "data[0]": "value",
        "facets[series][]": "PET.RBRTE.D",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # 💥 crash if API fails
    data = response.json()

    records = data["response"]["data"]

    df = pd.DataFrame(records)

    return df
