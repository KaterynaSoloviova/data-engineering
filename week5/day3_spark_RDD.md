## Apache Spark RDD – Theory Questions
### 1. What is an RDD? Explain the meaning of "Resilient," "Distributed," and "Dataset" in Resilient Distributed Dataset.
```
An RDD (Resilient Distributed Dataset) is a fundamental data structure in Apache Spark. It is a collection of data divided into partitions that can be processed in parallel across multiple machines.
- Resilient means that Spark can recover lost data using lineage and recompute lost partitions.
- Distributed means that data is divided into partitions and distributed across multiple machines.
- Dataset means a collection of data elements.
RDDs allow Spark to process large datasets in parallel and recover from failures.
```

### 2. Explain the difference between transformations and actions in RDDs. Give two examples of each.
```
Transformations are operations that create a new RDD from an existing RDD. They are lazy, which means they do not execute immediately.

Examples:
- map() — transforms each element.
- filter() — selects elements that satisfy a condition.
Actions trigger the execution of transformations and return a result or save data.

Examples:
- collect() — returns all elements to the driver.
- count() — returns the number of elements.
```

### 3. What is lazy evaluation in Spark? Why does Spark use it, and how does it benefit RDD processing?
```
Lazy evaluation means that Spark does not execute transformations immediately. Instead, it builds an execution plan and waits until an action is called.

Spark uses lazy evaluation to optimise execution.

Benefits:
- Combines operations when possible.
- Avoids unnecessary computations.
- Improves performance.
- Creates a more efficient execution plan.
```

### 4. What is RDD lineage (DAG)? How does it help Spark achieve fault tolerance without replicating data?
```
RDD lineage is the record of transformations used to create an RDD. It is represented as a Directed Acyclic Graph (DAG).

It helps Spark recover lost partitions. If a partition is lost because of a failure, Spark can use lineage to recompute it from the original data and previous transformations.

This provides fault tolerance without requiring every intermediate RDD to be replicated.
```

### 5. Differentiate between narrow and wide transformations. Why do wide transformations cause a shuffle?
```
Narrow transformations are operations where each output partition depends on a limited number of input partitions, usually one. They do not normally require data redistribution.

Examples:
- map()
- filter()
Wide transformations are operations where data from multiple input partitions must be redistributed between partitions.

Examples:
- groupByKey()
- reduceByKey()
- repartition()
Wide transformations cause a shuffle because Spark needs to move data across partitions, usually to bring related records together.
```

### 6. Which is better, Python or Scala while working with Spark?
```
Both Python and Scala can be used with Apache Spark.
- Scala is Spark's native language and can provide better integration with Spark's internal APIs.
- Python is easier to learn for many beginners and is widely used in data engineering and data science through PySpark.
For most beginners, Python is a good choice because it has simple syntax and many useful libraries.
```

### 7. What is the difference between SparkSession and SparkContext?
```
SparkSession is the main entry point for working with Spark SQL and DataFrames. It allows users to read data, create DataFrames, execute SQL queries, and write data.

SparkContext is a lower-level component that provides access to Spark Core functionality, including RDD operations and distributed execution.

In modern Spark applications, SparkSession is usually created first, and SparkContext can be accessed through it using spark.sparkContext.
```

### 8. What is the difference between RDD and DataFrames?
```
RDD and DataFrame are distributed data structures in Apache Spark.

RDD:
- A distributed collection of objects.
- Does not require a predefined schema.
- Provides low-level control.
- Has fewer automatic optimisations.
DataFrame:
- A distributed collection of rows with named columns.
- Has a schema.
- Supports SQL and structured operations.
- Uses Catalyst Optimizer for query optimisation.
DataFrames are generally preferred for structured data processing because they are easier to use and can be optimised more efficiently.
```

### 9. What is a driver program? What is Spark Driver?
```
The Spark Driver is the main process of a Spark application.

It:
- Runs the main application code.
- Creates the SparkSession and SparkContext.
- Builds execution plans.
- Divides jobs into stages and tasks.
- Schedules tasks on executors.
- Monitors the execution and collects results.
The driver coordinates the application, while executors perform the distributed data processing.
```

### 10. Where does Spark store the data?
```
Spark does not require all data to be stored in one specific location.

It can read data from different storage systems, such as:
- Local file systems.
- HDFS (Hadoop Distributed File System).
- Amazon S3.
- Azure Data Lake Storage.
- Other compatible storage systems.
During execution, Spark processes data in partitions on executors. Intermediate data can be stored in memory or on local disks. If caching is used, Spark can keep data in memory or use disk depending on the storage level.

The final results can be written back to external storage systems such as HDFS, S3, or Parquet files.
```