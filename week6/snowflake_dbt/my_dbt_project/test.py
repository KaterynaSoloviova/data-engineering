python - <<'PY'
import os
import snowflake.connector

try:
    conn = snowflake.connector.connect(
        account="RXJMGUH-CI44129",
        user="soloviova.kateryna",
        authenticator="PROGRAMMATIC_ACCESS_TOKEN",
        token=os.environ["DBT_SNOWFLAKE_PAT"],
        role="DBT_ROLE",
        warehouse="DBT_WH",
        database="DBT_DB",
        schema="DEV_KATERYNA",
    )
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_USER(), CURRENT_ROLE()")
    print("SUCCESS:", cur.fetchone())
    conn.close()
except Exception as e:
    print("CONNECTION FAILED:", type(e).__name__, str(e))
PY