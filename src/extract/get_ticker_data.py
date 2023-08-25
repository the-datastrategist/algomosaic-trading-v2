
import datetime as dt
from datetime import timedelta
from pandas_datareader import data as pd_data

DEFAULT_DATE_RANGE = 30
DEFAULT_LOOK_BACK = 365
DEFAULT_LOOK_FORWARD = 14
DEFAULT_DATA_SOURCE = 'yahoo'
TICKER_VARIABLE = 'ticker'


def get_ticker_data(
    ticker,
    start_date=None,
    end_date=None,
    date_range = DEFAULT_DATE_RANGE,
    look_back = DEFAULT_LOOK_BACK,
    look_forward = DEFAULT_LOOK_FORWARD,
    data_source = DEFAULT_DATA_SOURCE
):
    """
    Get ticker prices over a specified time period, sourced from Yahoo Finance
    (by default). start_date defaults to 1 year from current date. end_date 
    defaults to current date.

    Args:
        ticker : string : Ticker of desired stock or asset
        start_date : string : First date you would like complete price data for.
                              We add a 365 day lookback window to collect EMA
                              data for the full date range.
        end_date : string : Last date to pull complete dat. Defaults to current date.
        souce : string : pandas DataReader sources; defaults as Yahoo finance.
    """
    start_date = start_date or (dt.date.today() - timedelta(days=date_range)).strftime("%Y-%m-%d")
    end_date = end_date or dt.date.today().strftime("%Y-%m-%d")
    start_date_api = dt.datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=look_back)
    end_date_api = dt.datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=look_forward)

    try:
        df = pd_data.DataReader(
            ticker,
            DEFAULT_DATA_SOURCE, 
            start_date_api,
            end_date_api).reset_index()
        df[TICKER_VARIABLE] = ticker
        df.columns = [h.lower().replace(' ', '_') for h in list(df)]
        return df
    except Exception as e:
        print('ERROR: {}'.format(e))
