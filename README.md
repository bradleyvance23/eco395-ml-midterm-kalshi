# Opening Hour Financial Movement Using Kalshi Federal Funds Rate Predictions

## Project Overview
This project seeks to predict how the financial markets move during the opening hour based on Kalshi's Federal Funds Rate Prediction Market using Kalshi's API. The movement measures the difference between the previous trading day's closing price and the current trading day's opening price. The outcome variables of interest are 1, 2, 3. 

*Further discuss problem and assert goals*

## Data
### Data Sources
The S&P 500 opening and closing price data is collected from [Yahoo's S&P 500 Data]()
The Federal Funds Rate Prediction Market is collected from [Kalshi's]()
The data set values range from July 30th 2025 to March 10th 2026
### Data Collection and Cleaning
The project uses a Jupiter Notebook called the [S&P 500 Notebook](SP500_notebook.ipynb) to sort through the Yahoo S&P 500 data and collect the intraday differences between the previous trading day's closing price and the current trading day's opening price. The S&P 500 data is pulled into a csv file under

*summarize the documentation of the data like in Causal*
*document all columns/features that are relevant to your analysis*
*summarize what isn’t in the data*

All time data will be displayed in Eastern Time (EST) for consistency with operating market hours
### Data Limitations
Time frame provided by FRED is limited (only a little more than 7 months). The past 7 months have experienced considerable volatility given an increased prevalence of 5^W^$$GKFJGK shocks.

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
