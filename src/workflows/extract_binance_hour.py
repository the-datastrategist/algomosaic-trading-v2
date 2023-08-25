""" extract_binance_hour.py

For a set of crypto pairs, run the standard extract
process for a time series with minute intervals. 
"""

import datetime as dt
from src.extract import ticker_extract


# Specify input parameters
START_DATE = None
END_DATE = None
INTERVAL = 'minute'
ITERATION = 'i00'
EXCHANGE = 'binance'
GOOGLE_PROJECT_ID = 'algom-trading'
DESTINATION_TABLE='train_features.features_{ticker}_{interval}_{iteration}_{partition}'
DATA_LIBRARY = 'src.extract.cryptocompare_ticker_data'
FEATURE_LIBRARY = 'src.features.algom_trading_v001.get_features_minute_i00'
TICKERS = [
    'ADA-USDT',
    'BCH-USDT',
    'BNB-USDT',
    'BTC-USDT',
    'ETH-USDT',
    'EOS-USDT',
    'LTC-USDT',
    'LINK-USDT',
    'NEO-USDT',
    'OMG-USDT',
    'TRX-USDT',
    'XRP-USDT',
    'XLM-USDT',
    'ZRX-USDT',
]

# Run extract for each ticker
partition = dt.datetime.now().strftime('%Y%m%d')
for ticker in TICKERS:
    print("RUNNING: {}".format(ticker))
    model = ticker_extract.run_extract_process(
        ticker=ticker,
        start_date=START_DATE,
        end_date=END_DATE,
        project_id=GOOGLE_PROJECT_ID,
        destination_table=DESTINATION_TABLE,
        table_params={
            'ticker': ticker,
            'interval': INTERVAL,
            'iteration': ITERATION,
            'partition': partition
        },
        interval=INTERVAL,
        exchange=EXCHANGE,
        data_library=DATA_LIBRARY,
        features_library=FEATURE_LIBRARY,
        to_bq=True,
        if_exists='replace'
    )
