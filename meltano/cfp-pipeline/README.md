# What is this?
This is the meltano managed data pipeline.  It uses the meltano tool to organize ELT taps, targets, dbt transforms, and airflow pipelines.  It can also help automate reports.

## Setup
Meltano is part of the docker-compose.yml file, so you can connect to the UI by going to http://localhost:5000 after `docker-compose up`.

#### Configuration
There are a few configuration settings you want to sent in a `.env` file:

    DEFAULT_USER=postgres
    DEFAULT_PASSWORD=<some password for your db>

## Configuration
You don't want to commit secrets to github, so the secrets are stored in `.env` files.  In the directory where the `meltano.yml` file is, create another `.env` file that has the secrets needed for the taps and targets.  It will look something like below.  The secrets in this `.env` file are named with the `TAP_name` or `TARGET_NAME` and then `_SECRET_NAME`.

    # .env file for meltano
    TAP_SLACK_TOKEN=slack_secret_token
    TAP_GITHUB_ACCESS_TOKEN=github personal access token
    TARGET_POSTGRES_POSTGRES_USERNAME=username
    TARGET_POSTGRES_POSTGRES_PASSWORD=some password

