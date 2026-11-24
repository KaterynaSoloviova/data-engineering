
# Import libraries

import json
# Converts Python data (dictionaries) into JSON format.
# We use JSON to send structured data through Kafka.

import time
# Allows us to pause the program between orders.

import random
# Generates random values, for example, products and cities.

from datetime import datetime
# Gets the current date and time.

from faker import Faker
# Generates fake data, such as customer names.

from confluent_kafka import Producer
# Imports the Kafka Producer class.
# Producer sends messages to a Kafka topic.


# --------------------------------------------------
# 1. INITIALIZE FAKER
# --------------------------------------------------

# Create a Faker object.
# We will use it to generate random customer names.
fake = Faker()


# --------------------------------------------------
# 2. CONFIGURE KAFKA PRODUCER
# --------------------------------------------------

# Create a Kafka Producer and configure its connection.
producer = Producer({
    # Address of our Kafka broker.
    # Kafka runs inside Docker, but port 9092 is available on our Mac.
    'bootstrap.servers': 'localhost:9092'
})


# --------------------------------------------------
# 3. DEFINE AVAILABLE ORDER VALUES
# --------------------------------------------------

# Lists of products that customers can purchase.
products = ['Laptop', 'Phone', 'Tablet', 'Headphones']

# Cities where customers are located.
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Pune']

# Available payment methods.
payments = ['UPI', 'Card', 'Cash']


# --------------------------------------------------
# 4. INITIALIZE ORDER ID
# --------------------------------------------------

# The first order will have ID 1.
# We increase this number after every generated order.
order_id = 1


# --------------------------------------------------
# 5. GENERATE AND SEND ORDERS CONTINUOUSLY
# --------------------------------------------------

# Start an infinite loop.
# The code inside this loop repeats until we stop the program.
while True:

    # Create a Python dictionary representing one order.
    # Each key describes a field, and each value contains the order data.
    order = {
        "order_id": order_id,  
        # Current order number.

        "customer_name": fake.name(),
        # Generate a random customer name.

        "city": random.choice(cities),
        # Select one random city from our cities list.

        "product": random.choice(products),
        # Select one random product from our products list.

        "amount": round(random.uniform(500, 80000), 2),
        # Generate a random price between 500 and 80,000.
        # round(..., 2) keeps two digits after the decimal point.

        "payment_mode": random.choice(payments),
        # Select a random payment method.

        "order_time": str(datetime.now())
        # Get the current date and time.
        # str() converts the datetime object into a string.
    }


    # --------------------------------------------------
    # 6. SEND THE ORDER TO KAFKA
    # --------------------------------------------------

    # producer.produce() sends a message to a Kafka topic.
    producer.produce(
        'ecommerce_orders',
        # Name of the Kafka topic where we store our messages.

        value=json.dumps(order).encode('utf-8')
        # json.dumps(order) converts the Python dictionary into a JSON string.
        # encode('utf-8') converts the string into bytes.
        # Kafka sends message values as bytes.
    )


    # --------------------------------------------------
    # 7. PROCESS DELIVERY EVENTS
    # --------------------------------------------------

    # Producer works asynchronously.
    # poll(0) processes available delivery events and callbacks
    # without waiting.
    producer.poll(0)


    # --------------------------------------------------
    # 8. DISPLAY THE GENERATED ORDER
    # --------------------------------------------------

    # Print the order in the Terminal so we can see what was sent.
    print("Sent:", order)


    # --------------------------------------------------
    # 9. INCREASE ORDER ID
    # --------------------------------------------------

    # Increase the order ID by 1.
    # Example: 1 becomes 2, 2 becomes 3, and so on.
    order_id += 1


    # --------------------------------------------------
    # 10. WAIT BEFORE GENERATING THE NEXT ORDER
    # --------------------------------------------------

    # Pause the program for 2 seconds.
    # This controls how frequently new orders are generated.
    time.sleep(2)
