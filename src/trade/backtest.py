import pandas as pd
import datetime as dt
from importlib import import_module
from inspect import getsource

from algom.utils.data_object import get_hash_id
from algom.utils.data_object import dataObject
from algom import configs


# Default variables
CLOSE = 'close'
DATETIME = 'ticker_time'
TRADE = 'trade'
ACCOUNT = 'account'
RESPONSE = 'trade_response'

# Name of python package with trading business rules
BUSINESS_RULES = 'trade_business_rules'

# Name of output datasets
BACKTEST_DESTINATION_TABLE = configs.BACKTEST_TABLE
BACKTEST_SUMMARY_DESTINATION_TABLE = configs.BACKTEST_SUMMARY_TABLE
BACKTEST_METADATA_DESTINATION_TABLE = configs.BACKTEST_METADATA_TABLE
BACKTEST_OUTPUT_HEADERS = [
    'backtest_execution_id',
    'backtest_executed',
    'model_execution_id',
    DATETIME,
    'ticker',
    'week',
    'month',
    'quarter',
    'year',
    'day_of_week',
    'day_of_year',
    'high',
    'low',
    'open',
    'close',
    'volume',
    RESPONSE,
    'commission',
    'amount',
    'trade',
    ACCOUNT,
    'account_value',
    'quantity',
    'quantity_margin',
    'buy_trades',
    'sell_trades',
    'sell_short_trades',
    'buy_cover_trades',
    'buy_volume',
    'sell_volume',
    'sell_short_volume',
    'buy_cover_volume',
    'account_change'
]



class backtestTrades():
    """Pulls data required for backtestTrades().
    
    This data includes prediction variables (pulled from BQ), 
    as well as ticker prices. We then apply business rules 
    to this input data for backtesting. 
    """
    def __init__(
        self,
        df,
        business_rule_functions=BUSINESS_RULES,
        account_start=10_000,
        start_date=None,
        end_date=None,
        to_bq=False
    ):
        # Set variables
        self.df = df.sort_values(by='ticker_time')
        self.datetime = DATETIME
        self.start_date = start_date or min(df[self.datetime])
        self.end_date = end_date or max(df[self.datetime])
        self.business_rules = import_module(business_rule_functions)
        self.account_start = account_start
        self.to_bq = to_bq

    def run_backtest(self):
        # Run backtest
        self.start_time = dt.datetime.now()
        self._get_backtest_metadata()
        self._apply_trades()
        self._transpose_key_columns(self.df, RESPONSE)
        self._get_backtest_performance()
        self._get_backtest_summary()
        self._print_backtest_summary()
        self._load_backtest_to_bq()
        
    ###########################
    #  BACKTEST DATA PREP
    ###########################
    
    def _get_backtest_features():
        return [h for h in list(self.df) if h not in \
         backtest.BACKTEST_OUTPUT_HEADERS + 
         configs.INDEX_FEATURES + 
         configs.OMIT_FEATURES +
         ['response']]
    
    def _get_backtest_metadata(self):
        print("BACKTEST: Getting backtest metadata")
        # Get backtest ID (without execution time)
        backtest_metadata_dict = dict(
            account_start = self.account_start,
            start_date = self.start_date,
            end_date = self.end_date,
            buy = getsource(self.business_rules.buy),
            sell = getsource(self.business_rules.sell),
            backtest_features = self._get_backtest_features)        
        self.backtest_id = get_hash_id(backtest_metadata_dict)
        
        # Get backtest ID (with execution time)
        backtest_metadata_dict['backtest_executed'] = self.start_time
        self.backtest_execution_id = get_hash_id(backtest_metadata_dict)
        
        # Load backtest metadata to DataFrame
        backtest_metadata_dict['backtest_id'] = self.backtest_id
        backtest_metadata_dict['backtest_execution_id'] = self.backtest_execution_id
        backtest_metadata = pd.DataFrame.from_dict(
            backtest_metadata_dict, orient='index').reset_index()
        backtest_metadata = backtest_metadata.rename(
            {'index': 'parameter', 0: 'value'}, axis=1)
        backtest_metadata['backtest_id'] = self.backtest_id
        backtest_metadata['backtest_execution_id'] = self.backtest_execution_id
        backtest_metadata['backtest_executed'] = self.start_time
        backtest_metadata = backtest_metadata[[
            'backtest_execution_id',
            'backtest_id',
            'backtest_executed',
            'parameter',
            'value']]
        self.backtest_metadata = backtest_metadata

