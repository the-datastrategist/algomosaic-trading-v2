"""configs.py

Configurations for this algoMosaic project.

"""

# ECOSYSTEM
# The ecosystem is the entire domain for your project.
# This is basically the project ID and name, but we
# didn't want to confuse it for our GCP project_id.
ALGOM_ID = 'algomosaic_template'
ALGOM_DESCRIPTION = "Development for algomosaic base platform. Version 0.01."
ALGOM_CONFIG_FILEPATH = '/home/jovyan/algomosaic/algom/configs.py'


# GOOGLE CLOUD PLATFORM
# Below are details need to connect algoMosaic to
# your Google Cloud Platform.
GOOGLE_PROJECT_ID = 'algom-trading'

# GCP Storage bucket where models will be saved
GOOGLE_STORAGE_BUCKET = 'algom-trading-sto'

# Location of the GCP service account key
GOOGLE_APPLICATION_CREDENTIALS = '/home/jovyan/algomosaic/algom-trading-6041337f9d76.json'


# ANALYTICAL DATABASE
# Below are dataset specs for the tables the algom
# library produces. When you save or run models with
# algom, metadata is  recorded in the following tables.

# features table that stores production feature information
# Note that this is different from the tables used to train models
FEATURE_TABLE = 'features.features_{ticker}_{interval}'
FEATURE_LIBRARY='src.features.algom_trading_v001.get_features_hour_i0'
DATA_LIBRARY='src.extract.cryptocompare_ticker_data'

# metadata_table stores info about each stored model
METDATA_TABLE = 'metadata.model_metadata_YYYYMMDD'

# parameters_table stores info about the model's parameters
PARAMETERS_TABLE = 'metadata.model_parameters_YYYYMMDD'

# results from algoM predictions or evaluations
PREDICTION_TABLE = 'predictions.model_prediction_YYYYMMDD'
EVALUATION_TABLE = 'predictions.model_evaluation_YYYYMMDD'
PERFORMANCE_TABLE = 'predictions.model_performance_YYYYMMDD'
FEATURE_IMPORTANCE_TABLE = 'feature_importance.model_features_imp_YYYYMMDD'

# Model metadata datasets
STORAGE_TABLE = 'metadata.model_storage_YYYYMMDD'
QUERY_TABLE = 'metadata.model_queries_YYYYMMDD'

# Backtesting datasets
BACKTEST_TABLE = 'backtest.model_backtest_YYYYMMDD'
BACKTEST_SUMMARY_TABLE = 'backtest.model_backtest_summary_YYYYMMDD'
BACKTEST_METADATA_TABLE = 'backtest.model_backtest_metadata_YYYYMMDD'

# MODEL STORAGE
# The information below specifies where to store models
# on Google Cloud Storage. When you store models, they
# will be stored to this location.
MODEL_STORAGE_DIRECTORY = 'models/'
MODEL_LOCAL_DIRECTORY = '/home/jovyan/algomosaic/data/models/'

# Default index list
INDEX_FEATURES = [

    # Metadata
    'partition_date',
    'ticker',
    'ticker_time_sec',
    'ticker_time',
    'etl_time',
    'exchange',
    'ticker_interval',
    'interval',

    # Datetime derivatives
    'hour',
    'week',
    'month',
    'quarter',
    'year',
    'day_of_year',

    # OHLVC prices
    'high',
    'low',
    'open',
    'close',
    'volume_base',
    'volume',
]

# Default feature omit list
OMIT_FEATURES = [

    # Outcomes
    'ROR_n1',
    'ROR_n3',
    'ROR_n5',
    'ROR_n6',
    'ROR_n10',
    'ROR_n12',
    'ROR_n15',
    'ROR_n20',
    'ROR_n24',
    'ROR_n25',
    'ROR_n30',
    'ROR_n36',
    'ROR_n48',
    'ROR_n72',
    'ROR_n96',
    'ROR_n120',
    'ROR_n144',
    'ROR_n168',

    # Price action features
    'open1',
    'high1',
    'low1',
    'close1',
    'open2',
    'high2',
    'low2',
    'close2',
    'open3',
    'high3',
    'low3',
    'close3',
    'open4',
    'high4',
    'low4',
    'close4',
    'open5',
    'high5',
    'low5',
    'close5',
    'open6',
    'high6',
    'low6',
    'close6',
    
    # Other shit
    'conversionType',
    'conversionSymbol',
]
