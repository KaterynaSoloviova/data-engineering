# Hive, Avro, Parquet, Sqoop, and Impala

## Q1. Create an external table in the default database on accounts .
1. Run the following statement in Hive

```sql
create external table accounts
(
acct_id int,
user_name string,
acct_city string,
acct_open_date date

);
````
Because this is an external table, Hive does not manage the underlying
data in the same way it manages a managed table. In this example, no
LOCATION is specified, so Hive uses the default warehouse location for
the table.

2. Verify the table in Hive:

``sql
describe accounts;
```

## Q2. Create an avro external table on accounts avro
-- Check for the .avsc file: 
```sql
ls
````

-- put the .avsc file from local to HDFS storage:

```
hdfs dfs -put /home/training/accounts.avsc /data_formats/
```
-- Create the external table in Hive:

```
    create external table accounts_avro
    stored as AVRO
    location '/data_formats/avro_files'
    tblproperties (
    'avro.schema.url' = 'hdfs:///data_formats/accounts.avsc'
    );
```
The table uses the Avro schema stored at /data_formats/accounts.avsc,
while the Avro data files are expected in /data_formats/avro_files.

Verify the table definition:

```sql
DESCRIBE FORMATTED accounts_avro;
```

## Q3. Create a Parquet Table on accounts.parquet

In the Hive environment used for this exercise, creating a Parquet table
with a DATE column caused the following error:

- UnsupportedOperationException: Parquet does not support date. See HIVE-6384

This is a compatibility issue associated with the Hive/Parquet versions
in that environment. Support for Parquet DATE values depends on the
versions and configuration being used.

As a workaround for this environment, the date columns were defined as
BIGINT:
```sql
CREATE external table accounts_parquet(
acct_num int,
acct_create_dt BIGINT,
acct_close_dt BIGINT,
first_name string,
last_name string,
address string,
city string,
state string,
zipcode string,
phone_number string,
created BIGINT,
modified BIGINT

)
stored as parquet
location '/data_formats/accounts_parquet';
```
## Q4. Import directly through sqoop table called ‘basestations’ into Hive.

- Run the following command in the terminal:
```
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table basestations \
  --hive-import
```
Sqoop connects to the loudacre MySQL database, imports the
basestations table, and creates or populates a corresponding Hive
table through --hive-import.

Verify the imported table in Hive:
```sql
SHOW TABLES LIKE 'basestations';
DESCRIBE basestations;
```
## Q5. Import only first name and last name using sqoop in hdfs for table accounts . The table should be reflected on Hive/Impala.

1. Import the selected columns with Sqoop

The following example imports only the two requested columns and writes
text data to the HDFS directory /Loudacre/customer_names:

```sql
sqoop import \
  --connect jdbc:mysql://localhost/loudacre \
  --username training \
  --password training \
  --table accounts \
  --columns first_name,last_name \
  --target-dir /Loudacre/customer_names \
  --as-textfile \
  --fields-terminated-by ' ' \
  --delete-target-dir
```
--columns selects only first_name and last_name. The field
separator is set to a space so that it matches the Hive table definition
below. --delete-target-dir removes an existing target directory before
importing; use it only if replacing the existing data is intended.

2. Create an external Hive table

```sql
CREATE EXTERNAL TABLE customer_names_fixed (
    first_name STRING,
    last_name  STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
STORED AS TEXTFILE
LOCATION '/Loudacre/customer_names';
```
The Hive table points to the HDFS directory populated by Sqoop. Since
the table is external, it references the existing files rather than
importing the data again.

Verify the data:
```sql
DESCRIBE customer_names_fixed;

SELECT *
FROM customer_names_fixed
LIMIT 10;
```
3. Make the table available in Impala
If Hive and Impala use the same metastore, refresh Impala's metadata
after creating the Hive table:

```sql
SELECT *
FROM customer_names_fixed
LIMIT 10;
```

## Q6. Run a query on hive and impala both : group the accounts on the basis of city and order them by their names in alphabetical order . 

1. Group the account records by city and display the first names for each
city in alphabetical order.

Hive solution:
Hive supports collecting values into an array, sorting the array, and
joining the values into a string:
```sql
SELECT
    city,
    CONCAT_WS(', ', SORT_ARRAY(COLLECT_LIST(first_name))) AS account_names
FROM accounts
GROUP BY city
ORDER BY city ASC;
How it works:
- COLLECT_LIST(first_name) collects the first names for each city
  into an array.
- SORT_ARRAY(...) sorts the array in ascending order.
- CONCAT_WS(', ', ...) joins the sorted names into one
  comma-separated string.
- GROUP BY city produces one result row per city.
- ORDER BY city ASC sorts the result rows by city name.
```

2. If the requirement is to display each account as a separate row rather
than combine names into one string, use:

```sql
SELECT
    city,
    first_name,
    last_name
FROM accounts
ORDER BY city ASC, first_name ASC, last_name ASC;
Impala solution
A straightforward Impala aggregation is:
SELECT
    city,
    GROUP_CONCAT(first_name, ', ') AS account_names
FROM accounts
GROUP BY city
ORDER BY city ASC;
```
GROUP_CONCAT combines the first names for each city into a comma-separated string. However, this query does not guarantee alphabetical ordering of the names inside each concatenated string.
The outer ORDER BY city sorts the city rows, not the names within each group.
To guarantee alphabetical row order in Impala, return one account per
row:

```sql
SELECT
    city,
    first_name,
    last_name
FROM accounts
ORDER BY city ASC, first_name ASC, last_name ASC;
```
In the tested environment, the Impala query completed faster than the
equivalent Hive query. This is an observation from that execution, not a
universal rule: performance depends on data size, cluster resources,
file format, metadata, and query design.
