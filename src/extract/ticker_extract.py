"""ticker_etl.py

Data extract for building technical indicator pipelines. Relies on two modules:
get_indicators and get_feature_engineering. These modules abstracts the 
calculations / transformations from the operational code. Adjustments to the 
fields in the output dataset should be made within these two modules. 

ETL Steps
1. get_ticker_price
2. get_indicators
3. get_feature_engineering
4. clean data
    _transform_dates()
    _normalize_headers()
    _adjust_df_dates()

"""

import pandas
import datetime as dt
from datetime import timedelta
from importlib import import_module

from algom import configs
from algom.utils.data_object import dataObject

# module parameters
EXCHANGE = 'binance'
INTERVAL = 'hour'
PROJECT_ID = configs.GOOGLE_PROJECT_ID
DEFAULT_DATE_RANGE = 30
DEFAULT_LOOK_BACK = 365
DEFAULT_LOOK_FORWARD = 30
DEFAULT_DATA_SOURCE = 'yahoo'
DEFAULT_DATA_LIBRARY = 'src.extract.get_ticker_data'
DEFAULT_FEATURES_LIBRARY = 'src.features.get_features'
DEFAULT_SCHEMA = [
    {'name': 'partition_date', 'type': 'STRING'},
    {'name': 'etl_time', 'type': 'STRING'},
    {'name': 'ticker_time', 'type': 'TIMESTAMP'},
    {'name': 'ticker', 'type': 'STRING'},
    {'name': 'exchange', 'type': 'STRING'},
    {'name': 'interval', 'type': 'STRING'},
    {'name': 'week', 'type': 'INTEGER'},
    {'name': 'month', 'type': 'INTEGER'},
    {'name': 'quarter', 'type': 'INTEGER'},
    {'name': 'year', 'type': 'INTEGER'},
    {'name': 'day_of_week', 'type': 'INTEGER'},
    {'name': 'day_of_year', 'type': 'INTEGER'},
]


def run_extract_process(
    ticker,
    destination_table,
    start_date=None,
    end_date=None,
    interval=None,
    exchange=None,
    project_id=None,
    table_params=None,
    date_range=None,
    look_back=None,
    look_forward=None,
    data_library=None,
    features_library=None,
    to_bq=False,
    if_exists='replace'
):
    etl_process = etlProcess(
        ticker,
        destination_table,
        start_date,
        end_date,
        interval,
        exchange,
        project_id,
        table_params,
        date_range,
        look_back,
        look_forward,
        data_library,
        features_library,
        to_bq,
        if_exists,
    )
    etl_process.run_etl_process()
    return etl_process



class etlProcess():
    """Class that stores and executed an ETL process for ticker data from Pandas DataReader.
    
    """

    def __init__(
        self, 
        ticker,
        destination_table,
        start_date=None,
        end_date=None,
        interval=None,
        exchange=None,
        project_id=None,
        table_params=None,
        date_range=None,
        look_back=None,
        look_forward=None,
        data_library=None,
        features_library=None,
        to_bq=False,
        if_exists='replace'
    ):
        # Specify default parameters
        self.destination_table = destination_table
        self.interval = interval or INTERVAL
        self.exchange = exchange or EXCHANGE
        self.project_id = project_id or PROJECT_ID
        self.date_range = date_range or DEFAULT_DATE_RANGE
        self.look_back = look_back or DEFAULT_LOOK_BACK
        self.look_forward = look_forward or DEFAULT_LOOK_FORWARD
        self.table_params = table_params
        self.to_bq=to_bq
        self.if_exists=if_exists
        
        # Specify ticker, start, end dates
        self.ticker = ticker
        self.start_date = start_date or (dt.datetime.now() - timedelta(days=self.date_range)).strftime('%Y-%m-%d %H:%M:%S')
        self.end_date = end_date or dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Specify ETL libraries
        self.data_library = data_library or DEFAULT_DATA_LIBRARY
        self.features_library = features_library or DEFAULT_FEATURES_LIBRARY

    def run_etl_process(self):
        """
        Runs an ETL process and outputs as a Pandas Dataframe. The
        following steps are applied during this process.
            1. Get ticker prices
            2. Calculate indicators
            3. Engineer features
            4. Normalize data

        The following modules can be customized based on the packages
        you would like to run. 

        self.ohlc_library : outputs OHLCV time series
        self.indicators_library : calculates financial indicators
        self.features_library : engineers features
        """
        # Specify packages to use for indicators and etl
        print('RUNNING: {}:{} is being extracted and transformed.'.format(
            self.project_id, self.destination_table))
        clock_start = dt.datetime.now()

        # Get data and feature libraries
        get_data = import_module(self.data_library)
        get_features = import_module(self.features_library)

        # Apply data extraction and transformations
        print('RUNNING: Extracting data using {}.'.format(self.data_library))
        df = get_data.get_ticker_data(
            ticker=self.ticker,
            start_date=self.start_date,
            end_date=self.end_date,
            interval=self.interval,
            exchange=self.exchange
        )
        print('RUNNING: Applying feature engineering using {}.'.format(self.features_library))
        df = get_features.get_features(df)

        # Clean feature data
        print('RUNNING: Cleaning final dataset.')
        df.columns = [h.replace(' ', '_') for h in list(df)]
        df.columns = [h.replace('-', 'n') for h in list(df)]
        df.columns = [h.replace('%', '_pct_') for h in list(df)]
        self.data = dataObject(df)
        
        # Load to BigQuery if requested
        if self.to_bq:
            print("RUNNING: loading features into BigQuery.")
            #self.table_schema = bigquery_data.get_table_schema(self.data.df, schema=DEFAULT_SCHEMA)
            #print(self.table_schema)  # <<< -------------------------------- LOOK INTO THIS
            self.data.to_db(
                destination_table=self.destination_table,
                table_params=self.table_params,
                #schema=self.table_schema,     # <<< -------------------------------- LOOK INTO THIS
                if_exists=self.if_exists
            )

            # Get runtime for extract, transform AND load
            clock_stop = dt.datetime.now()
            runtime = clock_stop - clock_start
            print('SUCCESS: {}:{} has been loaded to BigQuery. Runtime: {}.'.format(
                self.data.project_id, self.data.destination_table_id, runtime))
        else:
            clock_stop = dt.datetime.now()
            runtime = clock_stop - clock_start
            print('SUCCESS: {}:{} dataframe has been created in {}. Access the output dataframe with `self.data.df`.'.format(
                self.project_id, self.destination_table, runtime))
