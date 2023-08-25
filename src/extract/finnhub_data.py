from finnhub import client as Finnhub
#import finnhub_client as Finnhub
client = Finnhub.Client(api_key="bq8ete7rh5rc96c0i040")

import datetime as dt
from datetime import timedelta
import requests
import pandas as pd


# default variables
LIMIT=2000
DATE_RANGE=30

DATETIME_FORMATS = [
    # datetime formats
    '%Y%m%d_%H%M%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%Y.%m.%d %H:%M:%S',
    # date formats
    '%Y%m%d',
    '%Y/%m/%d',
    '%Y-%m-%d',
    '%Y.%m.%d',
]

TICKER_SCHEMA = {
    't': 'ticker_time_sec',
    'o': 'open',
    'h': 'high',
    'l': 'low',
    'c': 'close',
    'v': 'volume',
    's': 'status',
}

INTERVAL_DATA = {
    'm': {'time': 60, 'resolution': 1},
    '1m': {'time': 60, 'resolution': 1},
    '5m': {'time': 5 * 60, 'resolution': 5},
    '10m': {'time': 10 * 60, 'resolution': 10},
    '30m': {'time': 30 * 60, 'resolution': 30},
    'H': {'time': 60 * 60, 'resolution': 60},
    'D': {'time': 24 * 60 * 60, 'resolution': 'D'},
    'W': {'time': 7 * 24 * 60 * 60, 'resolution': 'W'},
    'M': {'time': 30 * 24 * 60 * 60, 'resolution': 'M'},
}

HEADER_ORDER = [
    'partition_date',
    'etl_time',
    'ticker_time',
    'ticker_time_sec',
    'ticker',
    'interval',
    'close',
    'high',
    'low',
    'open',
    'volume',
]


def get_ticker_data(
    ticker,
    start_date=None,
    end_date=None,
    date_range=DATE_RANGE,
    interval='H',
):
    # Initialize parameters; handle args as needed
    start_date = start_date or (dt.date.today() - timedelta(days=date_range)).strftime("%Y-%m-%d")
    end_date = end_date or dt.date.today().strftime("%Y-%m-%d")
    df = _get_data(ticker, start_date, end_date, interval)
    df = _adjust_ticker_data(df, ticker, interval)
    return df


def _get_sec_interval_list(start_date, end_date, interval, limit=LIMIT, interval_data=INTERVAL_DATA):
    # Get interval symbol; otherwise, select minute
    interval_sec = interval_data[interval]['time'] if interval in interval_data.keys() else interval_data['m']['time']
    start_sec, end_sec = _datetime_to_sec(start_date), _datetime_to_sec(end_date)
    
    # Initiate a tuple of lists containing start/end datetime pairs
    #limit = _check_limit(interval, limit=LIMIT)    
    end_i = end_sec
    start_i = end_sec - (limit * interval_sec)
    dt_list = [(start_i, end_i)]
    
    # Add each datetime interval and subtract the desired time period
    while start_i > start_sec:
        end_i = end_i - (limit * interval_sec)
        start_i = start_i - (limit * interval_sec)
        dt_list = dt_list + [(start_i, end_i)]
        next
    return dt_list


def _get_data(ticker, start_date, end_date, interval, interval_data=INTERVAL_DATA):
    """Loop through each date range and extract OHLCV data
    """
    dt_interval_list = _get_sec_interval_list(start_date, end_date, interval)
    data = []
    for i, dt_interval in enumerate(dt_interval_list):
        print("Extracting {} of {} for {}: from {} to {}".format(
            i + 1, 
            len(dt_interval_list) + 1,
            ticker, 
            _sec_to_datetime(dt_interval[0]),
            _sec_to_datetime(dt_interval[1])
        ))
        url = 'https://finnhub.io/api/v1/stock/candle' + \
        '?symbol={}'.format(ticker) + \
        '&resolution={}'.format(interval_data[interval]['resolution']) + \
        '&from={}'.format(dt_interval[0]) + \
        '&to={}'.format(dt_interval[1]) + \
        '&token={}'.format(client.api_key)
        print(url)
        response = requests.get(url)
        data = response.json()
        df_tmp = pd.DataFrame(data)
        df = df_tmp.append(df_tmp)
    df['interval'] = interval
    return df


def _adjust_ticker_data(df, ticker, interval, header_order=HEADER_ORDER):
    df = df.rename(columns=TICKER_SCHEMA)
    df['partition_date'] = dt.datetime.now().strftime("%Y-%m-%d")
    df['etl_time'] = dt.datetime.now()
    df['ticker_time'] = [_sec_to_datetime(m) for m in df['ticker_time_sec']]
    df['ticker'] = ticker
    df['interval'] = interval
    df.drop(columns='status', inplace=True)
    df = df.sort_values(by='ticker_time', ascending=False)
    df.drop_duplicates(subset="ticker_time", inplace=True)
    df = df.reset_index().drop('index', axis=1)
    df = df[header_order]
    return df


def _datetime_to_sec(datetime):
    """Convert a datetime or date (string) to milliseconds (int).
    Returns: seconds timestamp for corresponding datetime. 
    """
    sec = None
    is_formatted = False
    dt_formats = DATETIME_FORMATS
    
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


def _sec_to_datetime(ms, dt_format=None):
    """Convert a second (int) to a datetime (date or string).
    Returns: milliseconds timestamp for corresponding datetime.  
    """
    datetime = dt.datetime.fromtimestamp(ms)
    return  datetime.strftime(dt_format) if dt_format else datetime
