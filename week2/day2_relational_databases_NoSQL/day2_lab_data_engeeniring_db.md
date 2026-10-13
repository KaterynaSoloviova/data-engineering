# Part 1 — Relational Databases and NoSQL
## Q. 1 — Build a Small Relational Model

````sql
CREATE TABLE customers (
	customer_id INT primary key,
	customer_name VARCHAR(100) NOT NULL,
	city VARCHAR(50) NOT NULL	
);

CREATE TABLE orders (
	order_id INT primary key,
	customer_id INT NOT NULL,
	amount_gbp DECIMAL(8,2) NOT NULL,
	status VARCHAR(50) NOT NULL,
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
````
## Q. 2 — Insert and Join the Relational Data

````sql
INSERT INTO customers (customer_id, customer_name, city) VALUES 
(1, 'Amelia Clarke', 'London'),
(2, 'Oliver Bennett', 'Manchester'),
(3, 'Aisha Khan', 'Leeds');

INSERT INTO orders (order_id, customer_id, amount_gbp, status) VALUES 
(101, 1, 45.50, 'complete'),
(102, 2, 18.00, 'cancelled'),
(103, 1, 62.25, 'complete'),
(104, 3, 30.00, 'complete');

SELECT o.order_id, c. customer_name, c.city, o.amount_gbp, o.status FROM orders o 
INNER JOIN customers c ON o.customer_id = c.customer_id 
ORDER BY o.order_id;
````

## Q. 3 — Represent the Same Customer as a Flexible Document

````python
customer_1 = {
"customer_id": 1,
"name": "Amelia Clarke",
"city": "London",
"email": "amelia@example.com",
"preferences": {
    "newsletter": True,
    "language": "en"
    }
}

customer_2 = {
"customer_id": 2,
"name": "Amelia Clarke",
"city": "London",
"preferences": {
    "newsletter": True,
    "language": "en"
    }
}
print(customer_1)
print(customer_2)

# The two documents do not need to contain exactly the same optional fields.
````

## Q. 4 — MCQ: Relational Database
Which requirement strongly supports a relational design?
````
Answer: C. Orders must reference valid customers and transaction consistency is important.
````

# Part 2 — Document, Key-Value, and Column-Family Designs
## Q. 5 — Choose the Better NoSQL Model
Match each requirement to document, key-value, or column-family.

````
A. Product records have different optional attributes. - Document
B. Session ID must return session data very quickly. - Key-value
C. Large event data is grouped by a known key and may contain many columns. - Column-family
D. Customer profile contains nested addresses and preferences. - Document
````

## Q. 6 — Build a Key-Value Example
Use a Python dictionary as a simple key-value representation.
Store:
SESSION-1001 -> customer 1, cart_count 3
SESSION-1002 -> customer 2, cart_count 1
SESSION-1003 -> customer 3, cart_count 5

````python
all_sessions = {
    "SESSION-1001":{
        "customer_id": 1,
        "cart_count": 3,
    },
    "SESSION-1002":{
        "customer_id": 2,
        "cart_count": 1,
   },
   "SESSION-1003":{
        "customer_id": 3,
        "cart_count": 5,
    }
}

print(all_sessions["SESSION-1002"])
````

## Q. 7 — Design Three Product Documents
Create three JSON-like product documents.

````json
all_products = [
    {
        "product_id": "P101",
        "name": "Office Chair",
        "color": "Black",
        "material": "Mesh",
    },
    {
        "product_id": "P102",
        "name": "Laptop Stand",
        "color": "Silver",
        "height_adjustable": True,
    },
    {
        "product_id": "P103",
        "name": "Notebook Set",
        "page_count": 200,
        "paper_size": "A5",
    }
]

Requiring every product to contain all possible fields can be inconvenient because different products have different features. Many fields would be empty or unnecessary, making the data harder to manage.
````

## Q. 8 — MCQ: Key-Value Database
Which access pattern is the best fit for a key-value database?
````
Answer: A. Find a session directly from its session ID.
````

# Part 3 — Graph Data, ACID, and BASE
## Q. 9 — Model Connected Data

````mermaid
flowchart LR
    A[Customer 1] --> |uses| C[CARD-A]
    B[Customer 2] --> |uses|C
    A --> |lives_at| D[ADDR-X]
    B --> |lives_at| D
````

## Q. 10 — Identify the ACID Property
Match each example to Atomicity, Consistency, Isolation, or Durability.

````
A. An order and its payment should not be half-completed. - Atomicity
B. A successful commit remains stored after a restart. - Durability
C. Two transactions should not see unsafe partial work from each other. - Isolation
D. A transaction must leave the database in a valid state. - Consistency
````

## Q. 11 — ACID or BASE?

````
Requirement	                                                        ACID or BASE?        Reason

Bank-like payment update	                                         ACID	             Payments must be processed reliably and correctly.
Social activity count can be briefly out of date	                 BASE	             A short delay in updating the count is acceptable.
Order and stock update must remain consistent	                     ACID	             Orders and stock quantities must stay correct.
Very high availability is more important than immediate consistency	 BASE	             The system prioritises availability 
````

## Q. 12 — MCQ: BASE
Which statement best describes a BASE-style design?
````
Answer: B. Temporary inconsistency may be accepted to support availability and scale. 
````

# Part 4 — Fixed vs Flexible Schema and Choosing a Database Model
## Q. 13 — Fixed or Flexible Schema?

````
Data	                                                Fixed or flexible?	  Reason

Payment transaction with required fields	            fixed	              Payment data needs required fields and correctness is important
Product catalogue with category-specific attributes		flexible              Different product categories have different attributes
Customer order line with required quantity and price.   fixed                 Quantity and price are required  
Event payload where optional fields may change          flexible              Event fields can change or be added over time
````

## Q. 14 — Choose Relational or NoSQL
For each requirement, choose a starting model and explain why.

````
1. Customer orders with strong foreign-key relationships. - Relational
2. Product descriptions with many optional attributes. - Document
3. User session lookup by session ID. - Key-value
4. Fraud investigation based on many connected entities. - Graph
````

## Q. 15 — Review a Poor Design Choice
BritMart stores payment transactions as flexible documents with no required fields.
Some records contain: payment_id
but no:
order_id
amount_gbp
status
Explain two risks and suggest a better starting design based only on today's concepts.

````
Risk 1: Missing fields make it difficult to link payments to orders or check payment amounts and status.
Risk 2: Incomplete or incorrect data can cause payment errors and inaccurate reports.
We should use the better design -  a fixed schema with required fields and validation rules to ensure payment data is complete and correct.
````

## Q. 16 — MCQ: Choosing a Database
BritMart must store orders, customers, and payments with strong relationships and transaction correctness. Which is the strongest starting choice?

````
Answer: D. Relational database
````
## Q. 17 — Design the Same Product Two Ways
Model this product as:
- a relational table row;
- a document.

````
Relational table:

product_id	    name	        price_gbp	color	    motor_count	    height_min_cm	height_max_cm	page_count	paper_size
P200	        Smart Desk	    450	        White	    2	            70	            120	            NULL	    NULL
P201	        Notebook	    5	        NULL	    NULL	        NULL	        NULL	        200	        A5

Both products use the same columns, so some fields are empty (NULL).
````

````json
Document:

product_p200 = {
  "product_id": "P200",
  "name": "Smart Desk",
  "price_gbp": 450,
  "color": "White",
  "motor_count": 2,
  "height_min_cm": 70,
  "height_max_cm": 120
}

product_p201 = {
  "product_id": "P201",
  "name": "Notebook",
  "price_gbp": 5,
  "page_count": 200,
  "paper_size": "A5"
}

Documents allow each product to have different fields, so there is no need for unnecessary empty values.
````

## Q. 18 — Find Shared Fraud Links

````python
relationships = [
    ("C1", "CARD-A"),
    ("C2", "CARD-A"),
    ("C1", "ADDR-X"),
    ("C2", "ADDR-X"),
    ("C3", "CARD-B"),
]

# Step 1: Automatically build a dictionary of sets for EVERY customer
customer_links = {}

for customer, linked_value in relationships:
    if customer not in customer_links:
        customer_links[customer] = set()  # Create a set for new customers
    customer_links[customer].add(linked_value)

# Step 2: Now you can check any two customers dynamically!
# Let's check C1 and C2:
shared_c1_c2 = customer_links["C1"].intersection(customer_links["C2"])
print(f"Shared between C1 and C2: {shared_c1_c2}")

# What about C1 and C3?
shared_c1_c3 = customer_links["C1"].intersection(customer_links["C3"])
print(f"Shared between C1 and C3: {shared_c1_c3}")
````

## Q. 19 — Database Choice Review

````
System Database         Model           Schema       Consistency       Main Access
1. Checkout Orders      Relational      fixed        strong            Transactional writes, point lookups by order ID, range queries.
2. Product Catalogue    Document        flexible     moderate          High read-to-write ratio, category filtering, attribute searches
3. Website Sessions	    Key-Value       flexible     eventual          High-throughput point reads/writes by session ID, short TTL.
4. Fraud Investigation  Graph Database	schema	     moderate	       Multi-hop traversals, path-finding, connection mapping.
````

## Q. 20 — Explain the Trade-Off
A team says:
"NoSQL is always faster, so all BritMart data should move to NoSQL."
Write a short response using only today's concepts.

````
No single database fits every job.
Relational databases are best when you need strict rules and safe financial transactions (like checkout orders).
NoSQL databases are better for specific tasks like fast session lookups, flexible product info, or fraud link mapping.
The right choice always depends on how your data looks, how you need to read it, and how strict your consistency rules are.
````


