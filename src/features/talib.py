"""talib.py
Calculate financial indicators based on OHLCV time series data. 
Most standard indicators are included. 

For each function, the output dataframe contains all input columns as 
well as the new column(s). Some workflows output multiple columns. Most
workflows have parameters that can be adjusted, but the default
can be used instead.

Sample code:
```
from etl import talib
df = talib.ROR(df, -10)      # log-adj Rate of Return, next 10 sessions
df = talib.AROR(df, 10)      # log-adj Avg Rate of Return, past 10 sessions
df = talib.BBANDS(df, 100)   # Bollinger Bands, past 100 sessions
```

Calculations were orginally based on the following Quantopian blog post; 
however, the code has been refactored and the naming conventions of the 
output columns have been adjusted.
    https://www.quantopian.com/posts/technical-analysis-indicators-without-talib-code

Commentary in function doc strings is sourced from Investopedia.
    https://www.investopedia.com
    
See the link below for a complete list of workflows along with doc
string documentation and metadata:
    https://docs.google.com/spreadsheets/d/1lyBSCZz6JidprUJ-rn2ddnMDwSpp52RkQWN_GAvVflI/edit#gid=0

"""

import numpy as np 
import pandas as pd  
import math as m

# Enter the column names of the input dataset
CLOSE = 'close'
HIGH = 'high'
LOW = 'low'
VOLUME = 'volume'



# STANDARD FUNCTIONS

def SMA(df, n, value=CLOSE):  
    """ Simple Moving Average (SMA)
    
    Calculates the Simple Moving Average of a value over n time-periods. 
    Defaults to Close price. A simple moving average (SMA) is an 
    arithmetic moving average calculated by adding recent closing prices 
    and then dividing that by the number of time periods in the 
    calculation average.
    
    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing Close price

    n : int
        Lookback window period, n-sessions

    value : string (optional)
        Indicator or metric to calculate SMA; defaults to Close price

    Returns
    -------
    Pandas dataframe containing columns:
        SMA_{n} or SMA_{value}_{n}
    """
    MA = df[CLOSE].rolling(window=n, center=False).mean()
    df = df.join(MA, rsuffix = '_SMA{}'.format(str(n)))
    return df


