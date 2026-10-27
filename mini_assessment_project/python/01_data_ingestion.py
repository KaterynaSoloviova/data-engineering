import pandas as pd
from pathlib import Path

project_dir = Path("/Users/katerynasoloviova/Documents/ironhack_DE/mini_assessment_project/")
data_dir = project_dir / "data"

# Read dataset 
customers = pd.read_csv(data_dir / "customers.csv")
orders = pd.read_csv(data_dir / "orders.csv")
products = pd.read_csv(data_dir / "products.csv")
clickstream = pd.read_csv(data_dir / "clickstream.csv")

data_files = {
    "customers": customers,
    "orders": orders,
    "products": products,
    "clickstream": clickstream
}

for name, df in data_files.items():
    print(f"\n{'=' * 60}")
    print(f"DATASET: {name.upper()}")
    print("=" * 60)

    # Display the first 5 rows
    print(f"The first 5 rows of {name} dataset:\n {df.head()}")
    # Check the number of rows and columns
    print(f"Shape of {name}: {df.shape[0]} rows, and {df.shape[1]} columns")
    # List all column names
    print(f"Column names of {name} dataset:\n {df.columns.tolist()} ")
    # Data types and non-null values
    print(f"Data info of {name} dataset:")
    df.info()
    # Check the missing values
    print(f"Missing values per column of {name} dataset:\n {df.isnull().sum()}")
    # Check the duplicate rows
    print(f"Amount of duplicated rows for {name} dataset: \n {df.duplicated().sum()}")
    # Basic statistics
    print("\nBasic statistics:")
    print(df.describe(include="all").T)


print(f"\n{'=' * 60}")
print("ID columns contain duplicates")
print("=" * 60)

# Check the ID columns contain duplicates
id_columns = {
    "customers": "customer_id",
    "orders": "order_id",
    "products": "product_id",
    "clickstream": "event_id"
}

for name, column in id_columns.items():
    df = data_files[name]
    print(
        f"{name}.{column}: "
        f"{df[column].duplicated().sum()} duplicate IDs"
    )

print(f"\n{'=' * 60}")
print("Schema consistency validation")
print("=" * 60)

# Schema consistency validation
expected_columns = {
    "customers": [
        "customer_id", "customer_name", "email", "city", "signup_date"
    ],
    "orders": [
        "order_id", "customer_id", "product_id",
        "order_date", "quantity", "unit_price", "payment_status"
    ],
    "products": [
        "product_id", "product_name", "category",
        "supplier_id", "cost_price", "selling_price"
    ],
    "clickstream": [
        "event_id", "customer_id", "event_type",
        "page_url", "event_timestamp", "device_type"
    ]
}

for name, df in data_files.items():
    expected = set(expected_columns[name])
    actual = set(df.columns)

    missing_columns = expected - actual
    unexpected_columns = actual - expected

    print(f"\nSchema validation: {name}")
    print("Missing columns:", missing_columns)
    print("Unexpected columns:", unexpected_columns)

print(f"\n{'=' * 60}")
print("Identify invalid records")
print("=" * 60)

# Identify invalid records
# 1. Orders: quantity must be greater than zero
invalid_quantities = orders[orders["quantity"] <= 0]
print(f"Number of orders with quantity <= 0: {len(invalid_quantities)}")
print(invalid_quantities)

# 2. Orders: unit price must not be negative
invalid_order_prices = orders[orders["unit_price"] < 0]
print(f"Number of orders with negative unit prices: {len(invalid_order_prices)}")
print(invalid_order_prices)

# 3. Products: cost price must not be negative
invalid_cost_prices = products[products["cost_price"] < 0]
print(f"Number of products with negative cost prices: {len(invalid_cost_prices)}")
print(invalid_cost_prices)

# 4. Products: selling price must not be negative
invalid_selling_prices = products[products["selling_price"] < 0]
print(f"Number of products with negative selling prices: {len(invalid_selling_prices)}")
print(invalid_selling_prices)

# 5. Customers: check email format
invalid_emails = customers[
    ~customers["email"].str.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        na=False
    )
]
print(f"Number of customers with invalid email format: {len(invalid_emails)}")
print(invalid_emails)

# 6. Clickstream: investigate duplicate event IDs
number_of_duplicate_ids = clickstream.loc[
    clickstream["event_id"].duplicated(keep=False),
    "event_id"
].nunique()

print(f"Number of distinct duplicated event IDs: {number_of_duplicate_ids}")



    


    


