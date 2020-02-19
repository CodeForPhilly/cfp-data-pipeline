import os
import re
from inflection import underscore

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from gusty.templates.sql_templates import postgres_comment_table

#############
## Globals ##
#############

# csv_dir = os.path.join(os.getenv('AIRFLOW_HOME'), "dags", "csv")
# csv_files = [os.path.join(csv_dir, file) for file in os.listdir(csv_dir) if file.endswith("csv")]

###############
## Functions ##
###############

def clean_columns(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.map(lambda x: underscore(x))
    df.columns = df.columns.map(lambda x: re.sub('\'', '', x))
    df.columns = df.columns.map(lambda x: re.sub('\"', '', x))
    df.columns = df.columns.map(lambda x: re.sub('[^0-9a-zA-Z_]+', '_', x))
    df.columns = df.columns.map(lambda x: re.sub('_+', '_', x))
    return df

def upload_csv(csv_file, table_name, schema, engine):
    csv_path = os.path.join(csv_dir, csv_file)
    assert csv_path in csv_files, "CSV file " + csv_file + " does not exist in " + csv_dir

    import pandas as pd
    csv_file = pd.read_csv(csv_path)
    csv_file = clean_columns(csv_file)
    csv_file.to_sql(name=table_name,
                    con=engine,
                    schema=schema,
                    if_exists="replace",
                    index=False)

class CSVToPostgresOperator(BaseOperator):
    """Upload a CSV file from the dags/csv folder to a Postgres connection."""
    ui_color = "#fffad8"

    @apply_defaults
    def __init__(
            self,
            csv_file,
            postgres_conn_id = "postgres_default",
            schema = "views",
            **kwargs):

        self.csv_file = csv_file
        self.postgres_conn_id = postgres_conn_id
        self.schema = schema
        super(CSVToPostgresOperator, self).__init__(**kwargs)

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id = postgres_conn_id)
        engine = hook.get_sqlalchemy_engine()

        upload_csv(self.csv_file, self.task_id, self.schema, engine)
        
        # comment the table
        comment_sql = postgres_comment_table.render(task_id = self.task_id,
                                                    schema = self.schema,
                                                    fields = self.fields,
                                                    description = self.description)

        engine.run(comment_sql, autocommit = True)

