###### IN DEVELOPMENT

# algoMosaic

#### algoMosaic is an open-source data science automation framework.

Automating data science can be complicated. algoMosaic makes it seamless by 
combining these commonly used open-source platforms:

- Jupyter Lab
- Apache Airflow
- MLflow
- Docker
- Google Cloud Platform

algoMosaic allows data scientists to **move easily between ad hoc analysis**
(in Jupyter) **and scheduled processes** (with Airflow). It uses GCP Service
Accounts to connect to BigQuery and Storage, allowing for scalable and
decentralized data science.

<br><br>


## Setup

Before running algoMosaic, we must take a few steps to properly 
set up the ecosystem. 

<br>

### 1. Clone a template project

1. Clone the template repository from Github.

```
git clone https://github.com/algomosaic/algomosaic.git
```

<br>


### 2. Set up Google Cloud Platform infrastructure

algoMosaic connects with a set of GCP infrastructure. We must setup this
infrastructure before initializing our algomosaic project.

1. **Set up a [Cloud SQL](https://cloud.google.com/sql/) database**. Follow these 
instructions to 
[setup a new Cloud SQL instance](https://cloud.google.com/sql/docs/mysql/create-instance).

2. **Set up Google [Storage](https://cloud.google.com/storage)**. Next, we will  
[setup a Storage instance](https://cloud.google.com/storage/docs/quickstart-console). 
We will store models here when using algoMosaic.

3. **Create a new bucket**. 
Create a [Storage bucket](https://cloud.google.com/storage/docs/creating-buckets). 
We'll configure this bucket shortly.

<br>


### 3. Set up GCP Service Account 

Service accounts allow us to connect to BigQuery without user-level authentication.
This account will be used for both ad hoc and scheduled analysis.


1. **Create a GCP Service Account**. Follow these instructions to 
[create a Service Account](https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-console).

2. **Create a GCP Service Account key**. Follow these

<br>


### 4. Update config.py and .env

1. **Update algom/config.py.**
Open `algom/configs.py` and update the variables to fit your project. Specifically, we
will add parameters for:
    
    - _algoMosaic ecosystem._ Information related to your algoM instance, i.e. the
    project's 'ecosystem.'
     
    - _Google Cloud Platform._ Includes the GCP project you will use, as well as
    the location you will store your models. 
    
    - _algoMosaic analytics database._ These tables track information about saved
    and executed models.

2. **Update src/config.py** (optional).
The code you add to algoMosaic should be added to the src directory. Simiarly,
you should add project-specific configurations to src/configs.py (or any filename
you want).

3. **Update .env.**
Open the `.env` file and change the connection details. 

<br>


### 5. Launch algomosaic

Once you've updated the parameters for the algomosaic ecosystem, we can launch the platform
There are two ways we can launch algoMosaic -- **ad hoc analysis** or **scheduled analysis**.

<br>

##### Launching algoM with Jupyter Lab (ad hoc analysis)

```
pip install -r requirements.txt
docker-compose -f docker-compose-jupyter.yaml up --build
```

You terminal will launch the standard Jupyter Lab setup. Copy
and paste the URL provided into your browser. 

<br>


##### algoM with Airflow + Jupyter Lab (scheduled analysis or processes)

```
pip install -r requirements.txt
docker-compose -f docker-compose-airflow.yaml up --build
```

We can connect to each services connect via the ports below:

- Jupyter Lab: `http://localhost:8888` (secure connection required)
- Airflow: `http://localhost:8080`
- MLflow: `http://localhost:5000`   

<br><br>


## How to use

algoMosaic is built with the following ML lifecycle in mind. Our 
[documentation](https://github.com/algomosaic/algomosaic/tree/master/docs) 
provides details on how to complete each step in this lifecycle. 

1. Data extraction
2. Feature engineering
3. Model training and storage
4. Model prediction
5. Python process tracking

We streamline and/or automate aspects of this lifecycle. See the
[example notebooks](https://github.com/algomosaic/algomosaic/tree/master/notebooks/examples) 
for more details.

<br><br>


## Features 

Key features of algoMosaic include:

- **Decentralized modeling.** In a single project, users can independently train, evaluate, 
and predict models stored in a central GCP Storage bucket. Users can access and store data 
in a central BigQuery database. 

- **Python process automation.** Users can add Python files to the src file and reference
them in Airflow DAGs. This is a great way to automate aspects of your analysis. 

- **ML tracking.** algoMosaic tracks and stores information through the entire machine 
learning lifecycle. Users can save models to storage and get them with a `model_id`.

###### _Note: some of this functionality has not been created yet._

<br><br>


## Playbooks

We have created a series of 
[Playbooks](https://github.com/gordonsilvera/algom-trading/tree/master/notebooks/playbooks)
that walk through how to complete each phase of the Lifecycle. Each step is parameterized, 
so it's easy to customize the workflow.

We have included the following Playbooks:

- `playbook_00_all_steps.ipynb` (WIP): end-to-end walk through of each step of the ML lifecyle
- `playbook_01_etl.ipynb`: run an ETL/ELT and feature generation process
- `playbook_02_train.ipynb`: train, evaludate, and store a model
- `playbook_03_predict.ipynb`: predict new data using a stored model
- `playbook_04_process.ipynb`: run any of these processes via a YAML configuration

<br>


## Examples 

What can you do with algoMosaic? Here are a couple sample projects. 

### Stock Prediction

We have used stock/cryptocurrency market prediction and trading as our preliminary use case. 
We have done this for the following reasons:

+ Training data are small, free, and easily accessible
+ Challenging and meritocratic use case (if you can succeed here, then you can anywhere)
+ Allows for easy scaling as we expand the framework. We can scale within a domain (by predicting multiple tickers) 
or across domains (by adding new asset classes or data sources).
+ Tests predictions as well as the actions that are taken from predictions.

<br>

### RSS Sentiment Analysis

We have used stock/cryptocurrency market prediction and trading as our preliminary use case. 

<br>


## Notes

+ In Development
+ Built with Python 3
+ Currently built for Scikit Learn and GCP
+ See [docs](https://github.com/gordonsilvera/algom-trading/tree/master/docs) for more details 

<br>

## To Do

This project is still in development. The 
[projects](https://github.com/orgs/algomosaic/projects/1) tab tracks the
planned updates. 
