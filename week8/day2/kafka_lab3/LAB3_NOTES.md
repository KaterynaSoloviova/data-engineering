# Lab 3: Kafka Partitions, Keys and Consumer Groups

**Date:** November 24, 2026

## 1. Lab Objectives

The goal of this lab was to understand how Apache Kafka distributes messages across partitions and how consumer groups work.


## 2. Environment

- Operating System: macOS
- Docker Desktop
- Apache Kafka running in a Docker container
- Container name: `kafka`
- Kafka broker address: `localhost:9092`
- Kafka topic: `orders`
- Number of partitions: 3
- Replication factor: 1

The Kafka environment uses one broker with both broker and controller roles enabled.

---

## 3. Part 1: Creating a Topic with Multiple Partitions

### 3.1 Create the topic

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic orders --partitions 3 --bootstrap-server localhost:9092
```

Explanation:

- `docker exec` — executes a command inside a running Docker container.
- `-it` — enables interactive terminal mode.
- `kafka` — the name of the Kafka container.
- `kafka-topics.sh` — Kafka command-line tool for topic management.
- `--create` — creates a new topic.
- `--topic orders` — specifies the topic name.
- `--partitions 3` — creates three partitions.
- `--bootstrap-server localhost:9092` — connects to the Kafka broker.

Expected output:

```text
Created topic orders.
```

### 3.2 Describe the topic

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
```

Observed result:

```text
Topic: orders
PartitionCount: 3
ReplicationFactor: 1

Partition: 0    Leader: 1    Replicas: 1    Isr: 1
Partition: 1    Leader: 1    Replicas: 1    Isr: 1
Partition: 2    Leader: 1    Replicas: 1    Isr: 1
```

### 3.3 Understanding the output

**PartitionCount: 3**

The topic contains three partitions:

- Partition 0
- Partition 1
- Partition 2

A partition is an ordered log of messages. Kafka uses partitions to distribute data and allow parallel processing.

**ReplicationFactor: 1**

Each partition has only one replica because the lab environment uses a single Kafka broker.

In a production cluster, multiple replicas can be distributed across different brokers to improve fault tolerance.

**Leader**

The leader is the broker responsible for handling reads and writes for a partition.

In my environment, the leader ID is `1`, because the Kafka configuration uses `node.id=1`.

The teacher's example shows leader `0`, but this difference is normal because broker IDs depend on the Kafka configuration.

**Replicas**

The brokers that store copies of a partition.

**ISR (In-Sync Replicas)**

The replicas that are currently synchronized with the partition leader.

In this lab, each partition has one replica, so the leader and ISR are both broker 1.

---

## 4. Part 2: Keys and Message Ordering

### 4.1 Start a consumer

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

Explanation:

- `kafka-console-consumer.sh` — starts a console consumer.
- `--topic orders` — reads messages from the `orders` topic.
- `--from-beginning` — reads existing messages from the beginning.
- `print.key=true` — displays the message key.
- `print.partition=true` — displays the partition number.

### 4.2 Start a producer

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092 --property parse.key=true --property key.separator=:
```

Explanation:

- `kafka-console-producer.sh` — starts a console producer.
- `--topic orders` — sends messages to the `orders` topic.
- `parse.key=true` — tells the producer to parse message keys.
- `key.separator=:` — uses a colon to separate the key from the value.

For example:

```text
user1:login
```

Kafka interprets this as:

- Key: `user1`
- Value: `login`

### 4.3 Send test messages

Messages sent to Kafka:

```text
user1:login
user2:login
user3:login
user1:add-to-cart
user2:add-to-cart
user1:logout
user3:logout
user2:logout
```

### 4.4 Observed result

```text
Partition:0    user1    login
Partition:2    user2    login
Partition:2    user3    login
Partition:0    user1    add-to-cart
Partition:2    user2    add-to-cart
Partition:0    user1    logout
Partition:2    user3    logout
Partition:2    user2    logout
```

### 4.5 Understanding partition assignment

Kafka uses the message key to determine which partition receives a message.

With the default key-based partitioner, the same key is mapped to the same partition, provided the partition count and partitioning configuration remain unchanged.

In my experiment:

- All `user1` messages went to Partition 0.
- All `user2` messages went to Partition 2.
- All `user3` messages went to Partition 2.
- Partition 1 did not receive messages in this experiment.

Different keys can be assigned to the same partition.

Kafka does not create a separate partition for every user.

### 4.6 Why are keys important?

Keys are useful when messages belonging to the same entity must be processed in order.

For example, an online store might send:

```text
user1:login
user1:add-to-cart
user1:payment
user1:logout
```

Using `user1` as the key ensures that these messages are assigned to the same partition.

Kafka guarantees ordering within a partition, but not a global ordering across all partitions.

This is important when processing events that belong to the same user, order, or account.

---

## 5. Part 3: Consumer Groups

### 5.1 What is a consumer group?

A consumer group is a collection of consumers that cooperate to read messages from Kafka topics.

Kafka distributes partitions between active consumers in the same group.

Important rules:

- Each partition is assigned to at most one active consumer within a consumer group at a time.
- Multiple consumers can process different partitions in parallel.
- Consumers in different groups can independently read the same messages.
- A consumer group maintains its own offsets.

### 5.2 Start the first consumer

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group ironhack-group --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

The option:

```text
--group ironhack-group
```

assigns the consumer to the `ironhack-group` consumer group.

### 5.3 Start the second consumer

Run the same command in another terminal window:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group ironhack-group --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

Both consumers belong to the same group.

Kafka coordinates them and distributes the topic partitions between them.

### 5.4 Send additional messages

Start a producer and send:

```text
user1:one
user2:two
user3:three
user4:four
user5:five
user6:six
```

The messages are distributed between the two consumers according to their assigned partitions.

Each message is delivered to one consumer in the group, rather than being independently broadcast to both consumers.

### 5.5 Inspect the consumer group

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-consumer-groups.sh --describe --group ironhack-group --bootstrap-server localhost:9092
```

