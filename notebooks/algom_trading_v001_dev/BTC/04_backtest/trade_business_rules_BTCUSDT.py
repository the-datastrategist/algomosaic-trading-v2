"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data.

"""


CLOSE = 'close'

# def trade(row):
#     amount = 10_000
#     commission = 0
#     response = None

#     if float(row['AROR_12']) <= -0.001 \
#     and float(row['AROR_12']) <= float(row['AROR_24']):
#         trade_value = round(amount * .1 / row[CLOSE],5)
#         response = {
#             'trade': 'BUY',
#             'amount': trade_value,
#             'commission': trade_value * 0.001
#         }
#     elif float(row['AROR_12']) >= -0.001 \
#     and float(row['AROR_12']) >= float(row['AROR_24']):
#         trade_value = round(amount * .5 / row[CLOSE],5)
#         response = {
#             'trade': 'SELL',
#             'amount': trade_value,
#             'commission': trade_value * 0.001
#         }
#     return response


# Specify function on row
def buy(row):
    amount = 10_000
    commission = 0
    response = None
    if float(row['AROR_12']) <= -0.001 \
    and float(row['AROR_12']) <= float(row['AROR_24']):
        trade_value = round(amount * .1 / row[CLOSE], 5)
        response = {
            'trade': 'BUY',
            'amount': trade_value,
            'commission': trade_value * 0.001
        }
    return response

def sell(row):
    amount = 10_000
    commission = 0
    response = None
    if float(row['AROR_12']) >= -0.001 \
    and float(row['AROR_12']) >= float(row['AROR_24']):
        trade_value = round(amount * .5 / row[CLOSE],5)
        response = {
            'trade': 'SELL',
            'amount': trade_value,
            'commission': trade_value * 0.001
        }
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
