"""Apply financial indicator calculations using the talib package.

"""

from src.features import talib
from src.features import talib_features


def get_features(df):

    # Sort time in correct order
    df = df.sort_values(by='ticker_time')
    
    # Get standard date transformations
    df = talib_features.get_date_variables(df, 'ticker_time')

    """
    FINANCIAL INDICATORS
    """
    # outcome variables
    # next N hours from the close time
    df = talib.ROR(df, -1)
    df = talib.ROR(df, -3)
    df = talib.ROR(df, -6)
    df = talib.ROR(df, -12)
    df = talib.ROR(df, -18)
    df = talib.ROR(df, -24)
    df = talib.ROR(df, -48)
    df = talib.ROR(df, -72)
    df = talib.ROR(df, -96)
    df = talib.ROR(df, -120)

    # input variables: AROR
    df = talib.AROR(df, 1)
    df = talib.AROR(df, 2)
    df = talib.AROR(df, 3)
    df = talib.AROR(df, 6)
    df = talib.AROR(df, 9)
    df = talib.AROR(df, 12)
    df = talib.AROR(df, 18)
    df = talib.AROR(df, 24)
    df = talib.AROR(df, 30)
    df = talib.AROR(df, 36)
    df = talib.AROR(df, 40)
    df = talib.AROR(df, 48)
    df = talib.AROR(df, 50)
    df = talib.AROR(df, 60)
    df = talib.AROR(df, 70)
    df = talib.AROR(df, 72)
    df = talib.AROR(df, 80)
    df = talib.AROR(df, 90)
    df = talib.AROR(df, 96)
    df = talib.AROR(df, 100)
    df = talib.AROR(df, 120)
    df = talib.AROR(df, 144)
    df = talib.AROR(df, 150)
    df = talib.AROR(df, 168)
    df = talib.AROR(df, 192)
    df = talib.AROR(df, 200)
    df = talib.AROR(df, 216)
    df = talib.AROR(df, 240)
    df = talib.AROR(df, 250)
    df = talib.AROR(df, 264)
    df = talib.AROR(df, 288)
    df = talib.AROR(df, 300)

    # close price EMA
    df = talib.EMA(df, 12)
    df = talib.EMA(df, 24)
    df = talib.EMA(df, 48)
    df = talib.EMA(df, 120)
    df = talib.EMA(df, 168)
    df = talib.EMA(df, 240)

    # Avg True Range
    df = talib.ATR(df, 6)
    df = talib.ATR(df, 12)
    df = talib.ATR(df, 24)
    df = talib.ATR(df, 48)
    df = talib.ATR(df, 72)
    df = talib.ATR(df, 96)
    df = talib.ATR(df, 120)
    df = talib.ATR(df, 168)
    df = talib.ATR(df, 240)
    
    # Bollinger Bands
    df = talib.BBANDS(df, 12)
    df = talib.BBANDS(df, 24)
    df = talib.BBANDS(df, 48)
    df = talib.BBANDS(df, 72)
    df = talib.BBANDS(df, 96)
    df = talib.BBANDS(df, 120)
    df = talib.BBANDS(df, 168)
    df = talib.BBANDS(df, 240)
    
    # MACD
    df = talib.MACD(df, 12, 24)
    df = talib.MACD(df, 24, 168)
    df = talib.MACD(df, 24, 240)
    
    # RSI
    df = talib.RSI(df, 12)
    df = talib.RSI(df, 24)
    df = talib.RSI(df, 48)
    df = talib.RSI(df, 72)
    df = talib.RSI(df, 96)
    df = talib.RSI(df, 120)
    df = talib.RSI(df, 168)
    df = talib.RSI(df, 240)

    # Other indicators
    df = talib.MassI(df, 12, 24)
    df = talib.MassI(df, 24, 168)

    df = talib.ACCDIST(df, n=12)
    df = talib.ACCDIST(df, n=24)
    df = talib.ACCDIST(df, n=168)
    
    df = talib.Vortex(df, n=12)
    df = talib.Vortex(df, n=24)
    df = talib.Vortex(df, n=168)
    
    """
    FEATURE ENGINEERING
    """
    # trailing min over n-periods
    df = talib_features.SM_MIN(df, n=24)
    df = talib_features.SM_MIN(df, n=168)
    df = talib_features.SM_MIN(df, n=240)

    # trailing max over n-periods
    df = talib_features.SM_MAX(df, n=24)
    df = talib_features.SM_MAX(df, n=168)
    df = talib_features.SM_MAX(df, n=240)

    return df

