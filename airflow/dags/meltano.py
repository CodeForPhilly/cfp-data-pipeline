import os
import subprocess
import json
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

DEFAULT_ARGS = {
    "owner": "Michael Chow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "mchow@codeforphilly.org",
    "catchup": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": days_ago(1),
    "concurrency": 1,
}

project_root = os.getenv("MELTANO_PROJECT_ROOT")
meltano_bin = "/usr/local/venv/meltano/bin/meltano"

result = subprocess.run(
    [meltano_bin, "schedule", "list", "--format=json"],
    cwd=project_root,
    stdout=subprocess.PIPE,
    universal_newlines=True,
    check=True,
)

schedules = json.loads(result.stdout)

dag = DAG(
    "meltano",
    catchup=False,
    default_args=DEFAULT_ARGS,
    schedule_interval="0 0 * * *",
    max_active_runs=1,
)

for schedule in schedules:
    elt = BashOperator(
        task_id=schedule["name"],
        bash_command=f"{meltano_bin} elt {schedule['extractor']} {schedule['loader']} --job_id={schedule['name']}",
        dag=dag,
    )
