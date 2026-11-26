
import pandas as pd
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load raw data
file_path = PROJECT_ROOT / "data" / "raw" / "soc-sign-bitcoinotc.csv.gz"

df = pd.read_csv(
    file_path,
    compression="gzip",
    header=None,
    names=["source", "target", "rating", "timestamp"]
)

print("\nTIMESTAMP CHECK")

fractional = df[
    (df["timestamp"] - df["timestamp"].round()).abs() > 0.000001
]

print("Number of fractional timestamps:", len(fractional))
print("Examples:")
print(fractional["timestamp"].head(10).to_list())

# 1. Check timestamp values
print("Are all timestamps whole numbers?")
print((df["timestamp"] % 1 == 0).all())

# Convert timestamp to integer and datetime
df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="s",
    utc=True
)
df["datetime"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)

print("\nTIMESTAMP EXAMPLES")
print(df[["timestamp", "datetime"]].head())

print("\nDATE RANGE:")
print("First date:", df["datetime"].min())
print("Last date:", df["datetime"].max())

# 2. Count unique users
unique_users = set(df["source"]).union(set(df["target"]))

print("\nNETWORK:")
print("Unique users:", len(unique_users))
print("Unique interactions:", len(df))

# 3. Rating distribution
print("\nRATING DISTRIBUTION:")
print(df["rating"].value_counts().sort_index())

# 4. Positive, negative and neutral ratings
positive = (df["rating"] > 0).sum()
negative = (df["rating"] < 0).sum()
neutral = (df["rating"] == 0).sum()

total = len(df)

print("\nRATING CATEGORIES:")
print(f"Positive: {positive} ({positive / total * 100:.2f}%)")
print(f"Negative: {negative} ({negative / total * 100:.2f}%)")
print(f"Neutral: {neutral} ({neutral / total * 100:.2f}%)")

# 5. Data quality checks
print("\nDATA QUALITY:")
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Self-ratings:", (df["source"] == df["target"]).sum())

# 6. Most frequently rated users
top_targets = df["target"].value_counts().head(10)

print("\nTOP 10 MOST RATED USERS:")
print(top_targets)
