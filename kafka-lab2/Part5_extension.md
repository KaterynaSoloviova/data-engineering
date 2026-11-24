## Part 5: Extension Exercises

### Exercise 1: Line Numbers

**Objective:** Add a line number to each message sent by the producer.

In `producer.py`, I modified the value assignment:

```python
value = f"{count + 1}: {line.rstrip('\r\n')}"
```

This adds a line number before the original text.

In `consumer.py`, I modified the message processing:

```python
value = msg.value().decode('utf-8')
print(value)
out.write(value + '\n')
```

This prints each received message in the Terminal and writes it into the output file.

**Producer command:**

```bash
python producer.py sample.txt --topic file-topic
```

**Consumer command:**

```bash
python consumer.py --topic file-topic --out numbered.txt
```

**Result:**

```text
1: Kafka moves messages between programs.
2: Each line of this file is one message.
3: Producers write to topics.
4: Consumers read from topics.
5: This is the last line.
```

### Exercise 2: Send Several Files to Kafka.

#### 1. Objective

The objective of this exercise is to learn how to send data from multiple text files to the same Kafka topic and retrieve the messages into separate output files.

In the previous exercise, we created a Python Producer that reads a text file and sends each line as an individual Kafka message.

We also created a Consumer that reads messages from Kafka and writes them into a text file.

Now, we will extend this functionality.

We want to:
- Send messages from multiple input files to one Kafka topic.
- Use a different message key for each source file.
- Understand the difference between a Kafka message key and message value.
- Read messages from Kafka using a Python Consumer.
- Separate received messages into different output files based on their keys.

This is a useful technique when working with data from multiple sources.

For example, in a real data engineering project, we might receive:
- `customers.csv` — customer information.
- `orders.csv` — order information.
- `payments.csv` — payment information.

All these records could be sent to the same Kafka topic and later processed according to their message keys.

#### 2. Input Files

For this exercise, we reused files created during previous exercises instead of creating unnecessary new data.

We used two input files:

**sample.txt**

Contains five original text lines:

```text
Kafka moves messages between programs.
Each line of this file is one message.
Producers write to topics.
Consumers read from topics.
This is the last line.
```

**numbered.txt**

Contains fifteen lines, including the original messages and the numbered messages created in Exercise 1.

Each line in an input file becomes an individual Kafka message.

#### 3. Understanding Kafka Message Keys and Values

Before sending multiple files, it is important to understand the structure of a Kafka message.

A Kafka message can contain:
- **Key** — identifies or groups related messages.
- **Value** — contains the actual message data.
- **Headers** — optional metadata.
- **Timestamp** — message timestamp.

In our exercise, we use the filename as the message key and the file line as the message value.

For example:

| Message component | Example |
|---|---|
| Topic | `file-topic` |
| Key | `sample.txt` |
| Value | `Kafka moves messages between programs.` |

For another message:

| Message component | Example |
|---|---|
| Topic | `file-topic` |
| Key | `numbered.txt` |
| Value | `1: Kafka moves messages between programs.` |

The key helps our Consumer identify the original source of each message.

**Important:** Kafka does not automatically understand that a key represents a filename. We define this meaning in our Python application.

#### 4. Producer: Sending Multiple Files

We did not need to modify the Producer code because it already determines the message key from the input filename.

The relevant code is:

```python
key = os.path.basename(args.file)
```

#### Explanation

**`args.file`**

This is the input filename provided when running the Producer.

For example:

```bash
python producer.py sample.txt --topic file-topic
```

In this case:

```python
args.file = "sample.txt"
```

**`os.path.basename()`**

This function extracts the filename from a path.

For example:

```python
os.path.basename("/Users/student/kafka-lab2/sample.txt")
```

Returns:

```text
sample.txt
```

**`key`**

The filename is assigned to the Kafka message key.

Therefore, every message read from `sample.txt` receives the key `sample.txt`.

#### Sending the First File

Command:

