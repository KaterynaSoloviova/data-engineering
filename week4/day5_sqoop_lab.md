## Week 4 Day 5: Sqoop Lab Assignement

```
Problem Scenario:
Loudacre Inc. is a leading electronics retailer
– More than 1,000 brick and mortar stores 
– Dualcore also has a thriving e-commerce Web site

Loudacre has hired you to help find value in its data 
– You will process and analyse data from internal and external sources 
– Identify opportunities to increase revenue 
– Find new ways to reduce costs
– Help other departments achieve their goals
```
## Introduction to Apache Sqoop
What is Apache Sqoop?
Apache Sqoop is a command-line tool designed to transfer data between relational databases and Hadoop.

It allows users to import data from relational databases such as MySQL, Oracle, and PostgreSQL into Hadoop, as well as export data from Hadoop back into relational databases.

Main features of Sqoop:
- Imports data from RDBMS into HDFS.
- Exports data from HDFS into RDBMS.
- Supports parallel data transfer using MapReduce.
- Allows importing specific tables, columns, and filtered records.
- Supports different data formats and field delimiters.

Sqoop Import:
The sqoop import command transfers data from a relational database into Hadoop.

General syntax:
sqoop import \
--connect jdbc:mysql://hostname/database_name \
--username username \
--password password \
--table table_name \
--target-dir /hdfs/directory

Sqoop Export:
The sqoop export command transfers data from Hadoop back into a relational database.


### Q.1 List all the databases in the RDBMS
Theory:
A Relational Database Management System (RDBMS) is software used to store, manage, and retrieve structured data.

Examples include:
- MySQL
- PostgreSQL
- Oracle Database
- Microsoft SQL Server
A database contains tables, and tables contain rows and columns.

Command:
```
mysgl> SHOW DATABASES;
```
Explanation:
The SHOW DATABASES command displays all databases available on the MySQL server.
To connect to MySQL:
mysql -u root -p
To select the Loudacre database:
USE loudacre;

### Q.2 Make a directory on HDFS named as /Loudacre
Theory
HDFS (Hadoop Distributed File System) is a distributed storage system designed to store large datasets across multiple machines.
It divides files into blocks and distributes them across the Hadoop cluster.
HDFS provides:
- Dstributed storage.
- Fault tolerance.
- High-throughput data access.
- Scalability.

Command:
```
hdfs dfs -mkdir /Loudacre
```
Explanation:
hdfs dfs – Executes an HDFS file system command.
-mkdir – Creates a new directory.
/Loudacre – Specifies the directory name and location.
Verify the directory:
hdfs dfs -ls /
The newly created /Loudacre directory should appear in the output.

### Q.3 Import accounts, accountdevice, webpage into the directory /Loudacre seperately
Theory:
- Sqoop allows us to import complete tables from an RDBMS into HDFS.
- Each table can be imported into a separate HDFS directory.
- The --table option specifies the source table, while --target-dir specifies the destination directory.

1. Import the Accounts Table
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table accounts \
--target-dir /Loudacre/accounts \
```
2. Import the Accountdevice Table
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table accountdevice \
--target-dir /Loudacre/accountdevice \
```
3. Import the Webpage Table
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table webpage \
--target-dir /Loudacre/webpage \
```
Explanation of Important Parameters:
Parameter                   Description
--connect                   Specifies the database connection URL.

--username                  Specifies the database username.

--password                  Specifies the database password.

--table                     Specifies the source table.

--target-dir                Specifies the HDFS destination directory.

Verify Imported Tables:
hdfs dfs -ls /Loudacre

### Q. 4 Import table accounts in /user/training changing the mappers to 10 and changing the field terminator to ‘:’.  Also split them on the basis of state.
Theory:
Sqoop supports parallel data imports using MapReduce.
A mapper is a processing task responsible for importing a portion of the source data.
Using multiple mappers can improve import performance because several portions of the data can be processed simultaneously.

Important Sqoop Parameters:
1. --target-dir
Defines the destination directory in HDFS.
2. --num-mappers
Specifies the number of mapper tasks.
3. --fields-terminated-by
Defines the character used to separate columns in the output files.
4. --split-by
Specifies the column used by Sqoop to calculate data splits for parallel imports.

Command:
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table accounts \
--target-dir /user/training/new_accounts \
--num-mappers 10 \
--fields-terminated-by ':' \
--split-by state
```
Explanation
Parameter                          Description
--table accounts                   Imports the accounts table.
--target-dir /user/training        Stores the imported data in this HDFS directory.
--num-mappers 10                   Uses 10 mapper tasks.
--fields-terminated-by ':'         Separates fields using a colon.
--split-by state                   Uses the state column to calculate the import splits.

### Q.5 Import the Complete names of people having accounts in Loudacre  ex: firstname <space> last_name ex: Britney Spears.
Theory:
Sometimes we do not need to import an entire database table.
Sqoop provides the --query option, which allows us to execute a custom SQL query and import only the required information.
In this task, we combine the first name and last name into a complete name.

Command:
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table accounts \
--columns first_name, last_name
--target-dir /Loudacre/customer_names\
--fields-terminated-by '' \
```

### Q.6 Import only those records where device_id is between 10 and 50  in table accountdevice.
Theory:
SQL provides the WHERE clause to filter records based on specific conditions.
The BETWEEN operator selects values within a specified range.
The BETWEEN operator includes both boundary values.

For example:
SELECT *
FROM accountdevice
WHERE device_id BETWEEN 10 AND 50;

This query returns records where:
device_id >= 10 AND device_id <= 50

Sqoop Command:
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training \
--table accountdevice \
--where "device_id BETWEEN 10 AND 50" \
--target-dir /Loudacre/filtered_devices\
```

### Q.7 Copy the  acct no.from the table customerservicerep where customer name is Roger Miller.
Theory:
Sqoop supports importing selected columns and filtered records using the --query option.
This is useful when we need only specific information rather than an entire database table.
SQL uses the SELECT statement to retrieve columns and the WHERE clause to filter records.

SQL Query:
SELECT acct_no
FROM customerservicerep
WHERE customer_name = 'Roger Miller';

Sqoop Command:
```
sqoop import \
--connect jdbc:mysql://localhost/loudacre \
--username training \
--password training\
--query "SELECT acct_no FROM customerservicerep WHERE customer_name = 'Roger Miller'\
--target-dir /Loudacre/roger_miller \
```
