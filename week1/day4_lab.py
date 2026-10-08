import pandas as pd

# Part 1 — DataFrames and CSV Files

#1 Create a DataFrame

df = pd.DataFrame({
    "order_id": [100, 102, 103, 104],
    "city": ["London", "Manchester", "London", "Leeds"],
    "amount_gbp": [45.50, 18.00, 62.25, 30.00],
    "status": ["complete", "cancelled", "complete", "complete"],
})

print(df)
print(df.columns)
print(df.shape)

#2 Create and Read Three CSV Batches
batch_1_q2 = pd.read_csv("week1/batch_1_q2.csv")
print(batch_1_q2)

batch_2_q2 = pd.read_csv("week1/batch_2_q2.csv")
print(batch_2_q2)

batch_3_q2 = pd.read_csv("week1/batch_3_q2.csv")
print(batch_3_q2)


#3 Combine the CSV Batches into one DataFrame

all_batches = pd.concat([batch_1_q2, batch_2_q2, batch_3_q2], ignore_index=True)
print(all_batches)

#total row count
print(len(all_batches))
#first three rows
print(all_batches.head(3))
#last three rows
print(all_batches.tail(3))

#4 MCQ: DataFrame: Which description best matches a Pandas DataFrame? 
#Answer: A. A two-dimensional labelled table with rows and columns.

# Part 2 — Excel, JSON, Inspection, and Column Selection
# 5 Write and Read an Excel File

products = pd.DataFrame({
    "product_id": [1, 2, 3],
    "product_name": ["Desk Lamp", "Office Chair", "Notebook Set"],
    "price_gbp": [24.99, 89.50, 8.75],
})

products.to_excel("products.xlsx", index=False)

products_from_excel = pd.read_excel("week1/products.xlsx")
print(products_from_excel)

#6 Read a JSON File
customers = pd.read_json("week1/customers.json")
print(customers.head())
print(customers.shape)
print(customers.info())

#7 Select Only Required Columns

new_data_frame = all_batches[
    ["order_id", "city", "amount_gbp"]
]
print(new_data_frame)

amount_series = all_batches["amount_gbp"]
print(amount_series)

#8 MCQ: Inspecting Data: Which command gives the number of rows and columns as a tuple?
# Answer: C. df.shape

# Part 3 — Filtering, Missing Values, Renaming, and Derived Columns
#9 Filter Completed Orders

completed_orders= all_batches[all_batches["status"] == "complete"]
completed_revenue = completed_orders["amount_gbp"].sum()

print(f"{completed_revenue:.2f}")

#10 Clean Missing Values
df = pd.DataFrame({
    "order_id": [301, 302, 303, 304],
    "city": ["London", None, "Leeds", "Bristol"],
    "amount_gbp": [45.50, 20.00, None, 30.00],
})

print(df.isnull().sum())

df["city"] = df["city"].fillna("Unknown")
df = df.dropna(subset=["amount_gbp"])
print(df)

#11  Rename and Create New Columns
df = pd.DataFrame({
    "id": [401, 402, 403],
    "price": [20.00, 50.00, 12.50],
    "qty": [2, 1, 4],
})

df = df.rename(columns={
    "id": "order_id",
    "price": "unit_price_gbp",
    "qty": "quantity"
})


df["line_total_gbp"] = df["unit_price_gbp"] * df["quantity"]
print(df)

# Part 4 — Sorting, Grouping, Aggregation, and Merging
#13 Sort Sales from Highest to Lowest

print(all_batches[["order_id", "city", "amount_gbp"]].sort_values("amount_gbp", ascending=False))

#14 Revenue by City
completed = all_batches[all_batches["status"] == "complete"]
 
result = (
    completed
    .groupby(
        "city",
        as_index=False,
    )
    .agg(
        revenue_gbp=(
            "amount_gbp",
            "sum",
        ),
        order_count=(
            "order_id",
            "count",
        ),
    )
    .sort_values(
        "revenue_gbp",
        ascending=False,
    )
)
 
print(result)

#15 Merge Orders with Store Details
orders = pd.DataFrame({
    "order_id": [501, 502, 503, 504],
    "store_id": ["LDN-01", "MAN-02", "LDN-01", "LDS-04"],
    "amount_gbp": [45.50, 30.00, 62.25, 20.00],
})

stores = pd.DataFrame({
    "store_id": ["LDN-01", "MAN-02", "LDS-04"],
    "city": ["London", "Manchester", "Leeds"],
    "region": ["South", "North", "North"],
})

merged = pd.merge(orders, stores, on="store_id",how="left")
print(merged)


#16 MCQ: Merge: Why is a left merge useful when orders is the left DataFrame?
#Answer: D. It keeps every order and adds matching store details when available.

#17-19 Optional Practice

batch1 = pd.read_csv("week1/batch_1_q17.csv")
batch2 = pd.read_csv("week1/batch_2_q17.csv")
batch3 = pd.read_csv("week1/batch_3_q17.csv")

all_orders = pd.concat([batch1, batch2, batch3], ignore_index=True)

non_positive = all_orders["amount_gbp"] <= 0
missing_city = all_orders["city"].isnull()
duplicate_id = all_orders["order_id"].duplicated(keep=False)

rejected = (
    (all_orders["amount_gbp"] <= 0)
    | (all_orders["city"].isnull())
    | (all_orders["order_id"].duplicated(keep=False))
)

rejected_orders = all_orders[rejected]
print(rejected_orders)

valid_orders = all_orders[~rejected]
print(valid_orders)

orders = all_orders.copy()
orders["rejection_reason"] = None

orders.loc[orders["city"].isnull(),"rejection_reason"] = "missing_city"
orders.loc[(orders["amount_gbp"] <= 0) & orders["rejection_reason"].isnull(), "rejection_reason"] = "non_positive_amount"

orders["duplicate_order"] = orders["order_id"].duplicated(keep=False)

orders.loc[orders["duplicate_order"] & orders["rejection_reason"].isnull(), "rejection_reason"] = "duplicate_order"

valid_orders = orders[orders["rejection_reason"].isnull()
]

rejected_orders = orders[orders["rejection_reason"].notna()]

print(valid_orders)

print(rejected_orders)













