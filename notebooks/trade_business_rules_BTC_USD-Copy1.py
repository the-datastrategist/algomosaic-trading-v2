"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data. 

"""



# specify function on row
def buy(row):
    amount = 10_000
    commission = 0
    response = None
    
    if float(row['AVG_ROR_n10_5']) > .1:
        if float(row['AVG_ROR_n3_3']) > .1 \
        or float(row['AVG_ROR_n5_5']) > .1 \
        or float(row['AVG_ROR_n10_5']) > .1:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row['Close']),
                'commission': commission
            }
        elif float(row['AVG_ROR_n3_3']) > .05 \
        or float(row['AVG_ROR_n5_5']) > .05:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row['Close']),
                'commission': commission
            }

    elif float(row['AVG_ROR_n10_5']) > .05:
        if float(row['AVG_ROR_n3_3']) > .05 \
        or float(row['AVG_ROR_n5_5']) > .05:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row['Close']),
                'commission': commission
            }
        elif float(row['AVG_ROR_n3_3']) > .03 \
        or float(row['AVG_ROR_n5_5']) > .03:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .025 / row['Close']),
                'commission': commission
            }
    return response





def sell(row):
    amount = 10_000
    commission = 0
    response = None
    if float(row['AVG_ROR_n10_5']) <= 0:
        if float(row['AVG_ROR_n5_5']) < 0 \
        or float(row['AVG_ROR_n3_3']) < 0:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .05 / row['Close']),
                'commission': commission
            }
    elif float(row['AVG_ROR_n10_5']) <= 0:
        if float(row['AVG_ROR_n5_5']) < 0 \
        or float(row['AVG_ROR_n3_3']) < 0:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .05 / row['Close']),
                'commission': commission
            }
    return response
