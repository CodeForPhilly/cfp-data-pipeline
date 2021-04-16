FROM rocker/ml
USER root

# PSQL Requirements
RUN apt-get update \
    && apt-get install -y libpq-dev build-essential unixodbc libpq-dev libnss3-tools

# R Requirements
RUN Rscript -e 'install.packages("odbc")'
RUN Rscript -e 'install.packages("snakecase")'
RUN Rscript -e 'remotes::install_github(c("dgrtwo/dbcooper"))'
RUN Rscript -e 'remotes::install_github(c("machow/dbpath", "codeforphilly/cfpr"))'

# Python Requirements
ADD airflow/requirements.txt .
RUN pip3 install -r requirements.txt

# Install snowflake odbc driver ---
RUN wget \
    https://sfc-repo.snowflakecomputing.com/odbc/linux/latest/snowflake-odbc-2.23.0.x86_64.deb \
    -O snowflake-odbc.deb

RUN dpkg -i snowflake-odbc.deb \
    && apt-get install -f -y \
    && sed -i 's/SnowflakeDSIIDriver/Snowflake/g' /etc/odbcinst.ini


# Create venv for meltano, install taps in virtualenvs ----
ENV MELTANO_PROJECT_ROOT=/usr/local/meltano/cfp-pipeline

ADD meltano/cfp-pipeline ${MELTANO_PROJECT_ROOT}

RUN virtualenv -p python3 /usr/local/venv/meltano
RUN . /usr/local/venv/meltano/bin/activate \
    && pip3 install meltano \
    && cd /usr/local/meltano/cfp-pipeline \
    && meltano install


# Airflow Env Vars
ENV AIRFLOW_HOME='/usr/local/airflow'

# Set wd
WORKDIR /usr/local/airflow

# Sleep forever
CMD sleep infinity
