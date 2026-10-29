## HDFS & Distributed Systems – MCQ Quiz 

### Q.1 What does HDFS stand for?
Answer: b) Hadoop Distributed File System

### Q.2 In HDFS, what is the default block size in Hadoop 2.x and later?
Answer: c) 128 MB

### Q.3 Which component of HDFS is responsible for storing metadata about files and blocks?
Answer: b) NameNode

### Q.4 What is the default replication factor in HDFS?
Answer: c) 3

### Q.5 What is the primary role of the Secondary NameNode?
Answer: b) Periodically merges the FsImage and EditLogs

### Q.6 Which of the following best describes the CAP theorem?
Answer: b) A distributed system can only guarantee at most two of Consistency, Availability, and Partition toleranc

### Q.7 In HDFS architecture, what is a "rack awareness" policy used for?
Answer: b) Optimizing network bandwidth and improving fault tolerance by considering node placement

### Q.8 Which protocol does HDFS primarily use for communication between client and NameNode?
Answer: c) RPC (Remote Procedure Call) (SSH)

### Q.9 What happens when a DataNode fails in HDFS?
Answer: b) The NameNode detects it via missed heartbeats and re-replicates blocks to other DataNodes

### Q.10 In distributed systems, what is "eventual consistency"?
Answer: b) Given enough time without new updates, all replicas will converge to the same value

### Q.11 What is the purpose of the "heartbeat" mechanism in HDFS?
Answer: b) To signal that a DataNode is alive and functioning to the NameNode

### Q.12 Which of the following is a single point of failure in classic (non-HA) HDFS architecture?
Answer: b) NameNode

### Q.13 What is "write-once-read-many" (WORM) in the context of HDFS?
Answer: b) A file access model where files are written once and read multiple times without modification




