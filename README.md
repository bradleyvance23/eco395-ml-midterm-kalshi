# Opening Hour Financial Movement Using Kalshi Federal Funds Rate Predictions

## Project Overview
This project seeks to predict how the financial markets move during the opening hour based on Kalshi's Federal Funds Rate Prediction Market using Kalshi's API along with S&P 500 Overnight futures trading activity and other macroeconomic indicates such as treasury yields, VIX (volatility index for all stocks traded), and the federal funds rate. The movement measures the difference between the previous trading day's closing price and the current trading day's opening price.

*Marco and Trevor*
*Further discuss problem and assert goals*

## Data
### Data Sources
Train/Forecast window: 07/30/2025 - 03/10/2026
The S&P 500 opening and closing price data is collected from Yahoo's S&P 500 Data via the yfinance python library. S&P500 overnight futures are also collected through the yfinance python library.
3 month, 2 year, and 10 year treasury yields are collected from the [FRED's API](https://fred.stlouisfed.org/docs/api/api_key.html) along with the yield curve, VIX, and the federal funds rate for a given day. 
*Brad*
The Federal Funds Rate Prediction Market is collected from [Kalshi's API](https://docs.kalshi.com/welcome) using the series ticker "KXFEDDECISION"
*Marco*
The data set values range from July 30th 2025 to March 10th 2026.
### Data Collection and Cleaning
The project uses a Jupiter Notebook called the [SP500_notebook](SP500_notebook.ipynb) to sort through the Yahoo S&P 500 data and collect the intraday differences between the previous trading day's closing price and the current trading day's opening price. SP500 data is pulled from the yahoo finance api in a daily, wide dataframe with multiple indexes. The dataframe indexes are collapsed to be indexed only on date, day change %, and lag variables are added to the data frame. The S&P 500 data is exported into a csv file under [SP500_data](SP500_data.csv). 

The project also uses anoter Jupiter Notebook called the [SP500futures_otebook](SP500futures_notebook.ipynb) to sort through the Yahoo S&P 500 futures data for overnight trading. The notebook collects the trading price hourly starting from market close from 6:00pm EST to thirty minutes before market open at 9:00am EST. The data then creates an overnight return variable, an overnight volatility variable, and collects the last observed hourly price at 9:00am EST to be stored in a csv file. The S&P 500 overnight futures data is exported into a csv file under [Overnight_SP500_data](Overnight_SP500_data.csv). 

The python file called [fred_data_download](fred_data_download.py) collects the 3 month, 2 year, and 10 year treasury yields, the yield curve, VIX, and the federal funds rate for the given period. The file pulls the data into a single dataframe used to parquet for pipeline.

*trevor, marco, brad*

*summarize the documentation of the data like in Causal*
*document all columns/features that are relevant to your analysis*
*summarize what isn’t in the data*

All time data will be displayed in Eastern Time (EST) for consistency with operating market hours
### Data Limitations
Time frame provided by FRED is limited (only a little more than 7 months). The past 7 months have experienced considerable volatility given an increased prevalence of policy shocks.

## Methodology
*blayne*

*explain and evaluated modeling approaches*
### Modeling Limitations 

## Results
The train and test MSE values from the five models are reproduced below:
| Model | Train MSE | Test MSE |
| :--- | :--- | :--- |
| Linear Regression | 0.0002363762177756273 | 0.0003169875288916838 |
| Lasso | 0.0002563307767950481 | 0.0002463168461297715 |
| Ridge | 0.0010176078034475062 | 0.0010134060445877683 |
| Elastic Net | 0.0002755623454545451 | 0.00025072575196162235 |
| Random Forest | 0.06431674622296985 | 0.40042649247406187 |

The linear regression model has very close train and test MSEs, signaling that the model generalizes well as a baseline model. However, given many of the variables are very closely related, such as opening S&P 500 price and overnight future price at 9:00am EST, these MSEs may signal that there is high autocorrelation in the model. Financial market variables that are measured within minutes of each other often move together, meaning that ordinary least squares may suffer from multicollinearity even though the model appears to fit the data well.

The LASSO model also has very close train and test MSEs like the linear regression but with the test MSE being slightly lower than the the train MSE. The LASSO model performs better than the linear regression model because it drops the S&P 500 high and low, the federal funds rate, the 3month and 10 year treasury yields, and the volume of betting betting no change in the federal funds rate. This shrinks the less informative coefficients to zero, given many of the predictors have overlapping information on predicting monetary policy. Since the LASSO model uses only the most predictive variable, the LASSO reduces the most noise and produces the lowest MSEs overall between the models.

The Ridge regression model produces larger train and test MSE values than the other linear models. Ridge uses a penalty that shrinks coefficients toward zero but it does not eliminate them entirely. Since all of the variables are in the model, correlated predictors such as S&P 500 futures prices and recent index returns continue to introduce redundancy into the regression. Therefore, the Ridge model may over-penalize the coefficients while still keeping noisy predictors in the model. This leads to weaker predictive accuracy compared to the LASSO and Elastic Net models.

The Elastic Net model, which combines both types of penalties from the LASSO and Ridge regression, performs closely to the LASSO model. This resulted in the second-lowest test MSE. Given that many predictors are correlated but still contain incremental information about overnight market expectations, Elastic Net is able to stabilize the regression while still removing some redundant variables and noise. The Elastic Net model's MSEs  suggests that a hybrid approach is works well when predicing financial  problems where predictors are highly correlated.

The Random Forest model performs worse than all of the linear models given the larger train and test MSE values. The large gap between the train and test errors indicates significant overfitting. Random Forest models are powerful for capturing nonlinear relationships, but the dataset consists of financial variables that are largely linear transformations of each other. Additionaly, the small sample size of daily market observations limits the ability of tree-based models to learn stable patterns.

### Recommendations
Overall, the results suggest that regularized linear models like the standard Linear Regression, LASSO, and Elastic Net perform the best for predicting the S&P 500 opening price for this project. Among the models tested, the LASSO regression provides the strongest out-of-sample performance. This indicates that variable selection plays the most important role when working with highly correlated financial indicators. The Elastic Net performed the second best given its hybrid nature between LASSO and Ridge models. The Random Forest is not recommended for this study given the non-linear nature of the model and the linear nature of the financial variables.

*brad*
## Limitations
*idk if this section is redundant* 

## Reproduction
1. Clone the repository `git@github.com:bradleyvance23/eco395-ml-midterm-kalshi.git`
2. Install additional packages `pip install -r requirements`
3. Run 


