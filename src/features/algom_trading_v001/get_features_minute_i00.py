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
    df = talib.ROR(df, -15)
    df = talib.ROR(df, -30)
    df = talib.ROR(df, -45)
    df = talib.ROR(df, -12)
    df = talib.ROR(df, -18)
    df = talib.ROR(df, -24)
    df = talib.ROR(df, -48)
    df = talib.ROR(df, -72)
    df = talib.ROR(df, -96)
    df = talib.ROR(df, -120)

    # input variables: AROR
    df = talib.AROR(df, 5)
    df = talib.AROR(df, 10)
    
    # 15 minute intervals
    df = talib.AROR(df, 15)
    df = talib.AROR(df, 30)
    df = talib.AROR(df, 45)
    df = talib.AROR(df, 60)
    df = talib.AROR(df, 75)
    df = talib.AROR(df, 90)
    df = talib.AROR(df, 105)
    df = talib.AROR(df, 120)
    df = talib.AROR(df, 135)
    df = talib.AROR(df, 150)
    df = talib.AROR(df, 165)
    df = talib.AROR(df, 180)
    df = talib.AROR(df, 195)
    df = talib.AROR(df, 210)
    df = talib.AROR(df, 225)
    df = talib.AROR(df, 240)
    df = talib.AROR(df, 255)
    df = talib.AROR(df, 270)
    df = talib.AROR(df, 285)
    df = talib.AROR(df, 300)
    df = talib.AROR(df, 315)
    df = talib.AROR(df, 330)
    df = talib.AROR(df, 345)
    
    # 30 minute intervals, after 6 hours
    df = talib.AROR(df, 360)
    df = talib.AROR(df, 390)
    df = talib.AROR(df, 420)
    df = talib.AROR(df, 450)
    df = talib.AROR(df, 480)
    df = talib.AROR(df, 510)
    df = talib.AROR(df, 540)
    df = talib.AROR(df, 570)
    df = talib.AROR(df, 600)
    df = talib.AROR(df, 630)
    df = talib.AROR(df, 660)
    df = talib.AROR(df, 690)
    df = talib.AROR(df, 720)


    # close price EMA
    df = talib.EMA(df, 15)
    df = talib.EMA(df, 30)
    df = talib.EMA(df, 60)
    df = talib.EMA(df, 120)
    df = talib.EMA(df, 180)
    df = talib.EMA(df, 240)
    df = talib.EMA(df, 300)
    df = talib.EMA(df, 360)
    df = talib.EMA(df, 720)
    df = talib.EMA(df, 1440)

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
    df = talib.BBANDS(df, 15)
    df = talib.BBANDS(df, 30)
    df = talib.BBANDS(df, 60)
    df = talib.BBANDS(df, 120)
    df = talib.BBANDS(df, 180)
    df = talib.BBANDS(df, 360)
    df = talib.BBANDS(df, 720)
    df = talib.BBANDS(df, 1440)
    
    # MACD
    df = talib.MACD(df, 15, 30)
    df = talib.MACD(df, 15, 60)
    df = talib.MACD(df, 15, 360)
    df = talib.MACD(df, 30, 360)
    df = talib.MACD(df, 30, 720)
    df = talib.MACD(df, 30, 1440)
    
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
    df = talib.MassI(df, 15, 30)
    df = talib.MassI(df, 15, 180)
    df = talib.MassI(df, 15, 360)
    df = talib.MassI(df, 30, 360)
    df = talib.MassI(df, 60, 360)

    df = talib.ACCDIST(df, n=15)
    df = talib.ACCDIST(df, n=30)
    df = talib.ACCDIST(df, n=360)
    
    df = talib.Vortex(df, n=15)
    df = talib.Vortex(df, n=30)
    df = talib.Vortex(df, n=180)
    df = talib.Vortex(df, n=360)
    
    """
    FEATURE ENGINEERING
    """
    # trailing min over n-periods
    df = talib_features.SM_MIN(df, n=15)
    df = talib_features.SM_MIN(df, n=30)
    df = talib_features.SM_MIN(df, n=60)
    df = talib_features.SM_MIN(df, n=120)
    df = talib_features.SM_MIN(df, n=180)
    df = talib_features.SM_MIN(df, n=360)
    df = talib_features.SM_MIN(df, n=720)
    df = talib_features.SM_MIN(df, n=1440)

    # trailing max over n-periods
    df = talib_features.SM_MAX(df, n=15)
    df = talib_features.SM_MAX(df, n=30)
    df = talib_features.SM_MAX(df, n=60)
    df = talib_features.SM_MAX(df, n=120)
    df = talib_features.SM_MAX(df, n=180)
    df = talib_features.SM_MAX(df, n=360)
    df = talib_features.SM_MAX(df, n=720)
    df = talib_features.SM_MAX(df, n=1440)

    return df

