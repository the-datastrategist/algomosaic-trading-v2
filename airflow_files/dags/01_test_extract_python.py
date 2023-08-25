from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.python import PythonOperator


def run_ticker_extract(ticker):
    model = run_etl_process(
        ticker=ticker,
        start_date='2020-01-01',
        end_date=None,
        project=None,
        destination_table='test_features.features_{ticker}_YYYYMMDD',
        table_params={'ticker': ticker},
        data_library='src.extract.cryptocompare_ticker_data',
        features_library='src.features.get_features',
        date_range=None,
        look_back=None,
        look_forward=None,
        to_bq=True,
        if_exists='replace'
    )
    print(model.model_execution_id)

def test_func():
    print('Hello!')

# <<<<<<  AIRFLOW SETUP  >>>>>>>
args = {
    'owner': 'silvera',
    'start_date': days_ago(1),
}

print('Setup DAG.')
dag = DAG(
    dag_id='test_python_extract',
    default_args=args,
    schedule_interval=None,
)

print('Setup task.')
ticker = 'BTC-USD'
task1 = PythonOperator(
    task_id='run_ticker_extract_{}'.format(ticker.replace('-', '_')),
    python_callable=run_ticker_extract,
    op_kwargs={'ticker': ticker},
    dag=dag,
)

task2 = PythonOperator(
    task_id='test_func',
    python_callable=test_func,
    dag=dag,
)

print('Run task.')
task1 >> task2
