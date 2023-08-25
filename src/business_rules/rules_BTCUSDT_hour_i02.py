"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data.

"""

CLOSE = 'close'

""" BUY STRATEGIES

# 02.1
    if float(row['AROR_12']) <= -0.001 \
    and float(row['LAG3_AROR_12']) <= float(row['AROR_12']):
        response = {
            'trade': 'BUY',
            'amount': round(account * .1 / row[CLOSE], 5),
            'commission': (account * .1) * 0.001
        }


# 02.2
    if float(row['AROR_12']) <= -0.001 \
    and float(row['LAG3_AROR_12']) <= float(row['AROR_12']):
        response = {
            'trade': 'BUY',
            'amount': round(account * .1 / row[CLOSE], 5),
            'commission': (account * .1) * 0.001
        }
    if float(row['AROR_12']) >= 0.001 \
    and float(row['AROR_12']) <= float(row['AROR_24']):
        response = {
            'trade': 'SELL',
            'amount': round(account * .5 / row[CLOSE],5),
            'commission': (account * .5) * 0.001
        }

# 02.3
    if float(row['AROR_12']) <= -0.001 \
    and float(row['LAG3_AROR_12']) <= float(row['AROR_12']):
        response = {
            'trade': 'BUY',
            'amount': round(account * .1 / row[CLOSE], 5),
            'commission': (account * .1) * 0.001
        }
    if float(row['AROR_12']) >= 0.001:
        response = {
            'trade': 'SELL',
            'amount': round(account * .5 / row[CLOSE],5),
            'commission': (account * .5) * 0.001
        }


"""

# Specify function on row
def buy(row):
    account = 10_000
    commission = 0
    response = None

    if float(row['AROR_6']) <= -0.001 \
    and float(row['LAG1_AROR_6']) <= float(row['AROR_6']):
        response = {
            'trade': 'BUY',
            'amount': round(account * .1 / row[CLOSE], 5),
            'commission': (account * .1) * 0.001
        }

    return response


def sell(row):
    account = 10_000
    commission = 0
    response = None
    if float(row['AROR_6']) >= 0.001 \
    and float(row['AROR_6']) <= float(row['AROR_12']):
        response = {
            'trade': 'SELL',
            'amount': round(account * .5 / row[CLOSE], 5),
            'commission': (account * .5) * 0.001
        }

#     if float(row['AROR_12']) >= 0.001 \
#     and float(row['AROR_12']) <= float(row['AROR_24']):
#         response = {
#             'trade': 'SELL',
#             'amount': round(account * .5 / row[CLOSE],5),
#             'commission': (account * .5) * 0.001
#         }
    return response


def sell_short(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'SELL SHORT'
    response = None
    return response


def buy_cover(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'BUY COVER'
    response = None
    return response
