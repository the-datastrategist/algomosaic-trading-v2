# Tutorials: Extract

<br>

## Overview 
The first step of the lifecycle is to extract data for a given ticker (i.e. asset symbol) that 
you would like to predict or trade. The function `run_extract_process` from 
`src.extract.ticker_extract` seamlessly pulls 
[OHLC and volume](https://en.wikipedia.org/wiki/Open-high-low-close_chart#:~:text=An%20open%2Dhigh%2Dlow%2D,one%20day%20or%20one%20hour.) 
data in 2 steps:

1. _Data Extraction_. Extract price data using the Yahoo, Cryptocompare, or other financial APIs
    by specifying a `data_library`

2. _Financial Indicators_. Apply a selection of financial indicators or data transformations with
    the `features_library`. We can specify technical indicators using `src.features.talib` and/or
    engineer features using `src.features.talib_features.py`

<br>


#### Data Extraction

We leverage the Yahoo Finance API via [Pandas Data Reader](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html) 
to extract daily OHLC data for any ticker. For algoM, we leverage 
the [Cryptocompare.com](https://min-api.cryptocompare.com/) API to access a variety of crypto-related data.


#### Financial Indicators & Engineering

You have the option to select any number of financial indicators. 
The indicators were originally based on 
[Quantopian's blog post](https://www.quantopian.com/posts/technical-analysis-indicators-without-talib-code)
but they have been refactored to comply with Python3 and the naming conventions for the output
columns have been adjusted. 

<br>


## Steps to Execution
Below are the steps required to pull OHLC data, calculate financial indicators, 
and feature engineering, as well as store the results to BigQuery.

<br>

### 1. Open src/etl/get_features.py and update calculations

Add as many indicators and feature engineering calculations to `src.features.get_features.py` as you wish. 
Alternatively, you can create a new feature specification file and point to it with the `features_library` in
`run_extract_process()` (see more details below). 

When running `ticker_extract.run_extract_process()`, these calculations will be passed through to the 
output Pandas Dataframe. The basic structure of `get_features.py` is:

```
# get_features.py

def get_features(df):
    from etl import talib
    from etl import talib_features

    # Enter your functions here, for instance:
    df = talib.ROR(df, -10)
    df = talib.EMA(df, 20)
    df = talib.MACD(df, 12, 24)
    
    return df
```

<br>

### 2. Run ETL function on a single ticker

Once the underlying indicators have been applied, we can run a script to generate a dataset
containing relevant data for any given ticker. As mentioned, some of the data in this output 
dataset include:

+ _Asset Info_. `ticker`, `exchange`
+ _Dates_. `ticker_time`, `week`, `month`, `quarter`, `year`, `day_of_week`, `day_of_year`, 
    `hour_of_day`
+ _OHLC Data_. `high`, `low`, `open`, `close`, `volume`
+ _Rates of return_. Log ROR for past or future time intervals (e.g. `ROR_n5`, `AROR_20`)
+ _Financial Indicators_. Custom financial indicators (e.g. `EMA_12`)
+ _Feature Engineering_. Custom feature engineering

Run the following code in a Python file or Jupyter Notebook to execute an ETL process. 
The parameters `data_library` and `features_library` defaults to `src.extract.get_ticker_data` 
and `src.features.get_features`, respectively. 

However, you can change these parameters to point to a different source files to customize the
ETL process. This is particularly useful if you'd like to vary feature calculation for different
tickers or domains. 

```
from src.extract import ticker_extract

extract = ticker_extract.run_extract_process(
    """
    Run a data extraction process that includes
    - OHLC and volume
    - financial indicators
    - feature transformations 
    """

    # Specify the trading pair
    ticker=ticker,
    
    # Specify start and end dates (or datetimes)
    # If left blank, will pull the latest 30 days
    start_date='2020-01-01 00:00:00',
    end_date='2021-01-01 12:00:00',

    # GCP Project ID
    project_id='my-project-id',

    # Specify the destination table if to_bq=True
    destination_table='features.features_{ticker}_{interval}_{iteration}_{partition}',

    # Use `table_parameters` to customize the destination table name
    table_params={
        'ticker': ticker,
        'interval': 'hour',
        'iteration': iteration,
        'parition': dt.datetime.now().strftime('%Y%m%d')
    },

    # Specify the datetime interval for the time series
    # Options: 'minute', 'hour', 'day', 'week'
    interval='hour',

    # Specify exchange
    # See https://min-api.cryptocompare.com for more details 
    exchange='binance',

    # Specify the path of the data library from the algomosaic base directory
    data_library='src.extract.cryptocompare_ticker_data',

    # Specify the path of the feature library used to calculate indicators
    features_library='src.features.get_features',

    # Whether and how to load data into BigQuery
    to_bq=True,
    if_exists=replace
)
```

Once run, you can access the data as a Pandas Dataframe using `extract.data.df` 
(or `self.data.df`).

<br>

###### [Return to main](https://github.com/algomosaic/algom-trading/blob/master/docs/tutorials/tutorials.md)
