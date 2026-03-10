import os
import fredapi
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
fred = fredapi.Fred(api_key=os.getenv("FRED_API_KEY"))

SERIES = {
    "2yr_treasury": "DGS2",
    "10yr_treasury": "DGS10",
    "yield_curve": "T10Y2Y",
    "VIX": "VIXCLS",
    "fed_funds_rate": "DFF"
    
}

START_DATE = "2025-07-30"

def pull_series(series_id, start_date):
    """Pull a single FRED series by ID and return as a pandas Series."""
    return fred.get_series(series_id, observation_start=start_date)


def pull_all_series(series_dict, start_date):
    """Pull all FRED series into a single combined DataFrame."""
    frames = {
        name: pull_series(series_id, start_date)
        for name, series_id in series_dict.items()
    }
    return pd.DataFrame(frames)

if __name__ == "__main__":
    df = pull_all_series(SERIES, START_DATE)
    df.index.name = "date"
    os.makedirs("data/fred", exist_ok=True)
    df.to_csv("data/fred/fred_data.csv")
    print(df.head())