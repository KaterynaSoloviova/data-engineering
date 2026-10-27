# QuickCart — Data Quality 

## Data Ingestion Pipeline
The objective of this stage was to ingest the four QuickCart datasets using Python and Pandas, validate their schemas, detect duplicate customer records, and identify invalid data.

1. Datasets Overview
We have loaded 4 CSV datasets using Pandas:

```
Dataset                Rows         Columns     

customers              100          5
orders                 500          7
products                10          6
clickstream             2000        6
```
2. Schema Validation

```
The actual column names were compared with the expected schema for each dataset.
Result: All four datasets contain the expected columns. No missing or unexpected columns were detected.
Dataset.            Expected columns

Customers           customer_id, customer_name, email, city, signup_date
Orders              order_id, customer_id, product_id, order_date, quantity, unit_price, payment_status
Products            product_id, product_name, category, supplier_id, cost_price, selling_price
Clickstream         event_id, customer_id, event_type, page_url, event_timestamp, device_type
```

3. Missing Values
```
The  missing values were detected  only in clickstream dataset:

Column                Missing values
event_id              0
customer_id           60
event_type            0
page_url              83
event_timestamp       0

The missing values will be investigated during the cleaning stage. 
Rows will not be removed automatically just because they contain missing values.
```
4. Duplicate Records
```
No fully duplicated rows were detected in any of the four datasets.

The ID uniqueness checks returned the following results:

Dataset         ID column       Duplicate IDs

Customers       customer_id     0
Orders          order_id        0
Products        product_id      0
Clickstream     event_id        37

The 37 repeated event IDs require further investigation. These records will be inspected before deciding whether any rows should be removed.
```
5. Identify invalid records
```
The initial validation checks found no orders with non-positive quantities and no negative order or product prices.
Examples of validation rules included:
Customers must have a customer ID, email address, and valid signup date.
Orders must have an order ID, customer ID, product ID, valid order date, positive quantity, and non-negative unit price.
Products must have a product ID and valid, non-negative cost and selling prices.
Clickstream events must have an event ID, timestamp, and page URL.
Invalid records were counted and identified for cleaning.
```
## Data Cleaning & Transformation
The purpose of this stage was to improve data quality by standardizing text fields, converting dates and timestamps, handling missing values, and removing corrupted records.

1. Standardizing City Names
```
Customer city names were cleaned by removing leading and trailing whitespace and applying title case.
Email addresses were also converted to lowercase to support consistent duplicate detection.
```

2. Date and Timestamp Conversion
```
- Date fields were converted to Pandas datetime types using pd.to_datetime().
- signup_date was converted to a datetime value.
- order_date was converted to a datetime value.
- event_timestamp was converted to a UTC-aware datetime value.
- The parameter errors="coerce" converts unparseable date values into NaT, allowing invalid timestamps to be identified and handled consistently.
- Using UTC for clickstream timestamps helps maintain consistency when analyzing events across time zones.
```

3. Handling Missing Values
```
- Missing values in critical fields were handled by removing records that could not be processed reliably.
- For example, an order without an order date, customer ID, product ID, quantity, or unit price cannot be reliably used for sales analysis.
- Non-critical missing fields were not automatically filled with invented values. In a production environment, the appropriate treatment would depend on business rules.
```

4. Removing Corrupted Rows
```
- Exact duplicate rows were removed using drop_duplicates().
- Additional validation rules were applied to exclude records with invalid numeric values, such as:
- Orders with zero or negative quantities.
- Orders with negative unit prices.
- Products with negative cost or selling prices.
- Clickstream events without a valid timestamp or page URL.
- The number of rows before and after cleaning was compared to measure the impact of the transformation process.
```
5. Saving Cleaned Datasets
The cleaned datasets were saved as separate CSV files in the data/cleaned_data/ directory

```
Original Dataset            Cleaned Output

customers.csv               customers_cleaned.csv
orders.csv                  orders_cleaned.csv
products.csv                products_cleaned.csv
clickstream.csv             clickstream_cleaned.csv
```

## Clickstream Analytics Report
After completing the data cleaning process, the cleaned clickstream dataset was used to perform web traffic analysis. The goal was to understand which pages received the most visits, estimate the number of user sessions, and compare mobile and desktop traffic.
The analysis was performed using Python and pandas. The results were saved as CSV reports in the data/processed/ directory for further inspection and reporting.

1. Most Visited Pages
```
- Page visits were counted by grouping events by page_url.
- Pages were ranked by visit count in descending order.
- Missing page URLs represented by Unknown were treated as a separate category.
- Results: 
    Most visited page: [insert page URL]
    Number of visits to the most visited page: [insert visit count]
    Total number of page visits included in the analysis: [insert total]
```
2. User Session Analysis
A new session was counted when:
```
- A customer had their first recorded event in the dataset.
- More than 30 minutes had passed since that customer's previous event.
- Events without a customer ID or a valid timestamp were excluded from session calculations because they could not be reliably assigned to a customer session.
```
Results:
```
- Total estimated sessions: [insert total session count]
- Customers included in the session analysis: [insert number of customers]
- Session definition: a new session begins after a gap of more than 30 minutes.
```

3. Mobile vs. Desktop Traffic
```
- Device types were standardized by removing surrounding whitespace and converting text to lowercase.
- Events labeled mobile or desktop were included in the comparison.
- The number of events for each device type was calculated.
- Each device type's percentage was calculated as its event count divided by the total mobile and desktop event count, multiplied by 100.
- Other device categories and missing values were excluded from this comparison.
Results:
- Mobile events: [insert count] ([insert percentage]%)
- Desktop events: [insert count] ([insert percentage]%)
- Business value: This comparison helps show how website activity is distributed between mobile and desktop devices. It can help inform - decisions about responsive design, usability improvements, and device-specific testing.
```
4. Output Files
The analytics process produces the following reports in data/processed/:
most_visited_pages.csv
session_counts.csv
device_traffic_report.csv

Note: The filenames above should match the actual filenames used in the analytics script.
