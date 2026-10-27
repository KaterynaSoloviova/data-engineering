# Q1. ETL vs ELT Architecture 
Tasks 
1. Compare ETL vs ELT.  
ETL (Extract, Transform, Load): Data is extracted, cleaned, and transformed before loading into the database.
ELT (Extract, Load, Transform): Data is extracted, loaded into the database, and transformed there using SQL.
The main difference is when the data is transformed.

2. Explain why cloud warehouses prefer ELT.
Cloud warehouses can process large amounts of data efficiently. ELT allows raw data to be stored first and transformed later. This makes the pipeline more flexible, scalable, and easier to maintain.

3. Design modern ELT pipeline for QuickCart. 
The proposed pipeline is:
CSV files → Airflow → Python (Pandas) → PostgreSQL staging tables → SQL transformations → Analytics tables

- Extract and Validate: Python and Pandas read the CSV files and check data quality.
- Load: Load the data into PostgreSQL staging tables.
- Transform: SQL cleans and transforms the data into analytics tables.
- Orchestration: Airflow schedules and manages the Python and SQL tasks, monitors execution, and retries failed tasks.
