
from pathlib import Path
import duckdb

DATA_DIR = Path(__file__).resolve().parent
CSV_FILE = DATA_DIR / "sales.csv"
DB_FILE = DATA_DIR / "sales.duckdb"

con = duckdb.connect(str(DB_FILE)) # opens the database if it exists or creates it if it doesn't

con.execute("""
    CREATE OR REPLACE TABLE sales_raw AS
    SELECT
        order_id::INTEGER AS order_id,
        customer::VARCHAR AS customer,
        city::VARCHAR AS city,
        product::VARCHAR AS product,
        quantity::INTEGER AS quantity,
        price::DECIMAL(10, 2) AS price
    FROM read_csv_auto(?, header = true)
""", [str(CSV_FILE)])

print(con.execute("SELECT * FROM sales_raw ORDER BY order_id").fetchdf())
print("Total rows:", con.execute("SELECT COUNT(*) FROM sales_raw").fetchone()[0])

con.close()