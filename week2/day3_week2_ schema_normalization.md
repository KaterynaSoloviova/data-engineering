## Part 1 — Entities, Attributes, Keys, and Relationships
# Q. 1 — Find the Entities

````
Answer: 

Customer:
customer_id
customer_name
customer_city

Order:
order_id
order_date
customer_id

Product:
product_id
product_name
unit_price_gbp

Order Item:
order_id
product_id
quantity
````

# Q. 2 — Draw the Relationships

````mermaid
erDiagram
    CUSTOMER ||--o{ ORDER :  places
    ORDER ||--o{ PRODUCTS: contains
    PRODUCT ||--o{ORDER_ITEM: appears_in
````

# Q. 3 — Create the Base Tables

````sql
CREATE TABLE customers (
customer_id INT primary key, 
customer_name VARCHAR(100) NOT NULL, 
customer_city VARCHAR(50) NOT NULL
);

CREATE TABLE products (
product_id INT primary key,
product_name VARCHAR(100) NOT NULL,
unit_price_gbp DECIMAL(8,2) NOT NULL
);

CREATE TABLE orders (
order_id INT primary key,
order_date DATE NOT NULL,
customer_id INT NOT NULL,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
order_id INT,
product_id INT NOT NULL,
quantity INT NOT NULL,
FOREIGN KEY (product_id) REFERENCES products(product_id),
FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
````

## Q. 4 — MCQ: Entity
Which item is most clearly an entity in this model?

````
The correct answer is C. Product.
````

# Part 2 — 1NF, 2NF, and 3NF
## Q. 5 — Fix a 1NF Problem
This table stores more than one product in one cell:
order_id	customer_id	    products
101	            1	        P1, P2
102	            2	        P3
Explain why this is a problem for 1NF.
Rewrite the data so each stored value is atomic.

````
1. This is a problem for 1NF, because in 1NF each cell contains only one value.
2. Therefore we need to rewrite this table:

order_id	customer_id	    products
101	            1	        P1
101             1           P2
102	            2	        P3
````

## Q. 6 — Find the 2NF Problem
Consider:
order_id
product_id
product_name
quantity

Assume the row is uniquely identified by: (order_id, product_id)
product_name depends only on product_id.

Why is that a problem, and where should product_name be stored?

````
We have here the composite key: order_id + product_id
product_name --> product_id - we have a partial dependency
It could cause duplicate and make the database harder to maintain, therefore we need to avoid the partial dependency in 2NF.

For this we need to create 2 separated tables:

1. Orders Table:
order_id -- product_id -- quantity

2. Products Table:
product_id -- product_name
````

## Q. 7 — Find the 3NF Problem
Consider:
customer_id
customer_name
postcode
city

Assume:
customer_id -> postcode
postcode -> city

Why can storing city in the same customer row create repeated data?
Suggest a 3NF-style split.

````
We have here a transitive dependency because non-key attribute "city" depends on another non-key attribute "postcode". And customer_id determines city indirectly through postcode.
We can change it:

1. Customers table:
customer_id -- customer_name -- postcode

2. Postcodes table:
postcode -- city
````

## Q. 8 — MCQ: Normalisation
What is the main aim of normalisation in an OLTP-style model?
````
Answer: B. Reduce repeated facts and keep relationships clear.
````

#  Part 3 — Normalised and Denormalised Models
## Q. 9 — Insert a Small Normalised Dataset

````sql
INSERT INTO customers (customer_id, customer_name, customer_city) VALUES
(1, 'Amelia Clarke', 'London'),
(2, 'Oliver Bennett', 'Manchester');

INSERT INTO products (product_id, product_name, unit_price_gbp) VALUES
(10, 'Desk Lamp', 25.00),
(11, 'Office Chair', 80.00),
(12, 'Notebook Set', 10.00);

INSERT INTO orders  (order_id, customer_id, order_date) VALUES
(1001, 1, '2026-08-01'),
(1002, 2, '2026-08-01'),
(1003, 1, '2026-08-02');

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1001, 10, 2),
(1001, 12, 1),
(1002, 11, 1),
(1003, 12, 3);
````
## Q. 10 — Rebuild a Denormalised Result with a Join

````sql
SELECT o.order_id, o.order_date, c.customer_name, c.customer_city, p.product_name, oi.quantity, p.unit_price_gbp,oi.quantity * p.unit_price_gbp
AS line_total_gbp FROM orders o INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
ORDER BY o.order_id, p.product_id;
````

## Q. 11 — Compare Update Behaviour
Imagine the product name changes from:
Notebook Set to Premium Notebook Set
Model A
The product name is stored only once in products.
Model B
The product name is repeated in every order line.
Which model needs fewer data changes? Why?

````
Model A needs fewer data changes, because the product name is stored only once in the products table.
````

## Q. 12 — MCQ: Denormalisation
Why might an analytical dataset deliberately repeat some descriptive values?

````
Answer: D. To make some analytical queries simpler to read and use
````

# Part 4 — Scalable Model Thinking and Star Schema Introduction
## Q. 13 — Identify the Fact and Dimensions
BritMart wants to analyse sales by:
date
customer
product
store

Measures are:
quantity
sales_gbp

Choose:
fact table
dimension tables

````
1. Fact Table:
date
customer_id
product_id
store_id
quantity
sales_gbp

2. Dimension Table:
DimDate (date, month, year)
DimCustomer (name, city)
DimProduct (name)
DimStore (name, city)
````
````mermaid
erDiagram
    DimDate ||--o{ Fact_Sales : describes
    DimCustomer ||--o{ Fact_Sales : describes
    DimProduct ||--o{ Fact_Sales : describes
    DimStore ||--o{ Fact_Sales : describes
````

## Q. 14 — Define the Grain
Choose the clearer grain for FactSales.
Choice A
One row per order
Choice B
One row per product sold within an order

BritMart needs product-level sales analysis.
Which grain should be used and why?

````
Answer. B. Because grain tells us how detailed each row is. One row per order is less detailed; one row per product sold within an order is more detailed.
````

## Q. 15 — Draw the Star

````mermaid
erDiagram
    DimDate ||--o{ Fact_Sales : describes
    DimCustomer ||--o{ Fact_Sales : describes
    DimProduct ||--o{ Fact_Sales : describes
    DimStore ||--o{ Fact_Sales : describes
````

## Q. 16 — MCQ: Fact Table
Which values belong most naturally in a sales fact table?
````
Answer: A. quantity and sales_gbp
````

# Optional Practice
## Q. 17 — Normalise a Poor Order Table
BritMart currently stores:
order_id
order_date
customer_id
customer_name
customer_city
product_id
product_name
unit_price_gbp
quantity

Sample rows:
1001 | 2026-08-01 | 1 | Amelia Clarke | London | 10 | Desk Lamp | 25.00 | 2
1001 | 2026-08-01 | 1 | Amelia Clarke | London | 12 | Notebook Set | 10.00 | 1
1002 | 2026-08-01 | 2 | Oliver Bennett | Manchester | 11 | Office Chair | 80.00 | 1

Split the data into suitable tables and identify each table's key.

````
1. Orders Table:
order_id (PK) | order_date| customer_id(FK)
Each order belongs to one customer.

1NF: Each column contains one value per row.
2NF: order_date and customer_id depend on the whole primary key, order_id.
3NF: No transitive dependency is present, assuming the customer details are stored in Customers.
-------------------------------------------------------------------------------------------------
2. Customers Table:
customer_id(PK) | customer_name | customer_city
Customer information is stored once instead of being repeated for every order item.

1NF: Each cell contains one value.
2NF: The non-key attributes depend on the whole primary key, customer_id.
3NF: No transitive dependency, assuming customer_city depends directly on customer_id and not on another non-key attribute.
--------------------------------------------------------------------------------------------------
3. Products Table:
product_id(PK) | product_name | unit_price_gbp
Product details are stored once, even if the product appears in many orders.

1NF: Each cell contains one value.
2NF: The attributes depend on the whole primary key, product_id.
3NF: No transitive dependency, assuming product name and price depend directly on product_id.
---------------------------------------------------------------------------------------------------

4. Orders Items:
order_id (PK/FK) | product_id (PK/FK) | quantity
The primary key is (order_id, product_id) together, not order_id alone.

1NF: Each cell contains one value.
2NF: quantity depends on the whole composite key (order_id, product_id), because it describes how many of that product were included in that order.
3NF: No transitive dependency, assuming there are no additional non-key attributes with dependencies on one another.
-------------------------------------------------------------------------------------------------------
````

## Q. 18 — Find Update Anomalies
In the poor table from Q. 17, Amelia's city appears in two rows.
If only one row is changed from London to Bristol what problem appears?

````
Amelia's city is stored in two rows. If you change only one row from London to Bristol, the table will show two different cities for the same customer. The database will contain conflicting information about where Amelia lives. (data inconsistency)
````

## Q. 19 — Convert the Normalised Model into a Sales Star
Starting from:
customers
products
orders
order_items

design:
FactSales
DimCustomer
DimProduct
DimDate

State the grain and list the main columns.

````
1. Grain - one row per product line in an order.

2. FactSales:
customer_id
product_id
order_id
date_id
quantity
sales_gbp

3. DimCustomer:
customer_id
customer_name
customer_city

4. DimProduct:
product_id
product_name

5. DimDate:
date_id
date
day
month
year
````

##Q. 20 — Review the Model Before Building It
Before creating tables, write answers to these questions:

````
1. What does one row represent? - One row in FactSales represents one product line for an order.
2. Which fields identify the row? - In the original order_items table, the combination of order_id and product_id identifies each row.
3. Which facts repeat? - Customer names, customer cities, and product names may repeat across multiple orders.
4. Which fields describe another entity? - customer_name and customer_city describe a customer. product_name and unit_price_gbp describe a product. order_date describes an order date.
5. Which relationships must remain valid? - Each order must reference an existing customer. Each order item must reference an existing order and product. In the analytics model, each FactSales row must reference valid customer, product, and date dimension records.
6. Is the model mainly for transactions or analytics? - The original tables (customers, products, orders, and order_items) are designed mainly for transactions (OLTP). The star schema (FactSales, DimCustomer, DimProduct, and DimDate) is designed mainly for analytics (OLAP).
````







