import os
from pykalshi import KalshiClient
import pandas as pd
from pykalshi import CandlestickPeriod
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

def get_fed_decision_tickers(client):
    """Get all tickers associated with fed decision market"""
    markets = client.get_markets(series_ticker="KXFEDDECISION")
    df = markets.to_dataframe()
    return df, df["ticker"].tolist()

def fetch_ticker_candles(client, ticker, ticker_data):
    """Fetch hourly candlestick data for a single ticker and return as dataframe."""
    current_ts = int(datetime.now(timezone.utc).timestamp())

    start_ts = int(
        datetime.fromisoformat(
            ticker_data["open_time"].iloc[0].replace("Z", "+00:00")
        ).timestamp()
    )
    end_ts = int(
        datetime.fromisoformat(
            ticker_data["close_time"].iloc[0].replace("Z", "+00:00")
        ).timestamp()
    )

    if end_ts > current_ts:
        end_ts = current_ts

    market = client.get_market(ticker)
    candles = market.get_candlesticks(start_ts, end_ts, period=CandlestickPeriod.ONE_HOUR)
    return candles.to_dataframe()

def download_kalshi_data():
    """Download fed decision market candlestick data and return as dataframe"""
    client = KalshiClient()
    df, tickers = get_fed_decision_tickers(client)

    full_df_list = []
    for ticker in tickers:
        try:
            ticker_data = df[df["ticker"] == ticker]
            if ticker_data.empty:
                continue
            sample = fetch_ticker_candles(client, ticker, ticker_data)
            full_df_list.append(sample)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue

    return pd.concat(full_df_list, ignore_index=True)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    full_df = download_kalshi_data()
    full_df.to_csv("data/kalshi_data_raw.csv", index=True)
    print("Kalshi data pulled and saved to data/kalshi_data_raw.csv")