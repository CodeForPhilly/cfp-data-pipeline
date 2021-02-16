from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy_utils import create_database, database_exists
import sqlalchemy
import os

uri = PostgresHook.get_connection('postgres_default').get_uri()
engine = sqlalchemy.create_engine(uri)

# create database
if not database_exists(engine.url):
    create_database(engine.url)
    engine.execute("GRANT ALL PRIVILEGES ON DATABASE {db} TO {user};".format(user = engine.url.username, db = engine.url.database))
    engine.execute("CREATE ROLE analysis WITH PASSWORD '{0}'".format(os.environ["ANALYSIS_PASSWORD"]))

# create schema, give permissions
if not engine.dialect.has_schema(engine, 'views'):
    engine.execute(sqlalchemy.schema.CreateSchema('views'))
    engine.execute("GRANT ALL PRIVILEGES ON SCHEMA views TO {user};".format(user = engine.url.username))
    engine.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA views TO {user};".format(user = engine.url.username))
    engine.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA views GRANT ALL PRIVILEGES ON TABLES TO {user};".format(user = engine.url.username))
    engine.execute("GRANT SELECT ON ALL TABLES IN SCHEMA views TO analysis")    

# separate schema for github
if not engine.dialect.has_schema(engine, 'tap_github'):
    engine.execute(sqlalchemy.schema.CreateSchema('tap_github'))
    engine.execute("GRANT ALL PRIVILEGES ON SCHEMA tap_github TO {user};".format(user = engine.url.username))
    engine.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA tap_github TO {user};".format(user = engine.url.username))
    engine.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA tap_github GRANT ALL PRIVILEGES ON TABLES TO {user};".format(user = engine.url.username))
    engine.execute("GRANT SELECT ON ALL TABLES IN SCHEMA tap_github TO analysis")

# separate schema for slack
if not engine.dialect.has_schema(engine, 'tap_slack'):
    engine.execute(sqlalchemy.schema.CreateSchema('tap_slack'))
    engine.execute("GRANT ALL PRIVILEGES ON SCHEMA tap_slack TO {user};".format(user = engine.url.username))
    engine.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA tap_slack TO {user};".format(user = engine.url.username))
    engine.execute("ALTER DEFAULT PRIVILEGES IN SCHEMA tap_slack GRANT ALL PRIVILEGES ON TABLES TO {user};".format(user = engine.url.username))
    engine.execute("GRANT SELECT ON ALL TABLES IN SCHEMA tap_slack TO analysis")
