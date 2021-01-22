# Meltano
This is the Meltano managed project folder. We use it to organize ELT taps and targets. It can also help automate reports and handle dbt transforms. The `meltano.yaml` file holds all information about the taps and targets we use, and the jobs we run with them.

Meltano impressively gets our data from tap to target, handling state and more. We use Meltano to extract data from different sources and load it into our data warehouse. 

## Meltano with Airflow

Our implementation of Meltano runs in a single Airflow DAG named `meltano`. By adding taps, targets, and schedules to `meltano.yaml`, we can easily use Meltano to extract and load data from tap to target, and Airflow will automatically add these additional jobs to the `meltano` DAG.

The benefit of housing Meltano jobs in a single DAG is that subsequent DAGs can depend on the `meltano` DAG as whole, or on specific tasks in the DAG if needed.

## Setup

When you run `docker-compose up`, Docker will add a `.meltano` folder in the your `meltano` directory and install extractors (e.g. Github) and loaders (e.g. Postgres).

You can connect to the UI by going to http://localhost:5000 after `docker-compose up`, but note the `meltano` service in `docker-compose.yml` is not required for Meltano to work with Airflow.

#### Configuration
For our current implementation, there are a few configuration settings you must save in a `.env` file that lives in the directory with `docker-compose.yml`:

    # .env file
    DEFAULT_USER=<username>
    DEFAULT_PASSWORD=<password>
    TAP_SLACK_TOKEN=<slack_secret_token>
    TAP_GITHUB_ACCESS_TOKEN=<github_PAT>
    TARGET_POSTGRES_POSTGRES_USERNAME=<username>
    TARGET_POSTGRES_POSTGRES_PASSWORD=<password>
    MELTANO_PROJECT_ROOT=/usr/local/meltano/cfp-pipeline
