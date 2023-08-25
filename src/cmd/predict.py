#!/usr/bin/env python

import argparse
from algom.model_regression import modelRegression
from algom.utils.data_object import dataObject

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run and output predictions from algoMosaic "
        "with a given dataset and model_id.")

    parser.add_argument(
        'data',
        type=str,
        help='Input data. We recommend that you specify a SQL file.')

    parser.add_argument(
        'outcome',
        type=str,
        help='Name of outcome variable.')

    parser.add_argument(
        'model_id',
        type=str,
        help='algoMosaic model_id.')

    parser.add_argument(
        '--index_features',
        nargs='+',
        type=str,
        default=['date'],
        help='Variables that relate to the index. These will be removed'
        'from the feature list but output in the predictions output.')

    parser.add_argument(
        '--omit_features',
        nargs='+',
        default=[],
        type=str,
        help='Variables that should be removed from the feature list. '
        'These will not be included in the predictions outout.')

    parser.add_argument(
        '--to_bq',
        type=bool,
        default=True,
        help='Save prediction results to BigQuery. Use boolean.')

    # Parse arguments above
    args = parser.parse_args()

    # Run prediction process
    data_object = dataObject(args.data)
    model = modelRegression(
        data=data_object.df,
        outcome=args.outcome,
        model_id=args.model_id,
        index_features=args.index_features,
        omit_features=args.omit_features,
        to_bq=args.to_bq
    )
    model.predict()

    # Print notifications
    print("COMPLETE. Model prediction is complete.")
    print("Model ID: {}".format(model.model_id))
    print("Model Execution ID: {}".format(model.model_execution_id))
    print("Model loaded to {}".format(model.predictions_table))
