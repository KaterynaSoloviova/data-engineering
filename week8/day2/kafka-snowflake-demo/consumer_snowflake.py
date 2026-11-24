
import os
import json

# Loads variables from the .env file.
from dotenv import load_dotenv

# Kafka Consumer reads messages from a Kafka topic.
from confluent_kafka import Consumer

# Snowflake Connector allows Python to connect to Snowflake.
import snowflake.connector

# Used to load and convert our private key for authentication.
from cryptography.hazmat.primitives import serialization


# 1. LOAD ENVIRONMENT VARIABLES

# Reads configuration values from the .env file.
# This keeps credentials and other settings outside our Python code.
load_dotenv()


# 2. CONFIGURE KAFKA CONSUMER

consumer = Consumer({
    # Address of our Kafka broker.
    # Kafka runs in Docker, but port 9092 is accessible from our Mac.
    'bootstrap.servers': 'localhost:9092',

    # Identifies our Consumer Group.
    # Kafka uses this ID to track the group's reading progress (offsets).
    'group.id': 'snowflake-consumer-group',

    # If this group has no previously committed offset,
    # start reading from the earliest available message.
    'auto.offset.reset': 'earliest'
})


# Subscribe to the topic from which we want to receive messages.
consumer.subscribe(['ecommerce_orders'])


# 3. LOAD THE SNOWFLAKE PRIVATE KEY

# Get the private key file path from the .env file.
# "rb" means read the file in binary mode.
with open(os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH"), "rb") as key_file:

    # Read the private key and load it into a Python key object.
    # password=None because our private key is not password-protected.
    p_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )


# Convert the private key into DER format.
# This is the format required by Snowflake Connector.
private_key = p_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# 4. CONNECT TO SNOWFLAKE

# Establish a connection between Python and Snowflake.
# We use key-pair authentication instead of a password.
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),  # Snowflake account identifier
    user=os.getenv("SNOWFLAKE_USER"),        # Snowflake login name
    private_key=private_key,                  # Private key for authentication
    warehouse="SNOWFLAKE_LEARNING_WH",       # Computing resources for SQL queries
    database="KAFKA_DEMO",                   # Our project database
    schema="REALTIME",                       # Schema containing our table
    role="ACCOUNTADMIN"                      # Role used for Snowflake permissions
)


# Create a cursor to execute SQL commands in Snowflake.
cursor = conn.cursor()


# 5. READ MESSAGES FROM KAFKA

try:
    # Infinite loop: continuously check Kafka for new messages.
    while True:

        # Ask Kafka for a message.
        # 1.0 means wait up to one second for a message.
        msg = consumer.poll(1.0)

        # If no message arrives, go back to the beginning of the loop.
        if msg is None:
            continue

        # Check if Kafka returned an error.
        # If there is an error, display it and continue reading.
        if msg.error():
            print("Consumer error:", msg.error())
            continue


        # 6. CONVERT JSON MESSAGE INTO PYTHON DATA

        # Kafka messages arrive as bytes.
        # decode('utf-8') converts bytes into a text string.
        # json.loads() converts the JSON string into a Python dictionary.
        order = json.loads(msg.value().decode('utf-8'))

        # Display the received order in the Terminal.
        print("Received:", order)


        # 7. INSERT THE ORDER INTO SNOWFLAKE

        # cursor.execute() sends an SQL command to Snowflake.
        # INSERT INTO adds a new row to our ORDERS table.
        cursor.execute(
            """
            INSERT INTO KAFKA_DEMO.REALTIME.ORDERS
            (
                ORDER_ID,
                CUSTOMER_NAME,
                CITY,
                PRODUCT,
                AMOUNT,
                PAYMENT_MODE,
                ORDER_TIME
            )
            VALUES (%s, %s, %s, %s, %s, %s, TO_TIMESTAMP_NTZ(%s))
            """,

            # Values that replace the %s placeholders in the SQL query.
            # Each value comes from our Python order dictionary.
            # This is called parameterized SQL.
            # It is safer than inserting values directly into an SQL string.
            (
                order["order_id"],
                order["customer_name"],
                order["city"],
                order["product"],
                order["amount"],
                order["payment_mode"],
                order["order_time"]
            )
        )

        # Commit confirms the transaction in Snowflake.
        # It makes the inserted order part of the committed table data.
        conn.commit()

        # Display the ID of the order successfully inserted.
        print("Inserted into Snowflake:", order["order_id"])


# Stop the program gracefully when we press Ctrl + C.
except KeyboardInterrupt:
    print("Stopping consumer...")


# 8. CLOSE CONNECTIONS

# finally runs when the try block ends or an exception occurs.
# It helps release resources even when the program is interrupted.
finally:

    # Close the SQL cursor.
    cursor.close()

    # Close the Snowflake connection.
    conn.close()

    # Close the Kafka Consumer connection.
    consumer.close()

    print("Connections closed.")
