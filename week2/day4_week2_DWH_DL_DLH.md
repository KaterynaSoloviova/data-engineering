# Part 1 — Data Lake, Data Warehouse, and Lakehouse

## Q. 1 — Choose the Better Platform
For each requirement, choose data lake, data warehouse, or lakehouse.

````
Requirement	                                                                    Choice	    Reason
Keep large amounts of raw structured and semi-structured data		            DL          Stores large volumes of data in different formats
Give analysts controlled SQL-ready business tables		                        DWH         Supports structured data - SQL tables       
Keep flexible storage while also supporting governed table-style analytics		LH          Combines flexible lake storage with managed analytical tables
Keep raw website events for future use	                                        DL          Preserves raw events for future processing and analysis
````

## Q. 2 — Place BritMart Data
BritMart has:
MySQL order extract
supplier CSV files
website JSON events
monthly finance table
daily sales summary

Place each item where it would most naturally fit in a data lake, warehouse, or lakehouse design.
There may be more than one valid answer. Explain your choice.

````
Item	                                 Choice	                                            Reason
MySQL order extract                      Data lake or lakehouse (Bronze layer)              We can store the initial data before transformations  
supplier CSV files                       Data lake or lakehouse (Bronze layer)              We can store the initial supplier files for future processing   
website JSON events                      Data lake or lakehouse (Bronze layer)              Store flexible semi-structured events.
monthly finance table                    Data Warehouse                                     Supports controlled structured financial reporting
daily sales summary                      Data Warehouse                                     We have ready data for the reports
````

## Q. 3 — Compare the Three Architectures

````
Area	                                 Data Lake     	                            Data Warehouse                      	Lakehouse
Raw data support			             Strong                                     Usually not main focus                  Strong
Strong structured reporting			     Possible but we need extra tools           Strong                                  Strong
Flexible data shapes                     Strong                                     Structured data                         Strong            			
Table-style analytics	                 Depends on tools                           Strong                                  Strong
````

## Q. 4 — MCQ: Data Warehouse
Which requirement is the strongest fit for a data warehouse?

````
Answer: D. Run controlled business reporting over trusted structured data
````

# Part 2 — Schema-on-Read, Schema-on-Write, Bronze, and Silver

## Q. 5 — Schema-on-Read or Schema-on-Write?
Choose the better description.

````
A. Data is stored first and interpreted when it is read.- Schema-on-Read
B. Data must match an expected structure before it is accepted into the target. - Schema-on-Write
C. A raw JSON area keeps different optional fields. - Schema-on-Read
D. A controlled reporting table requires known columns and types - Schema-on-Write
````

## Q. 6 — Design Bronze and Silver Rules
BritMart receives:
order_id
city
amount_gbp
status

Define what should happen in:

````
Bronze
What should be kept? - Bronze should keep the incoming order records as close to the source as possible. It should store the original values of order_id, city, amount_gbp, and status, including invalid amounts

Silver
What should be checked or cleaned? - Silver should validate data types, check that order_id is present, trim whitespace from city names, validate amount_gbp, and remove duplicate orders using a defined business rule.
````
## Q. 7 — Process Three Batches from Bronze to Silver
Use Pandas.

````python
import pandas as pd

all_order = [batch_1, batch_2, batch_3]

import pandas as pd

batch_1 = pd.DataFrame(
    {
        "order_id": [101, 102],
        "city": ["London", "Manchester"],
        "amount_gbp": [45.50, -5.00],
        "status": ["complete", "complete"],
    }
)

batch_2 = pd.DataFrame(
    {
        "order_id": [103, 104],
        "city": [" Bristol ", "Leeds"],
        "amount_gbp": [30.00, 20.00],
        "status": ["complete", "cancelled"],
    }
)

batch_3 = pd.DataFrame(
    {
        "order_id": [101, 105],
        "city": ["London", "Manchester"],
        "amount_gbp": [45.50, 51.00],
        "status": ["complete", "complete"],
    }
)

bronze = pd.concat([batch_1, batch_2, batch_3],ignore_index=True,)

silver = bronze[
    bronze["amount_gbp"] > 0
].copy()
 
silver["city"] = (
    silver["city"].str.strip()
)
 
silver = silver.drop_duplicates(
    subset=["order_id"],
    keep="first",
)
 
print("Bronze rows:", len(bronze))
print("Silver rows:", len(silver))
````

## Q. 8 — MCQ: Silver
Which record belongs most naturally in Silver?