```bash
python producer.py sample.txt --topic file-topic
```

Result:

```text
Sent 5 of 5 lines from sample.txt to topic file-topic
```

Explanation:

- Python opens `sample.txt`.
- The Producer reads the file line by line.
- Each line becomes a separate Kafka message.
- Each message receives the key `sample.txt`.
- All messages are sent to the topic `file-topic`.

Five messages were successfully delivered.

#### Sending the Second File

Command:

```bash
python producer.py numbered.txt --topic file-topic
```

Result:

```text
Sent 15 of 15 lines from numbered.txt to topic file-topic
```

Explanation:

- Python opens `numbered.txt`.
- The Producer reads all fifteen lines.
- Each line becomes an individual Kafka message.
- Each message receives the key `numbered.txt`.
- All messages are sent to the same topic, `file-topic`.

#### Producer Results

| Input file | Messages sent | Message key |
|---|---:|---|
| `sample.txt` | 5 | `sample.txt` |
| `numbered.txt` | 15 | `numbered.txt` |
| **Total** | **20** | **Two different keys** |

Both files were successfully sent to the same Kafka topic.

## 5. Understanding the Kafka Topic

We used one Kafka topic:

```text
file-topic
```

A topic is a logical place where Kafka stores messages.

Kafka does not create a separate topic for every input file.

Instead, both files send their messages to the same topic.

Conceptually, the data flow looks like this:

```text
sample.txt
    |
    v
Python Producer
    |
    | Key: sample.txt
    | Value: Each line of the file
    |
    v
                         Kafka
                    Topic: file-topic
                         ^
                         |
    | Key: numbered.txt
    | Value: Each line of the file
    |
Python Producer
    ^
    |
numbered.txt
```

Kafka stores messages in an append-only log.

This means new messages are appended to the topic's partition rather than replacing previously stored messages.

**Important concept:**

Kafka does not delete previously sent messages just because a new Producer sends another file.

This explains why our Consumer can retrieve messages from previous exercises as well.

#### 6. Consumer: Reading Messages from Kafka

In the previous exercise, our Consumer read only the message value.

Now we extend it to read both the message key and the message value.

#### Reading the Message Key

```python
key_bytes = msg.key()
```

This retrieves the message key from Kafka.

Kafka message keys are returned as bytes.

We convert the key into a Python string:

```python
key = key_bytes.decode('utf-8')
```

For example:

```text
b'sample.txt'
```

becomes:

```text
sample.txt
```

We also check whether a message has a key:

```python
if key_bytes is None:
    print('Skipping message without a key')
    continue
```

This prevents the program from trying to decode a missing key.

#### Reading the Message Value

```python
value = msg.value().decode('utf-8')
```

This retrieves the actual message content.

The `decode('utf-8')` method converts bytes into readable text.

For example:

```text
b'Kafka moves messages between programs.'
```

becomes:

```text
Kafka moves messages between programs.
```

Now the Consumer knows both:
- Where the message came from (key).
- What the message contains (value).

#### 7. Creating a Dictionary to Map Messages to Output Files

We want to save messages from different input files into separate output files.

To do this, we created a Python dictionary:

```python
outputs = {
    'sample.txt': 'sample_received.txt',
    'numbered.txt': 'numbered_received.txt'
}
```

A dictionary is a Python data structure that stores information as key-value pairs.

In our example:

| Dictionary key | Dictionary value |
|---|---|
| `sample.txt` | `sample_received.txt` |
| `numbered.txt` | `numbered_received.txt` |

This dictionary defines the routing rules for our Consumer.

For example:

If a Kafka message has the key `sample.txt`, the Consumer writes its value into `sample_received.txt`.

If a Kafka message has the key `numbered.txt`, the Consumer writes its value into `numbered_received.txt`.

The dictionary does not open the files. It only stores the mapping between message keys and output filenames.

#### 8. Opening Multiple Output Files

We created another dictionary called `file_handles`.

