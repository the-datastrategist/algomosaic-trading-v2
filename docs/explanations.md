# Explanations

<br>

## Modules


### business_rules.py
###### Source: _src.business_rules_

This module applies actions based on a defined set of input data and 
business rules (or conditional statements) that related to the input
dataset. Within the scope of `algom-trading`, we use it to define when
trades are executed. This module is referenced in `backtest.py` and
`trade.py`. 

Within `algom-trading`, users should update the module `trade(data)`,
which returns a dictionary containing:
+ trade type (e.g. BUY, SELL)
+ trade amount (in the asset, not dollars)
+ commission (optional)

The data input into the function can be a dictionary or a row of a
Dataframe. Here is a sample business rules script:

```
# trade_business_rules.py

def trade(data):
    initial_account = 10_000
    commission = 0
    response = None

    # If AROR_3 falls below 5% buy asset with 10% of the initial account
    if float(row['AROR_3']) <= -0.05:
        trade_value = (initial_account * .1 / data.close)
        response = {
            'trade': 'BUY',
            'amount': trade_value,
            'commission': trade_value * 0.001
        }

    # If AROR_3 raises above 5% sell position at 50% of initial account (or close position) 
    if float(row['AROR_3']) >= 0.05:
        trade_value = (initial_account * .5 / data.close)
        response = {
            'trade': 'SELL',
            'amount': trade_value,
            'commission': trade_value * 0.001
        }
    return response

``` 

<br>


### get_features.py
###### Source: _src.features_

Get features is the default library to add features to our extracted dataset.
These features may include financial indicators (eg. _RSI_14_) or data
transformations (e.g. _AROR_7_, _SMA_MIN_7_).

The transformations added to this file are dynamically loaded to the output
DataFrame in `etlProcess()` from `src.extract.ticker_extract.py`.


<br>

### talib.py
###### Source: _src.features_

This module provides calculations several financial indicators.

<br>

### talib_features.py
###### Source: _src.features_

This module provides a set of common data transformations related to
time series data. These are not financial indicators, per se, but they
supplement them.

<br>


## Classes

### dataObject
###### Source: _algom.utils.data_object_

This is a description ...

<br>


### modelRegression
###### Source: _algom.model_regression_

This is a description ...

<br>


## Identifiers

### model_id
###### Source: _algom.model_clustering, algom.model_regression_

This is a description ...

<br>


### storageObject
###### Type: Class
###### Source: _algom.utils.storage_object_

This is a description ...

<br>
