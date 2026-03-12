import os
import fredapi
import pandas as pd
from dotenv import load_dotenv
import papermill as pm

load_dotenv()

fred = fredapi.Fred(api_key=os.getenv("FRED_API_KEY"))

SERIES = {
    "3m_treasury": "DGS3MO",
    "2yr_treasury": "DGS2",
    "10yr_treasury": "DGS10",
    "yield_curve": "T10Y2Y",
    "VIX": "VIXCLS",
    "fed_funds_rate": "DFF"
}

START_DATE = "2025-07-30"


def pull_series(series_id, start_date):
    return fred.get_series(series_id, observation_start=start_date)


def pull_all_series(series_dict, start_date):
    frames = {
        name: pull_series(series_id, start_date)
        for name, series_id in series_dict.items()
    }
    return pd.DataFrame(frames)


def run_fred_download():
    df = pull_all_series(SERIES, START_DATE)
    df.index.name = "date"
    df.to_parquet("fred_data.parquet")
    print(df.head())


if __name__ == "__main__":
    
    # download fred data
    run_fred_download()

    # run notebook pipeline
    pm.execute_notebook(
        "SP500_notebook.ipynb",
        "SP500_notebook_output.ipynb"
    )