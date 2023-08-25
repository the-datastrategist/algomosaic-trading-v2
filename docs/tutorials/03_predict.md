# Tutorials: Predict


## Overview
Once we have trained and saved our models, we can generate predictions on 
new data. Our models are stored in Google Storage and we can call 
them via the `modelRegression()` class in the `algom.model_regression` module.

From a high level, we will pass 3 parameters into the modelRegression class:

1. The dataset (or dataObject class) containing the model features
2. The outcome variable
3. The saved model_id 

<br>

## Steps to Execution

Below are the steps required to generate predictions on persistent basis.

<br>

### 1. Pull prediction data

We recommend that you use `dataObject(file)` to collect the
model data. Doing so will ensure the input data are persistent and aligned with the
training data.

```
from algom.utils.data_object import dataObject
file = "../../src/query/BTC/BTC_features_n10.sql"
attributes = {'partition': "20191019"}
data = dataObject(file=file, attributes=attributes)
```

TODO: add attributes to SQL file load.


<br>


### 2. Initiate the regression model

```
from algom.src.model_regression import modelRegression

# Initialize model class
model = modelRegression(
    # Input data
    # This is either a dataObject class or dataframe
    data=data,

    # Outcome variable
    # These values can be null 
    outcome='ROR_n24',

    # Saved model_id
    model_id='7959fdd354a37ab43d2786edc7a6b041edb9c5f5',

    # List of fields that should be indexed or removed
    # from the feature set
    index_features=configs.INDEX_FEATURES, 
    omit_features=configs.OMIT_FEATURES
)
```

<br>

Running this will provide the following response:

```
SUCCESS: Loaded dataObject.
SUCCESS: Model 7959fdd354a37ab43d2786edc7a6b041edb9c5f5 has been loaded successfully.
Downloaded file from GCS to: /home/jovyan/algomosaic/data/models/20210105_GradientBoostingRegressor_7959fdd354a37ab43d2786edc7a6b041edb9c5f5.pickle
Initialized model. As a next step, run self.predict() or self.train().
```

<br>


### 4. Run the prediction

Simply run the following code to execute the prediction:

```
model.predict()
```

If the outcome features are available (or partially available), the following
model performance summary will be provided. This is relevant when performing
out-of-sample validation.

```
MODEL PERFORMANCE SUMMARY
        - Mean Absolute Error:	 0.04405
        - Mean Absolute Outcome:	 0.02292
        - Mean Absolute Percent Error:	 1.92188
        - Error Variance:	 0.00398
        - R-Squared:		 -1.85717
``` 

<br>

###### [Return to main](https://github.com/algomosaic/algom-trading/blob/master/docs/tutorials/tutorials.md)
