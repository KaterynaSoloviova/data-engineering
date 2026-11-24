# Real-Time E-commerce Orders Pipeline

## Project Overview

This project demonstrates a real-time data pipeline using Apache Kafka, Python, Snowflake, and Tableau.

The pipeline generates simulated e-commerce orders, streams them through Kafka, stores them in Snowflake, and visualizes the data in an interactive Tableau dashboard.

## Architecture

```text
Python Producer
      |
      v
Apache Kafka
(ecommerce_orders topic)
      |
      v
Python Consumer
      |
      v
Snowflake
(KAFKA_DEMO.REALTIME.ORDERS)
      |
      v
Tableau Dashboard
```

## Technologies Used

- **Python** – generates and processes order data.
- **Apache Kafka** – real-time message streaming.
- **Confluent Kafka Python Client** – Python integration with Kafka.
- **Faker** – generates sample customer data.
- **Snowflake** – cloud data warehouse.
- **Tableau Desktop** – data visualization.
- **Docker** – runs the Kafka broker locally.

## Project Structure

```text
kafka-snowflake-demo/
│
├── producer.py
├── consumer_snowflake.py
├── setup.sql
├── README.md
├── .env
├── .gitignore
│
└── tableau/
    └── ecommerce_orders.twbx
```

## Kafka Configuration

- Topic: `ecommerce_orders`
- Partitions: 1
- Replication factor: 1
- Kafka broker: `localhost:9092`

## Snowflake Configuration

- Database: `KAFKA_DEMO`
- Schema: `REALTIME`
- Table: `ORDERS`
- Warehouse: `SNOWFLAKE_LEARNING_WH`

The Snowflake table stores the following information:

- Order ID
- Customer name
- City
- Product
- Amount
- Payment mode
- Order time

## Tableau Dashboard

The Tableau dashboard provides visual insights into the e-commerce orders.

It includes four visualizations:

1. **Orders by City** – number of orders in each city.
2. **Sales by Product** – total sales amount for each product.
3. **Orders by Payment** – distribution of orders by payment method.
4. **Orders Over Time** – number of orders over time.

The packaged Tableau workbook is located in:

`tableau/ecommerce_orders.twbx`

Open this file using Tableau Desktop to explore the dashboard.

## Security

Sensitive credentials and private keys are stored locally and must not be committed to Git.

The `.env` file and private key files are excluded through `.gitignore`.

## Project Status

The Kafka-to-Snowflake data pipeline has been implemented and tested with sample e-commerce orders. The Tableau dashboard has been created using the Snowflake data.