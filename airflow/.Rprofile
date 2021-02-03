require("stats")   # required for dplyr to attach filter correctly...
require("dplyr")
require("glue")
require("dbcooper")
require("dbpath")

# setup dbs...
DB_URL <- Sys.getenv("AIRFLOW_CONN_POSTGRES_DEFAULT")
if (DB_URL == "") {
  DB_URL <- glue(
      "postgresql://{DEFAULT_USER}:{DEFAULT_PASSWORD}@{DEFAULT_HOST}:{DEFAULT_PORT}/datawarehouse",
      .envir = as.list(Sys.getenv())
  )
}

cfp_tbl <- dbcooper::dbc_init(
    DBI::dbConnect(dbpath::dbpath(DB_URL)),
    "cfp"
)

cfp_create_table <- function(tbl, table_name) {
  DBI::dbWriteTable(
    cfp_src()$con,
    DBI::SQL(table_name),
    dplyr::collect(tbl),
    overwrite = TRUE,
  )
}

cfp_create_schema <- function(schema_name) {
  cfp_execute(
    glue("CREATE SCHEMA IF NOT EXISTS {schema_name} AUTHORIZATION {Sys.getenv('DEFAULT_USER')};")
  )
}
