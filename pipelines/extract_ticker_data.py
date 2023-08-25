import kfp
from kfp.containers import build_image_from_working_dir
from kfp.components import func_to_container_op, InputPath, OutputPath


# row limit for API response
PROJECT_ID = 'algom-trading'
DESTINATION_TABLE = 'extract_raw.{exchange}_{ticker}_{interval}'
OUTPUT_DIR='gs://algom-trading-pipelines/staging'
TARGET_IMAGE='python'

RATE_LIMIT = 2000
DATE_RANGE = 30
EXCHANGE = 'binance'



@func_to_container_op
def extract_ticker(
    ticker: InputPath(str),
    start_date: InputPath(str) = None,
    end_date: InputPath(str) = None,
    project_id: InputPath(str) = None,
    destination_table: InputPath(str) = None,
    if_exists: InputPath(str) = None,
    interval: InputPath(str) = None,
    exchange: InputPath(str) = None,
    date_range: InputPath(int) = None,
    rate_limit: InputPath(int) = None,
):
    import datetime as dt
    from datetime import timedelta
    import requests
    import pandas as pd
    import pandas_gbq as gbq
    import numpy as np

    # Initialize parameters; handle args as needed
    start_date = start_date or (dt.datetime.now() - timedelta(days=date_range)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = end_date or dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    project_id = project_id or PROJECT_ID
    destination_table = destination_table or DESTINATION_TABLE.format(
        exchange=exchange,
        ticker=ticker.replace('-', '_'),
        interval=interval
    )
    if_exists = if_exists or 'replace'
    date_range = date_range or DATE_RANGE
    interval = interval or 'hour'
    exchange = exchange or EXCHANGE
    rate_limit = rate_limit or RATE_LIMIT


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
    
    # Extract cryptocompare data
    print('RUNNING: Extracting data for {} from Cryptocompare API'.format(ticker))
    df = _get_cryptocompare_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        exchange=exchange,
        rate_limit=rate_limit
    )

    # Make adjustments to output table
    print('RUNNING: Adjusting data for {}'.format(ticker))
    df = _adjust_ticker_data(
        df=df,
        ticker=ticker,
        interval=interval,
        exchange=exchange
    )
    
    # Load to BigQuery
    print('RUNNING: Loading data for {} to {}.{}.'.format(ticker, project_id, destination_table))
    df.to_gbq(
        destination_table=destination_table,
        project_id=project_id,
        if_exists=if_exists
    )


@kfp.dsl.pipeline(
   name='extract_ticker_pipeline',
   description='Extracts OHLCV data from Cryptocompare API.'
)
def extract_ticker_pipeline(
    ticker: InputPath(str),
    start_date: InputPath(str) = None,
    end_date: InputPath(str) = None,
    project_id: InputPath(str) = None,
    destination_table: InputPath(str) = None,
    if_exists: InputPath(str) = None,
    interval: InputPath(str) = None,
    exchange: InputPath(str) = None,
    date_range: InputPath(int) = None,

):
    task = extract_ticker(ticker)

    
if __name__ == '__main__':
    # Compiling the pipeline
    kfp.compiler.Compiler().compile(extract_ticker_pipeline, __file__ + '.yaml')
