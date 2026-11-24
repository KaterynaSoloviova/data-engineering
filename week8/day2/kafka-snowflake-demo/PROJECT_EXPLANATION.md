# Project Code Explanation — Kafka, Python, Snowflake & Tableau

My personal study guide. This document explains the code used in this project, line by line, in simple English.

---

# PART 1 — PYTHON PRODUCER

File: `producer.py`

## 1. Imports

```python
import json
import time
import random
from datetime import datetime

from faker import Faker
from confluent_kafka import Producer
```

What does each import do?

- `json` — converts Python data into JSON format. Kafka messages are sent as bytes, so we need to serialize our data.
- `time` — allows us to pause the program between orders.
- `random` — selects random products, cities, payment methods and prices.
- `datetime` — gets the current date and time.
- `Faker` — generates fake customer information, such as names.
- `Producer` — creates a Kafka Producer that sends messages to Kafka.

**Why do we need these libraries?**

Our goal is to generate realistic sample orders and send them to Kafka automatically.

## 2. Initialize Faker

```python
fake = Faker()
```

This creates a Faker object.

We use it to generate random customer names:

```python
fake.name()
```

For example, it might generate:

`John Smith`

Every time we call `fake.name()`, it can generate a different name.

## 3. Configure Kafka Producer

```python
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})
```

This creates our Kafka Producer.

- `Producer()` — creates a Producer object.
- `bootstrap.servers` — tells Python where the Kafka broker is located.
- `localhost` — means our own computer.
- `9092` — the port through which our Kafka broker accepts connections.

**Important:** Kafka is running inside Docker, but port 9092 is exposed to our Mac. Therefore, Python connects using `localhost:9092`.

## 4. Create Lists of Available Values

```python
products = ['Laptop', 'Phone', 'Tablet', 'Headphones']

cities = ['Mumbai', 'Delhi', 'Bangalore', 'Pune']

payments = ['UPI', 'Card', 'Cash']
```

These are Python lists.

We use them as predefined options when generating orders.

For example:

```python
random.choice(products)
```

This selects one random product from the list.

## 5. Initialize Order ID

```python
order_id = 1
```

This variable stores the order number.

The first order has ID 1.

After every order, we increase the number:

```python
order_id += 1
```

This is equivalent to:

```python
order_id = order_id + 1
```

## 6. Generate Orders Continuously

```python
while True:
```

This starts an infinite loop.

`True` is always true, so Python continues executing the code inside the loop until we stop the program.

We use this because we want to generate orders continuously, not just one order.

## 7. Create an Order

```python
order = {
    "order_id": order_id,
    "customer_name": fake.name(),
    "city": random.choice(cities),
    "product": random.choice(products),
    "amount": round(random.uniform(500, 80000), 2),
    "payment_mode": random.choice(payments),
    "order_time": str(datetime.now())
}
```

This creates a Python dictionary.

A dictionary stores information as key-value pairs.

For example:

- `"city"` is a key.
- `"Mumbai"` is its value.

Let's understand the values:

- `order_id` — current order number.
- `fake.name()` — generates a random customer name.
- `random.choice(cities)` — selects a random city.
- `random.choice(products)` — selects a random product.
- `random.uniform(500, 80000)` — generates a random decimal number between 500 and 80,000.
- `round(..., 2)` — rounds the price to two decimal places.
- `random.choice(payments)` — selects a payment method.
- `datetime.now()` — gets the current date and time.
- `str()` — converts the datetime object into a string.

## 8. Convert the Order into JSON and Send It to Kafka

```python
producer.produce(
    'ecommerce_orders',
    value=json.dumps(order).encode('utf-8')
)
```

This is one of the most important parts of our Producer.

Let's break it down.

**`producer.produce()`**

Sends a message to Kafka.

**`'ecommerce_orders'`**

The name of our Kafka topic.

A topic is where Kafka stores messages.

**`json.dumps(order)`**

Converts our Python dictionary into a JSON string.

