#!/usr/bin/env python

from algom import configs
from algom.model_metadata import modelMetadata
from algom.feature_importance import featureImportance
from algom.model_plots import modelPlots
from algom.utils.data_object import dataObject
from algom.model_storage import modelStorage

from datetime import datetime
import hashlib
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import explained_variance_score


GOOGLE_PROJECT_ID = configs.GOOGLE_PROJECT_ID
METDATA_TABLE = configs.METDATA_TABLE
PARAMETERS_TABLE = configs.PARAMETERS_TABLE
PREDICTION_TABLE = configs.PREDICTION_TABLE
EVALUATION_TABLE = configs.EVALUATION_TABLE
PERFORMANCE_TABLE = configs.PERFORMANCE_TABLE
FEATURE_IMPORTANCE_TABLE = configs.FEATURE_IMPORTANCE_TABLE
STORAGE_TABLE = configs.STORAGE_TABLE
QUERY_TABLE = configs.QUERY_TABLE


class modelRegression():

    def __init__(
        self,
        data,
        outcome,
        model_id=None,
        model=None,
        index_features=None,
        omit_features=[],
        to_bq=False
    ):
        """modelRegression

        Predicts an outcome, given a model_execution_id and a data input.
        The data input can be any data type accepted by algom's dataObject
        class.

        Args:
            data: Accepts any data type accepted by algom's dataObject class

            outcome (str): Name of the outcome variable.

        TO DO: Complete docstrings

        """
        # model data and outcome
        self.data = dataObject(data)
        self.outcome = outcome
        self.model_id = model_id
        self.model = self._get_model(
            model_id=model_id, model=model)

        # model parameters
        self.test_size = .7
        self.random_state = 0

        # model metadata
        self.index_features = self._set_index_features(index_features)
        self.omit_features = omit_features
        self.feature_list = self.get_feature_list()
        self.model_name = None
        self.model_description = None
        self.to_bq = to_bq

        # initialize output dataframes
        self.predictions = None
        self.evaluations = None
        self.performance = None
        self.execution_started_at = None

        # table parameters
        self.project_id = GOOGLE_PROJECT_ID
        self.metadata_table = METDATA_TABLE
        self.parameters_table = PARAMETERS_TABLE
        self.predictions_table = PREDICTION_TABLE
        self.evaluations_table = EVALUATION_TABLE
        self.performance_table = PERFORMANCE_TABLE
        self.feature_importance_table = FEATURE_IMPORTANCE_TABLE
        self.storage_table = STORAGE_TABLE
        self.query_table = QUERY_TABLE
        print(
            "Initialized model. As a next step, "
            "run self.predict() or self.train()."
        )

    # DATA PREP FUNCTIONS
    def _time_function(self, function):
        self.execution_started_at = datetime.now()
        f = function
        self.execution_ended_at = datetime.now()
        self.execution_run_time = self.execution_ended_at - \
            self.execution_started_at
        return f

    def _get_hash_id(self, data):
        """Create SHA1 hash ID from any data input"""
        x = str(data).encode()
        #gid = hashlib.sha1(x).hexdigest()
        gid = hashlib.sha1(x).hexdigest()
        return gid

    def _get_class_attributes(self, cls):
        return {k: v for k, v in cls.__dict__.items() if k[:1] != '_' and k[-1] != '_'}

    def _get_model_ids(self, model_execution_type=None):
        """Add key model metadata to any model instance. Keeps model_id and
        model_execution_id if they already exist in the model_object.
        Ensures model IDs are generated consistently. Model metadata includes:
            - model_execution_id
            - model_id
            - model_parameter_id
            - model_data_id
            - model_execution_type
        """
        execution_started_at = self.execution_started_at or datetime.now()
        model_attributes = self._get_class_attributes(self.model)

        # Model ID is based on (1) the model type, (2) the model parameters
        # (3) the outcome variable, and (4) the features used.
        #self.model_id = self.model_id or self._get_hash_id(
        self.model_id = self.model_id if model_execution_type=='predict' else self._get_hash_id(
            str(self.outcome) +
            str(self.model) +
            str(self.data.data_id) +
            str(self.feature_list)
        )

        # Model Execution ID is based on (1) the model type, 
        # (2) the model parameters, (3) the outcome variable, 
        # and (4) the features used.
        self.model_execution_id = self._get_hash_id(
            str(execution_started_at) +
            str(self.outcome) +
            str(self.model) +
            str(self.data.data_id) +
            str(self.feature_list)
        )
        self.model_parameter_id = self._get_hash_id(self.model)
        self.model_data_id = self.data.data_id
        self.model_execution_type = model_execution_type

    def _get_model(self, model_id=None, model=None):
        """Get model if it isn't already available."""
        if model:
            return model
        elif model_id:
            storage = modelStorage()
            return storage.get_model_from_storage(self.model_id)
        else:
            return None

    def _set_index_features(self, index_features):
        if index_features:
            index_features = [
                f for f in index_features if f in list(self.data.df)]
        else:
            index_features = []
        return index_features

    def get_feature_list(self):
        feature_list = [
            f for f in list(self.data.df) if f not in
            ([self.outcome] + self.index_features + self.omit_features)]
        # Load to dict to ensure output order is correct
        x = {}
        for feature in feature_list:
            x[feature] = None
        return list(x.keys())

    def get_feature_sets(self, test_size=None, random_state=None, **kwargs):
        """Use Skicit-learn to split data into training and testing sets.
        Adds test/train versions of these tables:
            - featues
            - outputs
            - outcomes
        """
        self.outputs = self.data.df[
            self.index_features + [self.outcome]]
        self.outcomes = self.data.df[[self.outcome]]
        self.features = self.data.df[self.feature_list]
        test_features, train_features, test_outputs, train_outputs \
            = train_test_split(
                self.features,
                self.outputs,
                test_size=test_size or self.test_size,
                random_state=random_state or self.random_state)
        self.train_features = train_features
        self.test_features = test_features
        self.train_outputs = train_outputs
        self.test_outputs = test_outputs
        self.train_outcomes = train_outputs[self.outcome]
        self.test_outcomes = test_outputs[self.outcome]

    def _get_clean_output_dataframe(
        self,
        input_dataframe,
        model_execution_type
    ):
        """Get a standardized output for metadata tables, including
        - self.metadata_table
        - self.parameter_table
        - self.queries_table
        """
        # Create metadata
        md_index = {}
        md_index['model_id'] = self.model_id
        md_index['model_execution_id'] = self.model_execution_id
        md_index['model_parameter_id'] = self.model_parameter_id
        md_index['model_data_id'] = self.data.data_id
        md_index['execution_started_at'] = self.execution_started_at if \
            hasattr(self, 'execution_started_at') else None
        md_index['execution_ended_at'] = self.execution_ended_at if \
            hasattr(self, 'execution_ended_at') else None
        md_index['execution_run_time'] = self.execution_run_time if \
            hasattr(self, 'execution_run_time') else None
        md_index['model_execution_type'] = model_execution_type
        md_index['model_outcome'] = self.outcome

        # Merge input dataset onto metadata
        df_index = DataFrame.from_dict(md_index, orient='index').T
        input_dataframe['model_execution_id'] = self.model_execution_id
        df_output = df_index.merge(
            input_dataframe,
            how='inner',
            on='model_execution_id',
            suffixes=('_drop', '')
        )
        column_list = [h for h in list(df_output) if '_drop' not in h]
        df_output = df_output[column_list]
        return df_output

    # DATA I/O

    def load_to_bq(self):
        """Load model outputs to BigQuery:
            - model_metadata
            - predictions
            - performance
            - feature_importance

        <<<<<< UPDATE THIS: USE os.exist() INSTEAD >>>>>>>
        """
        def _check_and_load(df, table_name):
            if df:
                dataObject(df).to_db(
                    destination_table=table_name,
                    project_id=GOOGLE_PROJECT_ID,
                    table_partition=None,
                    table_params=None,
                    if_exists='append'
                )
            else:
                print('{} does not exist. Skipping.'.format(table_name))

        _check_and_load(self.predictions, self.predictions_table)
        _check_and_load(self.evaluations, self.evaluations_table)
        _check_and_load(self.performance, self.performance_table)
        _check_and_load(self.metadata.metadata, self.metadata_table)
        _check_and_load(self.metadata.parameters, self.parameters_table)
        _check_and_load(self.feature_importance.feature_importance,
                        self.feature_importance_table)
        print("COMPLETE: all model outputs have been loaded to BigQuery!")

    """ MODELING

    Functions used in training models. Includes:
        - predict
        - evaluate
        - save
    """

    # PREDICTION

    def predict(self, to_bq=None):
        """Output predictions to dataframe based on the Scikit Learn
        model provided. Uses all technical_analysis from the input dataset to
        generate predictions. Generates metadata about the model prediction
        execution.

        Attributes
        ----------
        outputs
            DataFrame; Dataframe containing single column of outputs.
            Not all entries need to have outcomes.

        technical_analysis
            DataFrame; Dataframe of technical_analysis to run prediction.

        to_bq
            Boolean; If True then push to BigQuery.

        Returns
        -------
        predictions   DataFrame; Dataframe of predictions and
            outcomes (if available).
        """
        def _set_model_features(model_object):
            """Return datasets needed for prediction."""
            model_object.get_feature_sets()
            self.outputs = model_object.outputs
            self.features = model_object.features[self.get_feature_list()]
            self.outcomes = model_object.outcomes

        def _get_model_predictions():
            """Output dataframe with prediction outputs."""
            _set_model_features(self)
            self.predictions = pd.Series(
                self.model.predict(self.features), name='predictions')
            df_predictions = self._get_prediction_df(
                self.outputs, self.outcomes, self.predictions)
            df_predictions = self._get_clean_output_dataframe(
                df_predictions, 'predict')
            return df_predictions

        def _load_to_bq():
            dataObject(self.predictions).to_db(
                destination_table=self.predictions_table,
                project_id=GOOGLE_PROJECT_ID,
                table_partition=None,
                table_params=None,
                if_exists='append')

        # Get feature and outcome data
        self._get_model_ids(model_execution_type='predict')
        self.predictions = self._time_function(_get_model_predictions())
        self.metadata = modelMetadata(self)

        # Get model performance
        print('Get model performance.')
        self.get_performance()
        self.plots = modelPlots(self)

        # Load to BigQuery
        to_bq = to_bq or self.to_bq
        if to_bq:
            _load_to_bq()

    # TRAINING

    def train(self, model):
        """Fit a Scikit Learn model to a given feature set, and get
        metadata related to the training execution.

        Parameters
        ----------
        model : Scikit Learn model

        Returns
        -------
        self.query.metadata : pandas.DataFrame()
            Dataframe containing metadata related to the model execution
        """
        def _set_model_features(model_object):
            # Get training feature set
            model_object.get_feature_sets()
            self.features = self.train_features[self.get_feature_list()]
            self.outcomes = self.train_outcomes

        def _train_model(model_object):
            _set_model_features(model_object)
            self.model.fit(self.features, self.outcomes)

        # Train model
        print('Training model on {}.'.format(self.outcome))
        self.model = model
        self._get_model_ids(model_execution_type='train')
        self._time_function(_train_model(self))

        # Add model IDs and metadata to class
        self.metadata = modelMetadata(self)

        # Get model feature importance
        self.feature_importance = featureImportance(self)
        print('Fit model in {}.'.format(self.execution_run_time))

        # Get model performance
        print('Get model performance.')
        self._evaluate()
        self.get_performance()
        self.plots = modelPlots(self)

    # EVALUATION

    def _evaluate(self):
        """Once a model has been trained, perform a validation
        and output the predictions to a dataframe.

        Steps:
        - predict the test technical_analysis
        - generate evaluations dataframe
        - collect model metadata
        - load evaluations table to BQ if to_bq==True
        """
        def _get_test_model_features(model_object):
            model_object.get_feature_sets()
            outputs = model_object.test_outputs
            features = model_object.test_features[self.get_feature_list()]
            outcomes = model_object.test_outcomes
            return outputs, features, outcomes

        def _get_model_evaluations():
            [outputs, features, outcomes] = _get_test_model_features(self)
            evaluations = pd.Series(
                self.model.predict(features), name='evaluations')
            df_evaluations = self._get_prediction_df(
                outputs, outcomes, evaluations)
            df_evaluations = self._get_clean_output_dataframe(
                df_evaluations, 'evaluations')
            return df_evaluations

        if self.model:
            self.evaluations = _get_model_evaluations()
            print('Set evaluation to self.evaluations in {}.'.format(
                self.execution_run_time))
            # load to BigQuery
            if self.to_bq:
                dataObject(self.evaluations).to_db(
                    destination_table=self.evaluations_table,
                    project_id=GOOGLE_PROJECT_ID,
                    table_partition=None,
                    table_params=None,
                    if_exists='append'
                )

    # STORAGE
    def save(self):
        self.storage = modelStorage(self)
        self.storage.load_model_to_storage()
        print("Saved model to Google Storage:\n\t{}".format(
            self.storage.model_storage_filepath))

    # PERFORMANCE
    def get_performance(self):
        """ Get performance metrics, if possible when predicting
        future outcomes; otherwise, leave blank.
        """
        self._get_rsquared()
        self._get_mean_errors()
        data = {
            'rsquared': self.rsquared,
            'mae': self.mean_abs_error,
            'error_variance': self.error_var}
        df_performance = pd.DataFrame.from_dict(data=data, orient='index')
        df_performance = df_performance.reset_index()
        df_performance.columns = ['parameter', 'value']
        df_performance = self._get_clean_output_dataframe(
            df_performance, 'performance')
        self.performance = df_performance
        print('Performance metrics added to `self.performance`')

        # load performance to BigQuery
        self._print_performance()
        if self.to_bq:
            pass

            # <<<<<<<<<< FIX THIS !!! >>>>>>>>>>>>

