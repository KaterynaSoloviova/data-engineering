# Week 5 — Day 4: Apache Spark Foundations — Lab

## Part 1 — Spark Applications, Drivers, and Executors
### Q. 1 — Driver or Executor?
```
Classify each responsibility.
A. Creates the Spark application. - driver
B. Builds the execution plan. - driver
C. Runs tasks on data partitions. - executor
D. Stores cached partition data. - executor
E. Coordinates work across executors. - driver
```
### Q. 2 — Trace a Spark Application
```
Put these steps in order:
Executors run tasks - 4
Driver creates the Spark application - 1
Cluster manager allocates resources - 2
Driver sends work to executors - 3
Executors return status or results - 5
```
### Q. 4 — MCQ: Spark Driver
```
What is the main job of the Spark driver?
Answer: A. Coordinate the application and plan its work
```
## Part 2 — Cluster Managers, Local Mode, SparkSession, and RDDs
### Q. 5 — Local or Cluster?
```
Choose the better mode.
A. Small demonstration on one laptop. - local
B. Production processing across many machines. - cluster
C. Testing basic syntax during training. - local
D. Shared processing of several terabytes. - cluster
```
### Q. 6 — Read a Local Master Setting
```
Explain:
.master("local[4]")
What does the 4 mean?
Answer: ‘The 4 means "use 4 CPU cores on my local computer."‘
```
### Q. 8 — MCQ: Cluster Manager
```
What does a Spark cluster manager mainly allocate?
Answer: D. CPU and memory resources
```
## Part 3 — DataFrames, Transformations, and Actions
### Q. 9 — Identify Transformations and Actions
```
Classify:
filter() - transformations
select() - transformations
show() - actions
count() - actions
withColumn() - transformations
write.parquet() - actions
```
### Q. 12 — MCQ: Action
```
Which operation triggers Spark execution?
Answer: B. show()
```
## Part 4 — Lazy Evaluation, Jobs, Stages, Tasks, and Shuffles
### Q. 13 — Explain Lazy Evaluation
```
Review:
completed = orders.filter("status = 'complete'")
selected = completed.select("city", "amount_gbp")
No action has run.
What has Spark done so far?

Here is what is happening under the hood:

- Building a Blueprint (Execution Plan): When you run .filter() and .select(), Spark does not look at a single row of your data. Instead, it just writes down the instructions: "Okay, first filter rows where status is complete, then grab only the city and amount_gbp columns."

- Waiting for an Action: Spark stores these instructions into a logical plan. It sits and waits patiently until you call an action (like .show(), .count(), .collect(), or .write()).
```
### Q. 14 — Job, Stage, Task, or Partition?
```
Match each term:

A. Work created when an action triggers execution. - Job (Created every time we run an action (like .count() or .show()). If we run three actions, you trigger three jobs)

B. A group of tasks separated by shuffle boundaries. - Stage (A job is broken down into stages. Stages are separated by shuffles (moments where data has to be reshuffled or sent across different network computers, like when we do a GROUP BY or a JOIN).)

C. One unit of work on one partition. - Task (This is the actual work being done on a single partition. If a stage has 100 partitions, Spark will launch 100 individual tasks to process them in parallel.)

D. A logical slice of distributed data. - Partition (This is a chunk of our dataset. If we have a 100 GB file, Spark splits it into pieces (e.g., 100 partitions of 1 GB each) so multiple computers can work on it at the same time.)
```
### Q. 15 — Identify Shuffle Operations
A shuffle is when Spark has to move data across the network from one computer (or CPU core) to another

```
Choose whether a shuffle is likely.

filter rows by status - No shuffle (Each partition can filter its own rows independently.)
select two columns - No shuffle (Dropping columns is a local operation; no data needs to move.)
groupBy city - Shuffle (Rows with the same city from all different partitions must be gathered together to calculate the group.)
join two large DataFrames by customer_id - Shuffle (Matching customer IDs from both datasets must be sent across the network to meet each other.)
repartition by city - Shuffle (This is an explicit shuffle command designed to redistribute data across partitions based on the city column.)
```
### Q. 16 — MCQ: Shuffle
```
Which operation commonly causes a shuffle?
Answer:  C. groupBy("city") 
```
## Optional Practice
### Q. 18 — Calculate Tasks from Partitions
```
A stage processes: 12 partitions
Assume one task is created per partition.
How many tasks are created in that stage?
Answer: 12 partitions = 12 tasks
```
### Q. 19 — Find the Driver Risk
A DataFrame contains: 50 million rows
A developer runs: rows = df.collect()
Explain the risk.
Answer:

```
The risk is an ‘Out of Memory (OOM)‘ error on the driver node, which will crash your program.
The `.collect()` action tells Spark to pull all 50 million rows from the distributed workers across the cluster and copy them all at once into the memory (RAM) of a single computer (the driver node). 50 million rows will almost certainly overwhelm the driver's memory limit, causing it to run out of RAM and fail.
Instead of `.collect()`, you should use `.show()`, `.take(5)`, or write the results directly to storage/disk if you need to inspect that much data.
```
### Q. 20 — Compare Two Spark Pipelines
Pipeline A: filter -> select -> show
Pipeline B: groupBy -> aggregation -> show
Which pipeline is more likely to contain a shuffle and why?
Answer:
```
Pipeline B (groupBy -> aggregation -> show) is much more likely to contain a shuffle.

Why?
Pipeline B (groupBy): To group data by a specific key (like city or category), Spark must collect all rows sharing that same key from every different partition and bring them together. This requires moving data across the network, which triggers a shuffle.

Pipeline A (filter -> select): Both filtering rows and selecting columns happen entirely locally inside each partition. Every partition can filter and drop columns on its own data without needing to talk to or share data with other partitions, meaning no shuffle occurs.
```



