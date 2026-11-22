import snowflake.connector

conn = snowflake.connector.connect(
    account="RXJMGUH-CI44129",
    user="soloviova.kateryna",
    authenticator="OAUTH_AUTHORIZATION_CODE",
    warehouse="DBT_WH",
    database="BREWBEATS_DB",
    schema="DBT_DEV",
    role="ACCOUNTADMIN"
)

print("Successfully connected to Snowflake!")

conn.close()