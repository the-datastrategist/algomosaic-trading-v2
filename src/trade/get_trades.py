import pandas as pd
from importlib import import_module


def get_business_rules_response(data, function, module=None, column_name=None, transpose=True):
    """Get a response based on a set of business rules and input data.

    Given an input DataFrame or dictionary, provide a response based 
    on the parameters in a business rules set. The business rules are
    specified in a Python file.
    
    Example module:
        ```# execute_business_rules.py
        
        def execute(data):
            if data['metric'] > 10:
                response = {'segment': 'high'}
            elif data['metric'] > 5:
                response = {'segment': 'mid'}
            else:
                response = {'segment': 'low'}
            return response
        ```
        
    Example code:
        ```
        response = get_rules_response(
            data=df,
            function='execute',
            module='execute_business_rules'
        )
        ```
    """
    _module = import_module(module) if module else None
    eval_str = '_module.{}(x)'.format(function) if module else '{}(x)'.format(function)
    if isinstance(data, pd.DataFrame):
        col_name = column_name if column_name else 'response'
        output = data
        output[col_name] = [eval(eval_str, {'_module': _module, 'x': row}) for index, row in data.iterrows()]
        output = _transpose_key_columns(data, col_name) if transpose else output
    elif isinstance(data, dict):
        output = eval(eval_str, {'_module': _module, 'x': data})
    else:
        output = None
    return output


def _transpose_key_columns(df, column_name):
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
    return df

# def _get_df_rules_response(data, column_name, transpose=True):
#     # If input data is a dataframe, run this
#     # Adds responses (row-by-row) to the input dataframe
#     col_name = column_name if column_name else 'response'
#     output = data
#     output[col_name] = [eval(eval_str, {'_module': _module, 'x': row}) for index, row in data.iterrows()]
#     output = _transpose_key_columns(data, column_name) if transpose else output
