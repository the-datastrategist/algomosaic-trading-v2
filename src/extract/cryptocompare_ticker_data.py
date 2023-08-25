# -*- coding: utf-8 -*-
"""Extract cryptocurrency OHLCV data from the Cryptocompare.com API.

For any ticker pair in Cryptocompare's API, extracts a Pandas Dataframe
with OHLCV data.

Attributes:

    ticker (str): Ticker paid (e.g. BTC-USD) to extract.
    start_date (str): Formatted date string containing the start date for
        the output dataset (inclusive).
    end_date (str): Optional. Formatted date string containing the end date 
        for the output dataset (inclusive).
    date_range (int): Optional. Lookback window if start_date is not provided.
    interval (str): Optional. Time interval of the output dataset. Defaults to 'day'.
        Options include:
            - day
            - hour
            - minute
    exchange (str): Crypto exchange to extract data from. Defaults to CCCAGG.

Todo:
    * Add CI/CD process
    * Fix lookup windows (start/end date, date range)

Documentation:
   ...

"""

import datetime as dt
from datetime import timedelta
import requests
import pandas as pd
import numpy as np

# row limit for API response
RATE_LIMIT = 2000
DATE_RANGE = 30
EXCHANGE = 'binance'


def get_ticker_data(
    ticker,
    start_date=None,
    end_date=None,
    date_range=DATE_RANGE,
    interval='hour',
    exchange=EXCHANGE,
    rate_limit=RATE_LIMIT
):
    # Initialize parameters; handle args as needed
    start_date = start_date or (dt.datetime.now() - timedelta(days=date_range)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = end_date or dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    exchange = _handle_args(exchange, arg='exchange')
    interval = _handle_args(interval, arg='interval')
    df = _get_cryptocompare_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        exchange=exchange,
        rate_limit=rate_limit)
    df = _adjust_ticker_data(
        df=df,
        ticker=ticker,
        interval=interval,
        exchange=exchange)
    return df


def _get_cryptocompare_data(
    ticker,
    start_date,
    end_date,
    interval,
    exchange,
    rate_limit=RATE_LIMIT
):
    # Loop through each date range and extract OHLCV data
    dt_interval_list = get_sec_interval_list(start_date, end_date, interval)
    base_asset = ticker.split('-')[0]
    quote_asset = ticker.split('-')[1]
    data = []
    for i, dt_interval in enumerate(dt_interval_list):
        print("Extracting {} of {}: {} up to {}".format(
            i+1, len(dt_interval_list), ticker, sec_to_datetime(dt_interval)
        ))
        url = 'https://min-api.cryptocompare.com/data/histo{}'.format(interval) +\
                '?fsym={}'.format(base_asset) +\
                '&tsym={}'.format(quote_asset) +\
                '&e={}'.format(exchange) +\
                '&limit={}'.format(rate_limit) +\
                '&aggregate=1' +\
                '&toTs={}'.format(dt_interval)
        response = requests.get(url)
        data_tmp = response.json()['Data']
        data = data + (data_tmp if isinstance(data_tmp, list) else [data_tmp])

    # Once all ranges are collected, convert to dataframe
    df = pd.DataFrame(data)
    df.drop_duplicates(subset=['time'], inplace=True)
    df.dropna(subset=['time'], inplace=True)
    return df


def _adjust_ticker_data(df, ticker, interval, exchange):
    df = df.rename(columns={
        'volumefrom': 'volume_base',
        'volumeto': 'volume',
        'time': 'ticker_time_sec'})

    # Add relevant metadata
    df['partition_date'] = dt.datetime.now().strftime("%Y-%m-%d")
    df['etl_time'] = dt.datetime.now()
    df['ticker_time'] = [sec_to_datetime(m) for m in df['ticker_time_sec']]
    df['ticker'] = ticker
    df['interval'] = interval
    df['exchange'] = exchange

    # Sort and structure data
    df = df.sort_values(by='ticker_time', ascending=False)
    df = df.reset_index().drop('index', axis=1)
    return df


def _handle_args(kwargs, arg):
    return kwargs[arg] if isinstance(kwargs, dict) else kwargs


def datetime_to_sec(datetime):
    # Convert a datetime or date (string) to milliseconds (int).
    # Returns: seconds timestamp for corresponding datetime. 
    sec = None
    is_formatted = False
    dt_formats = [
        # datetime formats
        '%Y%m%d_%H%M%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%Y.%m.%d %H:%M:%S',
        # date formats
        '%Y%m%d',
        '%Y/%m/%d',
        '%Y-%m-%d',
        '%Y.%m.%d']

    # Loop through potential datetime format types
    for dt_format in dt_formats:
        try:
            dt_obj = dt.datetime.strptime(datetime, dt_format)
            sec = int(dt_obj.timestamp())
        except ValueError:
            continue
    if not sec:
        print('Must provide a valid datetime string format.')
    return sec 


def sec_to_datetime(ms, dt_format=None):
    # Convert a second (int) to a datetime (date or string).
    # Returns: milliseconds timestamp for corresponding datetime.
    datetime = dt.datetime.fromtimestamp(ms)
    if dt_format:
        return datetime.strftime(dt_format)
    else:
        return datetime


def get_sec_interval_list(
        start_date,
        end_date,
        interval,
        rate_limit=RATE_LIMIT
):
    interval_dict = {
        'day': 24 * 60 * 60,
        'hour': 60 * 60,
        'minute': 60,
    }
    dt_interval = interval_dict[interval]
    end_ms = datetime_to_sec(end_date)
    start_ms = datetime_to_sec(start_date)

    # Take the earliest timestamp in the date range
    dt_list = [end_ms]
    dt_i = end_ms - (rate_limit * dt_interval)

    # Add each datetime interval and subtract the desired time period
    while dt_i > start_ms:
        dt_list = dt_list + [dt_i]
        dt_i = dt_i - (rate_limit * dt_interval)
        next
    return dt_list