**`.encode('utf-8')`**

Converts the JSON string into bytes.

Kafka messages are transmitted as bytes, so we encode the data before sending it.

The complete process is:

Python dictionary → JSON string → bytes → Kafka.

## 9. Process Delivery Events

```python
producer.poll(0)
```

Kafka Producer works asynchronously.

This means `produce()` queues the message for sending, rather than waiting for the entire delivery process to finish.

`poll(0)` allows the Producer to process available delivery callbacks and other events without waiting.

## 10. Display the Sent Order

```python
print("Sent:", order)
```

Displays the generated order in the Terminal.

This helps us check that the Producer is working.

## 11. Increase Order ID

```python
order_id += 1
```

Increases the order number by one.

For example:

1 → 2 → 3 → 4

## 12. Wait Two Seconds

```python
time.sleep(2)
```

Pauses the program for two seconds.

Without this command, the Producer would generate orders as quickly as possible.

## 13. How the Producer Works as a Whole

The loop repeats these actions:

1. Generate an order.
2. Convert it into JSON.
3. Send it to Kafka.
4. Process delivery events.
5. Print the order.
6. Increase the order ID.
7. Wait two seconds.
8. Repeat.

To stop the Producer, press `Ctrl + C` in Terminal.

---

# PART 2 — PYTHON CONSUMER

File: `consumer_snowflake.py`

The Consumer has a different responsibility.

The Producer sends data to Kafka.

The Consumer reads data from Kafka and inserts it into Snowflake.

## 1. Main Imports

```python
import os
import json

from dotenv import load_dotenv
from confluent_kafka import Consumer
import snowflake.connector

from cryptography.hazmat.primitives import serialization
```

- `os` — reads environment variables and works with file paths.
- `json` — converts JSON messages into Python dictionaries.
- `load_dotenv` — loads configuration values from the `.env` file.
- `Consumer` — creates a Kafka Consumer.
- `snowflake.connector` — connects Python to Snowflake.
- `serialization` — reads and converts our private key into the format Snowflake requires.

## 2. Load Environment Variables

```python
load_dotenv()
```

This loads variables from our `.env` file.

For example:

```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PRIVATE_KEY_PATH=snowflake_key.p8
```

We access these values in Python using:

```python
os.getenv("SNOWFLAKE_ACCOUNT")
```

**Why?**

We do not want to write sensitive configuration directly inside our Python code.

## 3. Load the Private Key

```python
with open(os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH"), "rb") as key_file:
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )
```

What happens here?

- `open()` — opens our private key file.
- `os.getenv()` — gets its path from `.env`.
- `"rb"` — opens the file in binary reading mode.
- `key_file.read()` — reads the private key.
- `load_pem_private_key()` — converts the PEM key into a Python key object.
- `password=None` — our private key is not encrypted with a password.

The `with` statement automatically closes the file when Python finishes reading it.

## 4. Convert the Private Key

```python
private_key = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
```

Snowflake Connector expects the private key in DER format.

We convert our PEM key into DER format.

- `Encoding.DER` — specifies the output encoding.
- `PrivateFormat.PKCS8` — specifies the private key structure.
- `NoEncryption()` — does not encrypt the converted key.

**Important:** The private key must remain secret. Never upload it to GitHub.

## 5. Connect to Snowflake

```python
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    private_key=private_key,
    warehouse="SNOWFLAKE_LEARNING_WH",
    database="KAFKA_DEMO",
    schema="REALTIME",
    role="ACCOUNTADMIN"
)
```

This establishes a connection between Python and Snowflake.

Explanation:

- `account` — identifies our Snowflake account.
- `user` — identifies our Snowflake user.
- `private_key` — authenticates us using key-pair authentication.
- `warehouse` — specifies the computing resources used to execute SQL.
- `database` — selects our database.
- `schema` — selects our schema.
- `role` — specifies the Snowflake role used by the connection.

**Important difference:**

A database stores data. A warehouse provides computing resources to run queries.

