"""trade_business_rules.py

Specify the business rules you'd like to apply when making trades.
The function reads a row of input data and applies a `trade_response`
based on any of the variables specified from the input data.

"""

from algom import configs

CLOSE = configs.CLOSE


# specify function on row
def buy(row):
    amount = 10_000
    commission = 0
    response = None
    
    # AVG_ROR_n10/15_5: 15%+
    if float(row['SMA_ROR_n10_5']) > .15 \
    or float(row['SMA_ROR_n15_5']) > .15:

        if float(row['SMA_ROR_n3_3']) > .15 \
        or float(row['SMA_ROR_n5_5']) > .15:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .2 / row[CLOSE],5),
                'commission': commissions
            }
        elif float(row['SMA_ROR_n3_3']) > .1 \
        or float(row['SMA_ROR_n5_5']) > .1:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row[CLOSE],5),
                'commission': commission
            }
        elif float(row['SMA_ROR_n3_3']) > .05 \
        or float(row['SMA_ROR_n5_5']) > .05:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row[CLOSE],5),
                'commission': commission
            }

    # AVG_ROR_n10/15_5: 10-15%
    elif float(row['SMA_ROR_n10_5']) > .1 \
    or float(row['SMA_ROR_n15_5']) > .1:

        if float(row['SMA_ROR_n3_3']) > .1 \
        or float(row['SMA_ROR_n5_5']) > .1 \
        or float(row['SMA_ROR_n10_5']) > .1:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .1 / row[CLOSE],5),
                'commission': commission
            }
        elif float(row['SMA_ROR_n3_3']) > .05 \
        or float(row['SMA_ROR_n5_5']) > .05:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row[CLOSE],5),
                'commission': commission
            }

    # AVG_ROR_n10/15_5: 5-10%
    elif float(row['SMA_ROR_n10_5']) > 0:
        if float(row['SMA_ROR_n3_3']) > .05 \
        or float(row['SMA_ROR_n5_5']) > .05:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .05 / row[CLOSE],5),
                'commission': commission
            }
        elif float(row['SMA_ROR_n3_3']) > .03 \
        or float(row['SMA_ROR_n5_5']) > .03:
            response = {
                'trade': 'BUY',
                'amount': round(amount * .03 / row[CLOSE],5),
                'commission': commission
            }
    return response



def sell(row):
    amount = 10_000
    commission = 0
    response = None

    if float(row['SMA_ROR_n10_5']) <= -.1:
        if float(row['SMA_ROR_n5_5']) < -.2 \
        or float(row['SMA_ROR_n3_3']) < -.2:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .1 / row[CLOSE],5),
                'commission': commission
            }
        elif float(row['SMA_ROR_n3_3']) <= -.1 \
        or float(row['SMA_ROR_n5_5']) < -.1:
                response = {
                    'trade': 'SELL',
                    'amount': round(amount * .05 / row[CLOSE],5),
                    'commission': commission
            }
    elif float(row['SMA_ROR_n3_3']) <= -.05 \
    or float(row['SMA_ROR_n5_5']) < -.05:
            response = {
                'trade': 'SELL',
                'amount': round(amount * .025 / row[CLOSE],5),
                'commission': commission
            }
    elif float(row['SMA_ROR_n3_3']) <= 0 \
    or float(row['SMA_ROR_n5_5']) < 0:
        response = {
            'trade': 'SELL',
            'amount': round(amount * .01 / row[CLOSE],5),
            'commission': commission
        }
    return response



def sell_short(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'SELL SHORT'
    response = None
    return response
#     if float(row['SMA_ROR_n15_10']) <= -.1:
#         if float(row['SMA_ROR_n5_5']) < 0:
#             response = {
#                 'trade': TRADE,
#                 'amount': round(amount * .2 / row[CLOSE]),
#                 'commission': COMMISSION
#             }
#     elif float(row['SMA_ROR_n15_10']) <= -.05:
#         if float(row['SMA_ROR_n5_5']) < 0:
#             response = {
#                 'trade': TRADE,
#                 'amount': round(amount * .1 / row[CLOSE]),
#                 'commission': COMMISSION
#             }



def buy_cover(row):
    amount = 10_000
    COMMISSION = 0
    TRADE = 'BUY COVER'
    response = None
    return response
#     if float(row['SMA_ROR_n15_10']) >= .06:
#         if float(row['SMA_ROR_n5_5']) > 0:
#             response = {
#                 'trade': TRADE,
#                 'amount': round(amount * .5 / row[CLOSE]),
#                 'commission': COMMISSION
#             }
#     elif float(row['SMA_ROR_n15_10']) >= .04:
#         if float(row['SMA_ROR_n5_5']) > 0:
#             response = {
#                 'trade': TRADE,
#                 'amount': round(amount * .5 / row[CLOSE]),
#                 'commission': COMMISSION
#             }

