"""
Functions that can be used for feature engineering. Specifically, these have been
applied to price indicators from the python library, talib. 

RELATIVE DATE FUNCTIONS
    The following workflows calculate ratios by one or two input variables, over specified
    points in time. The shift arguments look n-periods back when their values are positive. 
        RATIO
        RATIO_ROR
        RATIO_ROC

WINDOW FUNCTIONS
    The following workflows provide calculations over time. The time window is specified
    with the argument, n.
        STDEV
        MAX
        MIN
        MEDIAN
        CORR
        KURT
        SKEW
        RANK
        PCT_RANK

DOCUMENTATION
    https://pandas.pydata.org/pandas-docs/version/0.17.0/api.html#standard-moving-window-functions

Functions to add
    ewma(arg[, com, span, halflife, ...])   Exponentially-weighted moving average
    ewmstd(arg[, com, span, halflife, ...]) Exponentially-weighted moving std
    ewmcorr(arg1[, arg2, com, span, halflife, ...]) Exponentially-weighted moving correlation
"""

# LIBRARIES
from numpy import log
import pandas as pd
import datetime as dt
import scipy.stats

# PARAMETERS
# default names of the dataframe fields
CLOSE = 'close'
HIGH = 'high'
LOW = 'low'
VOLUME = 'volume'
DATE = 'ticker_time'


# FUNCTIONS

def _normalize_headers(df):
    def _normalize_field(field):
        field = field.replace('-', 'n')
        field = field.replace('%', '_pct_')
        field = field.replace(' ', '_')
        return field
    new_headers = [_normalize_field(h) for h in list(df)]        
    df.columns = new_headers
    return df


def _get_ratio_suffix(numerator, denominator, numerator_shift=0, denominator_shift=0):
    """
    Set the suffix of ratio name, eg RATIO_Close_1_Close_3.
    If shift = 0 then it is omitted, eg RATIO_Open_Close.
    
    Returns:
        string  : string of the field name
    """
    if numerator_shift:
        numerator_abv = '{}_{}'.format(numerator, numerator_shift)
    else:
        numerator_abv = numerator
    if denominator_shift:
        denominator_abv = '{}_{}'.format(denominator, denominator_shift)
    else:
        denominator_abv = denominator
    ratio_name = '_{}_{}'.format(numerator_abv, denominator_abv)
    return ratio_name


def get_date_variables(df, date_column=DATE):
    """Get feature transformations based on date:
    - week
    - month
    - quarter
    - year
    - day_of_week
    - day_of_year
    
    Parameters
    ----------
    df : Pandas Dataframe
        Input dataframe containing date variable.
        
    date_column : str
        Date variable; must be a datetime format.

    """
    df['week'] = df[date_column].dt.week
    df['month'] = df[date_column].dt.month
    df['quarter'] = df[date_column].dt.quarter
    df['year'] = df[date_column].dt.year
    df['day_of_week'] = df[date_column].dt.dayofweek
    df['day_of_year'] = df[date_column].dt.dayofyear
    df['hour_of_day'] = df[date_column].dt.hour
    return df


def onehot_encoding(df, column):
    """Add one-hot coding for a single columm within a dataframe.

    Returns:
        Dataframe
    """
    def convert_dtype(d):
        import datetime as dt
        if isinstance(d, dt.datetime):
            o = d.strftime('%Y%m%d')
        elif isinstance(d, int):
            o = column + '_' + str(d)
        return o
    df_in = pd.DataFrame()
    #df_in[column] = [convert_dtype(d) for d in df[column]]
    df_in = [convert_dtype(d) for d in df[column]]
    s = pd.get_dummies(df_in)
    df = df.join(s, rsuffix = '_drop')
    df = _normalize_headers(df)
    return df