#     def _reset_df_index(self, df):
#         # clean dataset and adjust start/end dates as needed
#         df = df[df[DATE] >= self.start_date]
#         df = df[df[DATE] <= self.end_date]
#         df = df.sort_values(by=DATE)
#         df = df.reset_index().drop(columns='index')
#         return df

    def _apply_trades(self):
        """Run business rules module and receive a dictionary of responses."""
        print('BACKTEST: Applying trade signals based on business rules module.')
        self.df = self.df.sort_values(by=self.datetime)
        self.df['trade_response'] = [
            self.business_rules.sell_short(row) or \
            self.business_rules.buy_cover(row) or \
            self.business_rules.buy(row) or \
            self.business_rules.sell(row)
            for index, row in self.df.iterrows()]
        
    def _transpose_key_columns(self, df, column_name):
        # Given a dictionary within a dataframe column,
        # transpose to to separate columns.
        def _get_key_columns(df, column_name):
            key_list=[]
            for row in df[column_name]:
                if row:
                    key_list = [k for k in row.keys()]
            return key_list    
        cols = _get_key_columns(df, column_name)
        for col in cols:
            df[col] = [(row[col] if row else None) for row in df[column_name]]
        self.df = df


    ###########################
    #  BACKTEST CALCULATIONS
    ###########################
    
    def _get_backtest_performance(self):
        """ BACKTEST PERFORMANCE
        Run backtest performance
        - initialize account values
        - calculate buy/sell transactions
        - calculate buy/sell volume
        - calculate account value
        - load to BigQuery
        """
        print('BACKTEST: Calculating performance metrics based on business rules module.')
        df = self.df.sort_values(by=self.datetime)
        df[ACCOUNT] = self.account_start
        df['quantity'] = 0

        # buy/sell trades: # of times a trade is executed
        df = self._calc_trades(df)
        df = self._calc_volumes(df)
        df = self._calc_account(df)
        df['backtest_execution_id'] = self.backtest_execution_id
        df['backtest_executed'] = self.start_time
        self.df = df   # contains all input and output fields
        self.backtest_output = df[[h for h in BACKTEST_OUTPUT_HEADERS if h in list(df)]]

    def _calc_trades(self, df):
        def _iter_calc_trades(df, var, signal):
            def f(row):
                return 1 if row[TRADE] == signal else 0
            df[var] = [ f(row) for index, row in df.iterrows() ]
            return df
        # Run trade calculations
        df = _iter_calc_trades(df, 'buy_trades', 'BUY')
        df = _iter_calc_trades(df, 'sell_trades', 'SELL')
        df = _iter_calc_trades(df, 'sell_short_trades', 'SELL SHORT')
        df = _iter_calc_trades(df, 'buy_cover_trades', 'BUY COVER')
        return df

    def _calc_volumes(self, df):
        def _iter_calc_volumes(df, var, signal):
            # Calculate volume given a signal            
            def _row_iter_calc_volumes(row, signal):
                # Get amount if trade signal matches
                return row['amount'] if row[TRADE] == signal else 0
            df[var] = [_row_iter_calc_volumes(row, signal) for index, row in df.iterrows()]
            return df

        # Run volume calculations
        df = _iter_calc_volumes(df, var='buy_volume', signal='BUY')
        df = _iter_calc_volumes(df, var='sell_volume', signal='SELL')
        df = _iter_calc_volumes(df, var='sell_short_volume', signal='SELL SHORT')
        df = _iter_calc_volumes(df, var='buy_cover_volume', signal='BUY COVER')
        return df

    def _calc_account(self, df):
        df = df.reset_index().drop(columns='index')
        for r in range(0, len(df)):
            if r==0:
                # Calculate performance metrics for the first row in input data
                # No trades executed on first day
                prior_acct = self.account_start
                prior_qty = 0
                prior_qty_margin = 0
                price = df.loc[r, CLOSE]
                chng_qty = 0
                chng_qty_margin = 0
                chng_acct = 0

            else:
                # Calculate performance metrics for all other rows
                # Get prior day acct value
                prior_acct = df.loc[r-1, ACCOUNT]
                prior_qty = df.loc[r-1, 'quantity']
                prior_qty_margin = df.loc[r-1, 'quantity_margin']
                
                # Get current values
                acct = df.loc[r, ACCOUNT]
                qty = df.loc[r, 'quantity']
                price = df.loc[r, CLOSE]
                trade = df.loc[r, TRADE]
                
                # BUY TRANSACTIONS
                if trade == 'BUY':
                    if prior_acct > 0:
                        chng_qty = df.loc[r, 'buy_volume']
                        chng_qty_margin = 0
                        chng_acct = chng_qty * price * -1
                    else:
                        chng_qty = 0
                        chng_qty_margin = 0
                        chng_acct = 0

                # SELL TRANSACTIONS
                elif trade == 'SELL':
                    if prior_qty >= df.loc[r, 'sell_volume']:
                        chng_qty = df.loc[r, 'sell_volume'] * -1
                        chng_qty_margin = 0
                        chng_acct = df.loc[r, 'sell_volume'] * price
                    elif prior_qty > 0:
                        chng_qty = prior_qty * -1
                        chng_qty_margin = 0
                        chng_acct = prior_qty * price
                    else:
                        chng_qty = 0
                        chng_qty_margin = 0
                        chng_acct = 0

                # SHORT SELL TRANSACTIONS
                elif trade == 'SELL SHORT':
                    if prior_acct >= price * df.loc[r, 'sell_short_volume']:
                        chng_qty = 0
                        chng_qty_margin = df.loc[r, 'sell_short_volume'] * -1
                        chng_acct = df.loc[r, 'sell_short_volume'] * price
                    else:
                        chng_qty = 0
                        chng_qty_margin = 0
                        chng_acct = 0

                # BUY COVER TRANSACTIONS
                elif trade == 'BUY COVER':
                    if prior_qty_margin >= df.loc[r, 'buy_cover_volume']:
                        chng_qty = 0
                        chng_qty_margin = df.loc[r, 'buy_cover_volume']
                        chng_acct = df.loc[r, 'buy_cover_volume'] * price * -1
                    else:
                        chng_qty = 0
                        chng_qty_margin = 0
                        chng_acct = 0

                # NO TRANSACTIONS
                else:
                    chng_qty = 0
                    chng_qty_margin = 0
                    chng_acct = 0

            # Updated share quantity and account cash
            qty = prior_qty + chng_qty
            qty_margin = prior_qty_margin + chng_qty_margin
            acct = prior_acct + chng_acct
            acct_value = acct + (qty * price) + (qty_margin * price)

            # Output values to dataframe
            df.loc[r, 'quantity'] = qty
            df.loc[r, 'quantity_margin'] = qty_margin
            df.loc[r, ACCOUNT] = acct
            df.loc[r, 'account_value'] = round(acct_value, 2)
            df.loc[r, 'account_change'] = round(chng_acct, 2)

        return df
    
    ###########################
    #  BACKTEST PERFORMANCE
    ###########################

    def _get_backtest_summary(self):

        # Calculate backtest metrics based on its end state
        df = self.df
        n = len(df)
        account_cash = df[ACCOUNT][n-1]
        account_value = df['account_value'][n-1]
        account_value_min = df['account_value'].min()
        account_value_max = df['account_value'].max()
        commission = df['commission'].sum()
        account_start = df[ACCOUNT][0]
        account_cash_min = df[ACCOUNT].min()
        account_cash_max = df[ACCOUNT].max()
        income = account_value - account_start
        pct_gain = income / account_start
        pct_gain_market = (df[CLOSE][n-1] / df[CLOSE][0]) - 1
        trade_attempts = df['trade'].count()
        trades = df[df['account_change'] != 0]['trade'].count()

        # Load summary metrics to a dataframe
        self.summary_dict = dict(
            account_cash = account_cash,
            account_value = account_value,
            commission = commission,
            income = income,
            pct_gain = pct_gain,
            pct_gain_market = pct_gain_market,
            trade_attempts = trade_attempts,
            trades = trades,
            account_cash_min = account_cash_min,
            account_cash_max = account_cash_max,
            account_value_min = account_value_min,
            account_value_max = account_value_max,
        )
        backtest_summary = pd.DataFrame.from_dict(
            self.summary_dict, orient='index').reset_index()
        backtest_summary = backtest_summary.rename(
            {'index': 'parameter', 0: 'value'}, axis=1)
        backtest_summary['backtest_execution_id'] = self.backtest_execution_id
        backtest_summary['backtest_executed'] = self.start_time
        backtest_summary = backtest_summary[[
            'backtest_execution_id',
            'backtest_executed',
            'parameter',
            'value']]
        self.backtest_summary = backtest_summary


    def _print_backtest_summary(self):
        print("""
        ---------- BACKTEST PERFORMANCE SUMMARY ----------
        - % Gain: {}% vs {}% market
        - Income: ${}
        - Account Value: ${}
        - Account Cash:  ${}
        - Trades: {} of {} attempts ({}% execution rate)
        - Account Min: ${}
        - Account Max: ${}
        """.format(
            round(self.summary_dict['pct_gain'] * 100, 1),
            round(self.summary_dict['pct_gain_market'] * 100, 1),
            round(self.summary_dict['income']),
            round(self.summary_dict['account_value']),
            round(self.summary_dict['account_cash']),
            self.summary_dict['trades'],
            self.summary_dict['trade_attempts'],
            round(self.summary_dict['trades'] / self.summary_dict['trade_attempts'] * 100),
            round(self.summary_dict['account_value_min']),
            round(self.summary_dict['account_value_max'])
        ))


    def _load_backtest_to_bq(self):
        # load to BigQuery if specified
        if self.to_bq:
            print('BACKTEST: Loading backtest results to BigQuery.')
            data = dataObject(data = self.backtest_output)
            data.to_db(
                destination_table = BACKTEST_DESTINATION_TABLE,
                if_exists='append'
            )
            
            data = dataObject(data = self.backtest_summary)
            data.to_db(
                destination_table = BACKTEST_SUMMARY_DESTINATION_TABLE,
                if_exists='append'
            )
            
            data = dataObject(data = self.backtest_metadata)
            data.to_db(
                destination_table = BACKTEST_METADATA_DESTINATION_TABLE,
                if_exists='append'
            )
        else:
            print('BACKTEST: Results will not be loaded to BigQuery.')