```python
file_handles = {}

for key, filename in outputs.items():
    file_handles[key] = open(
        filename,
        'w',
        encoding='utf-8',
        newline='\n'
    )
```

#### Explanation

**`file_handles = {}`**

Creates an empty dictionary.

We will use it to store the opened files.

**`outputs.items()`**

Returns the key-value pairs from the `outputs` dictionary.

**`for key, filename in outputs.items()`**

Loops through each mapping.

**`open()`**

Opens the corresponding output file.

The parameters mean:

- `filename` — the output filename.
- `'w'` — write mode.
- `encoding='utf-8'` — text encoding.
- `newline='\n'` — use Unix-style line endings.

The program opens two files:

```text
sample_received.txt
numbered_received.txt
```

We store the opened file objects in `file_handles`.

**Important:** Write mode (`'w'`) creates a file if it does not exist and clears its previous contents if it already exists.

This is why our original input files remain unchanged: the Consumer writes to different filenames.

#### 9. Routing Messages to the Correct Output File

This is the most important part of the exercise.

```python
if key not in file_handles:
    print(f'Unknown message key: {key}')
    continue
```

This checks whether the received message key exists in our dictionary.

If the key is not recognized, the Consumer skips the message instead of trying to write it to an unknown file.

Next:

```python
file_handles[key].write(value + '\n')
```

This line writes the message value into the correct output file.

For example:

```python
file_handles['sample.txt'].write(value + '\n')
```

Writes to:

```text
sample_received.txt
```

And:

```python
file_handles['numbered.txt'].write(value + '\n')
```

Writes to:

```text
numbered_received.txt
```

This is how one Kafka Consumer can distribute messages into multiple output files.

#### 10. Counting Messages

We also added a dictionary for counting messages:

```python
counts = {
    key: 0 for key in outputs
}
```

This creates a counter for each source file.

Initially:

```python
{
    'sample.txt': 0,
    'numbered.txt': 0
}
```

Whenever a message is successfully written, we execute:

```python
counts[key] += 1
```

This increases the counter for the corresponding source.

For example, when the Consumer processes a message with key `sample.txt`, only the `sample.txt` counter increases.

This helps us understand how many messages were received from each source.

#### 11. Closing Files and the Consumer

After processing messages, we must close all opened files.

```python
for file in file_handles.values():
    file.close()
```

Why is this important?

Closing files:
- Flushes buffered data to disk.
- Releases operating system resources.
- Helps ensure that all received messages are saved correctly.

We also close the Kafka Consumer:

```python
consumer.close()
```

This releases the Consumer's Kafka resources and performs a clean shutdown.

The `finally` block ensures that cleanup is attempted even if an error or keyboard interruption occurs.

#### 12. Consumer Configuration: Consumer Groups and Offsets

Our Consumer uses the following configuration:

```python
consumer = Consumer({
    'bootstrap.servers': args.bootstrap,
    'group.id': args.group,
    'auto.offset.reset': 'earliest',
})
```

#### `bootstrap.servers`

```python
'bootstrap.servers': 'localhost:9092'
```

This tells the Consumer how to connect to our Kafka broker.

#### `group.id`

```python
'group.id': args.group
```

A Consumer Group identifies a group of consumers that cooperate to read messages from Kafka.

In our lab, the default group ID includes the current timestamp:

```python
file-consumer-{int(time.time())}
```

This means that each new execution normally creates a different Consumer Group.

#### `auto.offset.reset`

```python
'auto.offset.reset': 'earliest'
```

This tells Kafka where to start reading when the Consumer Group has no committed offset.

`earliest` means that the Consumer starts from the earliest available message in the partition.

This explains why our Consumer reads messages from previous exercises, not only the messages sent most recently.

**Important:** `auto.offset.reset='earliest'` does not mean that Kafka always starts reading from the beginning. It applies when the Consumer Group does not have a valid committed offset.

#### 13. Why Does the Consumer Stop Automatically?