````
C. A cleaned and deduplicated order row
````

# Part 3 — Gold, Data Types, and Storage-First Architecture

## Q. 9 — Build a Gold Summary
Using the Silver DataFrame from Q. 7:
keep only completed orders;
calculate revenue by city;
sort highest revenue first.

````
gold = (
    silver[silver["status"] == "complete"]
    .groupby("city", as_index=False)
    .agg(revenue_gbp=("amount_gbp", "sum"))
    .sort_values("revenue_gbp", ascending=False)
)

print(gold.to_string(index=False))
````

## Q. 10 — Structured, Semi-Structured, or Unstructured?

````
Item	                    Classification	

MySQL orders table	        Structured	
JSON website event	        Semi-structured	
CSV supplier file	        Usually structured	
Product photo	            Unstructured	
PDF supplier contract	    Usually unstructured
````

## Q. 11 — Design a Storage-First Flow

````mermaid
flowchart LR
    A["MySQL Extract"] --> S["Storage"]
    B["Supplier CSV"] --> S
    C["Website JSON"] --> S
    S --> P["Processing"]
    P --> T["Trusted Output"]
````

## Q. 12 — MCQ: Gold
Which output is the strongest Gold example?

````
Answer: A. Daily revenue by city for reporting 
````

# Part 4 — Compute, Storage, Metadata, and Catalogues
## Q13 — Compute or Storage?

````
Item	                                                Classification	
A. Files kept for later use	                            Storage	
B. CPU and memory used to run a transformation	        Compute
C. Stored analytical table data	                        Storage	
D. Processing resources used for a query                Compute
````

## Q14 — Why Separate Compute and Storage?

````
If data and computing resources are tightly coupled, a large task might require maintaining a powerful infrastructure on a permanent basis. By decoupling them, data can be stored persistently, while computing power can be scaled up only for the duration of the processing.
````

## Q. 15 — Create a Small Metadata Catalogue

````
Dataset	            Purpose	                Main columns	                    Source	            Owner/team	        Last update
bronze_orders	    Received order data	    order_id, city, amount, status	    Source batches	    Data Engineering	2026-08-01
silver_orders	    Clean reusable orders	order_id, city, amount, status	    bronze_orders	    Data Engineering	2026-08-01
gold_daily_sales	Reporting summary	    city, revenue_gbp	                silver_orders	    Analytics/Data	    2026-08-01
````

## Q. 16 — MCQ: Metadata
Why is metadata useful?

````
Answer: B. It describes data so people and systems can understand what the data represents
````

# Optional Practice
## Q. 17 — Trace One Record Through Bronze, Silver, and Gold

````python
initial_data = {
    "order_id": 9001,
    "city": " London ",
    "amount_gbp": 50,
    "status": "complete"
}

bronze = {
    "order_id": 9001,
    "city": " London ",
    "amount_gbp": 50,
    "status": "complete"
}

silver = {
    "order_id": 9001,
    "city": "London",
    "amount_gbp": 50.00,
    "status": "complete"
}

gold = "The row contributes £50 to London's reporting total."

print(bronze)
print(silver)
print(gold)
````

## Q. 18 — Find a Layering Mistake
A team creates Gold directly from raw Bronze data and repeats different cleaning rules in five reports.
Explain two problems with this design.

````
Without a Silver layer: Cleaning logic is duplicated, leading to inconsistent reports, corrupted totals, and hard-to-maintain rules.
````

## Q. 19 — Reconcile the Layers
BritMart has:
Bronze rows = 1000
Silver rows = 960

The team says:
25 rows had invalid amounts
15 rows were duplicates

Check whether the numbers reconcile.

````
Answer: 
Rejected/removed rows = 25 + 15 = 40
Expected Silver rows = 1000 - 40 = 960

The counts reconcile.
````

## Q. 20 — Design a Small Platform
Create one architecture using only today's concepts.
It must include:

3 source types
Bronze
Silver
Gold
storage
compute
metadata/catalogue
one reporting consumer

````mermaid
flowchart LR
    A["MySQL"] --> B["Bronze"]
    C["CSV Files"] --> B
    D["JSON"] --> B

    B --> E["Silver"]
    E --> F["Gold"]
    F --> G["Reporting"]

    S["Storage"] --- B
    S --- E
    S --- F

    C1["Compute"] --- E
    C1 --- F

    M["Metadata Catalogue"] --- B
    M --- E
    M --- F
````





