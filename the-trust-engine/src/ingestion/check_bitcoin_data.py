
import pandas as pd
from pathlib import Path


# ==========================================
# 1. PROJECT PATH
# ==========================================

# Find the root folder of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Path to the raw Bitcoin OTC dataset
file_path = PROJECT_ROOT / "data" / "raw" / "soc-sign-bitcoinotc.csv.gz"


# ==========================================
# 2. LOAD DATA
# ==========================================

def load_bitcoin_data():

    # Read the compressed CSV file into a DataFrame
    df = pd.read_csv(
        file_path,
        compression="gzip",
        header=None,
        names=["source", "target", "rating", "timestamp"]
    )

    return df

if __name__ == "__main__":

# Load the dataset
    df = load_bitcoin_data()

# ==========================================
# 3. BASIC DATA INSPECTION
# ==========================================

# Display the first 5 rows
    print("FIRST 5 ROWS:")
    print(df.head())

# Display the number of rows and columns
    print("\nDATASET SHAPE:")
    print(df.shape)

# Display column names, data types and missing values
    print("\nDATASET INFO:")
    df.info()

# Display basic statistical information
    print("\nDESCRIPTIVE STATISTICS:")
    print(df.describe())


# ==========================================
# 4. DATA QUALITY CHECKS
# ==========================================

# Count missing values in each column
    print("\nMISSING VALUES:")
    print(df.isnull().sum())

# Count duplicated rows
    print("\nDUPLICATE ROWS:")
    print(df.duplicated().sum())

# Check the minimum and maximum rating
    print("\nRATING RANGE:")
    print("Minimum rating:", df["rating"].min())
    print("Maximum rating:", df["rating"].max())

# Find ratings outside the expected range (-10 to +10)
    print("\nINVALID RATINGS:")
    print(df[~df["rating"].between(-10, 10)])


# ==========================================
# 5. USER ID INSPECTION
# ==========================================

# Check the range of source user IDs
    print("\nSOURCE ID RANGE:")
    print("Minimum source ID:", df["source"].min())
    print("Maximum source ID:", df["source"].max())

# Check the range of target user IDs
    print("\nTARGET ID RANGE:")
    print("Minimum target ID:", df["target"].min())
    print("Maximum target ID:", df["target"].max())

# Combine source and target IDs to find all unique users
    print("\nUNIQUE USERS:")
    all_users = pd.concat([df["source"], df["target"]])
    print("Total unique users:", all_users.nunique())


# ==========================================
# 6. USER ACTIVITY
# ==========================================

# Calculate the average number of ratings per unique user
    total_ratings = len(df)
    total_users = all_users.nunique()
    average_ratings = total_ratings / total_users

    print("\nAVERAGE RATINGS PER USER:")
    print(round(average_ratings, 2))

# Count how many ratings each user gave
    ratings_given = df["source"].value_counts()

    print("\nRATINGS GIVEN BY USERS:")
    print(ratings_given.head(10).to_string())

# Count how many ratings each user received
    ratings_received = df["target"].value_counts()

    print("\nRATINGS RECEIVED BY USERS:")
    print(ratings_received.head(10).to_string())


# ==========================================
# 7. USER REPUTATION EXPLORATION
# ==========================================

# Calculate average rating and number of ratings received by each user
    user_reputation = df.groupby("target")["rating"].agg(
        average_rating="mean",
        total_ratings="count"
    )

    # Sort users by average rating, from highest to lowest
    user_reputation = user_reputation.sort_values(
        by="average_rating",
        ascending=False
    )

    print("\nUSER REPUTATION:")
    print(user_reputation.head(10))
