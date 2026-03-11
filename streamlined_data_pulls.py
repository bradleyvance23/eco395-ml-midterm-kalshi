from fred_data_download import pull_all_fred, FRED_SERIES
from SP500_notebook import download_sp500
from SP500futures_notebook import download_futures
from pull_api import download_kalshi_data
import os

START_DATE = "2025-07-30"
END_DATE = "2026-03-11"

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    fred_df = pull_all_fred(FRED_SERIES, START_DATE)
    fred_df.index.name = "date"
    fred_df.to_csv("data/fred_data.csv")

    sp = download_sp500(start_date=START_DATE, end_date=END_DATE)
    sp.to_csv("data/SP500_data.csv")

    futures = download_futures(start_date=START_DATE, end_date=END_DATE)
    futures.to_csv("data/Overnight_SP500_data.csv")

    kalshi_df = download_kalshi_data()
    kalshi_df.to_csv("data/kalshi_data_raw.csv", index=True)