Observed result:

| Partition | Consumer ID | Current Offset | Log-End Offset | Lag |
|---|---|---:|---:|---:|
| 0 | Consumer A | 5 | 5 | 0 |
| 1 | Consumer A | 4 | 4 | 0 |
| 2 | Consumer B | 7 | 7 | 0 |

The actual consumer IDs are long UUID-like identifiers. They identify individual consumer instances.

Kafka assigned:

- Consumer A: Partitions 0 and 1.
- Consumer B: Partition 2.

### 5.6 Understanding offsets

An offset is the position of a message within a particular partition.

For example:

```text
Partition 0:
Offset 0
Offset 1
Offset 2
Offset 3
Offset 4
```

Consumers use offsets to track their reading progress.

Important fields:

- `CURRENT-OFFSET` — the consumer group's current committed reading position.
- `LOG-END-OFFSET` — the current end position of the partition.
- `LAG` — the difference between the end position and the consumer's current position.

When `LAG = 0`, the consumer group has caught up with the available messages.

In my experiment, all three partitions had a lag of zero.

---

## 6. Consumer Rebalancing

### 6.1 What is rebalancing?

Rebalancing is the process Kafka uses to redistribute partitions among active consumers in a consumer group.

It can happen when:

- A new consumer joins the group.
- A consumer stops or disconnects.
- The number of partitions changes.

### 6.2 Stop one consumer

I stopped Consumer A using:

```text
Ctrl + C
```

Consumer B remained active.

Kafka detected that Consumer A had left the group and reassigned its partitions.

### 6.3 Inspect the group again

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-consumer-groups.sh --describe --group ironhack-group --bootstrap-server localhost:9092
```

Observed result:

| Partition | Active Consumer |
|---|---|
| 0 | Consumer B |
| 1 | Consumer B |
| 2 | Consumer B |

Consumer B received all three partitions.

This demonstrated that Kafka can continue processing messages when one consumer leaves the group.

Rebalancing allows consumer groups to adapt to changes in the number of active consumers.

---

## 7. Different Consumer Groups Read Independently

### 7.1 Start a consumer in another group

Command:

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group other-group --from-beginning --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

This consumer belongs to a different group:

```text
other-group
```

The `--from-beginning` option requests reading from the beginning of the topic when the new group has no previously committed offsets.

### 7.2 Observed result

The new consumer received historical messages from all three partitions.

For example:

```text
Partition:0    user1    login
Partition:0    user1    add-to-cart
Partition:0    user1    logout
Partition:0    user1    one
Partition:0    user6    six

Partition:1    user4    four
Partition:1    user5    five

Partition:2    user2    login
Partition:2    user3    login
Partition:2    user2    add-to-cart
Partition:2    user3    logout
Partition:2    user2    logout
Partition:2    user2    two
Partition:2    user3    three
```

This demonstrates that a new consumer group can independently read messages that another group has already processed.

### 7.3 Why is this useful?

Different applications can read the same Kafka topic for different purposes.

For example:

- `ironhack-group` can process customer orders.
- `other-group` can analyze customer activity.

Both groups receive the same event stream but maintain independent reading positions.

This is one of the key features that makes Kafka useful for event-driven architectures.

---

## 8. Important Kafka Concepts

| Concept | Explanation |
|---|---|
| Topic | A named stream of messages |
| Partition | An ordered log of messages within a topic |
| Key | Determines partition assignment when using key-based partitioning |
| Value | The actual message content |
| Producer | Application that writes messages to Kafka |
| Consumer | Application that reads messages from Kafka |
| Consumer Group | A group of consumers sharing the work of reading partitions |
| Offset | A message position within a partition |
| Lag | Difference between the end of a partition and the consumer's committed position |
| Rebalancing | Redistribution of partitions among active consumers |

## 9. Useful Commands Reference

### Create a topic with three partitions

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic orders --partitions 3 --bootstrap-server localhost:9092
```

### Describe a topic

```bash
docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
```

### Start a consumer with keys and partitions displayed

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --from-beginning --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

### Start a producer with key parsing

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092 --property parse.key=true --property key.separator=:
```

### Start a consumer in a named group

```bash
docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic orders --group ironhack-group --bootstrap-server localhost:9092 --property print.key=true --property print.partition=true
```

### Describe a consumer group

```bash
docker exec -it kafka /opt/kafka/bin/kafka-consumer-groups.sh --describe --group ironhack-group --bootstrap-server localhost:9092
```

### Stop a producer or consumer

```text
Ctrl + C
```

---
