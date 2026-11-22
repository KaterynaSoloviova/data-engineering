## Q6 - Difference between RDD and DataFrame

RDD is a distributed collection of objects that does not require
a predefined tabular structure.

DataFrame is a distributed collection of data organized into
named columns and rows, similar to a table.

DataFrames have a schema and are optimized by Spark's Catalyst
optimizer. RDDs provide more low-level control, while DataFrames
are generally easier and more efficient for structured data processing.