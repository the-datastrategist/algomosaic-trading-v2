#!/usr/bin/env python

from algom import configs
from algom.utils.data_object import dataObject
import pandas as pd


GOOGLE_PROJECT_ID = configs.GOOGLE_PROJECT_ID


class featureImportance():
    """Get dataframe containing the feature importance of a model.
    """
    def __init__(self, modelObject):
        self.modelObject = modelObject
        self.get_feature_importance()

    def get_feature_importance(self):
        # Get numerical feature importances
        importances = list(self.modelObject.model.feature_importances_)
        # List of tuples with variable and importance
        feature_importances = [
            (feature, round(importance, 5)) for feature, importance
            in zip(self.modelObject.feature_list, importances)]
        # Sort the feature importances by most important first
        feature_importances = sorted(
            feature_importances, key=lambda x: x[1], reverse=True)

        # Output to dataframe
        feature_importances = [list(pair) for pair in feature_importances]
        df_feature_importances = pd.DataFrame(
            feature_importances,
            columns=['variable', 'importance']
        )

        # Get metadata IDs from class
        df_feature_importances['model_execution_id'] = \
            self.modelObject.model_execution_id
        df_feature_importances['data_id'] = self.modelObject.data.data_id
        df_feature_importances['outcome_variable'] = self.modelObject.outcome
        df_feature_importances['rank'] = \
            df_feature_importances['importance'].rank(ascending=False)
        df_feature_importances['pct_rank'] = \
            df_feature_importances['importance'].rank(pct=True)
        df_feature_importances = df_feature_importances[[
            'model_execution_id',
            'data_id',
            'outcome_variable',
            'variable',
            'importance',
            'rank',
            'pct_rank'
        ]]
        self.feature_importance = df_feature_importances

        # Load to BigQuery
        if self.modelObject.to_bq:
            dataObject(self.feature_importance).to_db(
                destination_table=self.modelObject.feature_importance_table,
                project_id=GOOGLE_PROJECT_ID,
                table_partition=None,
                table_params=None,
                if_exists='append'
            )
        print('Set feature_importance to '
              '`self.feature_importance.feature_importance`')
