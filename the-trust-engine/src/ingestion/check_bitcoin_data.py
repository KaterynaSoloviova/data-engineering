
import pandas as pd
from pathlib import Path

# Find the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the dataset path
file_path = PROJECT_ROOT / "data" / "raw" / "soc-sign-bitcoinotc.csv.gz"

# Load the dataset
df = pd.read_csv(
    file_path,
    compression="gzip",
    header=None,
    names=["source", "target", "rating", "timestamp"]
)

print("FIRST 5 ROWS:")
print(df.head())

print("\nDATASET SHAPE:")
print(df.shape)

print("\nDATASET INFO:")
df.info()

print("\nDESCRIPTIVE STATISTICS:")
print(df.describe())