#             dataObject(self.performance).to_db(
#                 destination_table=self.performance_table,
#                 project_id=GOOGLE_PROJECT_ID,
#                 table_partition=None,
#                 table_params=None,
#                 if_exists='append'
#             )

    # ANALYSIS

    def get_correlations(self):
        correlations = pd.DataFrame(self.df.corr()[self.outcome])
        correlations = correlations.rename(
            columns={self.outcome: 'correlation'})
        correlations['abs_correlation'] = abs(correlations['correlation'])
        correlations = correlations.sort_values(
            'abs_correlation', ascending=False)
        self.correlations = correlations[
            correlations.index.isin(self.feature_list)]
        return self.correlations

    def _get_correlation_order(self):
        correlations = self.get_correlations()
        correlations_dict = correlations.to_dict()
        correlations_dict = correlations_dict['correlation']
        correlations_order = list(correlations_dict.keys())
        return correlations_order

    def _get_prediction_df(self, outputs, outcomes, predictions):
        """Reformat predict outputs into a single dataframe"""

        # convert outputs to a dataframe
        predictions = pd.DataFrame(predictions)
        outputs = pd.DataFrame(outputs).reset_index().drop(
            'index', 'columns')
        outcomes = pd.DataFrame(outcomes).reset_index().drop(
            'index', 'columns')

        # ensure columns are labeled properly
        predictions.columns = ['predictions']
        outcomes.columns = ['outcomes']
        results = pd.concat(
            [outputs, predictions, outcomes], axis=1, sort=False)
        results['errors'] = results['outcomes'] - results['predictions']
        results = results.drop(self.outcome, 'columns')
        return results

    def _get_predictions_or_evaluations(self):
        """If class has predictions, get it. Otherwise, get evaluations."""
        if isinstance(self.predictions, DataFrame):
            df = self.predictions
        elif isinstance(self.evaluations, DataFrame):
            df = self.evaluations
        else:
            df = pd.DataFrame()
        return df

    def _get_rsquared(
        self,
        outcome_var='outcomes',
        prediction_var='predictions'
    ):
        try:
            df_predict = self._get_predictions_or_evaluations()
            outcomes = df_predict[outcome_var]
            predictions = df_predict[prediction_var]
            self.rsquared = explained_variance_score(outcomes, predictions)
            print('Set R^2 to `self.rsquared`')
        except Exception as e:
            self.rsquared = np.NaN
            print('R-Squared cannot be calculated.\n{}'.format(e))

    def _get_mean_errors(self):
        df_predict = self._get_predictions_or_evaluations()
        try:
            mean_abs_error = df_predict['errors'].abs().mean()
            mao = df_predict['outcomes'].abs().mean()
            mean_abs_pct_error = mean_abs_error / mao
            # ^^^^ CONFIRM CALCULATION OF MAE ^^^^
            error_var = df_predict['errors'].var()
            self.mean_abs_error = round(mean_abs_error, 8)
            self.mean_abs_outcome = round(mao, 8)
            self.mean_abs_pct_error = round(mean_abs_pct_error, 8)
            self.error_var = round(error_var, 8)
            print("""The following performance measures have been added:
                - self.mean_abs_error
                - self.mean_abs_outcome
                - self.mean_abs_pct_error
                - self.error_var
            """)
        except Exception as e:
            self.mean_abs_error = np.NaN
            self.mean_abs_outcome = np.NaN
            self.mean_abs_pct_error = np.NaN
            self.error_var = np.NaN
            print('Performance metrics cannot be calculated.\n{}'.format(e))

    def _print_performance(self):
        print("""\nMODEL PERFORMANCE SUMMARY
        - Mean Absolute Error:\t {}
        - Mean Absolute Outcome:\t {}
        - Mean Absolute Percent Error:\t {}
        - Error Variance:\t {}
        - R-Squared:\t\t {}
        """.format(
            round(self.mean_abs_error, 5),
            round(self.mean_abs_outcome, 5),
            round(self.mean_abs_pct_error, 5),
            round(self.error_var, 5),
            round(self.rsquared, 5),
        ))
        print("PLOT PREDICTIONS: Use the following commands"
              "to view model performance."
              """
              `self.plot_predictions_by_date(start_date, end_date)`
              `self.plot_predictions_histogram(start_date, end_date)`
              `self.plot_errors_by_date(start_date, end_date)`
              `self.plot_errors_histogram(start_date, end_date)`
              `self.plot_predictions_scatterplot(start_date, end_date)`
              """)
