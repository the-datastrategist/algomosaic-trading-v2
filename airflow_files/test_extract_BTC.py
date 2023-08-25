from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.python import PythonOperator

from src.features.ticker_etl import run_etl_process
from src.features import get_features
from src.extract import get_ticker_data


def run_ticker_extract(ticker):
    
    model = run_etl_process(
        ticker=ticker,
        start_date='2020-01-01',
        end_date=None,
        project=None,
        destination_table='test_features.features_{ticker}_YYYYMMDD',
        table_params={'ticker': ticker},
        data_library='src.extract.cryptocompare_ticker_data',
        features_library='src.features.get_features',
        date_range=None,
        look_back=None,
        look_forward=None,
        to_bq=True,
        if_exists='replace'
    )

run_ticker_extract('BTC-USD')
