#!/usr/bin/env python

from algom import configs
from algom.utils.client import bqClient

import hashlib
import pandas as pd
from datetime import datetime


def get_hash_id(obj):
    """Create SHA1 hash ID from any data input

    Args:
        data (str): String containing input information
            to be translated into an ID.

    Returns:
        str: Containing an ID based on the input data.
    """
    x = str(obj).encode()
    gid = hashlib.sha1(x).hexdigest()
    return gid

def _set_query_params(query, params):
    """ Format a query given a dict of parameters
    """
    for k, v in params.items():
        query = query.replace('{' + str(k) + '}', str(v))
    print(query)
    return query


class dataObject():
    """Convert various forms data of data within a single class.

    Input data types:
        - dataObject
        - Pandas DataFrame
        - CSV file
        - SQL file
        - JSON file

    Output data types:
        - Pandas DataFrame
        - CSV
        - Database
    """
    def __init__(self, data, params=None):
        client = bqClient()
        self.credentials = client.credentials
        self.df = pd.DataFrame()
        self.params = params
        self.data_type = self._get_data_type(data)
        self.data = self.load_data(data, params)
        self._get_data_metadata()

    def load_data(self, data, params):
        if 'dataObject' in str(type(data)):
            self.load_blob(data)
        elif isinstance(data, pd.DataFrame):
            self.load_df(data)
        elif isinstance(data, str):
            if data.endswith('.csv'):
                self.load_csv_file(data)
            elif data.endswith('.json'):
                self.load_json_file(data)
            elif data.endswith('.sql'):
                self.load_sql_file(data, params)
            elif 'select' in data.lower() and 'from' in data.lower():
                self.load_sql(data, params)
        elif isinstance(data, list):
            self.load_to_df(data)
        else:
            print("ERROR: This data type is not accepted.")
            # <<< NEED TO COMPLETE DATA INPUTS HERE >>>

            # <<< NEED TO ADD EXECPTION HANDLING HERE >>>

    """
    Input data:
        Load one of several data types into the dataObject class.
    """
    def load_blob(self, blob):
        try:
            self.input_type = 'dataObject'
            self.input_file = None
            self.input_code = None
            self.df = blob.df
            print("SUCCESS: Loaded dataObject.")
        except Exception as e:
            print("ERROR: Unable to import dataObject.\n{}".format(e))

    def load_df(self, df):
        try:
            self.input_type = 'dataframe'
            self.input_file = None
            self.input_code = None
            self.df = pd.DataFrame(df)
            print("SUCCESS: Loaded DataFrame.")
        except Exception as e:
            print("ERROR: Unable to import DataFrame.\n{}".format(e))

    def load_csv_file(self, csv_file):
        try:
            self.input_type = 'csv file'
            self.input_file = csv_file
            self.input_code = None
            self.df = pd.read_csv(csv_file)
            print("SUCCESS: Loaded CSV file.")
        except Exception as e:
            print("ERROR: Unable to import CSV.\n{}".format(e))

    def load_json_file(self, json_file):
        try:
            self.input_type = 'json file'
            self.input_file = json_file
            self.input_code = None
            self.df = pd.read_json(json_file)
            print("SUCCESS: Loaded JSON file.")
        except Exception as e:
            print("ERROR: Unable to import JSON file.\n{}".format(e))

    def load_sql_file(self, sql_file, params=None, **kwargs):
        try:
            with open(sql_file, 'r') as f:
                sql = f.read()
            self.input_type = 'sql file'
            self.input_file = sql_file
            self.input_code = _set_query_params(sql, params) if params else sql
            print("RUNNING: Loaded SQL file: {}.".format(sql_file))
            self.df = pd.read_gbq(
                self.input_code,
                credentials=self.credentials,
                **kwargs)
            print("SUCCESS: Loaded SQL query.")
        except Exception as e:
            print("ERROR: Unable to import SQL file.\n{}".format(e))

    def load_sql(self, sql, params=None, use_cache=True, **kwargs):
        try:
            self.input_type = 'sql'
            self.input_file = None
            self.input_code = _set_query_params(sql, params) if params else sql
            print("RUNNING: Querying SQL script.")
            self.df = pd.read_gbq(
                self.input_code,
                credentials=self.credentials,
                configuration = {'query': {'useQueryCache': use_cache}},
                **kwargs)
            print("SUCCESS: Loaded SQL query.")
        except Exception as e:
            print("ERROR: Unable to run SQL.\n{}".format(e))

    """ OUTPUT DATA

        Output one of several data types from the dataObject class.
    """

    def to_df(self):
        return self.df

    def to_json(self, **kwargs):
        return self.df.to_json(**kwargs)

    def to_csv(self, path, **kwargs):
        return self.df.to_csv(path, **kwargs)

    def to_db(
        self,
        destination_table,
        project_id=None,
        table_partition=None,
        table_params=None,
        **kwargs
    ):
        """Output dataframe to a database destination table.
        Currently only supports BigQuery.
        """
        def _set_destination_table_ids(destination_table):
            destination_list = destination_table.replace(':', '.').split('.')
            if len(destination_list) == 3:
                self.project_id = destination_list[0]
                self.dataset_id = destination_list[1]
                self.table_id = destination_list[2]
            if len(destination_list) == 2:
                self.project_id = project_id or configs.GOOGLE_PROJECT_ID
                self.dataset_id = destination_list[0]
                self.table_id = destination_list[1]

        # Get parameterized table IDs
        self.project_id = project_id or configs.GOOGLE_PROJECT_ID
        self.table_partition = table_partition
        self.table_params = table_params
        self.destination_table = destination_table
        self.destination_table_id = self._replace_string_parameters(
            destination_table, table_partition, table_params)
        _set_destination_table_ids(self.destination_table_id)
        # Load dataframe to BigQuery via gbq()
        self.df.to_gbq(
            destination_table=self.destination_table_id,
            project_id=self.project_id,
            credentials=self.credentials,
            **kwargs)

    """ METADATA

        Get metadata from data object.
    """
    def _get_data_metadata(self):
        self._get_features()
        self._get_data_id()

    def _get_features(self):
        self.feature_list = list(self.df).sort()

    def _get_data_id(self):
        "Create data_id based on technical_analysis included in data"
        self.data_id = get_hash_id(self.feature_list)

    """ HELPER FUNCTIONS

        Functions referenced in the code below.
    """

    def _get_data_type(self, data):
        data_type = type(data)
        return data_type

    def _replace_string_parameters(self, entry, partition=None, params=None):
        """Update a query or table name with today's date (i.e. YYYYMMDD)
        or custom parameters (e.g. {param_name}).
        """
        def _replace_date_partition(entry, partition=None):
            """
            Return table_id with YYYYMMDD notation as a date partition.
            Date partition defaults to today if not specified.
            """
            p1 = partition or datetime.now().strftime("%Y%m%d")
            p2 = entry.replace("YYYYMMDD", p1) \
                if "YYYYMMDD" in entry else entry
            return p2

        def _replace_string(r):
            # Remove spaces or dashes in the table name
            replace = {'-': '_', ' ': '_'}
            for k, v in replace.items():
                r = r.replace(k, v)
            return r

        def _replace_params(entry, params):
            # Replace all parameters in the destination table name
            if isinstance(params, dict):
                for k, v in params.items():
                    entry = entry.replace('{' + k + '}', _replace_string(v))
            return entry

        # Run function
        entry = _replace_date_partition(entry, partition)
        entry = _replace_params(entry, params)
        return entry
