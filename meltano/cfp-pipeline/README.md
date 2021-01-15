# What is this?
This is the meltano managed data pipeline.  It uses the meltano tool to organize ELT taps, targets, dbt transforms, and airflow pipelines.  It can also help automate reports.

## Setup
You'll first want to get meltano.  To use a docker image add this alias if you want to run it from the command line.   However, take a look further down to see how to use `docker-compose` so you can have it connect to a postgres database and airflow easily.

    alias meltano='docker run -it --rm -p 5000:5000 -v ${PWD}:/usr/local/share/melt -w /usr/local/share/melt meltano/meltano:latest-python3.8 $@'

If you would rather install it locally, then follow the instructions on https://meltano.com/docs/getting-started.html#install-meltano

### Docker-Compose
The docker-compose tool helps to set up all the networking across services run in docker.  There is a `docker-compose.meltano.yml` file in the root of the repo so you can easily start up meltano and postgres and then use the UI so you can see what is happening and still use the command line.

#### Configuration
There are a few configuration settings you want to sent in a `.env` file:

    DEFAULT_USER=postgres
    DEFAULT_PASSWORD=<some password for your db>

### Start the services

To start up the files run:

    docker-compose -f docker-compose.meltano.yml up

This starts the postgres datbase and the meltano ui.   The UI runs at http://localhost:5000

You can run meltano commands in a shell by doing this:

    docker-compose -f docker-compose.meltano.yml --rm run --entrypoint=bash meltano

You can connect to the running postgres database by running this (you will need to know the postgres password you set in your `.env` file):

    docker-compose -f docker-compose.meltano.yml --rm run postgres psql -h postgres -U postgres

## Getting started
After you clone/pull this, you can go into `./meltano/cfp-pipeline` and type `meltano install`.  This will install all the plugins, which are taps, targets, etc.

    cd meltano/cfp-pipeline
    meltano install

## Configuration
You don't want to commit secrets to github, so the secrets are stored in `.env` files.  In the directory where the `meltano.yml` file is, create another `.env` file that has the secrets needed for the taps and targets.  It will look something like below.  The secrets in this `.env` file are named with the `TAP_name` or `TARGET_NAME` and then `_SECRET_NAME`.

    # .env file for meltano
    TAP_SLACK_TOKEN=slack_secret_token
    TAP_GITHUB_ACCESS_TOKEN=github personal access token
    TARGET_POSTGRES_POSTGRES_USERNAME=username
    TARGET_POSTGRES_POSTGRES_PASSWORD=some password