We use an idle timeout:

```python
if time.time() - last_message > args.idle:
    break
```

The default idle timeout is 10 seconds.

The Consumer continuously checks Kafka for new messages:

```python
msg = consumer.poll(1.0)
```

If no message arrives, it checks how much time has passed since the last message.

If the Consumer receives no new messages for 10 seconds, it stops.

This is useful for file-transfer exercises because we do not need to stop the Consumer manually.

#### 14. Results and Verification

After running both Producers, we started the Consumer:

```bash
python consumer.py --topic file-topic
```

The Consumer displayed messages with their keys.

Example:

```text
[sample.txt] Kafka moves messages between programs.
[sample.txt] Each line of this file is one message.
[numbered.txt] 1: Kafka moves messages between programs.
[numbered.txt] 2: Each line of this file is one message.
```

The key in square brackets identifies the source of each message.

The Consumer then writes the messages into separate files.

Expected output files:

```text
sample_received.txt
numbered_received.txt
```

### Important: Messages from Previous Exercises

Our Kafka topic already contained messages from previous exercises.

We had sent:
- `sample.txt` multiple times.
- Numbered message values using `sample.txt` as the Producer input.
- `numbered.txt` during this exercise.

Because our Consumer used a new group ID and `auto.offset.reset='earliest'`, it read all available messages from the beginning of the topic.

Therefore, the observed results were:

| Message key | Messages received |
|---|---:|
| `sample.txt` | 20 |
| `numbered.txt` | 15 |
| **Total** | **35** |

This is expected and demonstrates how Kafka retains messages independently of individual Producer executions.

#### Verify the Output Files

We can check the number of lines:

```bash
wc -l sample_received.txt numbered_received.txt
```

Expected result:

```text
20 sample_received.txt
15 numbered_received.txt
```

We can also compare the received files with the original files when their contents correspond.

For example:

```bash
diff -u sample.txt sample_received.txt
```

The files will not be identical in this exercise because Kafka contains messages from multiple previous Producer runs. This is expected.

### Exercise 3: Only new messages

#### 1. Objective

The objective of this exercise is to understand how Kafka Consumer Groups and Offsets work.

In the previous exercises, every time we started the consumer, it used a new Consumer Group ID. Because of this, Kafka treated each run as a new consumer group and started reading messages from the beginning of the topic.

In this exercise, we use the same Consumer Group ID (`demo`) every time. Kafka remembers the group's reading position, so the consumer can continue reading from where it stopped previously.

#### 2. Understanding Consumer Groups and Offsets

A **Consumer Group** is a group of consumers that work together to read messages from Kafka topics.

A **Consumer Group ID** identifies a particular group. Kafka stores the reading position (offset) for each group separately.

An **Offset** is a position of a message within a Kafka partition. It helps Kafka keep track of which messages a consumer group has already processed.

For example:

- A new consumer group has no previously committed offset.
- Kafka uses the `auto.offset.reset` setting to determine where reading should begin.
- After processing messages and committing offsets, the group can continue from its saved position during the next run.

#### 3. Step 1: Start the Consumer with a Fixed Group ID

We started the consumer using the following command:

```bash
python consumer.py --topic file-topic --group demo
```

The important argument is:

```bash
--group demo
```

It assigns a fixed Consumer Group ID instead of generating a new ID every time.

Our consumer configuration includes:

```python
'group.id': args.group,
'auto.offset.reset': 'earliest',
```

**Explanation:**

- `group.id` identifies the consumer group.
- `auto.offset.reset = earliest` tells Kafka to start from the earliest available message if the group does not have a valid committed offset.

Because this was the first run of the `demo` group, Kafka had no saved offset for it. Therefore, the consumer read all available messages.

**Observed result:**

```text
Transfer completed:
Wrote 20 lines to sample_received.txt
Wrote 15 lines to numbered_received.txt
```

The consumer read 35 messages in total.

