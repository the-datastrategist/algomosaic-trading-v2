FROM puckel/docker-airflow:1.10.6
RUN pip install --user psycopg2-binary
ENV AIRFLOW_HOME=/usr/local/airflow

# add persistent python path (for local imports)
ENV PYTHONPATH "/home/jovyan/algomosaic:${AIRFLOW_HOME}"

COPY ./airflow.cfg /usr/local/airflow/airflow.cfg

# testing this
CMD ["airflow initdb"]
