#!/usr/bin/env python

from algom import configs
from algom.utils.data_object import dataObject
from algom.utils.data_object import get_hash_id
from pandas import DataFrame
from re import search

GOOGLE_PROJECT_ID = configs.GOOGLE_PROJECT_ID


class modelMetadata():
    """modelMetadata()

    Class that extracts metadata/parameters from model classes.
    Must receive model object from model_regression.py,
    model_classifier.py or model_cluster.py.
    """
    def __init__(self, modelBlob, model_execution_id=None, model_labels={}):
        self.modelBlob = modelBlob
        self.outcome = modelBlob.outcome
        self.model_labels = model_labels
        self.get_model_metadata()
        self.get_model_parameters()

    def get_model_metadata(self):
        """
        Get metadata about any Scikit Learn model and store
        to a database.
        """
        # get additional metadata
        ms = str(self.modelBlob.model)
        self.modelBlob.model_type = search(r"(\w*)\(", ms).group(1)

        # load metadata into dictionary
        metadata_dict = {
            'model_execution_id': self.modelBlob.model_execution_id,
            'model_parameter_id': self.modelBlob.model_parameter_id,
            'data_id': self.modelBlob.data.data_id,
            'model_execution_type': self.modelBlob.model_execution_type,
            'outcome_variable': self.modelBlob.outcome,
            'execution_started_at': self.modelBlob.execution_started_at,
            'execution_ended_at': self.modelBlob.execution_ended_at,
            'execution_run_time': self.modelBlob.execution_run_time,
            'model_type': self.modelBlob.model_type,
            'model_description': self.modelBlob.model_description,
            'model_labels': self.model_labels,
            'index_features': self._clean_string(
                self.modelBlob.index_features),
            'feature_list': self._clean_string(
                self.modelBlob.feature_list),
            'feature_count': len(self.modelBlob.feature_list),
            'record_count': len(self.modelBlob.data.df),
        }

        # transpose to dataframe
        metadata = DataFrame.from_dict(
            data=metadata_dict, orient='index').reset_index()
        metadata.columns = ['parameter', 'value']
        metadata['model_execution_id'] = self.modelBlob.model_execution_id
        self.metadata = metadata[['model_execution_id', 'parameter', 'value']]
        print('Model metadata added to `self.metadata.metadata`')

        # load to BigQuery
        if self.modelBlob.to_bq:
            dataObject(self.metadata).to_db(
                destination_table=self.modelBlob.metadata_table,
                project_id=GOOGLE_PROJECT_ID,
                table_partition=None,
                table_params=None,
                if_exists='append'
            )

    def get_model_parameters(self):
        # get model_type (eg RandomForestRegressor)
        ms = str(self.modelBlob.model)
        model_params = {}
        self.model_type = ms.split('(')[0]
        model_params['model_type'] = ms.split('(')[0]

        # create dict of parameters
        ms_list = ms.split(',')
        for ms in ms_list:
            key = search(r"(\w+)=", ms).group(1)
            value = search(r"=(.*)", ms).group(1)
            value = value.replace("'", "")
            value = value.replace(")", "")
            model_params[key] = value

        # add dict to model_params
        self.model_params = model_params
        df_parameters = DataFrame.from_dict(
            data=self.model_params, orient='index').reset_index()
        df_parameters.columns = ['parameter', 'value']
        df_parameters['model_execution_id'] = self.modelBlob.model_execution_id
        df_parameters = df_parameters[[
            'model_execution_id', 'parameter', 'value']]
        self.parameters = df_parameters

        # load to BigQuery
        print('Model metadata added to `self.metadata.parameters`')
        if self.modelBlob.to_bq:
            dataObject(self.parameters).to_db(
                destination_table=self.modelBlob.parameters_table,
                project_id=GOOGLE_PROJECT_ID,
                table_partition=None,
                table_params=None,
                if_exists='append')

    def _get_data_id(self):
        """hash an ordered list of the technical_analysis in the
        input dataset.
        """
        feature_list = self.modelBlob.feature_list
        feature_list.sort()
        return get_hash_id(feature_list)

    def _get_metdata_index_df(self, input_dataframe):
        """Get a standardized output for metadata tables, including
        - self.metadata_table
        - self.parameter_table
        - self.queries_table
        """
        index_headers = [
            'model_execution_id',
            'model_data_id',
            'model_executed_at',
            'model_outcome',
            'model_execution_type'
        ]
        md_index = {}
        md_index['model_execution_id'] = self.modelBlob.model_execution_id
        md_index['model_data_id'] = self.modelBlob.data.data_id
        md_index['model_executed_at'] = self.modelBlob.model_executed_at
        md_index['model_outcome'] = self.modelBlob.outcome
        md_index['model_execution_type'] = self.modelBlob.model_execution_type
        df_index = DataFrame.from_dict(md_index, orient='index').T
        df_index = df_index[index_headers]
        input_dataframe['model_execution_id'] = \
            self.modelBlob.model_execution_id
        df_output = df_index.merge(
            input_dataframe,
            how='inner',
            on='model_execution_id',
            suffixes=('_drop', '')
        )
        column_list = [h for h in list(df_output) if h.find('_drop') < 0]
        df_output = df_output[column_list]
        return df_output

    def _get_model_desc(self, msg=None):
        bootstrap_str = 'bootstrapped' if self.model_params['bootstrap'] \
            else 'not bootstapped'
        model_description = \
            "predict {} with {} variables; "\
            "{} optimized, {}, {} estimators".format(
                self.modelBlob.outcome,
                len(self.modelBlob.feature_list),
                self.model_params['criterion'].upper(),
                bootstrap_str,
                self.model_params['n_estimators'])
        model_description = model_description if not msg \
            else msg + '; ' + model_description
        return model_description

    def _clean_string(self, string):
        string = str(string)
        string = string.replace('{', '')
        string = string.replace('}', '')
        string = string.replace('[', '')
        string = string.replace(']', '')
        string = string.replace('(', '')
        string = string.replace(')', '')
        string = string.replace("'", '')
        return string
