
# Apache NiFi 

## 1. Flow-Based Processing (ETL / ELT)

Apache NiFi is a data integration tool that moves, processes, and transfers data between different systems. It automates ETL and ELT processes.

- **ETL (Extract, Transform, Load):** First collect data, then change it, and finally save it in the target system.
- **ELT (Extract, Load, Transform):** First collect data, save it in the target system, and then transform it.

**Example:** Get customer data from a CSV file, change its format, and send it to a database.

## 2. Dataflow

A dataflow is the path that data follows through NiFi.

- Consists of connected processors and queues.
- Defines where data comes from, how it is processed, and where it goes.
- Can contain many different processing steps.

**Example:** Read a file → Filter data → Convert it → Save it in a database.

## 3. FlowFile

A FlowFile is the basic unit of data that moves through NiFi.

It consists of two parts:

- **Attributes:** Information about the data (metadata).
- **Content:** The actual data.

**Example:** A CSV file uploaded to NiFi becomes a FlowFile.

**Remember:** FlowFile = Content + Attributes.

## 4. Processor

A processor is a component that performs a specific task on a FlowFile.

Examples:
- Read data from a file or database.
- Filter unwanted data.
- Change data formats.
- Send data to another system.
- Delete or split data.

Each processor has different settings and relationships.

**Example:**
- `GetFile` reads files from a folder.
- `PutFile` writes files into a folder.

## 5. Processor Group (Process Group)

A Process Group is a container that holds multiple processors and connections.

- Organizes large dataflows into smaller parts.
- Makes complex flows easier to understand.
- Can contain input and output ports.
- Helps reuse and manage parts of a flow.

**Example:** One Process Group collects data, another transforms it, and another stores it.

## 6. Funnel

A Funnel combines multiple incoming connections into one outgoing connection.

- Collects FlowFiles from different processors.
- Does not change the content or attributes.
- Makes a dataflow cleaner and easier to read.

**Example:** Three processors send their FlowFiles into one Funnel, which connects to another processor.

## 7. Attribute

An attribute is metadata that describes a FlowFile.

It contains information about the FlowFile, not the actual data.

Examples:
- `filename` – Name of the file.
- `filesize` – Size of the file.
- `mime.type` – Type of file.
- `path` – File location.

Attributes can be used to filter, identify, and route FlowFiles.

**Example:** Send only FlowFiles with the attribute `filename = customers.csv` to a specific processor.

## 8. Content

Content is the actual data stored inside a FlowFile.

It can contain:
- Text
- JSON
- XML
- CSV
- Images
- Binary data

Processors can read, modify, split, or replace the content.

**Example:** The content of a FlowFile could be a CSV table containing customer information.

**Remember:**
- Attribute = Information about the data.
- Content = Actual data.

## 9. Queue (Connection)

A queue is a temporary storage between two processors.

- Stores FlowFiles until the next processor is ready.
- Connects processors together.
- Allows processors to work at different speeds.
- Has limits for the number and size of FlowFiles.

Queues also support Back Pressure.

**Example:** If Processor 1 produces 100 FlowFiles but Processor 2 can process only 20, the remaining FlowFiles wait in the queue.

## 10. Data Provenance

Data Provenance tracks the history of a FlowFile.

It shows:
- Where the FlowFile came from.
- Which processors handled it.
- What operations were performed.
- Where the FlowFile was sent.

**Why is it useful?**
- Finding errors.
- Debugging dataflows.
- Auditing data.
- Understanding how data was processed.

**Example:** You can check why a customer record was sent to the wrong destination.

## 11. Penalty

Penalty temporarily delays the processing of a specific FlowFile.

- The FlowFile stays in the queue.
- It cannot be processed immediately.
- After the penalty period, it becomes available again.

**Example:** An external service is temporarily unavailable, so NiFi penalizes the FlowFile instead of processing it immediately again.

**Remember:** Penalty affects a FlowFile.

## 12. Yield

Yield temporarily pauses a processor.

- Prevents the processor from running repeatedly.
- Gives the system time to recover.
- Often happens when a processor cannot perform its task.

**Example:** A processor cannot connect to an external database, so it yields before trying again.

**Remember:** Yield affects the processor, not just one FlowFile.

## 13. CRON Jobs / Scheduling

Scheduling defines when and how often a processor should run.

NiFi supports different scheduling strategies:

- **Timer-driven:** Runs regularly after a defined time interval.
- **CRON-driven:** Runs at specific times according to a CRON expression.
- **Event-driven:** Runs when an event makes work available, where supported.

**Example:** Run a processor every day at midnight.

CRON expression example:

`0 0 0 * * ?`

This means every day at midnight in NiFi's CRON format.

## 14. Relationships (Success / Failure)

Relationships define what happens to a FlowFile after a processor finishes its work.

Common relationships:

- **Success:** The processor completed the task successfully.
- **Failure:** The processor could not complete the task.
- **Original:** The original FlowFile continues through a particular path (for processors that provide this relationship).

Relationships connect processors and determine the next step in the dataflow.

**Example:**
- Success → Send data to the next processor.
- Failure → Send data to an error-handling processor.

## 15. Retry / Terminate

These describe what happens when a FlowFile cannot be processed successfully.

- **Retry:** Try processing the FlowFile again, usually after a temporary problem.
- **Terminate:** Stop processing the FlowFile and remove it from the active flow.

In NiFi, failure handling is configured through relationships and processor settings. Retry can be implemented using retry mechanisms or loops in the flow; it is not automatically available for every processor.

**Example:** If a database is temporarily unavailable, retry the FlowFile. If the data is invalid and cannot be fixed, terminate it or route it to an error-handling flow.

## 16. Back Pressure

Back Pressure prevents queues from becoming too full.

