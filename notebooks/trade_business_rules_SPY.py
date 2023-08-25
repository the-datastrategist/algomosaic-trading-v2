"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data. 

"""

TRADE_TYPE = 'trade_type'
TRADE_AMOUNT = 'trade_amount'
COMMISSION = 'commission'
PRICE = 'close'

def rules(row):
    amount = 10_000
    commission = 0
    response = None

    BUY = 'BUY'
    SELL = 'SELL'
    SHORT = 'SHORT'
    COVER = 'COVER'
    
    ### BUY TRADES
    if float(row['SMA_ROR_n15_10']) > .03:

        if float(row['SMA_ROR_n5_5']) > .01:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .15 / row[PRICE]),
                'commission': commission
            }
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .08 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) > .02:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .1 / row[PRICE]),
                'commission': commission
            }
        elif float(row['SMA_ROR_n5_5']) > -.01:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .08 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) > .01:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .05 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) > 0:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .05 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) > -.01:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                TRADE_TYPE: BUY,
                TRADE_AMOUNT: round(amount * .02 / row[PRICE]),
                'commission': commission
            }
    #return response

    ### SELL
    if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                TRADE_TYPE: SELL,
                TRADE_AMOUNT: round(amount * .2 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) <= -.02:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                TRADE_TYPE: SELL,
                TRADE_AMOUNT: round(amount * .1 / row[PRICE]),
                'commission': commission
            }
    #return response

    ### SELL SHORT TRADES
    if float(row['SMA_ROR_n15_10']) <= -.1:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                TRADE_TYPE: SHORT,
                TRADE_AMOUNT: round(amount * .2 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) <= -.05:
        if float(row['SMA_ROR_n5_5']) < 0:
            response = {
                TRADE_TYPE: SHORT,
                TRADE_AMOUNT: round(amount * .1 / row[PRICE]),
                'commission': commission
            }

    ### BUY COVER TRADES
    if float(row['SMA_ROR_n15_10']) >= .06:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                TRADE_TYPE: COVER,
                TRADE_AMOUNT: round(amount * .5 / row[PRICE]),
                'commission': commission
            }
    elif float(row['SMA_ROR_n15_10']) >= .04:
        if float(row['SMA_ROR_n5_5']) > 0:
            response = {
                TRADE_TYPE: COVER,
                TRADE_AMOUNT: round(amount * .5 / row[PRICE]),
                'commission': commission
            }
    return response


