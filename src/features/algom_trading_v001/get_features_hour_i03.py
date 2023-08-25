"""Apply financial indicator calculations using the talib package.


"""
import numpy as np
from src.features import talib
from src.features import talib_features

CLOSE = 'close'
VOLUME = 'volume'


def safe_divide(numerator, denominator):
    try:
        return (numerator / denominator)
    except:
        return np.nan


def get_features(df):

    df = df.sort_values(by='ticker_time')

    """
    DATE VARIABLES
    """
    df = talib_features.get_date_variables(df, 'ticker_time')

    """
    OUTCOME VARIABLES
    """
    df = talib.ROR(df, -1)
    df = talib.ROR(df, -3)
    df = talib.ROR(df, -5)
    df = talib.ROR(df, -6)
    df = talib.ROR(df, -10)
    df = talib.ROR(df, -12)
    df = talib.ROR(df, -15)
    df = talib.ROR(df, -20)
    df = talib.ROR(df, -24)
    df = talib.ROR(df, -25)
    df = talib.ROR(df, -30)
    df = talib.ROR(df, -36)
    df = talib.ROR(df, -48)
    df = talib.ROR(df, -72)

    """
    FEATURE ENGINEERING
    Calculate lag of OHLC price action
    """
    df = talib_features.LAG(df, 'open', n=1)
    df = talib_features.LAG(df, 'high', n=1)
    df = talib_features.LAG(df, 'low', n=1)
    df = talib_features.LAG(df, 'close', n=1)

    df = talib_features.LAG(df, 'open', n=2)
    df = talib_features.LAG(df, 'high', n=2)
    df = talib_features.LAG(df, 'low', n=2)
    df = talib_features.LAG(df, 'close', n=2)

    df = talib_features.LAG(df, 'open', n=3)
    df = talib_features.LAG(df, 'high', n=3)
    df = talib_features.LAG(df, 'low', n=3)
    df = talib_features.LAG(df, 'close', n=3)

    df = talib_features.LAG(df, 'open', n=4)
    df = talib_features.LAG(df, 'high', n=4)
    df = talib_features.LAG(df, 'low', n=4)
    df = talib_features.LAG(df, 'close', n=4)

    df = talib_features.LAG(df, 'open', n=5)
    df = talib_features.LAG(df, 'high', n=5)
    df = talib_features.LAG(df, 'low', n=5)
    df = talib_features.LAG(df, 'close', n=5)

    df = talib_features.LAG(df, 'open', n=6)
    df = talib_features.LAG(df, 'high', n=6)
    df = talib_features.LAG(df, 'low', n=6)
    df = talib_features.LAG(df, 'close', n=6)

    df = talib_features.LAG(df, 'open', n=7)
    df = talib_features.LAG(df, 'high', n=7)
    df = talib_features.LAG(df, 'low', n=7)
    df = talib_features.LAG(df, 'close', n=7)

    df = talib_features.LAG(df, 'open', n=8)
    df = talib_features.LAG(df, 'high', n=8)
    df = talib_features.LAG(df, 'low', n=8)
    df = talib_features.LAG(df, 'close', n=8)

    df = talib_features.LAG(df, 'open', n=9)
    df = talib_features.LAG(df, 'high', n=9)
    df = talib_features.LAG(df, 'low', n=9)
    df = talib_features.LAG(df, 'close', n=9)

    df = talib_features.LAG(df, 'open', n=10)
    df = talib_features.LAG(df, 'high', n=10)
    df = talib_features.LAG(df, 'low', n=10)
    df = talib_features.LAG(df, 'close', n=10)

    df = talib_features.LAG(df, 'open', n=11)
    df = talib_features.LAG(df, 'high', n=11)
    df = talib_features.LAG(df, 'low', n=11)
    df = talib_features.LAG(df, 'close', n=11)

    df = talib_features.LAG(df, 'open', n=12)
    df = talib_features.LAG(df, 'high', n=12)
    df = talib_features.LAG(df, 'low', n=12)
    df = talib_features.LAG(df, 'close', n=12)

    df = talib_features.LAG(df, 'open', n=13)
    df = talib_features.LAG(df, 'high', n=13)
    df = talib_features.LAG(df, 'low', n=13)
    df = talib_features.LAG(df, 'close', n=13)

    df = talib_features.LAG(df, 'open', n=14)
    df = talib_features.LAG(df, 'high', n=14)
    df = talib_features.LAG(df, 'low', n=14)
    df = talib_features.LAG(df, 'close', n=14)

    df = talib_features.LAG(df, 'open', n=15)
    df = talib_features.LAG(df, 'high', n=15)
    df = talib_features.LAG(df, 'low', n=15)
    df = talib_features.LAG(df, 'close', n=15)

    df = talib_features.LAG(df, 'open', n=16)
    df = talib_features.LAG(df, 'high', n=16)
    df = talib_features.LAG(df, 'low', n=16)
    df = talib_features.LAG(df, 'close', n=16)

    df = talib_features.LAG(df, 'open', n=17)
    df = talib_features.LAG(df, 'high', n=17)
    df = talib_features.LAG(df, 'low', n=17)
    df = talib_features.LAG(df, 'close', n=17)

    df = talib_features.LAG(df, 'open', n=18)
    df = talib_features.LAG(df, 'high', n=18)
    df = talib_features.LAG(df, 'low', n=18)
    df = talib_features.LAG(df, 'close', n=18)

    df = talib_features.LAG(df, 'open', n=19)
    df = talib_features.LAG(df, 'high', n=19)
    df = talib_features.LAG(df, 'low', n=19)
    df = talib_features.LAG(df, 'close', n=19)

    df = talib_features.LAG(df, 'open', n=20)
    df = talib_features.LAG(df, 'high', n=20)
    df = talib_features.LAG(df, 'low', n=20)
    df = talib_features.LAG(df, 'close', n=20)

    df = talib_features.LAG(df, 'open', n=21)
    df = talib_features.LAG(df, 'high', n=21)
    df = talib_features.LAG(df, 'low', n=21)
    df = talib_features.LAG(df, 'close', n=21)

    df = talib_features.LAG(df, 'open', n=22)
    df = talib_features.LAG(df, 'high', n=22)
    df = talib_features.LAG(df, 'low', n=22)
    df = talib_features.LAG(df, 'close', n=22)

    df = talib_features.LAG(df, 'open', n=23)
    df = talib_features.LAG(df, 'high', n=23)
    df = talib_features.LAG(df, 'low', n=23)
    df = talib_features.LAG(df, 'close', n=23)

    df = talib_features.LAG(df, 'open', n=24)
    df = talib_features.LAG(df, 'high', n=24)
    df = talib_features.LAG(df, 'low', n=24)
    df = talib_features.LAG(df, 'close', n=24)


    """
    INPUT FEATURES
    Final input features
    """
    df['open_close1'] = safe_divide(np.log(df.LAG1_close), df.open)
    df['open_high1'] = safe_divide(np.log(df.LAG1_high), df.open)
    df['open_low1'] = safe_divide(np.log(df.LAG1_low), df.open)

    df['open_close2'] = safe_divide(np.log(df.LAG2_close), df.open)
    df['open_high2'] = safe_divide(np.log(df.LAG2_high), df.open)
    df['open_low2'] = safe_divide(np.log(df.LAG2_low), df.open)

    df['open_close3'] = safe_divide(np.log(df.LAG3_close), df.open)
    df['open_high3'] = safe_divide(np.log(df.LAG3_high), df.open)
    df['open_low3'] = safe_divide(np.log(df.LAG3_low), df.open)

    df['open_close4'] = safe_divide(np.log(df.LAG4_close), df.open)
    df['open_high4'] = safe_divide(np.log(df.LAG4_high), df.open)
    df['open_low4'] = safe_divide(np.log(df.LAG4_low), df.open)

    df['open_close5'] = safe_divide(np.log(df.LAG5_close), df.open)
    df['open_high5'] = safe_divide(np.log(df.LAG5_high), df.open)
    df['open_low5'] = safe_divide(np.log(df.LAG5_low), df.open)

    df['open_close6'] = safe_divide(np.log(df.LAG6_close), df.open)
    df['open_high6'] = safe_divide(np.log(df.LAG6_high), df.open)
    df['open_low6'] = safe_divide(np.log(df.LAG6_low), df.open)

    df['open_close7'] = safe_divide(np.log(df.LAG7_close), df.open)
    df['open_high7'] = safe_divide(np.log(df.LAG7_high), df.open)
    df['open_low7'] = safe_divide(np.log(df.LAG7_low), df.open)

    df['open_close8'] = safe_divide(np.log(df.LAG8_close), df.open)
    df['open_high8'] = safe_divide(np.log(df.LAG8_high), df.open)
    df['open_low8'] = safe_divide(np.log(df.LAG8_low), df.open)

    df['open_close9'] = safe_divide(np.log(df.LAG9_close), df.open)
    df['open_high9'] = safe_divide(np.log(df.LAG9_high), df.open)
    df['open_low9'] = safe_divide(np.log(df.LAG9_low), df.open)

    df['open_close10'] = safe_divide(np.log(df.LAG10_close), df.open)
    df['open_high10'] = safe_divide(np.log(df.LAG10_high), df.open)
    df['open_low10'] = safe_divide(np.log(df.LAG10_low), df.open)

    df['open_close11'] = safe_divide(np.log(df.LAG11_close), df.open)
    df['open_high11'] = safe_divide(np.log(df.LAG11_high), df.open)
    df['open_low11'] = safe_divide(np.log(df.LAG11_low), df.open)

    df['open_close12'] = safe_divide(np.log(df.LAG12_close), df.open)
    df['open_high12'] = safe_divide(np.log(df.LAG12_high), df.open)
    df['open_low12'] = safe_divide(np.log(df.LAG12_low), df.open)

    df['open_close13'] = safe_divide(np.log(df.LAG13_close), df.open)
    df['open_high13'] = safe_divide(np.log(df.LAG13_high), df.open)
    df['open_low13'] = safe_divide(np.log(df.LAG13_low), df.open)

    df['open_close14'] = safe_divide(np.log(df.LAG14_close), df.open)
    df['open_high14'] = safe_divide(np.log(df.LAG14_high), df.open)
    df['open_low14'] = safe_divide(np.log(df.LAG14_low), df.open)

    df['open_close15'] = safe_divide(np.log(df.LAG15_close), df.open)
    df['open_high15'] = safe_divide(np.log(df.LAG15_high), df.open)
    df['open_low15'] = safe_divide(np.log(df.LAG15_low), df.open)

    df['open_close16'] = safe_divide(np.log(df.LAG16_close), df.open)
    df['open_high16'] = safe_divide(np.log(df.LAG16_high), df.open)
    df['open_low16'] = safe_divide(np.log(df.LAG16_low), df.open)

    df['open_close17'] = safe_divide(np.log(df.LAG17_close), df.open)
    df['open_high17'] = safe_divide(np.log(df.LAG17_high), df.open)
    df['open_low17'] = safe_divide(np.log(df.LAG17_low), df.open)

    df['open_close18'] = safe_divide(np.log(df.LAG18_close), df.open)
    df['open_high18'] = safe_divide(np.log(df.LAG18_high), df.open)
    df['open_low18'] = safe_divide(np.log(df.LAG18_low), df.open)

    df['open_close19'] = safe_divide(np.log(df.LAG19_close), df.open)
    df['open_high19'] = safe_divide(np.log(df.LAG19_high), df.open)
    df['open_low19'] = safe_divide(np.log(df.LAG19_low), df.open)

    df['open_close20'] = safe_divide(np.log(df.LAG20_close), df.open)
    df['open_high20'] = safe_divide(np.log(df.LAG20_high), df.open)
    df['open_low20'] = safe_divide(np.log(df.LAG20_low), df.open)

    df['open_close21'] = safe_divide(np.log(df.LAG21_close), df.open)
    df['open_high21'] = safe_divide(np.log(df.LAG21_high), df.open)
    df['open_low21'] = safe_divide(np.log(df.LAG21_low), df.open)

    df['open_close22'] = safe_divide(np.log(df.LAG22_close), df.open)
    df['open_high22'] = safe_divide(np.log(df.LAG22_high), df.open)
    df['open_low22'] = safe_divide(np.log(df.LAG22_low), df.open)

    df['open_close23'] = safe_divide(np.log(df.LAG23_close), df.open)
    df['open_high23'] = safe_divide(np.log(df.LAG23_high), df.open)
    df['open_low23'] = safe_divide(np.log(df.LAG23_low), df.open)

    df['open_close24'] = safe_divide(np.log(df.LAG24_close), df.open)
    df['open_high24'] = safe_divide(np.log(df.LAG24_high), df.open)
    df['open_low24'] = safe_divide(np.log(df.LAG24_low), df.open)

    return df

