# Tutorials: Train

<br>

## Overview 
Once the data has been processed, we can use it to train predictive models. 

The standard outcome variable is the log-adjusted rates of return _N_ days
from the current period. This is denoted by the field name `ROR_nX`, where 
`X` is the number of periods in the future. 

Models can be trained on an ad hoc basis (locally) or on a persistent basis 
(in the cloud). If trained in the cloud, you will have to schedule a separate
Python script to run the process.

One of the benefits of the algoM system is that we collect metadata and 
performance data for each model training and prediction execution. This allows 
us to compare performance across many models.

The following tables are generate during the training process:
+ `my-project-id:predictions.model_evaluation_YYYYMMDD`
+ `my-project-id:metadata.model_metadata_YYYYMMDD`
+ `my-project-id:metadata.model_parameters_YYYYMMDD`

<br>

## Steps to Execution

Below are the steps required to train a model, view the performance, and store the results
to BigQuery and Storage.

<br>

### 1a. Get data from a SQL file

Create a `dataObject()` from `algom.utils.data_object` to query your desired data.
This data can be loaded back to BigQuery in the following way:

```
from algom.utils.data_object import dataObject

# Execute dataset
data = dataObject("SELECT * FROM `my-proj.my_dataset.my_table`")

# View top 5 records
data.df.head()

# Load to a new dataset
data.to_bq('my-proj.my_dataset.my_new_table')
```

Alternatively, you can specify a SQL file to query data from. dataObject will detect
the format you use to request the data (e.g. SQL script, SQL file, CSV, Dataframe).
```
from algom.utils.data_object import dataObject
file = '../queries/BTC/BTC_features.sql'
data = dataObject(file)
data.df.head()
```

TODO: need to add attributes to function `load_sql_file`.

<br>

### 1b. Get data from a SQL query

Alternatively, we can pull data as a Pandas Dataframe. This will not store query 
information but the modeling process works the same. 

```
import pandas as pd
from algom.utils.data_object import dataObject

# Assume this dataframe contains your feature dataset
df = pd.DataFrame()
data = dataObject(df)
```

<br><br>

### 2. Initialize model

To initialize the model, pass the input data object (or dataframe) and outcome variable
into the `modelRegression()` class. Initializing the model allows us to collect metadata
and other data related to the prediction process, which will get loaded to BigQuery later on.

```
from algom.model_regression import modelRegression
model = modelRegression(
    data=input_data, 
    outcome='ROR_n10'
)
```

<br><br>

### 3. Fit desired Scikit Learn model

Initialize a Scikit Learn model and pass it into the model class using `model.fit()`. Fitting
the model with this approach will extract metadata and performance data, allowing us to store
it in BigQuery.

> **_NOTE:_**  algoM currently only supports regression (or supervised learning) models.
               We're currently adding unsupervised learning (e.g. clustering) and other 
               forms of modeling.

<br>

The following code fits the regressor model you specify. The model class generates a training
and evaluation dataset and trains the model.

```
from sklearn import ensemble
regressor = ensemble.GradientBoostingRegressor(
    loss='ls', 
    learning_rate=0.1,
    n_estimators=800,
    subsample=.9,
    criterion='friedman_mse'
)
model.fit(regressor)
```

<br>

### 4. Evaluate the model and get performance

Once the model is fit, we receive a performance summary. By default, the following
performance summary will be output. This information is also saved to BigQuery:
- ...
- ...

```
Performance metrics added to `self.performance`

MODEL PERFORMANCE SUMMARY
        - Mean Absolute Error:	 0.01013
        - Mean Absolute Outcome:	 0.03236
        - Mean Absolute Percent Error:	 0.31295
        - Error Variance:	 0.00027
        - R-Squared:		 0.87886
```

We can also view a set of plots related to modeling performance with
the `modelPlots()` class.

```
# Initialize modelPlots
%matplotlib inline
model_plot = modelPlots(model)

# Specify start/end dates
start_date='2019-06-01'
end_date='2019-07-01'

model_plot.plot_predictions_by_date(start_date, end_date)
model_plot.plot_errors_by_date(start_date, end_date)
model_plot.plot_predictions_histogram(start_date, end_date)
model_plot.plot_errors_histogram(start_date, end_date)
model_plot.plot_predictions_scatterplot(start_date, end_date)

```

<br>


### 5. Store model and model data

Once we've evaluated the model, we can decide whether to save the model 
and its associated data. 

```
model.save()
```

You will receive the following information about the model save process. We
can later use the model ID (in the case `7959fdd354a37ab43d2786edc7a6b041edb9c5f5`)
to predict data 

```
Uploaded pickle to Google Storage:
	https://storage.googleapis.com/my-bucket/models/20210112_GradientBoostingRegressor_7959fdd354a37ab43d2786edc7a6b041edb9c5f5.pickle
SUCCESS: Loaded DataFrame.
Uploaded storage metadata to Google BigQuery:
	metadata.model_storage_YYYYMMDD
Saved model to Google Storage:
	models/20210112_GradientBoostingRegressor_7959fdd354a37ab43d2786edc7a6b041edb9c5f5.pickle

```

<br>

### 6. View feature importance

We can also view feature importance and save the results to BigQuery. Feature importance
will automatically be loaded to BigQuery when running `self.load_to_bq()`.

```
feature_importance = model.feature_importance.feature_importance
feature_importance.head()
```

<br>

###### [Return to main](https://github.com/algomosaic/algom-trading/blob/master/docs/tutorials/tutorials.md)
