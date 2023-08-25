"""process.py

Given a YAML input file, execute an ETL or prediction processes, based
on workflows from:
    - etl/ticker_etl.py
    - model/regression.py

YAML format should be as follows. Update <this text> where appropriate. 
Also, multiple processes can be run sequentially.

process_gid: SPY_n10_i1
processes:

    - process_type : etl
      process_id : etl_SPY_1993_to_date
      process_attributes:
        ticker : SPY
        start_date : 1993-01-01
        end_date   : 
        project : 
        destination_table : yahoo_features.features_{ticker}_YYYYMMDD    
        date_range : 
        look_back : 
        look_forward : 
        data_source :
        ohlc_library : etl.get_ticker_data
        indicators_library : etl.get_indicators
        features_library : etl.get_feature_engineering

    - process_type : predict
      process_id : < Add a unique ID for this process >
      process_attributes:
        ticker: < Ticker >
        outcome: < Outcome variable >
        to_bq: False
        query_filepath: < Filepath for the query; starts with ../queries/ >
        attributes:
            partition: < Output date partition; YYYYMMDD >
        model_storage_filepath: < Storage path for; e.g. general format: models/../model_name.pickle >
        model_filename: < Name of the .pickle file >
        model_storage_id: < Name of the Model Storage ID; e.g. 20190828_Regressor_SPY_b15f5af56f037655cbb >
        model_execution_id:	< Name of the Model Execution ID; e.g. 3b7595970b1981644beaa174a1d0bbc87cbfe9b8 >

"""

import pandas as pd
import numpy as np

from data_mgmt import bigquery_data as bqd
from data_mgmt import yaml_data
from etl import ticker_etl
from model import model_regression as mreg
from model import model_mgmt as mm


class runProcess():
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.process_config = self._get_process_config()
        self.process_list = self._get_process_list()

    def _try_entry(self, entry):
        try:
            return entry
        except:
            return None

    def _get_process_config(self, filepath=None):
        # Get the configuration YAML `self.process_config()` from the given filepath.
        # Returns a dictionary containing all configuration parameters.
        self.filepath = filepath or self.filepath
        process_config = yaml_data.get_yaml_data(self.filepath)
        return process_config

    def _get_process_list(self):
        # Get the list of all processes from self.process_config()
        processes = [process for process in self.process_config['processes']]
        return processes

    def _get_model_dataframe(self, process):
        file = self._try_entry(process['process_attributes']['query_filepath'])
        attributes = self._try_entry(process['process_attributes']['attributes'])
        df = bqd.file_to_df(file, attributes)
        df = df.replace([np.inf, -np.inf], np.nan)
        self.df = df.dropna()
        
    def run_all_processes(self, process_list=None):
        """Sequentially run each process in the workflow.
        """

        # Loop through each process in the config YAML
        process_list = process_list or self.process_list()
        for process in process_list:
            if 'etl' in process['process_type'].lower():
                print("RUNNING: ETL Process {}").format(process['process_id'])
                self.run_etl(process_id=process['process_id'])

            elif 'predict' in process['process_type'].lower():
                print("RUNNING: Prediction Process {}").format(process['process_id'])
                self.run_etl(process_id=process['process_id'])
    

    def run_etl(self, process):
        """Run ETL process based on YAML input file.
        
        YAML format should be as follows. Update <this text> where appropriate. 
        Also, multiple processes can be run sequentially.        
        """
        # Run ETL processes
        if 'etl' in process['process_type'].lower():
            print("ETL PROCESS: Running proccess {}".format(process['process_id']))
            start_time = dt.datetime.now()
            self.etl_process = ticker_etl.etl(
                ticker = process['process_attributes']['ticker'], 
                start_date = self._try_entry(process['process_attributes']['start_date']), 
                end_date = self._try_entry(process['process_attributes']['end_date']), 
                project = self._try_entry(process['process_attributes']['project']), 
                destination_table = self._try_entry(process['process_attributes']['destination_table']), 
                date_range = self._try_entry(process['process_attributes']['date_range']), 
                look_back = self._try_entry(process['process_attributes']['look_back']),
                look_forward = self._try_entry(process['process_attributes']['look_forward']),
                data_source = self._try_entry(process['process_attributes']['data_source']),
                ohlc_library = self._try_entry(process['process_attributes']['ohlc_library']),
                indicators_library = self._try_entry(process['process_attributes']['indicators_library']),
                features_library = self._try_entry(process['process_attributes']['features_library']),
            )
            end_time = dt.datetime.now()
            run_time = end_time - start_time
            print("PROCESS COMPLETE: Completed proccess {} in {}.".format(process['process_id'], run_time))
            self.etl_process.ticker_to_bigquery()


    def run_predict(self, process):
        """Run a prediction process based on a YAML input file.
        
        YAML format should be as follows. Update <this text> where appropriate. Also, multiple
        processes can be run sequentially.
        """
        # Run prediction process
        if 'predict' in process['process_type'].lower():
            print("PREDICT PROCESS: Running proccess {}".format(process['process_id']))
            start_time = dt.datetime.now()
            self._get_model_dataframe(process)
            self.file = process['process_attributes']['query_filepath']
            self.attributes = {'partition': "20190811"}    # <<<<<<<<<<<< NEED TO UPDATE THIS !!!
            self.data = mm.modelQuery(
                file=self.file, attributes=self.attributes)
            self.outcome = process['process_attributes']['outcome']
            self.model = mreg.modelRegression(self.data, self.outcome)

            print("PREDICT: Getting model from Google Storage.")
            self.model.storage = mm.modelStorage(self.model)
            self.model.model = self.model.storage.get_model_from_storage(
                model_execution_id = self._try_entry(process['process_attributes']['model_execution_id']),
                model_storage_filepath = self._try_entry(process['process_attributes']['model_storage_filepath']),
                model_filename = self._try_entry(process['process_attributes']['model_filename']),
                model_storage_id = self._try_entry(process['process_attributes']['model_storage_id']), )

            print("PREDICT: Predicting model.")
            self.model.predict()
            self.model.get_performance()
            self.to_bq = process['process_attributes']['to_bq']
            end_time = dt.datetime.now()
            run_time = end_time - start_time
            print("PROCESS COMPLETE: Completed proccess {} in {}.".format(process['process_id'], run_time))
            if self.to_bq:
                self.model.load_to_bq()

