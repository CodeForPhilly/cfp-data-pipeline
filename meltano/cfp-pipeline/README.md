# What is this?
This is the meltano managed data pipeline.  It uses the meltano tool to organize ELT taps, targets, and airflow pipelines, it can also help automate reports.

## Setup
You'll first want to get meltano.  To use a docker image add this alias:

    alias meltano='docker run -it --rm -p 5000:5000 -v ${PWD}:/usr/local/share/melt -w /usr/local/share/melt meltano/meltano:latest-python3.8 $@'

If you would rather install it locally, then follow the instructions on https://meltano.com/docs/getting-started.html#install-meltano

## Getting started
After you clone/pull this, you can go into `./meltano/cfp-pipeline` and type `meltano install`.  This will install all the plugins, which are taps, targets, etc.

    cd meltano/cfp-pipeline
    meltano install

## Configuration
You don't want to commit secrets to github, so the secrets are stored in `.env` files.  TODO: how to get secrets needed to run.