def LAG(df, value, n):
    """
    Get the lag of a value over a time period. Positive shift is n-periods in the past. 
    shift = 0 is the current time period.

    Args:
            df: Dataframe
            value: string
                Value to pull shift
            shift: integer
                Lookback window for value
    Returns:
            df: Dataframe
                Returns input dataframe with Rate of Return
    """
    LAG = pd.Series(
        df[value].shift(n),
        name = 'LAG{}_{}'.format(str(n), value)
    )
    df = df.join(LAG, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def DIFF(df, value1, value2, value1_shift=0, value2_shift=0):
    """
    Get the difference of two values over a time period.
        DIFF = value1 - value2
    Positive shift is n-periods in the past. shift = 0 is the current time period.

    Args:
            df : Dataframe
            value1 : string, numerator for ROR
            value2 : string, denominator for ROR
            value1_shift : integer, lookback window for numerator
            value2_shift : integer, lookback window for denominator
    Returns:
            df : Dataframe : returns input dataframe with Rate of Return
    """
    DIFF = pd.Series(
        df[value1].shift(value1_shift) - df[value2].shift(value2_shift), 
        name = 'DIFF{}'.format(
            _get_ratio_suffix(value1, value2, value1_shift, value2_shift)))  
    df = df.join(DIFF, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def RATIO(df, numerator, denominator, numerator_shift=0, denominator_shift=0):
    """
    Get the ratio of a given numerator and denominator over a time period.
        RATIO = numerator[ns] / denominator[ds]
    Positive shift is n-periods in the past. shift = 0 is the current time period.

    Args:
            df : Dataframe
            numerator : string : numerator for ROR
            denominator : string : denominator for ROR
            numerator_shift : integer : lookback window for numerator
            denominator_shift : integer : lookback window for denominator
    Returns:
            df : Dataframe : returns input dataframe with Rate of Return
    """
    RATIO = pd.Series(
        df[numerator].shift(numerator_shift) / df[denominator].shift(denominator_shift), 
        name = 'RATIO{}'.format(
            _get_ratio_suffix(numerator, denominator, numerator_shift, denominator_shift)))  
    df = df.join(RATIO, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def RATIO_LOG(df, numerator, denominator, numerator_shift=0, denominator_shift=0):
    """
    Get the log Rate of Return of a given numerator and denominator over a time period.
        ROR = log(numerator[ns] / denominator[ds])
    Positive shift is n-periods in the past. shift = 0 is the current time period.

    Args:
            df : Dataframe
            numerator : string : numerator for ROR
            denominator : string : denominator for ROR
            numerator_shift : integer : lookback window for numerator
            denominator_shift : integer : lookback window for denominator
    Returns:
            df : Dataframe : returns input dataframe with Rate of Return
    """
    RATIO = pd.Series( 
        log(df[numerator].shift(numerator_shift) / df[denominator].shift(denominator_shift)), 
        name = 'RATIO_LOG{}'.format(
            _get_ratio_suffix(numerator, denominator, numerator_shift, denominator_shift)))  
    df = df.join(RATIO, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df

  
def RATIO_ROC(df, numerator, denominator, numerator_shift=0, denominator_shift=0):
    """
    Get the percent Rate of Change of a given numerator and denominator over a 
    given time period. Positive shift is n-periods in the past. shift = 0 is 
    the current time period.

    Args:
            df : Dataframe
            numerator : string : numerator for ROR
            denominator : string : denominator for ROR
            numerator_shift : integer : lookback window for numerator
            denominator_shift : integer : lookback window for denominator
    Returns:
            df : Dataframe : returns input dataframe with Rate of Change (ie % change)
    """
    RATIO = pd.Series( 
        (df[numerator].shift(numerator_shift) / df[denominator].shift(denominator_shift)) -1, 
        name = 'ROC{}'.format(
            _get_ratio_suffix(numerator, denominator, numerator_shift, denominator_shift))) 
    df = df.join(RATIO, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def SM_STDDEV(df, n, value=CLOSE):
    """
    Calculates rolling Standard Deviation of a feature over n-periods. 
    Defaults to Close price.
    """
    prefix = 'STD_' if value==CLOSE else 'STD_{}_'.format(value)
    SDEV = pd.Series(df[value].rolling(n, n).std(), name = prefix + str(n))
    df = df.join(SDEV, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def SM_MAX(df, n, value=CLOSE):
    """
    Calculates the rolling Maxiumum value over a given time period.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.Rolling.max.html
    """
    prefix = 'MAX_' if value==CLOSE else 'SM_MAX_{}_'.format(value)
    MAX = pd.Series(df[value].rolling(n, n).max(), name = prefix + str(n))
    df = df.join(MAX, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df  


def SM_MIN(df, n, value=CLOSE):
    """
    Calculates the Maxiumum value over a given time period.
    """
    prefix = 'MIN_' if value==CLOSE else 'SM_MIN_{}_'.format(value)
    MIN = pd.Series(df[value].rolling(n, n).min(), name = prefix + str(n))
    df = df.join(MIN, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df  


def SMA(df, n, value=CLOSE):
    """
    Calculates the Maxiumum value over a given time period.
    """
    prefix = 'SMA_' if value==CLOSE else 'SMA_{}_'.format(value)
    AVG = pd.Series(df[value].rolling(n, n).median(), name = prefix + str(n))
    df = df.join(AVG, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def SM_MEDIAN(df, n, value=CLOSE):
    """
    Calculates the Maxiumum value over a given time period.
    """
    prefix = 'MEDIAN_' if value==CLOSE else 'SM_MEDIAN_{}_'.format(value)
    MEDIAN = pd.Series(df[value].rolling(n, n).median(), name = prefix + str(n))
    df = df.join(MEDIAN, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def SM_CORR(df, n, value1, value2):
    """
    Calculates the Rolling Pairwise Correlation over a given time period.
    """
    CORR = pd.Series(
        df[value1].rolling(n, n).median(df[value2]), 
        name = 'SM_CORR_{}_{}_{}'.format(n, value1, value2)
    )
    df = df.join(CORR, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df


def SM_KURT(df, n, value=CLOSE):
    """
    Calculates the Rolling Pairwise Correlation over a given time period.
    """
    KURT = pd.Series(df[value].rolling(n, n).kurt(), name = 'SM_KURT_{}'.format(value))
    df = df.join(KURT, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df  


def SM_SKEW(df, n, value=CLOSE):
    """
    Calculates the Rolling Pairwise Correlation over a given time period.
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.Rolling.skew.html
    """
    SKEW = pd.Series(df[value].rolling(n, n).skew(), name = 'SM_SKEW_{}'.format(value))
    df = df.join(SKEW, rsuffix = '_drop')
    col_list = [h for h in list(df) if h.find('_drop') < 0]
    df = df[col_list]
    df = _normalize_headers(df)
    return df  


def RANK(df, n, value=CLOSE):
    """
    Calculates the Rolling Rank over a given time period. 
    Defaults to Close price.
    """
    def rank(array):
        s = pd.Series(array)
        return s.rank(ascending=False)[len(s)-1]
    name = 'RANK_{}'.format(value)
    df[name] = df[value].rolling(n).apply(rank)
    df = _normalize_headers(df)
    return df  


def PCT_RANK(df, n, value=CLOSE):
    """
    Calculates the Rolling Percent Rank over a given time period. 
    Defaults to Close price.
    """
    def rank(array):
        s = pd.Series(array)
        return s.rank(ascending=False)[len(s)-1] / len(s)
    name = 'PCT_RANK_{}'.format(value)
    df[name] = df[value].rolling(n).apply(rank)
    df = _normalize_headers(df)
    return df  


# def QUARTILE(df, n, value=CLOSE, quantile=0.01):
#     """
#     Calculates the Maxiumum value over a given time period.
#     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.Rolling.quantile.html
#     """
#     Q = pd.Series(df[value].rolling(n, n).quantile(quantile), name = 'QTILE_' + str(n))
#     df = df.join(Q, rsuffix = '_drop')
#     col_list = [ h for h in list(df) if h.find('_drop') < 0 ]
#     df = df[ col_list ]
#     return df  


# def SLOPE(df, n, x='Date', y=CLOSE):
#     """
#     Calculates the Slope of a given feature. Defaults to Close price.
    
#     Args:
#         df : Dataframe : input pandas dataframe
#         x : string : name of the x-axis field; defaults to the dataframe
#                     index
#         y : string : name of the y-axis field; defaults to Close price.
#     Returns:
#         Dataframe : includes input tables
#     """
#     import pandas as pd
#     X = df.rolling(window=n, min_periods=n, on=x)
#     Y = df.rolling(window=n, min_periods=n, on=y)
#     if x=='Date':
#         field_name = 'SLOPE_{}'.format(y)
#     else:
#         field_name = 'SLOPE_{}_{}'.format(x, y)
#     # slope calculation
#     M = pd.Series(
#         ((X*Y).mean(axis=1) - X.mean()*Y.mean(axis=1)) / ((X**2).mean() - (X.mean())**2),
#         name = field_name)
#     df = df.join(M, rsuffix = '_drop')
#     col_list = [ h for h in list(df) if h.find('_drop') < 0 ]
#     df = df[ col_list ]
#     return df  





    