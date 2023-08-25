"""Apply financial indicator calculations using the talib package.

"""

from src.features import talib
from src.features import talib_features

CLOSE = 'close'
VOLUME = 'volume'

def get_features(df):
    
    df = df.sort_values(by='ticker_time')
    df = talib_features.get_date_variables(df, 'ticker_time')
    
    """
    FINANCIAL INDICATORS
    """

    # outcome variables
    df = talib.ROR(df, -1)
    df = talib.ROR(df, -3)
    df = talib.ROR(df, -6)
    df = talib.ROR(df, -12)
    df = talib.ROR(df, -18)
    df = talib.ROR(df, -24)
    df = talib.ROR(df, -48)

    # input variables: AROR
    df = talib.AROR(df, 1)
    df = talib.AROR(df, 2)
    df = talib.AROR(df, 3)
    df = talib.AROR(df, 6)
    df = talib.AROR(df, 9)
    df = talib.AROR(df, 12)
    df = talib.AROR(df, 16)
    df = talib.AROR(df, 20)
    df = talib.AROR(df, 24)
    df = talib.AROR(df, 28)
    df = talib.AROR(df, 30)
    df = talib.AROR(df, 40)
    df = talib.AROR(df, 50)
    df = talib.AROR(df, 60)
    df = talib.AROR(df, 70)
    df = talib.AROR(df, 80)
    df = talib.AROR(df, 90)
    df = talib.AROR(df, 100)
    df = talib.AROR(df, 110)
    df = talib.AROR(df, 120)
    df = talib.AROR(df, 130)
    df = talib.AROR(df, 140)
    df = talib.AROR(df, 150)
    df = talib.AROR(df, 160)
    df = talib.AROR(df, 170)
    df = talib.AROR(df, 180)
    df = talib.AROR(df, 190)
    df = talib.AROR(df, 200)
    df = talib.AROR(df, 210)
    df = talib.AROR(df, 220)
    df = talib.AROR(df, 230)
    df = talib.AROR(df, 240)
    df = talib.AROR(df, 250)
    df = talib.AROR(df, 300)

    # close price EMA
    df = talib.EMA(df, 3)
    df = talib.EMA(df, 9)    
    df = talib.EMA(df, 12)
    df = talib.EMA(df, 18)
    df = talib.EMA(df, 24)
    df = talib.EMA(df, 48)
    df = talib.EMA(df, 100)
    df = talib.EMA(df, 150)
    df = talib.EMA(df, 180)
    df = talib.EMA(df, 200)
    
    # Avg True Range
    df = talib.ATR(df, 3)
    df = talib.ATR(df, 6)
    df = talib.ATR(df, 9)
    df = talib.ATR(df, 12)
    df = talib.ATR(df, 16)
    df = talib.ATR(df, 24)
    df = talib.ATR(df, 50)
    df = talib.ATR(df, 100)
    df = talib.ATR(df, 150)
    df = talib.ATR(df, 200)
    
    # Bollinger Bands
    df = talib.BBANDS(df, 6)
    df = talib.BBANDS(df, 12)
    df = talib.BBANDS(df, 18)
    df = talib.BBANDS(df, 24)
    df = talib.BBANDS(df, 48)
    df = talib.BBANDS(df, 100)
    df = talib.BBANDS(df, 150)
    df = talib.BBANDS(df, 200)
    
    # MACD
    df = talib.MACD(df, 10, 20)
    df = talib.MACD(df, 12, 26)
    df = talib.MACD(df, 9, 12)
    df = talib.MACD(df, 26, 200)
    df = talib.MACD(df, 20, 200)
    
    # Other indicators
#     df = talib.RSI(df, 10)
#     df = talib.RSI(df, 20)
#     df = talib.RSI(df, 30)
#     df = talib.RSI(df, 40)
#     df = talib.RSI(df, 50)
#     df = talib.RSI(df, 100)
#     df = talib.RSI(df, 150)
#     df = talib.RSI(df, 200)
    df = talib.MassI(df)
    df = talib.STOK(df)    
    df = talib.ACCDIST(df, n=5)
    df = talib.ACCDIST(df, n=10)
    df = talib.ACCDIST(df, n=50)
    
    df = talib.Vortex(df, n=5)
    df = talib.Vortex(df, n=10)
    df = talib.Vortex(df, n=20)
    df = talib.Vortex(df, n=50)
    
    
    """
    FEATURE ENGINEERING
    """
    # one-hot variables
    #df = talib_features.get_onehot_coding(df, 'Month')
    #df = talib_features.get_onehot_coding(df, 'Quarter')

    # trailing min over n-periods
    df = talib_features.SM_MIN(df, n=6)
    df = talib_features.SM_MIN(df, n=12)
    df = talib_features.SM_MIN(df, n=24)
    df = talib_features.SM_MIN(df, n=48)
    df = talib_features.SM_MIN(df, n=150)
    df = talib_features.SM_MIN(df, n=200)
    
    # trailing max over n-periods
    df = talib_features.SM_MAX(df, n=6)
    df = talib_features.SM_MAX(df, n=12)
    df = talib_features.SM_MAX(df, n=24)
    df = talib_features.SM_MAX(df, n=48)
    df = talib_features.SM_MAX(df, n=150)
    df = talib_features.SM_MAX(df, n=200)
    
    # log (min+t0 / min+t1)
    #df = talib_features.RATIO_LOG(df, 'MIN_5', 'MIN_10', 0, 0)
    
    # log (max+t0 / max+t1)
    #df = talib_features.RATIO_LOG(df, 'MAX_5', 'MAX_10', 0, 0)

    # log ratio min/max
    #df = talib_features.RATIO_LOG(df, 'MIN_5', 'MAX_5', 0, 0)

    # AROR differences by time period 
    #df = talib_features.DIFF(df, 'AROR_1', 'AROR_3')

    # EMA Ratios
    #df = talib_features.RATIO_LOG(df, 'EMA_3', 'EMA_5')

    # Relative Volume EMA
    #df = talib_features.RATIO_LOG(df, VOLUME, 'EMA_volume_3')

    # price action: close prices vs recent history close
    #df = talib_features.RATIO(df, CLOSE, CLOSE,  0, 3)
    
    return df

