# Tutorials: Backtest
###### Work in progress

<br>

## Overview

Once you have a set of features you want to trade against, we need to establish
a set of business rules that we will trade against. Before executing these trades,
we should run a backtest to ensure that the trading strategy is profitable. 

The backtest consists of 3 sets of information. 
1. __Input data__: this contains the information required to 
2. __Start & end dates__: the effective period we should track performance
3. __Business rules__: a Python file that contains the business rules to trade against

<br>

### Business rules

algoM uses a Python file to specify trade strategies for `backtest.py` and `trade.py`.
We can customize this file however desired; however, this file must have a certain
structure to run properly. 

The business rules Python file must always contain the function `trade()` 
with that outputs a response dictionary with:
    - trade: the type of trade to execute
    - amount: the amount of the asset to trade (not the dollar amount)
    - commission: the amount of the commission

You can specify the following trade types:
    - BUY
    - SELL
    - SELL SHORT
    - BUY COVER

<br>

TODO: Remove references to buy/sell/etc functions
 
<br><br>

## Steps to Execution

Below are the steps required to backtest trade strategy performance.

### 1. Specify the business rule Python file

This is a basic structure of a business rule Python file:

```
# business_rules.py

def trade(row):
    """ Specify the trade business rules for a given trade."""
    # Specify the initial account amount
    # Trade amounts are based on the initial account amount  
    amount = 10_000
    commission = 0

    # Add conditional statement
    if float(row['AROR_12']) <= -0.01:
        response = {
            'trade': 'BUY',
            'amount': round(amount * .1 / row[CLOSE],5),
            'commission': commission
        }
    elif float(row['AROR_12']) >= -0.01:
        response = {
            'trade': 'SELL',
            'amount': round(amount * .5 / row[CLOSE],5),
            'commission': commission
        }
    else:
        response = None
    return response
```

<br>

### 2. Import feature dataset

Using `dataObject()` Import the DataFrame with the features used in the 
conditional statement, along with any other relevant metadata. 

<br>


### 3. Initialize and run backtestTrades()

Import and initialize the class `backtest_Trades()`. Here's an example:

```
bt = backtest.backtestTrades(
    df=data.df,
    start_date='2018-01-01',
    end_date='2018-12-31',
    business_rule_functions='src.business_rules.trade_business_rules_BTCUSDT'
)
```

The parameter, `business_rule_functions`, should contain the Python module
where the business rules are specified. 

<br>

### 3. Interpret results

Once the backtest runs, you will receive an output that looks like
the following:

```
---------- BACKTEST PERFORMANCE SUMMARY ----------
- % Gain: 690.3% vs -72.6% market
- Income: $69032.0
- Account Value: $79032.0
- Account Cash:  $79032.0
- Trades: 2435 of 5870 attempts (41.0% execution rate)
- Account Min: $9973
- Account Max: $79099
```

A performance and metadata summary for this backtest will be exported
to BigQuery.

<br>

###### [Return to main](https://github.com/algomosaic/algom-trading/blob/master/docs/tutorials/tutorials.md)
