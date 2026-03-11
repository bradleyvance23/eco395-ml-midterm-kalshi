import os
import yfinance as yf
import pandas as pd

def download_futures(start_date, end_date):
    """Download E-mini S&P 500 futures data and return as DataFrame"""
    es = yf.download(
        "ES=F",
        start=start_date,
        end=end_date,
        interval="60m",
    )
    es.columns = es.columns.droplevel(1)
    es = es.reset_index()
    es['Datetime'] = pd.to_datetime(es['Datetime'])
    es = es.set_index('Datetime')

    overnight = es[
        (es.index.time >= pd.to_datetime("18:00").time()) |
        (es.index.time <= pd.to_datetime("09:29").time())
    ].copy() 

    overnight['Return'] = overnight['Close'].pct_change()
    overnight['Date'] = pd.to_datetime(overnight.index.date)
    evening_mask = overnight.index.time >= pd.to_datetime("18:00").time()
    overnight.loc[evening_mask, "Date"] += pd.Timedelta(days=1)

    overnight_features = overnight.groupby('Date').agg(
        Overnight_Return = ('Return', 'sum'),
        Overnight_Volatility = ('Return', 'std'),
        Futures_Last_Price = ('Close', 'last')
    )
    overnight_features = overnight_features.fillna(0)
    return overnight_features

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    futures = download_futures(start_date="2025-07-30", end_date="2026-03-11")
    futures.to_csv("data/Overnight_SP500_data.csv")