def EMA(df, n, value=CLOSE):
    """Exponential Moving Average (EMA)
    
    Calculates the Exponential Moving Average of a value over n 
    time-periods. Parameter 'value' defaults to Close price. An 
    exponential moving average (EMA) is a type of moving average (MA) 
    that places a greater weight and significance on the most recent 
    data points.
    
    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing Close price

    n : int
        Lookback window period, n-sessions

    value : string (optional)
        Indicator or metric to calculate EMA; defaults to Close price

    Returns
    -------
    Pandas dataframe containing columns:
        EMA_{n} or EMA_{value}_{n}
    """
    if value==CLOSE:
        value_name = 'EMA_{}'.format(n)
    else:
        value_name = 'EMA_{}_{}'.format(value, n)
    EMA = pd.Series(
        df[value].ewm(span = n, min_periods = n - 1).mean(), 
        name = value_name
        )
    df = df.join(EMA, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def MOM(df, n):
    """Momentum (MOM)

    Difference in current Close and n-periods prior.

    Momentum is the rate of acceleration of a security's price or 
    volume – that is, the speed at which the price is changing. Simply 
    put, it refers to the rate of change on price movements for a 
    particular asset and is usually defined as a rate.
    """
    M = pd.Series(df[CLOSE].diff(n), name = 'Momentum_' + str(n))
    df = df.join(M, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ROC(df, n, value=CLOSE):
    """Rate of Change for Close Price

    % Change in current Close and n-periods prior
    """
    M = df[value].diff(n - 1) 
    N = df[value].shift(n - 1)
    ROC = pd.Series(M / N, name = 'ROC_{}_{}'.format(value, n))
    df = df.join(ROC, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ROR(df, n, value=CLOSE):
    """Rate of Return
    
    A rate of return (RoR) is the net gain or loss on an investment 
    over a specified time period, expressed as a percentage of the 
    investment’s initial cost. We have used the log-adjusted return.

    Calculation
        ROR = ln(P1/P0)

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing specified column; defaults to Close

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        ROR_{n}
    """
    column_name = 'ROR_{}'.format(n) if value == CLOSE else 'ROR_{}_{}'.format(value, n)
    # R =  (df[value] / df[value].shift(n))
    R = (df[value].shift(n) / df[value]) if n < 0 else (df[value] / df[value].shift(n))
    R = pd.Series(
        np.log(R), 
        name=column_name)
    df = df.join(R, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def AROR(df, n, value=CLOSE):
    """Average Rate of Return
    
    A rate of return (RoR) is the net gain or loss on an investment over 
    a specified time period, expressed as a percentage of the 
    investment’s initial cost. We have used the log-adjusted return.

    Calculation
        ROR = ln(P1/P0) / n

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing specified column; defaults to Close

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        AROR_{n} or AROR_{value}_{n}"
    """
    column_name = 'AROR_{}'.format(n) if value == CLOSE else 'AROR_{}_{}'.format(value, n)
    # R = (df[value] / df[value].shift(n))
    R = (df[value].shift(n) / df[value]) if n < 0 else (df[value] / df[value].shift(n))
    AR = pd.Series(np.log(R) / n, name=column_name)
    df = df.join(AR, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ATR(df, n=10):  
    """Average True Range (ATR)

    The Average True Range (ATR) is a technical analysis indicator that 
    measures market volatility by decomposing the entire range of an 
    asset price for that period.

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close prices

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        ATR_{n}
    """
    i = 0
    TR_l = [0]
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        TR = max(df.at[i + 1, HIGH], df.at[i, CLOSE]) - min(df.at[i + 1, LOW], df.at[i, CLOSE])
        TR_l.append(TR)  
        i = i + 1  
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(
        TR_s.ewm(span=n, min_periods = n).mean(),
        name='ATR_{}'.format(n))
    df = df.join(ATR, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def BBANDS(df, n=20):
    """Bollinger Bands

    Calculates Bollinger Bands over a trailing n-periods. Outputs 
    Bollinger Bands on an absolute and percentage basis. A Bollinger 
    Band is a technical analysis tool defined by a set of lines plotted 
    two standard deviations (positively and negatively) away from a 
    simple moving average (SMA) of the security's price, but can be 
    adjusted to user preferences.

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        BollingerB_{n}
        Bollinger_pct_b_{n}

    Formula
        BOLU=MA(TP,n)+m∗σ[TP,n]
        BOLD=MA(TP,n)−m∗σ[TP,n]

            where:
                BOLU=Upper Bollinger Band
                BOLD=Lower Bollinger Band
                MA=Moving average
                TP (typical price)=(High+Low+Close)÷3
                n=Number of days in smoothing period (typically 20)
                m=Number of standard deviations (typically 2)
                σ[TP,n]=Standard Deviation over last n periods of TP
    """
    MA = df[CLOSE].rolling(window=n,center=False).mean()
    MSD = df[CLOSE].rolling(window=n,center=False).std()
    b1 = 4 * MSD / MA  
    B1 = pd.Series(b1, name = 'BollingerB_' + str(n))  
    df = df.join(B1, rsuffix='_drop')
    b2 = (df[CLOSE] - MA + 2 * MSD) / (4 * MSD)  
    B2 = pd.Series(b2, name = 'Bollinger%b_' + str(n))  
    df = df.join(B2, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def PPSR(df):  
    """Pivot Points, Supports and Resistances
    """
    PP = pd.Series((df[HIGH] + df[LOW] + df[CLOSE]) / 3)  
    R1 = pd.Series(2 * PP - df[LOW])  
    S1 = pd.Series(2 * PP - df[HIGH])  
    R2 = pd.Series(PP + df[HIGH] - df[LOW])  
    S2 = pd.Series(PP - df[HIGH] + df[LOW])  
    R3 = pd.Series(df[HIGH] + 2 * (PP - df[LOW]))  
    S3 = pd.Series(df[LOW] - 2 * (df[HIGH] - PP))  
    psr = {'PP':PP, 'R1':R1, 'S1':S1, 'R2':R2, 'S2':S2, 'R3':R3, 'S3':S3}  
    PSR = pd.DataFrame(psr)  
    df = df.join(PSR, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def STOK(df):
    """Stochastic Oscillator of Close price

    A stochastic oscillator is a momentum indicator comparing a 
    particular closing price of a security to a range of its prices over 
    a certain period of time. It is used to generate overbought and 
    oversold trading signals, utilizing a 0-100 bounded range of values.
    """
    SOk = pd.Series((df[CLOSE] - df[LOW]) / (df[HIGH] - df[LOW]), 
        name='SO_pct_k')
    df = df.join(SOk, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def STO_EMA(df,  nK, nD, nS=1):
    """Stochastic Oscillator, with EMA smoothing

    A stochastic oscillator is a momentum indicator comparing a 
    particular closing price of a security to a range of its prices over
    a certain period of time. The sensitivity of the oscillator to 
    market movements is reducible by adjusting that time period or by 
    taking a moving average of the result. It is used to generate 
    overbought and oversold trading signals, utilizing a 0-100 bounded 
    range of values.

    Parameters
    ----------
    n : int
        Lookback window period, n-sessions
    nK : int
        ... 
    nD : int
        ... 
    nS : int
        Slowing (1 if no slowing)

    Returns
    -------
    Pandas dataframe containing columns:
        SO_EMA_nK{nK}_nS{nS}
        SO_EMA_nD{nK}_nS{nS}
    """
    SOk = pd.Series(
        (df[CLOSE] - df[LOW].rolling(nK).min()) / (df[HIGH].rolling(nK).max() - df[LOW].rolling(nK).min()), 
        name = 'SO_EMA_nK{}_nS{}'.format(str(nK), str(nS))
    )
    ## REVIEW: LOOK INTO THIS??
    SOd = pd.Series(
        SOk.ewm(ignore_na=False, span=nD, min_periods=nD-1, adjust=True).mean(), 
        name = 'SO_EMA_nD{}_nS{}'.format(str(nD), str(nS)))  
    SOk = SOk.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    SOd = SOd.ewm(ignore_na=False, span=nS, min_periods=nS-1, adjust=True).mean()  
    df = df.join(SOk, rsuffix='_drop')
    df = df.join(SOd, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df  


def STO_SMA(df, nK, nD,  nS=1):
    """Stochastic Oscillator, with SMA smoothing

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing Low, High and Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        SO_pct_k{nK}
        SO_SMA_pct_d{nD}"
    """
    SOk = pd.Series(
        (df[CLOSE] - df[LOW].rolling(nK).min()) /
        (df[HIGH].rolling(nK).max() - df[LOW].rolling(nK).min()), 
        name = 'SO_pct_k_{}'.format(nK))
    SOd = pd.Series(
        SOk.rolling(window=nD, center=False).mean(), 
        name = 'SO_SMA_{}'.format(nD))
    SOk = SOk.rolling(window=nS, center=False).mean()
    SOd = SOd.rolling(window=nS, center=False).mean()
    df = df.join(SOk, rsuffix='_drop')
    df = df.join(SOd, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def TRIX(df, n):
    """Triple Exponential Average (TRIX)

    The Triple Exponential Average (TRIX) is a momentum indicator used 
    by technical traders that shows the percentage change in a triple 
    exponentially smoothed moving average. When it is applied to triple 
    smoothing of moving averages, it is designed to filter out price 
    movements that are considered insignificant or unimportant. TRIX is 
    also implemented by technical traders to produce signals that are 
    similar in nature to the Moving Average Convergence Divergence (MACD).

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        TRIX_{n}
    """
    EX1 = df[CLOSE].ewm(span = n, min_periods = n-1).mean()
    EX2 = EX1.ewm(span = n, min_periods = n - 1).mean()
    EX3 = EX2.ewm(span = n, min_periods = n - 1).mean()
    i = 0
    ROC_l = [0]
    while i + 1 <= df.index[-1]:
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i]
        ROC_l.append(ROC)
        i = i + 1
    Trix = pd.Series(ROC_l, name = 'Trix_' + str(n))
    df = df.join(Trix, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ADX(df, n=14, n_ADX=14):
    """Average Directional Movement Index (ADX)

    The Plus Directional Indicator (+DI) and Minus Directional Indicator
    (-DI) are derived from smoothed averages of these differences and
    measure trend direction over time. These two indicators are often
    collectively referred to as the Directional Movement Indicator (DMI).

    The Average Directional Index (ADX) is in turn derived from the
    smoothed averages of the difference between +DI and -DI; it measures
    the strength of the trend (regardless of direction) over time. Using
    these three indicators together, chartists can determine both the
    direction and strength of the trend.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing Close price and other required columns

    n : int
        Lookback window period for +DI, -DI and Avg True Range (ATR), 
        n-sessions; dafeault = 14

    n_ADX : int
        Lookback window period for ADX, n-sessions; dafeault = 14

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        ADX_{n}_{n_ADX}
    """
    i = 0
    UpI = []
    DoI = []
    while i + 1 <= df.index[-1]:
        UpMove = df.at[i + 1, HIGH] - df.at[i, HIGH]
        DoMove = df.at[i, LOW] - df.at[i + 1, LOW]
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else: UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else: DoD = 0
        DoI.append(DoD)
        i = i + 1
    i = 0
    TR_l = [0]
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        TR = max(df.at[i + 1, HIGH], df.at[i, CLOSE]) - min(df.at[i + 1, LOW], df.at[i, CLOSE])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(
        span=n, min_periods = n - 1).mean())
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(
        span=n, min_periods=n - 1).mean() / ATR)
    NegDI = pd.Series(DoI.ewm(
        span=n, min_periods=n - 1).mean() / ATR)
    ADX = pd.Series(
        (abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(
            span=n_ADX, min_periods=n_ADX - 1).mean(),
        name='ADX_{}_{}'.format(str(n), str(n_ADX)))
    df = df.join(ADX, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def MACD(df, n_fast, n_slow):
    """Moving Average Convergence Divergence (MACD)
    
    Calculates MACD, MACD Signal and MACD difference. Moving Average 
    Convergence Divergence (MACD) is a trend-following momentum 
    indicator that shows the relationship between two moving averages of 
    a security’s price. The MACD is calculated by subtracting the 
    26-period Exponential Moving Average (EMA) from the 12-period EMA.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing Close price

    n_fast : int
        Lookback window period for fast oscillator

    n_slow : int
        Lookback window period for slow oscillator

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        MACD_{n}
        MACDsign_{n}
        MACDdiff_{n}
    """
    EMAfast = df[CLOSE].ewm(
        span = n_fast, min_periods = n_slow - 1).mean()
    EMAslow = df[CLOSE].ewm(
        span = n_slow, min_periods = n_slow - 1).mean()
    MACD = pd.Series(EMAfast - EMAslow, 
        name = 'MACD_{}_{}'.format(n_fast, n_slow))
    MACDsign = pd.Series(df[CLOSE].ewm(span = 9, min_periods = 8).mean(),
        name = 'MACDsign_{}_{}'.format(n_fast, n_slow))
    MACDdiff = pd.Series(MACD - MACDsign, 
        name = 'MACDdiff_{}_{}'.format(n_fast, n_slow))
    df = df.join(MACD, rsuffix='_drop')
    df = df.join(MACDsign, rsuffix='_drop')
    df = df.join(MACDdiff, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def MassI(df, n=9, w=25):
    """Mass Index

    WARNING: Confirm this is accurately calculated.

    Mass index is a form of technical analysis that examines the range 
    between high and low stock prices over a period of time. By 
    analyzing the narrowing and widening of trading ranges, mass index 
    identifies potential reversals based on market patterns. However, 
    since the patterns do not provide insight into the direction of the 
    reversals, technical analysts should combine the indicator’s 
    readings with directional indicators.

    Calculation
        1. Calculate the nine-day exponential moving average (EMA) of 
           the range between the high and low prices for a period of 
           time – typically 25 days.
        
        2. Divide this figure by the nine-day exponential moving average 
           of the moving average in the numerator

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing High and Low price

    n : int
        Lookback window period for High/Low range EMA; default = 9

    w : int
        Lookback window period for Mass Index; default = 25

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        Mass_Index_{n}_{w}
    """
    Range = df[HIGH] - df[LOW]
    EX1 = Range.ewm(span = n, min_periods=n-1).mean()
    EX2 = EX1.ewm(span = n, min_periods=n-1).mean()
    Mass = EX1 / EX2  
    MassI = pd.Series(
        Mass.rolling(w).sum(), 
        name = 'Mass_Index_{}_{}'.format(n, w)
    )
    df = df.join(MassI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def Vortex(df, n):
    """Vortex Indicator
    
    Vortex Indicator (VI) is an indicator composed of two lines - an 
    uptrend line (VI+) and a downtrend line (VI-). These lines are 
    typically colored green and red respectively. A vortex indicator is 
    used to spot trend reversals and confirm current trends.

    Calculation: 
    The calculation for the indicator is divided into four parts.

    1. True range (TR) is the greatest of:
        - Current high minus current low
        - Current high minus previous close
        - Current low minus previous close

    2. Uptrend and downtrend movement:
        VM+ = Absolute value of current high minus prior low
        VM- = Absolute value of current low minus prior high

    3. Parameter length (n)
        - Decide on a parameter length (between 14 and 30 days is common)
        - Sum the last n period’s true range, VM+ and VM-:
        - Sum of the last n periods’ true range = SUM TRn
        - Sum of the last n periods’ VM+ = SUM VMn+
        - Sum of the last n periods’ VM- = SUM VMn−

    4. Create the trendlines VI+ and VI-
        - SUM VMn+/SUM TRn = VIn+
        - SUM VMn-/SUM TRn = VIn−

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n : int
        Lookback window period

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        Vortex_{n}
    """
    i = 0
    TR = [0]
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        Range = max(df.at[i + 1, HIGH], df.at[i, CLOSE]) - min(df.at[i + 1, LOW], df.at[i, CLOSE])
        TR.append(Range)
        i = i + 1
    i = 0
    VM = [0]
    while i < index_len:
        Range = abs(df.at[i + 1, HIGH] - df.at[i, LOW]) - abs(df.at[i + 1, LOW] - df.at[i, HIGH])
        VM.append(Range)
        i = i + 1
    VI = pd.Series(
        pd.Series(VM).rolling(n).sum() / pd.Series(TR).rolling(n).sum(),
        name = 'Vortex_' + str(n))
    df = df.join(VI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def KST(df, r1=10, r2=10, r3=10, r4=15, n1=10, n2=15, n3=20, n4=30):
    """Know Sure Thing, aka Summed Rate of Change (KST)
    
    Know Sure Thing, or KST, is a momentum oscillator to make 
    rate-of-change readings easier for traders to interpret. The
    indicator is relatively common among technical analysts preferring
    momentum oscillators to make decisions. Know Sure Thing is
    calculated by taking the simple moving average (SMA) or four 
    different rate-of-change (ROC) periods, adding them together to 
    come up with the KST, and creating a signal line by taking the 
    9-period SMA of the KST.

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing Close price

    r1..4 : int
        Lookback window period for ROC calculation

    n1..4 : int
        Lookback window period for EMA calculation

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        KST_R1_{r1}n{n1}_R2_{r2}n{n2}_R3_{r3}n{n3}_R4_{r4}n{n4}
    """
    M = df[CLOSE].diff(r1 - 1)
    N = df[CLOSE].shift(r1 - 1)
    ROC1 = M / N
    M = df[CLOSE].diff(r2 - 1)
    N = df[CLOSE].shift(r2 - 1)
    ROC2 = M / N
    M = df[CLOSE].diff(r3 - 1)
    N = df[CLOSE].shift(r3 - 1)
    ROC3 = M / N
    M = df[CLOSE].diff(r4 - 1)
    N = df[CLOSE].shift(r4 - 1)
    ROC4 = M / N
    KST = pd.Series(
        pd.rolling_sum(ROC1, n1) + pd.rolling_sum(ROC2, n2) * 2 +
        pd.rolling_sum(ROC3, n3) * 3 + pd.rolling_sum(ROC4, n4) * 4,
        name = "KST_R1_{}n{}_R2_{}n{}_R3_{}n{}_R4_{}n{}".format(
            r1, n1, r2, n2, r3, n3, r4, n4))
    df = df.join(KST, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def RSI(df, n=14):
    """Relative Strength Index (RSI)

    The Relative Strength Index (RSI) is a momentum indicator that 
    measures the magnitude of recent price changes to evaluate 
    overbought or oversold conditions in the price of a stock or other 
    asset. The RSI is displayed as an oscillator (a line graph that 
    moves between two extremes) and can have a reading from 0 to 100.

    Traditional interpretation and usage of the RSI are that values of 
    70 or above indicate that a security is becoming overbought or 
    overvalued and may be primed for a trend reversal or corrective 
    pullback in price. An RSI reading of 30 or below indicates an 
    oversold or undervalued condition.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n : int
        Lookback window period, n-sessions; default = 14

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        RSI_{n}
    """
    i = 0
    UpI = [0]
    DoI = [0]

    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        UpMove = df.at[i + 1, HIGH] - df.at[i, HIGH]
        DoMove = df.at[i, LOW] - df.at[i + 1, LOW]
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else: UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else: DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = UpI.ewm(span=n, min_periods = n - 1).mean()
    NegDI = DoI.ewm(span=n, min_periods = n - 1).mean()
    RSI = pd.Series(PosDI / (PosDI + NegDI), name='RSI_{}'.format(n))
    df = df.join(RSI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def TSI(df, r, s):
    """True Strength Index

    The True Strength Index is a technical momentum oscillator. The 
    indicator may be useful for determining overbought and oversold 
    conditions, indicating potential trend direction changes via 
    centerline or signal line crossovers, and warning of trend weakness 
    through divergence.

    Key Takeaways:

        - The TSI fluctuates between positive and negative territory. 
        Positive territory means the bulls are more in control of the 
        asset. Negative territory means the bears are more in control.

        - When the indicator divergences with price, that may signal 
        the price trend is weakening and may reverse.

        - A signal line can be applied to the TSI indicator. When the 
        TSI crosses above the signal line it can be used as a buy signal, 
        and when it crosses below, a sell signal. Such crossovers occur 
        frequently so use with caution.

        - Overbought and oversold levels will vary by the asset being 
        traded.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing Close price

    r : int
        Lookback window period, n-sessions

    n : int
        Lookback window period, n-sessions

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        TSI_{r}_{n}"
    """
    M = pd.Series(df[CLOSE].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(M.ewm(
        span = r, min_periods = r - 1).mean())
    aEMA1 = pd.Series(aM.ewm(
        aM, span = r, min_periods = r - 1).mean())
    EMA2 = pd.Series(EMA1.ewm(
        span = s, min_periods = s - 1).mean())
    aEMA2 = pd.Series(aEMA1.ewm(
        aEMA1, span = s, min_periods = s - 1).mean())
    TSI = pd.Series(EMA2 / aEMA2, name = 'TSI_{}_{}'.format(r, s))
    df = df.join(TSI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ACCDIST(df, n):  
    """Accumulation/Distribution

    Accumulation/distribution is a cumulative indicator that uses 
    volume and price to assess whether a stock is being accumulated 
    or distributed. The measure seeks to identify divergences between 
    the stock price and volume flow. This provides insight into how 
    strong a trend is. If the price is rising but the indicator is 
    falling this indicates that buying or accumulation volume may not 
    be enough to support the price rise and a price decline could be 
    forthcoming.

    Key Takeaways:

        - The accumulation/distribution line gauges supply and demand 
        by looking at where the price closed within the period's range, 
        and then multiplying that by volume.

        - The A/D indicator is cumulative, meaning one period's value 
        is added or subtracted from the last.

        - A rising A/D line helps confirm a rising price trend.

        - A falling A/D line helps confirm a price downtrend.

        - If the price is rising but A/D is falling, it signals 
        underlying weakness and a potential decline in price.

        - If the price of an asset is falling but A/D is rising, it 
        signals underlying strength and the price may start to rise.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        Acc_Dist_ROC_{n}
    """
    ad = (2 * df[CLOSE] - df[HIGH] - df[LOW]) / (df[HIGH] - df[LOW]) * df[VOLUME]  
    M = ad.diff(n - 1)  
    N = ad.shift(n - 1)  
    ROC = M / N  
    AD = pd.Series(ROC, name='Acc_Dist_ROC_{}'.format(str(n)))
    df = df.join(AD, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def Chaikin(df, n_fast=3, n_slow=10):
    """Chaikin Oscillator

    The Chaikin oscillator measures the accumulation-distribution line 
    of moving average convergence-divergence (MACD). To calculate the 
    Chaikin oscillator, subtract a 10-day exponential moving average 
    (EMA) of the accumulation-distribution line from a 3-day EMA of the 
    accumulation-distribution line. This measures momentum predicted by 
    oscillations around the accumulation-distribution line.

    Takeaways
        - The Chaikin Indicator applies MACD to the 
        accumulation-distribution line rather than closing price.
        
        - A cross above the accumulation-distribution line indicates 
        that market players are accumulating shares, securities or 
        contracts, which is typically bullish.

    Parameters
    -----------------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n_fast : int
        Lookback window period for the fast EMA; default = 3

    n_slow : int
        Lookback window period for the fast EMA; default = 10

    Returns
    -------------
    Pandas dataframe containing all input columns and column(s):
        Chaikin_{n_fast}_{n_slow}"

    """
    ad = (2 * df[CLOSE] - df[HIGH] - df[LOW]) / (df[HIGH] - df[LOW]) * df[VOLUME]
    Chaikin = pd.Series(
        (ad.ewm(span=n_fast, min_periods=2)) - (ad.ewm(span=n_slow, min_periods=9)),
        name = 'Chaikin_{}_{}'.format(n_fast, n_slow)
    )
    df = df.join(Chaikin, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def MFI(df, n=14):
    """Money Flow Index (MFI)

    The Money Flow Index (MFI) is a technical oscillator that uses price
    and volume for identifying overbought or oversold conditions in an 
    asset. It can also be used to spot divergences which warn of a trend 
    change in price. The oscillator moves between 0 and 100. Unlike 
    conventional oscillators such as the Relative Strength Index (RSI), 
    the Money Flow Index incorporates both price and volume data, as 
    opposed to just price. For this reason, some analysts call MFI the 
    volume-weighted RSI.

    Key Takeaways

        - The indicator is typically calculated using 14 periods of data.

        - An MFI reading above 80 is considered overbought and an MFI 
        reading below 20 is considered oversold.

        - Overbought and oversold doesn't necessarily mean the price 
        will reverse, only that the price (factoring for volume) is 
        near the high or low of its recent price range.

        - We recommend using 90 and 10 as overbought and oversold levels. 
        These levels are rarely reached, but when they are it often 
        means the price could be due for a direction change.

        - A divergence between the indicator and price is noteworthy. 
        For example, if the indicator is rising while the price is 
        falling or flat, the price could start rising.

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        MFI_{n}
    """
    PP = (df[HIGH] + df[LOW] + df[CLOSE]) / 3
    i = 0
    PosMF = [0]
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        if PP[i + 1] > PP[i]:
            PosMF.append(PP[i + 1] * df.at[i + 1, VOLUME])
        else:
            PosMF.append(0)
        i = i + 1
    PosMF = pd.Series(PosMF)
    TotMF = PP * df[VOLUME]
    MFR = pd.Series(PosMF / TotMF)
    MFI = pd.Series(MFR.rolling(n).mean(), name='MFI_{}'.format(n))
    df = df.join(MFI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def OBV(df, n):  
    """On-balance Volume

    On-balance volume (OBV) is a technical trading momentum indicator 
    that uses volume flow to predict changes in stock price. The 
    creator, Granville, believed that when volume increases sharply 
    without a significant change in the stock's price, the price will 
    eventually jump upward or fall downward.

    Key Takeaways:
        
        - On-balance volume (OBV) is a technical indicator of momentum, 
        using volume changes to make price predictions.
        
        - OBV shows crowd sentiment that can predict a bullish or 
        bearish outcome.
        
        - Comparing relative action between price bars and OBV generates 
        more actionable signals than the green or red volume histograms 
        commonly found at the bottom of price charts. 

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing High, Low and Close price

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        OBV_{n}
    """
    i = 0
    OBV = [0]
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        if df.at[i + 1, CLOSE] - df.at[i, CLOSE] > 0:
            OBV.append(df.at[i + 1, VOLUME])
        if df.at[i + 1, CLOSE] - df.at[i, CLOSE] == 0:
            OBV.append(0)
        if df.at[i + 1, CLOSE] - df.at[i, CLOSE] < 0:
            OBV.append(-df.at[i + 1, VOLUME])
        i = i + 1
    OBV = pd.Series(OBV)
    OBV_ma = pd.Series(OBV.rolling(n).mean(), 
        name = 'OB_Volume_{}'.format(n))
    df = df.join(OBV_ma, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def FORCE(df, n=13):
    """Force Index

    "The Force Index is a technical indicator that measures the amount 
    of power used to move the price of an asset. The force index uses 
    price and volume to determine the amount of strength behind a price 
    move. The index is an oscillator, fluctuating between positive and 
    negative territory. It is unbounded meaning the index can go up or 
    down indefinitely. The force index is used for trend and breakout 
    confirmation, as well as spotting potential turning points by 
    looking for divergences.

    Key Takeaways:

        - A rising force index, above zero, helps confirm rising prices.
        
        - A falling force index, below zero, helps confirm falling prices.
        
        - A breakout, or a spike, in the force index, helps confirm a 
        breakout in price.
        
        - If the force index is making lower swing highs while the price 
        is making higher swing highs, this is bearish divergence and 
        warns the price may soon decline.
        
        - If the force index is making higher swing lows while the price 
        is making lower swing lows, this is bullish divergence and warns 
        the price may soon head higher.
        
        - The force index is typically 13 periods but this can be 
        adjusted based on preference. The more periods used the smoother 
        the movements of the index, typically preferred by longer-term 
        traders.

    Calculation:
    ​          
        FI(1) = (CCP − PCP)∗VFI(13) = 13-Period EMA of FI(1)
        where:
            FI = Force index
            CCP = Current close price
            PCP = Prior close price
            VFI = Volume force index
            EMA = Exponential moving average

    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing High, Low, Close and Volume

    n : int
        Lookback window period, n-sessions

    Returns
    -------
    Pandas dataframe containing all input columns and column(s):
        FORCE_{n}

    """
    F = pd.Series(df[CLOSE].diff(n) * df[VOLUME].diff(n), 
        name = 'Force_{}'.format(n))
    df = df.join(F, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def EOM(df, n):
    """Ease of Movement

    Ease of Movement indicator is a technical study that attempts to 
    quantify a mix of momentum and volume information into one value. 
    The intent is to use this value to discern whether prices are able 
    to rise, or fall, with little resistance in the directional 
    movement. Theoretically, if prices move easily, they will continue 
    to do so for a period of time that can be traded effectively.

    Key Takeaways:

        - This indicator calculates how easily a price can move up or down.

        - The calculation subtracts yesterday's average price from 
        today's average price and divides the difference by volume.

        - This generates a volume-weighted momentum indicator.
    """
    EoM = (df[HIGH].diff(1) + df[LOW].diff(1)) * (df[HIGH] - df[LOW]) / (2 * df[VOLUME])  
    Eom_ma = pd.Series(EoM.rolling(n).mean(), name='EoM_' + str(n))
    df = df.join(Eom_ma, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def CCI(df, n):  
    """Commodity Channel Index

    The Commodity Channel Index​ (CCI) is a momentum-based oscillator 
    used to help determine when an investment vehicle is reaching a 
    condition of being overbought or oversold. It is also used to assess 
    price trend direction and strength. This information allows traders 
    to determine if they want to enter or exit a trade, refrain from 
    taking a trade, or add to an existing position. In this way, the 
    indicator can be used to provide trade signals when it acts in a 
    certain way.

    Key Takeaways:

        - The CCI measures the difference between the current price and 
        the historical average price.

        - When the CCI is above zero it indicates the price is above 
        the historic average. When CCI is below zero, the price is 
        below the hsitoric average.

        - High readings of 100 or above, for example, indicate the price 
        is well above the historic average and the trend has been strong 
        to the upside.

        - Low readings below -100, for example, indicate the price is 
        well below the historic average and the trend has been strong to 
        the downside.

        - Going from negative or near-zero readings to +100 can be used 
        as a signal to watch for an emerging uptrend.

        - Going from positive or near-zero readings to -100 may indicate 
        an emerging downtrend.

        - CCI is an unbounded indicator meaning it can go higher or 
        lower indefinitely. For this reason, overbought and oversold 
        levels are typically determined for each individual asset by 
        looking at historical extreme CCI levels where the price 
        reversed from.
    """
    PP = (df[HIGH] + df[LOW] + df[CLOSE]) / 3
    CCI = pd.Series(
        (PP - PP.rolling(n).mean() / PP.rolling(n).stddev()), 
        name = 'CCI_{}'.fromat(n))
    df = df.join(CCI, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def COPP(df, n):  
    """Coppock Curve
    
    WARNING: Check accuracy of ROC1 + ROC2

    The Coppock Curve is a long-term price momentum indicator used 
    primarily to recognize major bottoms in the stock market. It is 
    calculated as a 10-month weighted moving average of the sum of the 
    14-month rate of change and the 11-month rate of change for the 
    index; it is also known as the Coppock Guide.
    """
    M = df[CLOSE].diff(int(n * 11 / 10) - 1)  
    N = df[CLOSE].shift(int(n * 11 / 10) - 1)  
    ROC1 = M / N  
    M = df[CLOSE].diff(int(n * 14 / 10) - 1)  
    N = df[CLOSE].shift(int(n * 14 / 10) - 1)  
    ROC2 = M / N
    Copp = pd.Series((ROC1 + ROC2).ewm(span = n, min_periods = n), 
        name = 'Copp_' + str(n))
    df = df.join(Copp, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def KELCH(df, n):
    """Keltner Channel

    A Keltner Channel is a volatility based technical indicator composed 
    of three separate lines. The middle line is an exponential moving 
    average (EMA) of the price. Additional lines are placed above and 
    below the EMA. The upper band is typically set two times the Average 
    True Range (ATR) above the EMA, and lower band is typically set two 
    times the ATR below the EMA. The bands expand and contract as 
    volatility (measured by ATR) expands and contracts.

    Since most price action will be encompassed within the upper and 
    lower bands (the channel), moves outside the channel can signal 
    trend changes or an acceleration of the trend. The direction of the 
    channel, such as up, down, or sideways, can also aid in identifying 
    the trend direction of the asset.

    Key Takeaways:
        
        - The EMA of a Keltner Channel is typically 20 periods, although 
        this can be adjusted if desired.
        
        - The upper and lower bands are typically set two times the ATR 
        above and below the EMA, although the multiplier can also be 
        adjusted based on personal preference. A larger multiplier will 
        result in a wider channel.
        
        - Price reaching the upper band is bullish, while reaching the 
        lower band is bearish. Reaching a band may indicate a continued 
        trend in that direction.
        
        - The angle of the channel also aids in identifying the trend 
        direction. When the channel is angled upwards, the price is 
        rising. When the channel is angled downward the price is 
        falling. If the channel is moving sideways, the price has been 
        as well.
        
        - The price may also oscillate between the upper and lower bands. 
        When this happens, the upper band is viewed as resistance and 
        the lower band is support.

    Formula:

    Keltner Channel Middle Line=EMA
    Keltner Channel Upper Band=EMA+2∗ATR
    Keltner Channel Lower Band=EMA−2∗ATR
        where:
        EMA=Exponential moving average (typically over 20 periods)
        ATR=Average True Range (typically over 10 or 20 periods)
    """
    KelChM = pd.Series(
        ((df[HIGH] + df[LOW] + df[CLOSE]) / 3).rolling(n).mean(), 
        name = 'KelChM_' + str(n))  
    KelChU = pd.Series(
        ((4 * df[HIGH] - 2 * df[LOW] + df[CLOSE]) / 3).rolling(n).mean(), 
        name = 'KelChU_' + str(n))  
    KelChD = pd.Series(
        ((-2 * df[HIGH] + 4 * df[LOW] + df[CLOSE]) / 3).rolling(n).mean(), 
        name = 'KelChD_' + str(n))  
    df = df.join(KelChM, rsuffix='_drop')
    df = df.join(KelChU, rsuffix='_drop')
    df = df.join(KelChD, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def ULTOSC(df, n1=7, n2=14, n3=28):
    """Ultimate Oscillator

    The Ultimate Oscillator is a technical indicator that measures the 
    price momentum of an asset across multiple timeframes. By using the 
    weighted average of three different timeframes the indicator has 
    less volatility and fewer trade signals compared to other 
    oscillators that rely on a single timeframe. Buy and sell signals 
    are generated following divergences. The Ultimately Oscillator 
    generates fewer divergence signals than other oscillators due to its 
    multi-timeframe construction.

    Key Takeaways:
        
        - The indicator uses three timeframes in its calculation: 
        7, 14, and 28 periods.
        
        - The shorter timeframe has the most weight in the calculation, 
        while the longer timeframe has the least weight.
        
        - Buy signals occur when there is bullish divergence, the 
        divergence low is below 30 on the indicator, and the oscillator 
        then rises above the divergence high.
        
        - A sell signal occurs when there is bearish divergence, the 
        divergence high is above 70, and the oscillator then falls below 
        the divergence low.
    """
    i = 0  
    TR_l = [0]  
    BP_l = [0]  
    index_len = (len(df) - 1)
    while i + 1 <= index_len:
        TR = max(df.at[i + 1, HIGH], df.at[i, CLOSE]) - min(df.at[i + 1, LOW], df.at[i, CLOSE])
        TR_l.append(TR)
        BP = df.at[i + 1, CLOSE] - min(df.at[i + 1, LOW], df.at[i, CLOSE])
        BP_l.append(BP)
        i = i + 1
    UltO = pd.Series(
        ( 4 * pd.Series(BP_l).rolling(n1).sum() / pd.Series(TR_l).rolling(n1).sum() ) + \
        ( 2 * pd.Series(BP_l).rolling(n2).sum() / pd.Series(TR_l).rolling(n2).sum() ) + \
        ( pd.Series(BP_l).rolling(n3).sum() / pd.Series(TR_l).rolling(n3).sum() ),
        name = 'Ultimate_Osc_{}_{}_{}'.format(n1, n2, n3) )
    df = df.join(UltO, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df


def DONCH(df, n):
    """Donchian Channel

    Donchian Channels are three lines generated by moving average 
    calculations that comprise an indicator formed by upper and lower 
    bands around a mid-range or median band. The upper band marks the 
    highest price of a security over N periods while the lower band 
    marks the lowest price of a security over N periods. The area 
    between the upper and lower bands represents the Donchian Channel.

    Key Takeaways:

        - The indicator seeks to identify bullish and bearish extremes 
        that favor reversals as well as breakouts, breakdowns and 
        emerging trends, higher and lower.

        - The middle band simply computes the average between the 
        highest high over N periods and lowest low over N periods, 
        identifying a median or mean reversion price.

    Formula:

        UC = Highest High in Last N Periods
        Middle Channel=((UC−LC)/2)
        LC = Lowest Low in Last N periods

            where:
                UC=Upper channel
                N= number of minutes, hours, days, weeks, months
                Period=Minutes, hours, days, weeks, months
                LC=Lower channel
    """
    i = 0
    DC_l = []
    while i < n - 1:
        DC_l.append(0)
        i = i + 1
    i = 0
    while i + n - 1 < df.index[-1]:
        DC = max(df[HIGH].ix[i:i + n - 1]) - min(df[LOW].ix[i:i + n - 1])
        DC_l.append(DC)
        i = i + 1
    DonCh = pd.Series(DC_l, name = 'Donchian_' + str(n))
    DonCh = DonCh.shift(n - 1)
    df = df.join(DonCh, rsuffix='_drop')
    column_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[column_list]
    return df
