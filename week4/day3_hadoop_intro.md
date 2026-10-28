# LAB | Introduction to Hadoop and Distributed Storage
## Part 1 — Why Hadoop and Distributed Storage

### Q. 1 — Scale Up or Scale Out?
Complete the table.

```
Change	                                    Scale up or scale out?
Add more RAM to one server                  Scale up
Add four worker machines	                Scale out
Replace one CPU with a faster CPU	        Scale up
Add three storage nodes                     Scale out
```

### Q. 2 — Calculate HDFS Blocks
Use:
File size = 700 MB
Block size = 128 MB
Calculate how many HDFS blocks are needed.

```
Number of Blocks = 700 / 128 = 5,46875 --> 6 Blocks
```

### Q. 3 — Calculate Blocks with Python
Use:
File size = 1,025 MB
Block size = 128 MB
Write Python code to calculate the number of blocks.

```python
file_size = 1025
block_size = 128

number_of_blocks = file_size  // block_size
if file_size % block_size != 0:
    number_of_blocks += 1

print(f"Number of blocks: {number_of_blocks}")
```
Answer: 9

### Q. 4 — MCQ: Scaling Out
What does scaling out mean?
```
Answer:
D. Add more machines to share the work
```
## Part 2 — NameNode, DataNodes, and File Reads
### Q. 5 — Classify HDFS Responsibilities

```
A. Stores file-system metadata. -  NameNode
B. Stores actual block contents. - DataNode.
C. Tracks block locations. - NameNode
D. Sends heartbeats. - DataNode.
E. Serves block data to clients. - DataNode.
```

### Q. 6 — Trace an HDFS Read
Put these steps in order:

```
Client asks NameNode for block locations.
NameNode returns block locations.
Client reads blocks from DataNodes.
Client combines the block data.
```

### Q. 7 — Simulate Block Placement
A file has four blocks:
B1
B2
B3
B4

BritMart has three DataNodes:
DN1
DN2
DN3

Create any valid distribution where the blocks are spread across the nodes.
Then explain why spreading data helps parallel processing
```
DataNode	Blocks
DN1	        B1, B4
DN2	        B2
DN3	        B3

Let’s assume that all four blocks need to be processed.
If they are located on different DataNodes, multiple machines can process different blocks simultaneously. This is called parallel processing.
For example:
- DN1 processes B1.
- DN2 processes B2.
- DN3 processes B3.
Afterward, the results can be combined.
```
### Q. 8 — MCQ: NameNode
What does the NameNode mainly store?

```
Answer: A. File-system metadata and block-location information 
```

## Part 3 — Small Files and Data Locality
### Q. 9 — Compare Two File Layouts
BritMart has the same 10 GB of data in two designs.
Design A
100 files
Design B
1,000,000 files
Which design creates more HDFS metadata pressure and why?

```
Answer:
Design B — 1,000,000 files
The NameNode must track the metadata for each file, as well as information about its blocks. A million files generate significantly more metadata than 100 files, even if the total data size is the same.
It is small-files problem.
```
### Q. 10 — Calculate Metadata Entries Conceptually
Assume:
Layout A = 10 files
Each file uses 2 blocks
Layout B = 1,000 files
Each file uses 1 block

Calculate the number of block entries that must be tracked in each layout.

```
Layout A:
10 × 2 = 20 block entries
 
Layout B:
1,000 × 1 = 1,000 block entries
```

### Q. 11 — Explain Data Locality
A processing task needs block B3.
Option A
Run the task on a machine that already stores B3.
Option B
Run it on another machine and transfer B3 across the network.

Which option better represents data locality, and why?

```
Answer: Option A.
In Option A, the data is already on the required machine. There is no need to transfer it over the network to another machine. This can reduce network traffic and speed up processing.
```
### Q. 12 — MCQ: Small Files
Why can millions of tiny files be inefficient in HDFS?

```
Answer:
 C. Every file and block creates metadata and processing overhead
``` 

## Part 4 — Replication, Failure, and Rack Awareness
### Q. 13 — Calculate Replicated Storage
Use:
File size = 700 MB
Replication factor = 3
Calculate the total amount of file data stored across replicas.

```
700 MB × 3 = 2,100 MB
```

### Q. 14 — Calculate Storage for Three Files
Use:
files_mb = [100, 250, 400]
replication_factor = 3

Write Python code to calculate:
original total
replicated total

```python
files_mb = [100, 250, 400]
replication_factor = 3

original_total = sum(files_mb)
replicated_total = original_total * replication_factor

print("Original total:", original_total, "MB")
print("Replicated total:", replicated_total, "MB")
```
### Q. 15 — Trace a DataNode Failure
Put these events in order:

```
DataNode stops sending heartbeats.
NameNode marks DataNode unavailable.
NameNode identifies under-replicated blocks.
Replacement replicas are created.
```

### Q. 16 — MCQ: Rack Awareness
Why place replicas across different racks?

```
Answer:
 B. To keep data available during a rack-level failure 
```

## Optional Practice
### Q. 17 — Compare Two Replication Choices
A 5 TB dataset can use:
replication factor 2
replication factor 3
Calculate approximate stored data for both choices and explain the trade-off.

```
RF 2:
5 TB × 2 = 10 TB
 
RF 3:
5 TB × 3 = 15 TB
```

### Q. 18 — Diagnose a Poor HDFS Layout
BritMart stores:
2 million files
average file size = 20 KB
Most jobs read thousands of files at a time.
Suggest two improvements using only concepts covered today.

```
Improvement 1 — Combine many small files into larger files to reduce NameNode metadata overhead.
Improvement 2 - Use data locality by running processing tasks close to the DataNodes that store the required blocks.
```
### Q. 19 — Design Replica Placement
BritMart has two racks:
Rack A: DN1, DN2
Rack B: DN3, DN4
A block needs three replicas.
Suggest one placement that survives the loss of either rack better than placing all three replicas in Rack A.

```
Replica 	DataNode	Rack
Replica 1	DN1	        Rack A
Replica 2	DN2	        Rack A
Replica 3	DN3	        Rack B
```

### Q. 20 — Build a Capacity Calculation
Use:
Original data = 12 TB
Replication factor = 3
Cluster raw storage = 48 TB
Calculate:
replicated data size
remaining raw capacity
Ignore system overhead for this exercise.

```
Replicated data:
12 TB × 3 = 36 TB
 
Remaining capacity:
48 TB - 36 TB = 12 TB
```
 