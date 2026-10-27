import pandas as pd
from pathlib import Path

print(f"\n{'=' * 60}")
print("Load datasets")
print("=" * 60)

project_dir = Path("/Users/katerynasoloviova/Documents/ironhack_DE/mini_assessment_project/")
data_dir = project_dir / "data"
output_dir = project_dir / "data" / "cleaned_data"

customers = pd.read_csv(data_dir / "customers.csv")
orders = pd.read_csv(data_dir / "orders.csv")
products = pd.read_csv(data_dir / "products.csv")
clickstream = pd.read_csv(data_dir / "clickstream.csv")

print("All datasets loaded successfully!")


print(f"\n{'=' * 60}")
print("Standardize city names")
print("=" * 60)


# Standardize city names
customers["city"] = customers["city"].str.strip().str.title()
print("Cities standardized.")


print(f"\n{'=' * 60}")
print("Convert dates and timestamps")
print("=" * 60)

# Convert timestamps
customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

clickstream["event_timestamp"] = pd.to_datetime(
    clickstream["event_timestamp"],
    errors="coerce",
    format="mixed",
    utc=True
)

print("Dates converted successfully.") 

# Report dates that could not be analyzed
print(f"Invalid customer signup dates: {customers['signup_date'].isna().sum()}")
print(f"Invalid order dates: {orders['order_date'].isna().sum()}")
print(f"Invalid clickstream timestamps: {clickstream['event_timestamp'].isna().sum()}")


print(f"\n{'=' * 60}")
print("Handle missing values")
print("=" * 60)

# Handle missing values
clickstream["page_url"] = clickstream["page_url"].fillna("Unknown")
clickstream["device_type"] = clickstream["device_type"].fillna("Unknown")

print("Missing values after handling:")
print(clickstream.isnull().sum())

print("Missing customer IDs:")
print(clickstream["customer_id"].isnull().sum())

print("Rows with missing customer IDs are kept.")

print(f"\n{'=' * 60}")
print("Remove corrupted rows")
print("=" * 60)

# Remove corrupted rows

# Orders: remove rows with invalid quantities or prices
rows_before = len(orders)

orders = orders[
    (orders["quantity"] > 0) &
    (orders["unit_price"] >= 0)
]
print(f"Invalid order rows removed: {rows_before - len(orders)}")

# Products: remove rows with negative prices
rows_before = len(products)

products = products[
    (products["cost_price"] >= 0) &
    (products["selling_price"] >= 0)
]

print(f"Invalid product rows removed: {rows_before - len(products)}")

# Customers: remove rows without a customer ID
customers = customers.dropna(subset=["customer_id"])

# Clickstream: remove rows without a valid timestamp
clickstream = clickstream.dropna(subset=["event_timestamp"])

print("Corrupted rows removed.")


print(f"\n{'=' * 60}")
print("Save cleaned datasets")
print("=" * 60)

output_dir.mkdir(parents=True, exist_ok=True)

customers.to_csv(output_dir / "customers_cleaned.csv", index=False)
orders.to_csv(output_dir / "orders_cleaned.csv", index=False)
products.to_csv(output_dir / "products_cleaned.csv", index=False)
clickstream.to_csv(output_dir / "clickstream_cleaned.csv", index=False)

print("All cleaned datasets saved successfully!")




