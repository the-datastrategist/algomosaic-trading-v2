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

    # Volume
    df = talib_features.LAG(df, 'volume_base', n=1)
    df = talib_features.LAG(df, 'volume_base', n=2)
    df = talib_features.LAG(df, 'volume_base', n=3)
    df = talib_features.LAG(df, 'volume_base', n=4)
    df = talib_features.LAG(df, 'volume_base', n=5)
    df = talib_features.LAG(df, 'volume_base', n=6)
    df = talib_features.LAG(df, 'volume_base', n=7)
    df = talib_features.LAG(df, 'volume_base', n=8)
    df = talib_features.LAG(df, 'volume_base', n=9)
    df = talib_features.LAG(df, 'volume_base', n=10)
    df = talib_features.LAG(df, 'volume_base', n=11)
    df = talib_features.LAG(df, 'volume_base', n=12)
    df = talib_features.LAG(df, 'volume_base', n=13)
    df = talib_features.LAG(df, 'volume_base', n=14)
    df = talib_features.LAG(df, 'volume_base', n=15)
    df = talib_features.LAG(df, 'volume_base', n=16)
    df = talib_features.LAG(df, 'volume_base', n=17)
    df = talib_features.LAG(df, 'volume_base', n=18)
    df = talib_features.LAG(df, 'volume_base', n=19)
    df = talib_features.LAG(df, 'volume_base', n=20)
    df = talib_features.LAG(df, 'volume_base', n=21)
    df = talib_features.LAG(df, 'volume_base', n=22)
    df = talib_features.LAG(df, 'volume_base', n=23)
    df = talib_features.LAG(df, 'volume_base', n=24)

    """
    INPUT FEATURES
    Price action features
    """
    df['open_close1'] = np.log(df.open / df.LAG1_close)
    df['open_high1'] = np.log(df.open / df.LAG1_high)
    df['open_low1'] = np.log(df.open / df.LAG1_low)

    df['open_close2'] = np.log(df.open / df.LAG2_close)
    df['open_high2'] = np.log(df.open / df.LAG2_high)
    df['open_low2'] = np.log(df.open / df.LAG2_low)

    df['open_close3'] = np.log(df.open / df.LAG3_close)
    df['open_high3'] = np.log(df.open / df.LAG3_high)
    df['open_low3'] = np.log(df.open / df.LAG3_low)

    df['open_close4'] = np.log(df.open / df.LAG4_close)
    df['open_high4'] = np.log(df.open / df.LAG4_high)
    df['open_low4'] = np.log(df.open / df.LAG4_low)

    df['open_close5'] = np.log(df.open / df.LAG5_close)
    df['open_high5'] = np.log(df.open / df.LAG5_high)
    df['open_low5'] = np.log(df.open / df.LAG5_low)

    df['open_close6'] = np.log(df.open / df.LAG6_close)
    df['open_high6'] = np.log(df.open / df.LAG6_high)
    df['open_low6'] = np.log(df.open / df.LAG6_low)

    df['open_close7'] = np.log(df.open / df.LAG7_close)
    df['open_high7'] = np.log(df.open / df.LAG7_high)
    df['open_low7'] = np.log(df.open / df.LAG7_low)

    df['open_close8'] = np.log(df.open / df.LAG8_close)
    df['open_high8'] = np.log(df.open / df.LAG8_high)
    df['open_low8'] = np.log(df.open / df.LAG8_low)

    df['open_close9'] = np.log(df.open / df.LAG9_close)
    df['open_high9'] = np.log(df.open / df.LAG9_high)
    df['open_low9'] = np.log(df.open / df.LAG9_low)

    df['open_close10'] = np.log(df.open / df.LAG10_close)
    df['open_high10'] = np.log(df.open / df.LAG10_high)
    df['open_low10'] = np.log(df.open / df.LAG10_low)

    df['open_close11'] = np.log(df.open / df.LAG11_close)
    df['open_high11'] = np.log(df.open / df.LAG11_high)
    df['open_low11'] = np.log(df.open / df.LAG11_low)

    df['open_close12'] = np.log(df.open / df.LAG12_close)
    df['open_high12'] = np.log(df.open / df.LAG12_high)
    df['open_low12'] = np.log(df.open / df.LAG12_low)

    df['open_close13'] = np.log(df.open / df.LAG13_close)
    df['open_high13'] = np.log(df.open / df.LAG13_high)
    df['open_low13'] = np.log(df.open / df.LAG13_low)

    df['open_close14'] = np.log(df.open / df.LAG14_close)
    df['open_high14'] = np.log(df.open / df.LAG14_high)
    df['open_low14'] = np.log(df.open / df.LAG14_low)

    df['open_close15'] = np.log(df.open / df.LAG15_close)
    df['open_high15'] = np.log(df.open / df.LAG15_high)
    df['open_low15'] = np.log(df.open / df.LAG15_low)

    df['open_close16'] = np.log(df.open / df.LAG16_close)
    df['open_high16'] = np.log(df.open / df.LAG16_high)
    df['open_low16'] = np.log(df.open / df.LAG16_low)

    df['open_close17'] = np.log(df.open / df.LAG17_close)
    df['open_high17'] = np.log(df.open / df.LAG17_high)
    df['open_low17'] = np.log(df.open / df.LAG17_low)

    df['open_close18'] = np.log(df.open / df.LAG18_close)
    df['open_high18'] = np.log(df.open / df.LAG18_high)
    df['open_low18'] = np.log(df.open / df.LAG18_low)

    df['open_close19'] = np.log(df.open / df.LAG19_close)
    df['open_high19'] = np.log(df.open / df.LAG19_high)
    df['open_low19'] = np.log(df.open / df.LAG19_low)

    df['open_close20'] = np.log(df.open / df.LAG20_close)
    df['open_high20'] = np.log(df.open / df.LAG20_high)
    df['open_low20'] = np.log(df.open / df.LAG20_low)

    df['open_close21'] = np.log(df.open / df.LAG21_close)
    df['open_high21'] = np.log(df.open / df.LAG21_high)
    df['open_low21'] = np.log(df.open / df.LAG21_low)

    df['open_close22'] = np.log(df.open / df.LAG22_close)
    df['open_high22'] = np.log(df.open / df.LAG22_high)
    df['open_low22'] = np.log(df.open / df.LAG22_low)

    df['open_close23'] = np.log(df.open / df.LAG23_close)
    df['open_high23'] = np.log(df.open / df.LAG23_high)
    df['open_low23'] = np.log(df.open / df.LAG23_low)

    df['open_close24'] = np.log(df.open / df.LAG24_close)
    df['open_high24'] = np.log(df.open / df.LAG24_high)
    df['open_low24'] = np.log(df.open / df.LAG24_low)

    """
    INPUT FEATURES
    Volume change
    """
    df['volume_lag1'] = np.log(df.volume_base / df.LAG1_volume_base)
    df['volume_lag2'] = np.log(df.volume_base / df.LAG2_volume_base)
    df['volume_lag3'] = np.log(df.volume_base / df.LAG3_volume_base)
    df['volume_lag4'] = np.log(df.volume_base / df.LAG4_volume_base)
    df['volume_lag5'] = np.log(df.volume_base / df.LAG5_volume_base)
    df['volume_lag6'] = np.log(df.volume_base / df.LAG6_volume_base)
    df['volume_lag7'] = np.log(df.volume_base / df.LAG7_volume_base)
    df['volume_lag8'] = np.log(df.volume_base / df.LAG8_volume_base)
    df['volume_lag9'] = np.log(df.volume_base / df.LAG9_volume_base)
    df['volume_lag10'] = np.log(df.volume_base / df.LAG10_volume_base)
    df['volume_lag11'] = np.log(df.volume_base / df.LAG11_volume_base)
    df['volume_lag12'] = np.log(df.volume_base / df.LAG12_volume_base)
    df['volume_lag13'] = np.log(df.volume_base / df.LAG13_volume_base)
    df['volume_lag14'] = np.log(df.volume_base / df.LAG14_volume_base)
    df['volume_lag15'] = np.log(df.volume_base / df.LAG15_volume_base)
    df['volume_lag16'] = np.log(df.volume_base / df.LAG16_volume_base)
    df['volume_lag17'] = np.log(df.volume_base / df.LAG17_volume_base)
    df['volume_lag18'] = np.log(df.volume_base / df.LAG18_volume_base)
    df['volume_lag19'] = np.log(df.volume_base / df.LAG19_volume_base)
    df['volume_lag20'] = np.log(df.volume_base / df.LAG20_volume_base)
    df['volume_lag21'] = np.log(df.volume_base / df.LAG21_volume_base)
    df['volume_lag22'] = np.log(df.volume_base / df.LAG22_volume_base)
    df['volume_lag23'] = np.log(df.volume_base / df.LAG23_volume_base)
    df['volume_lag24'] = np.log(df.volume_base / df.LAG24_volume_base)

    return df
