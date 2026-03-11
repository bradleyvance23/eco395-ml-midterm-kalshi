# Library imports
import os
import yfinance as yf
import pandas as pd

def download_sp500(start_date, end_date):
    """Download SP500 data and return as DataFrame"""
    sp = yf.download("^GSPC", start=start_date, end=end_date)
    sp.columns = sp.columns.droplevel(1)
    sp = sp.reset_index()
    sp.columns.name = None
    sp['Date'] = pd.to_datetime(sp['Date'])
    sp = sp.set_index('Date')
    sp['Day Change %'] = (sp['Close'] - sp['Open']) / sp['Open'] * 100
    return sp

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    sp = download_sp500(start_date="2025-07-30", end_date="2026-03-11")
    sp.to_csv("data/SP500_data.csv")