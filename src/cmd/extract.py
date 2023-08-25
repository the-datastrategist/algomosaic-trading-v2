import argparse
from src.extract import ticker_extract
from algom import configs

GOOGLE_PROJECT_ID = configs.GOOGLE_PROJECT_ID
DESTINATION_TABLE = configs.FEATURE_TABLE
DATA_LIBRARY = configs.DATA_LIBRARY
FEATURE_LIBRARY = configs.FEATURE_LIBRARY


# Add and parse bash arguments
parser = argparse.ArgumentParser(
    description="Run a ticker extraction processes and load to BigQuery."
)
parser.add_argument(
    'ticker',
    type=str,
    help='The ticker you want to extract (e.g. BTC-USDT).'
)
parser.add_argument(
    'interval',
    type=str,
    help='The time interval for the extract (hour, day).'
)
parser.add_argument(
    '--tickers',
    type=list,
    nargs='+',
    default=[],
    help='Supply a list of tickers.'
)
parser.add_argument(
    '--start_date',
    type=str,
    default=None,
    help='The start date for the extract. Use the format YYYY-MM-DD',
)
parser.add_argument(
    '--end_date',
    type=str,
    default=None,
    help='The end date for the extract. Use the format YYYY-MM-DD',
)
parser.add_argument(
    '--iteration',
    type=str,
    default='i0',
    help='Iteration of the features set. Use if there are mutiple'
         'versions of the same ticker and interval. Defaults to i0.',
)
parser.add_argument(
    '--exchange',
    type=str,
    default='binance',
    help='Name of the exchange we should track price action and volume.'
         'Defaults to binance.',
)
parser.add_argument(
    '--project_id',
    type=str,
    default=None,
    help='GCP project ID.',
)
parser.add_argument(
    '--destination',
    type=str,
    default=None,
    help='GCP project ID.',
)
parser.add_argument(
    '--data_library',
    type=str,
    default=None,
    help='Name of the data library we should use to extract price action.'
)
parser.add_argument(
    '--feature_library',
    type=str,
    default=None,
    help='Name of the feature library we should use to extract price action.'
)
parser.add_argument(
    '--to_bq',
    type=bool,
    default=True,
    help='Whether to load results to BigQuery. Defaults to True.'
)
args = parser.parse_args()



# Get parsed arguments and run extract
ticker = args.ticker
tickers = args.tickers
start_date = args.start_date
end_date = args.end_date
interval = args.interval
iteration = args.iteration
exchange = args.exchange
project = args.project_id or GOOGLE_PROJECT_ID
destination_table = args.destination or DESTINATION_TABLE
data_library = args.data_library or DATA_LIBRARY
feature_library = args.feature_library or FEATURE_LIBRARY
to_bq = args.to_bq


print("RUNNING: {} from {} to {}.".format(
    ticker,
    start_date or 'last 30 days',
    end_date or 'now'
))

ticker_extract.run_extract_process(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    project_id=project,
    destination_table=destination_table,
    table_params={
        'ticker': ticker,
        'interval': interval,
        'iteration': iteration,
    },
    interval=interval,
    exchange=exchange,
    data_library=data_library,
    features_library=feature_library,
    to_bq=to_bq,
)