## 6. Create a Kafka Consumer

```python
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'snowflake-consumer-group',
    'auto.offset.reset': 'earliest'
})
```

This creates a Kafka Consumer.

- `bootstrap.servers` — tells the Consumer where Kafka is running.
- `group.id` — identifies the Consumer Group.
- `auto.offset.reset` — determines where to start reading if the group has no previously committed offset.

`earliest` means start from the earliest available message when there is no committed offset for this group.

## 7. Subscribe to a Topic

```python
consumer.subscribe(['ecommerce_orders'])
```

This tells the Consumer which Kafka topic to read.

Our Consumer subscribes to `ecommerce_orders`.

## 8. Read Messages

The Consumer uses a loop to continuously check for new messages.

```python
msg = consumer.poll(1.0)
```

This asks Kafka for a message.

`1.0` means the Consumer can wait up to one second for a message.

If no message arrives during that time, the program continues and checks again.

## 9. Convert JSON into Python Data

When a message arrives, we decode its bytes and convert the JSON into a Python dictionary.

Conceptually:

```python
order = json.loads(msg.value().decode('utf-8'))
```

- `msg.value()` — gets the message value from Kafka.
- `decode('utf-8')` — converts bytes into a string.
- `json.loads()` — converts the JSON string into a Python dictionary.

This is the reverse of what our Producer did.

Producer:

Python dictionary → JSON → bytes.

Consumer:

Bytes → JSON string → Python dictionary.

## 10. Insert Data into Snowflake

We use an SQL INSERT statement to save the order in the Snowflake table.

Conceptually:

```sql
INSERT INTO KAFKA_DEMO.REALTIME.ORDERS
(ORDER_ID, CUSTOMER_NAME, CITY, PRODUCT, AMOUNT, PAYMENT_MODE, ORDER_TIME)
VALUES (%s, %s, %s, %s, %s, %s, %s)
```

The Python Consumer supplies the actual values from the order.

We use parameterized SQL instead of directly inserting values into the SQL string.

**Why?**

It is safer and handles values correctly, including names containing apostrophes.

## 11. Commit the Snowflake Transaction

```python
conn.commit()
```

This confirms the database transaction.

It makes the inserted order part of the committed data in Snowflake.

## 12. Close Connections

At the end of the program, we close:

- The Snowflake cursor.
- The Snowflake connection.
- The Kafka Consumer.

This releases resources and closes connections properly.

---

# PART 3 — IMPORTANT DIFFERENCES

## Producer vs Consumer

| Producer | Consumer |
|---|---|
| Creates orders | Reads orders |
| Sends messages | Receives messages |
| Writes to Kafka | Reads from Kafka |
| Uses `Producer` | Uses `Consumer` |

## JSON Serialization vs Deserialization

**Serialization:** converting Python data into JSON so it can be sent.

**Deserialization:** converting JSON back into Python data so it can be processed.

## Kafka vs Snowflake

Kafka transfers and temporarily stores messages for consumers to read.

Snowflake stores structured data for SQL queries and analysis.

## Snowflake vs Tableau

Snowflake stores the data.

Tableau connects to Snowflake and presents the data visually.

---

# PART 4 — HOW TO RUN THE PROJECT

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check that Kafka is running:

```bash
docker ps
```

Start the Producer:

```bash
python producer.py
```

Open another Terminal window, activate the same virtual environment, and start the Consumer:

```bash
python consumer_snowflake.py
```

Check the data in Snowflake:

```sql
SELECT *
FROM KAFKA_DEMO.REALTIME.ORDERS
ORDER BY ORDER_ID;
```

Count all orders:

```sql
SELECT COUNT(*)
FROM KAFKA_DEMO.REALTIME.ORDERS;
```

Stop either Python program with:

`Ctrl + C`

**Remember:** Start the Consumer before the Producer when testing a fresh flow, and check your Kafka offsets and Snowflake records when repeating tests. The Consumer Group may already have processed older messages.