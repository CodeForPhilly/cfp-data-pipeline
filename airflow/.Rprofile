require("stats")   # required for dplyr to attach filter correctly...
require("dplyr")
require("glue")
require("dbcooper")
require("dbpath")

# setup dbs...
cfp_tbl <- dbcooper::dbc_init(
    DBI::dbConnect(dbpath::dbpath(Sys.getenv("AIRFLOW_CONN_POSTGRES_DEFAULT"))),
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
