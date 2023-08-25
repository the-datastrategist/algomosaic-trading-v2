"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data. 

"""

from data_mgmt import data_mgmt
config = data_mgmt.getConfig('/home/jovyan/algom-trading/data_config.yaml')

CLOSE = config.CLOSE


# specify function on row
def buy(row):
    amount = 10_000
    commission = 0
    response = None
    
    # SMA_ROR_n15_10: 3%+
    if float(row['SMA_ROR_n15_10']) > .03:

        if float(row['SMA_ROR_n5_5']) > .01 \
        or float(row['SMA_ROR_n10_5']) > .01 \
        or float(row['SMA_ROR_n15_5']) > .01:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .15 / row[CLOSE]),
                'commission': commission
            }
        elif float(row['SMA_ROR_n5_5']) > 0 \
        or float(row['SMA_ROR_n10_5']) > 0 \
        or float(row['SMA_ROR_n15_5']) > 0:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row[CLOSE]),
                'commission': commission
            }
        elif float(row['SMA_ROR_n5_5']) > -.01 \
        or float(row['SMA_ROR_n10_5']) > -.01:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .08 / row[CLOSE]),
                'commission': commission
            }

    # SMA_ROR_n15_10: 2-3%
    elif float(row['SMA_ROR_n15_10']) > .02:
        if float(row['SMA_ROR_n5_5']) > 0 \
        or float(row['SMA_ROR_n10_5']) > 0:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row[CLOSE]),
                'commission': commission
            }
        elif float(row['SMA_ROR_n5_5']) > -.01 \
        or float(row['SMA_ROR_n10_5']) > -.01:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .08 / row[CLOSE]),
                'commission': commission
            }
            
    # SMA_ROR_n15_10: 1-2%
    elif float(row['SMA_ROR_n15_10']) > .01:
        if float(row['SMA_ROR_n5_5']) > 0 \
        or float(row['SMA_ROR_n10_5']) > 0:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row[CLOSE]),
                'commission': commission
            }
            
    # SMA_ROR_n15_10: 0-1%
    elif float(row['SMA_ROR_n15_10']) > 0:
        if float(row['SMA_ROR_n5_5']) > 0 \
        or float(row['SMA_ROR_n15_5']) > 0:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row[CLOSE]),
                'commission': commission
            }

    # SMA_ROR_n15_10: -1 to 0%
    elif float(row['SMA_ROR_n15_10']) > -.01:
        if float(row['SMA_ROR_n5_5']) > 0 \
        or float(row['SMA_ROR_n5_5']) > 0:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .02 / row[CLOSE]),
                'commission': commission
            }
    return response



def sell(row):
    amount = 10_000
    commission = 0
    response = None
    if float(row['SMA_ROR_n15_10']) <= -.04:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .2 / row[CLOSE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) <= -.02:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .1 / row[CLOSE]),
                'commission': commission
            }
    return response



def sell_short(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'SELL SHORT'
    response = None
    if float(row['SMA_ROR_n15_10']) <= -.1:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                'trade': TRADE,
                'amount': round(amount * .2 / row[CLOSE]),
                'commission': COMMISSION
            }
    elif float(row['SMA_ROR_n15_10']) <= -.05:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                'trade': TRADE,
                'amount': round(amount * .1 / row[CLOSE]),
                'commission': COMMISSION
            }
    return response



def buy_cover(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'BUY COVER'
    response = None
    if float(row['SMA_ROR_n15_10']) >= .06:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                'trade': TRADE,
                'amount': round(amount * .5 / row[CLOSE]),
                'commission': COMMISSION
            }
    elif float(row['SMA_ROR_n15_10']) >= .04:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                'trade': TRADE,
                'amount': round(amount * .5 / row[CLOSE]),
                'commission': COMMISSION
            }
    return response