- Each queue has configurable limits.
- Limits can be based on the number of FlowFiles or the total data size.
- When a limit is reached, the upstream processor stops sending more FlowFiles to that queue.
- Processing can continue when space becomes available.

**Example:** A queue can hold a maximum of 1,000 FlowFiles. When it reaches the limit, the previous processor stops sending more data.

**Purpose:** Protects system resources and prevents overload.

## 17. Input Port

An Input Port is an entry point for data into a Process Group.

- Receives FlowFiles from outside the group.
- Connects different Process Groups.
- Allows data to enter a reusable dataflow.

**Example:** One Process Group collects customer data and sends it through an Input Port into another group for transformation.

## 18. Output Port

An Output Port is an exit point for data from a Process Group.

- Sends FlowFiles outside the group.
- Connects one Process Group to another.
- Allows processed data to continue through the overall dataflow.

**Example:** After transforming customer data, a Process Group sends the FlowFiles through an Output Port to another group that stores them in a database.

## 19. Data Quality

Data Quality means checking whether data is correct, complete, consistent, and reliable.

It ensures that data can be trusted and used correctly.

### Main aspects of Data Quality:

- **Accuracy:** Data contains correct information.
- **Completeness:** No important information is missing.
- **Consistency:** Data is the same across different systems.
- **Validity:** Data follows the required format or rules.
- **Uniqueness:** No unnecessary duplicate records.
- **Timeliness:** Data is up to date.

**Example:** A customer database should not contain missing email addresses, incorrect phone numbers, or duplicate customers.

### Data Quality in Apache NiFi:

- Use processors to validate data.
- Filter incorrect or incomplete records.
- Detect duplicate data.
- Route invalid records to an error flow.
- Send valid records to the target database.

**Remember:** Data Quality ensures that data is correct, complete, consistent, and reliable before it is used or stored.

## 20. Apache Kafka – Handling High Data Volumes

Apache Kafka is a distributed event-streaming platform that collects, stores, and transfers large amounts of data between different systems in real time.

It can handle high data volumes because it distributes data across multiple servers called brokers.

### How Kafka handles large amounts of data:

1. **Partitions:** A topic is divided into smaller parts called partitions. This allows data to be processed in parallel.
2. **Brokers:** Multiple Kafka servers share the workload and store data.
3. **Replication:** Data is copied across brokers to prevent data loss if a server fails.
4. **Parallel Processing:** Multiple consumers can read different partitions at the same time.
5. **Batching:** Kafka groups messages together to transfer data more efficiently.
6. **Scalability:** More brokers can be added to handle increasing data volumes.

### Important Kafka Components:

- **Producer:** Sends messages or data to Kafka.
- **Topic:** Organizes messages into categories.
- **Partition:** Divides a topic into smaller parts for parallel processing.
- **Broker:** A Kafka server that stores and manages data.
- **Consumer:** Reads messages from Kafka.
- **Consumer Group:** A group of consumers that share the work of reading partitions.
- **Replication:** Creates copies of partitions for reliability.

**Example:** An online shop receives thousands of orders every minute. Kafka collects the order events and distributes them to different systems, such as payment, inventory, and analytics.

**Remember:** Kafka handles high data volumes through partitioning, distributed brokers, replication, batching, and parallel processing.

---

# Quick Revision – Important Differences

| Concepts | Difference |
|---|---|
| Attribute vs. Content | Metadata vs. actual data |
| Processor vs. Process Group | One task vs. container of tasks |
| Queue vs. Funnel | Stores data vs. combines connections |
| Penalty vs. Yield | Delays a FlowFile vs. pauses a processor |
| Input vs. Output Port | Data enters vs. data leaves a group |
| Success vs. Failure | Processing worked vs. processing failed |
| ETL vs. ELT | Transform before loading vs. transform after loading |
| Retry vs. Terminate | Try again vs. stop processing |
| Provenance vs. Attribute | Processing history vs. FlowFile metadata |
| Back Pressure vs. Yield | Controls queue overload vs. pauses a processor |

# Main Things to Remember for the Exam

- **Apache NiFi:** Connects systems and automates data movement and processing.
- **FlowFile:** Content + Attributes.
- **Processor:** Performs an action on data.
- **Process Group:** Container for multiple processors.
- **Funnel:** Combines multiple incoming connections.
- **Queue:** Temporarily stores FlowFiles.
- **Data Provenance:** Tracks the history of data.
- **Penalty:** Delays an individual FlowFile.
- **Yield:** Temporarily pauses a processor.
- **Scheduling:** Defines when a processor runs.
- **Relationship:** Defines the next path of a FlowFile.
- **Back Pressure:** Prevents queues from becoming too full.
- **Input Port:** Entry point into a Process Group.
- **Output Port:** Exit point from a Process Group.
- **Data Quality:** Ensures data is correct and reliable.
- **Apache Kafka:** Handles large data volumes using distributed storage and parallel processing.

# Simple Overview – NiFi Dataflow

1. Data enters NiFi through an Input Port or a data source.
2. A processor extracts or reads the data.
3. The data is stored temporarily in a Queue.
4. Another processor transforms or filters the data.
5. Relationships determine where the FlowFile goes next.
6. Back Pressure controls the amount of data in queues.
7. Data leaves through an Output Port or goes to a destination.

# Simple Overview – Kafka Dataflow

1. Producers send messages to Kafka.
2. Kafka organizes messages into Topics.
3. Topics are divided into Partitions.
4. Brokers store and manage the data.
5. Replication protects against data loss.
6. Consumers read and process messages.
7. Multiple consumers can work in parallel.

**Final Summary:**

Apache NiFi is mainly used to automate dataflows, move data, transform data, and connect systems.

Apache Kafka is mainly used to collect, store, and distribute large volumes of real-time data efficiently.
