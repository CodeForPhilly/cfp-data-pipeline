FROM rocker/ml
USER root

# PSQL Requirements
RUN apt-get update && apt-get install -y libpq-dev build-essential

# R Requirements
RUN Rscript -e 'remotes::install_github(c("machow/dbpath", "dgrtwo/dbcooper"))'
RUN Rscript -e 'install.packages("snakecase")'

# Python Requirements
ADD requirements.txt .
RUN pip3 install -r requirements.txt

# Create venv for meltano
RUN virtualenv -p python3 /usr/local/venv/meltano
RUN . /usr/local/venv/meltano/bin/activate && pip3 install meltano

# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Set wd
WORKDIR /usr/local/airflow

# Sleep forever
CMD sleep infinity
