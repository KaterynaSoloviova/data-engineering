import duckdb

con = duckdb.connect("/Users/katerynasoloviova/Documents/ironhack_DE/airflow_dbt/airflow/data/warehouse.duckdb")
print(con.execute("SELECT * FROM main.example_model").fetchdf())
