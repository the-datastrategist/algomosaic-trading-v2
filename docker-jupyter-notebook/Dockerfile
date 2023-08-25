# jupyter image
FROM jupyter/scipy-notebook

# create working dictionary
RUN rm -r work
RUN mkdir algomosaic

# install conda, mlflow, SQL db
RUN conda install --quiet --yes \
    'mlflow=1.0.0' \
    'psycopg2'

# add persistent python path (for local imports)
ENV PYTHONPATH "${PYTHONPATH}:/home/jovyan/algomosaic"

# jupyter notebook entry
RUN pip install jupyter -U && pip install jupyterlab
EXPOSE 8888
ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]