#### 4. Step 2: Run the Consumer Again with the Same Group ID

Next, we ran exactly the same command:

```bash
python consumer.py --topic file-topic --group demo
```

This time, the consumer did not read the old messages again.

**Observed result:**

```text
Transfer completed:
Wrote 0 lines to sample_received.txt
Wrote 0 lines to numbered_received.txt
```

**Why did this happen?**

Kafka remembered the committed offset for the `demo` group. Since there were no new messages, the consumer had nothing new to read.

This demonstrates that Kafka can remember the reading position of a consumer group between separate program executions.

#### 5. Step 3: Send New Messages to Kafka

To test whether the consumer could read new messages, we sent the contents of `sample.txt` again:

```bash
python producer.py sample.txt --topic file-topic
```

**Observed result:**

```text
Sent 5 of 5 lines from sample.txt to topic file-topic
```

The producer successfully sent five new messages to the `file-topic` topic.

At this point, the consumer had not yet been started again.

#### 6. Step 4: Read Only the New Messages

We started the consumer again using the same Consumer Group ID:

```bash
python consumer.py --topic file-topic --group demo
```

**Observed result:**

```text
[sample.txt] 1: Kafka moves messages between programs.
[sample.txt] 2: Each line of this file is one message.
[sample.txt] 3: Producers write to topics.
[sample.txt] 4: Consumers read from topics.
[sample.txt] 5: This is the last line.

Transfer completed:
Wrote 5 lines to sample_received.txt
Wrote 0 lines to numbered_received.txt
```

The consumer read only five new messages instead of reading all 35 previous messages again.

This happened because Kafka used the previously committed offset for the `demo` consumer group and continued reading from its saved position.

#### 7. Important Kafka Concepts Learned

**Consumer Group ID**

A Consumer Group ID identifies a consumer group. Using the same ID allows Kafka to maintain the group's reading position across different executions.

**Offsets**

Offsets represent message positions within a partition. Kafka uses committed offsets to track how far a consumer group has progressed.

**auto.offset.reset**

This setting controls where a consumer starts reading when there is no valid committed offset for its group.

In our exercise:

```python
'auto.offset.reset': 'earliest'
```

This means that a new consumer group starts reading from the earliest available message.

It does not mean that Kafka always starts from the beginning. If a valid committed offset already exists, Kafka uses that offset instead.

**Different Consumer Groups**

Different consumer groups maintain their own offsets. Therefore, two different groups can independently read the same messages from a topic.

#### 8. Results Summary

| Test | Result |
|---|---|
| First run with group `demo` | Read 35 existing messages |
| Second run with group `demo` | Read 0 messages |
| Producer sent new messages | Sent 5 messages |
| Third run with group `demo` | Read only 5 new messages |


### Exercise 4: Add an End-of-File (EOF) Marker

#### 1. Objective

The objective of this exercise is to improve the communication between the Kafka Producer and Consumer by introducing a special message called an **EOF marker**.

EOF stands for **End Of File**.

In the previous implementation, the Consumer stopped reading messages after a period of inactivity (10 seconds by default).

However, this approach has a limitation: the Consumer does not know whether the Producer has finished sending the file or whether messages are simply delayed.

To solve this problem, we can send a special message at the end of the file. This message tells the Consumer that the file transfer is complete.

#### 2. Understanding the EOF Marker

Normally, the Producer sends each line of the input file as a separate Kafka message.

For example, when sending `sample.txt`, the Producer sends five messages:

1. Kafka moves messages between programs.
2. Each line of this file is one message.
3. Producers write to topics.
4. Consumers read from topics.
5. This is the last line.

After sending all five lines, the Producer sends one additional message:

```text
__EOF__
```

This special message is not part of the original file. It is used only to signal that the transfer has finished.

#### 3. Step 1: Modify the Producer

We modified `producer.py` to send the EOF marker after processing all lines of the input file.

The original code reads the file line by line:

