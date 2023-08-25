# How To Guide


#### Overview
The algoM framework leverages several helper functions that are used in the source 
modules as well as Jupyter Notebooks. Below is an overview of how to use these modules.

#### Contents
+ [Managing and moving data](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#managing-and-moving-data)
+ [Building financial indicators](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#building-financial-indicators)
+ [Engineering features](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#engineering-features)


<br>


## [Managing and moving data](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#managing-and-moving-data)
The following modules are used to convert or transfer data from one form
to another. 


### YAML -> Dictionary
##### `get_yaml_data(yaml_source)`
Convert YAML into a dictionary. Specify either the file path of the YAML
or pass a YAML docstring.

```
from data_mgmt import yaml_data
dict = yaml_data.get_yaml_data(document)
```


### Dataframe -> BigQuery
##### `df_to_bq(df)`
Load a Pandas Dataframe to BigQuery. Using the suffix `_YYYYMMDD` will 
append the today's date to the output table name. 

```
from data_mgmt import bigquery_data as bqd
bqd.df_to_bq(df, 'algom.dataset_name.table_name')
```


### Query -> Dataframe
##### `query_to_df(query)`
Get a Pandas Dataframe based on a given SQL query. Uses _standard_ dialect
as a default.

```
from data_mgmt import bigquery_data as bqd
df = bqd.query_to_df(query)
```


### Query -> BigQuery
##### `query_to_bq(query)`
Load the results of a query directly back to BigQuery.

```
from data_mgmt import bigquery_data as bqd
bqd.query_to_bq(query)
```


### File -> BigQuery
##### `file_to_bq(filename)`
Load the results of a file (containing a SQL query with optional parameters) to a BigQuery. 

```
from data_mgmt import bigquery_data as bqd
bqd.file_to_bq(filename, params)
```


### File -> Dataframe
##### `file_to_df(filename)`
Load the results of a file (containing a SQL query with optional parameters) to a Pandas Dataframe.

```
from data_mgmt import bigquery_data as bqd
bqd.file_to_bq(filename, params)
```


### Storage -> File
##### `download_file(bucket_name, storage_path, destination_filename)`
Download a file based on a storage path.

```
from data_mgmt import storage_data as store
store.download_file(
    bucket_name, 
    storage_path, 
    destination_filename
    )
```


### File -> Storage
##### `upload_file(bucket_name, storage_path, source_file_name)`
Download a file based on a storage path.

```
from data_mgmt import storage_data as store
store.upload_file(
    bucket_name, 
    storage_path, 
    source_file_name
    )
```


<br><br>



## [Building financial indicators](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#building-financial-indicators)

We use a refactored version of the `talib` library to calculate financial indicators.
By applying the function `get_indicators(df)` in `src.etl.get_indicators`, we can 
add an unlimited number of indicator specifications to an ETL process.

To add indicators to the ETL process:

1. Open `src/etl/get_indicators.py`
2. Update the function, `get_indicators(df)`, to add the desired indicators.

```
def get_indicators(df):
    from etl import talib

    # outcome variables
    df = talib.ROR(df, -1)
    df = talib.ROR(df, -3)
    
    # indicators
    df = talib.EMA(df, 20)
    df = talib.MACD(df, 12, 26)
    df = talib.RSI(df, 50)
    return df
```

3. Execute an ETL process. The financial indicator calculations will be added to the output dataframe.

```
from etl import ticker_etl
etl_process = ticker_etl.etl(
    ticker='BTC-USD', start_date='2010-07-01')
```

<br>

For more information on the available indicators, [click here](https://docs.google.com/spreadsheets/d/1lyBSCZz6JidprUJ-rn2ddnMDwSpp52RkQWN_GAvVflI/edit#gid=0) or enter the snippet:

```
from etl import talib
help(talib)
```


<br><br>


## [Engineering features](https://github.com/gordonsilvera/algom-trading/blob/master/docs/how_to_guides.md#engineering-features)

Once the financial indicators have been calculated, we can apply additional feature 
engineering to them or any other data. We have a preselected set of feature engineering functions. 

To add engineered features to the ETL process:

1. Open `src/etl/get_feature_engineering.py`
2. Update the function, `get_feature_engineering(df)`, to add the desired indicators.

```
def get_feature_engineering(df):
    from etl import talib_features

    # 3day trade range
    df = talib_features.MIN(df, n=3)
    df = talib_features.MAX(df, n=3)
    df = talib_features.DIFF(df, 'MAX_Close_3', 'MIN_Close_3')

    # log(x/y)
    df = talib_features.RATIO_LOG(df, 'MIN_5', 'MIN_10', 0, 0)

    # x/y
    df = talib_features.RATIO(df, 'High',  'Low',   1, 1)
    
    return df
```

3. Execute an ETL process. The financial indicator calculations will be added to the output dataframe.

```
from etl import ticker_etl
etl_process = ticker_etl.etl(
    ticker='BTC-USD', start_date='2010-07-01')
```

<br>

For more information on the available indicators, enter:

```
from etl import talib_features
help(talib_features)
```

<br>
