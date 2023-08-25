# Ecosystem configurations

# System
SCOPE_ID = 'algom_trading_v001'
SCOPE_DESCRIPTION = 'Development for algoM trading platform. Version 0.01.'

# ETL libraries
DATA_LIBRARY = 'extract.get_ticker_data'
FEATURES_LIBRARY = 'features.get_features'

# Notebook setup
HOME_FILEPATH = '/home/jovyan/algomosaic/'
CREDENTIALS_FILEPATH = '/home/jovyan/algomosaic/algomosaic-nyc-19c4663f027d.json'
CONFIGS_FILEPATH = '/home/jovyan/algomosaic/src/configs.py'
SOURCE_CODE_FILEPATH = '/home/jovyan/algomosaic/src'
KEYCHAIN_FILEPATH = '/home/jovyan/algomosaic/src/keychain.json'

# GCP setup
PROJECT_ID = 'algomosaic-nyc'
BUCKET_NAME = 'algom-dev'

# Google Cloud Storage
MODEL_STORAGE_DIRECTORY = 'models/'
MODEL_LOCAL_DIRECTORY = '/home/jovyan/algomosaic/models/'
GOOGLE_CREDENTIALS_PATH = '/home/jovyan/algomosaic/'

# Database setup
FEATURE_TABLE = 'algom_dev_features.features_{ticker}_YYYYMMDD'
METDATA_TABLE = 'algom_dev_metadata.model_metadata_YYYYMMDD'
PARAMETERS_TABLE = 'algom_dev_metadata.model_parameters_YYYYMMDD'
PREDICTION_TABLE = 'algom_dev_predictions.model_prediction_YYYYMMDD'
EVALUATION_TABLE = 'algom_dev_predictions.model_evaluation_YYYYMMDD'
PERFORMANCE_TABLE = 'algom_dev_performance.model_performance_YYYYMMDD'
FEATURE_IMPORTANCE_TABLE = 'algom_dev_feature_importance.model_features_importance_YYYYMMDD'
STORAGE_TABLE = 'algom_dev_storage.model_storage_YYYYMMDD'
QUERY_TABLE = 'algom_dev_metadata.model_queries_YYYYMMDD'
BACKTEST_TABLE = 'algom_dev_performance.model_backtest_YYYYMMDD'
BACKTEST_SUMMARY_TABLE = 'algom_dev_performance.model_backtest_summary_YYYYMMDD'
BACKTEST_METADATA_TABLE = 'algom_dev_performance.model_backtest_metadata_YYYYMMDD'

# Default variables
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
VOLUME = 'volume'
DATE = 'ticker_datetime'
TRADE = 'trade'
ACCOUNT = 'account'

# Default index list
index_features = [
    'partition_date',
    'etl_time',
    'ticker_time',
    'ticker',
    'exchange',
    'interval',
    'ticker_time_sec',
]

# Default feature omit list
omit_features = [
    'ROR_n1',
    'ROR_n3',
    'ROR_n5',
    'ROR_n10',
    'ROR_n15',
    'ROR_n20',
    'ROR_n25',
    'ROR_n30',
]
