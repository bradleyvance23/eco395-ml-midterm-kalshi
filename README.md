# Opening Hour Financial Movement Using Kalshi Federal Funds Rate Predictions

## Project Overview
This project seeks to predict how the financial markets move during the opening hour based on Kalshi's Federal Funds Rate Prediction Market using Kalshi's API along with S&P 500 Overnight futures trading activity and other macroeconomic indicates such as treasury yields, VIX (volatility index for all stocks traded), and the federal funds rate. The movement measures the difference between the previous trading day's closing price and the current trading day's opening price.

*Further discuss problem and assert goals*

## Data
### Data Sources
Train/Forecast window: 07/30/2025 - 03/10/2026
The S&P 500 opening and closing price data is collected from Yahoo's S&P 500 Data via the yfinance python library. S&P500 overnight futures are also collected through the yfinance python library.
3 month, 2 year, and 10 year treasury yields are collected from the [FRED's API](https://fred.stlouisfed.org/docs/api/api_key.html) along with the yield curve, VIX, and the federal funds rate for a given day. 
The Federal Funds Rate Prediction Market is collected from [Kalshi's API](https://docs.kalshi.com/welcome) using the series ticker "KXFEDDECISION"
The data set values range from July 30th 2025 to March 10th 2026.
### Data Collection and Cleaning
The project uses a Jupiter Notebook called the [SP500_notebook](SP500_notebook.ipynb) to sort through the Yahoo S&P 500 data and collect the intraday differences between the previous trading day's closing price and the current trading day's opening price. SP500 data is pulled from the yahoo finance api in a daily, wide dataframe with multiple indexes. The dataframe indexes are collapsed to be indexed only on date, day change %, and lag variables are added to the data frame. The S&P 500 data is exported into a csv file under [SP500_data](SP500_data.csv). 

The project also uses anoter Jupiter Notebook called the [SP500futures_otebook](SP500futures_notebook.ipynb) to sort through the Yahoo S&P 500 futures data for overnight trading. The notebook collects the trading price hourly starting from market close from 6:00pm EST to thirty minutes before market open at 9:00am EST. The data then creates an overnight return variable, an overnight volatility variable, and collects the last observed hourly price at 9:00am EST to be stored in a csv file. The S&P 500 overnight futures data is exported into a csv file under [Overnight_SP500_data](Overnight_SP500_data.csv). 

The python file called [fred_data_download](fred_data_download.py) collects the 3 month, 2 year, and 10 year treasury yields, the yield curve, VIX, and the federal funds rate for the given period. The file pulls the data into a single dataframe used to parquet for pipeline.

*summarize the documentation of the data like in Causal*
*document all columns/features that are relevant to your analysis*
*summarize what isn’t in the data*

All time data will be displayed in Eastern Time (EST) for consistency with operating market hours
### Data Limitations
Time frame provided by FRED is limited (only a little more than 7 months). The past 7 months have experienced considerable volatility given an increased prevalence of policy shocks.

## Methodology
*explain and evaluated modeling approaches*
### Modeling Limitations 

## Results
### Recommendations
*discuss best model approach*
## Limitations

## Reproduction
1. Clone the repository `git@github.com:bradleyvance23/eco395-ml-midterm-kalshi.git`
2. Install additional packages `pip install -r requirements`
3. Run 