```python
with open(args.file, 'r', encoding='utf-8') as f:
    for line in f:
        value = line.rstrip('\r\n')
        while True:
            try:
                producer.produce(args.topic, key=key, value=value,
                                 callback=on_delivery)
                break
            except BufferError:
                producer.poll(1)

        count += 1
        producer.poll(0)
```

After the `for` loop, we added the following code:

```python
    # Send EOF marker after all file lines
    producer.produce(
        args.topic,
        key=key,
        value='__EOF__',
        callback=on_delivery
    )
    producer.poll(0)
```

**Explanation:**

- `producer.produce()` sends a new message to Kafka.
- `key=key` assigns the same message key as the other messages from the file.
- `value='__EOF__'` defines the special EOF marker.
- `callback=on_delivery` allows us to track message delivery.
- `producer.poll(0)` gives the Producer an opportunity to process delivery callbacks.

The EOF message is placed after the `for` loop because it should be sent only once, after all file lines have been processed.

The existing `producer.flush()` waits for the queued messages, including the EOF marker, to finish delivery.

#### 4. Step 2: Modify the Consumer

Next, we modified `consumer.py` so that it can recognize the EOF marker.

After decoding the Kafka message key and value, we added:

```python
key = key_bytes.decode('utf-8')
value = msg.value().decode('utf-8')

if value == '__EOF__':
    print(f'End of file received for {key}')
    continue
```

**Explanation:**

- `msg.value().decode('utf-8')` converts the Kafka message value from bytes into a readable string.
- `if value == '__EOF__':` checks whether the message is the special EOF marker.
- `print()` displays a message confirming that the end of the file has been received.
- `continue` skips the normal file-writing logic, so the EOF marker is not written into the output file.

#### 5. Step 3: Stop the Consumer When EOF Arrives

We then replaced `continue` with `break`:

```python
if value == '__EOF__':
    print(f'End of file received for {key}')
    break
```

**Why did we make this change?**

There is an important difference between `continue` and `break`:

- `continue` skips the current iteration and continues reading messages.
- `break` exits the loop completely.

By using `break`, the Consumer stops reading as soon as it receives the EOF marker.

This means we no longer need to wait for the idle timeout to detect that the file transfer has finished.

**Important:** This implementation assumes one file transfer per Consumer run. When processing multiple files in one run, we would need to handle each file's EOF marker separately instead of stopping the entire Consumer after the first marker.

#### 6. Step 4: Expected Producer and Consumer Workflow

The complete workflow is:

1. The Producer opens the input file.
2. The Producer reads each line.
3. Each line is sent to the Kafka topic as a separate message.
4. After the last line, the Producer sends the `__EOF__` marker.
5. The Consumer reads messages from Kafka.
6. The Consumer writes normal messages into the output file.
7. When the Consumer receives `__EOF__`, it recognizes that the transfer is complete and exits the reading loop.
8. The Consumer closes its output files and Kafka connection.

#### 7. Expected Results

When running the Producer:

```bash
python producer.py sample.txt --topic file-topic
```

Expected output:

```text
Sent 5 of 5 lines from sample.txt to topic file-topic
```

The output still reports five lines because the `count` variable counts only the original file lines, not the additional EOF message.

When running the Consumer with the same topic and an appropriate consumer group, we expect a message similar to:

```text
End of file received for sample.txt

Transfer completed:
Wrote 5 lines to sample_received.txt
```

The exact output depends on the consumer group's committed offset and which messages are available to that group.

#### 8. Important Concepts Learned

**EOF Marker**

A special message used to indicate that a file transfer has finished.

**Producer and Consumer Communication**

The Producer can communicate additional information to the Consumer by sending special messages through Kafka.

**break vs. continue**

`break` exits a loop, while `continue` skips the current iteration and continues the loop.

**Idle Timeout vs. EOF Marker**

An idle timeout stops the Consumer after a period without messages. An EOF marker provides an explicit signal that the Producer has finished sending the file.
