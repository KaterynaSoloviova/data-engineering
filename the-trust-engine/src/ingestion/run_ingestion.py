
# ==========================================
# THE TRUST ENGINE - INGESTION PIPELINE
# ==========================================

# 1. IMPORTS AND CONFIGURATION

import sys
from pathlib import Path

import pandas as pd

# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = PROJECT_ROOT / "src"

# Add src directory to Python module search path
sys.path.insert(0, str(SRC_PATH))

# Import project functions
from check_bitcoin_data import load_bitcoin_data
from check_dryad_data import load_dryad_data

from transformation.transform_data import (
    transform_bitcoin_data,
    transform_dryad_data
)


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def save_to_csv(df, file_name):
    """Save a DataFrame to the processed data directory."""

    processed_path = PROJECT_ROOT / "data" / "processed"
    processed_path.mkdir(parents=True, exist_ok=True)

    file_path = processed_path / file_name
    df.to_csv(file_path, index=False)

    print(f"Saved: {file_path.name}")


def inspect_dryad_data(df, dataset_name):
    """Display basic quality checks and interaction statistics."""

    print(f"\n{dataset_name} DATA TYPES:")
    print(df.dtypes)

    print(f"\n{dataset_name} MISSING VALUES:")
    print(df.isnull().sum())

    print(f"\n{dataset_name} PLAYER ACTIONS:")
    print(df["action_player"].value_counts())

    print(f"\n{dataset_name} OPPONENT ACTIONS:")
    print(df["action_opponent"].value_counts())

    print(f"\n{dataset_name} ROUND RANGE:")
    print("Minimum round:", df["round"].min())
    print("Maximum round:", df["round"].max())

    print(f"\n{dataset_name} INTERACTION PERCENTAGES:")
    percentages = (
        df["interaction_type"].value_counts(normalize=True) * 100
    ).round(2)

    print(percentages)


def verify_saved_data():
    """Read processed CSV files and verify their dimensions."""

    processed_path = PROJECT_ROOT / "data" / "processed"

    bitcoin_check = pd.read_csv(
        processed_path / "bitcoin_otc.csv"
    )
    fix_check = pd.read_csv(
        processed_path / "dryad_fix.csv"
    )
    rand_check = pd.read_csv(
        processed_path / "dryad_rand.csv"
    )
    users_check = pd.read_csv(
        processed_path / "dryad_user_information.csv"
    )

    print("\nVERIFYING SAVED DATA:")
    print("Bitcoin OTC:", bitcoin_check.shape)
    print("Dryad FIX:", fix_check.shape)
    print("Dryad RAND:", rand_check.shape)
    print("User Information:", users_check.shape)


# ==========================================
# 3. MAIN INGESTION PIPELINE
# ==========================================

def main():

    print("STARTING DATA INGESTION...")

    # --------------------------------------
    # BITCOIN OTC DATA
    # --------------------------------------

    # Load raw data
    bitcoin_df = load_bitcoin_data()

    # Transform data
    bitcoin_df = transform_bitcoin_data(bitcoin_df)

    # Preview transformed data
    print("\nBITCOIN OTC DATA AFTER TRANSFORMATION:")
    print(bitcoin_df[["timestamp", "datetime"]].head())

    # Validate datetime column
    print("\nMISSING DATETIME VALUES:")
    print(bitcoin_df["datetime"].isnull().sum())

    print("\nDATETIME DATA TYPE:")
    print(bitcoin_df["datetime"].dtype)

    print("\nDATETIME RANGE:")
    print("Earliest date:", bitcoin_df["datetime"].min())
    print("Latest date:", bitcoin_df["datetime"].max())

    print("\nBITCOIN OTC DATA SHAPE:")
    print(bitcoin_df.shape)

    # Save processed data
    save_to_csv(bitcoin_df, "bitcoin_otc.csv")

    # --------------------------------------
    # DRYAD DATA
    # --------------------------------------

    # Load raw datasets
    fix_df, rand_df, users_df = load_dryad_data()

    # Transform game datasets
    fix_df = transform_dryad_data(fix_df)
    rand_df = transform_dryad_data(rand_df)

    # Preview transformed data
    print("\nTRANSFORMED FIX ACTIONS:")
    print(fix_df[["action_player", "action_label"]].head())

    print("\nTRANSFORMED RAND ACTIONS:")
    print(rand_df[["action_player", "action_label"]].head())

    # Inspect fixed-partner dataset
    inspect_dryad_data(fix_df, "DRYAD FIX")

    # Inspect random-partner dataset
    inspect_dryad_data(rand_df, "DRYAD RAND")

    # --------------------------------------
    # DRYAD USER INFORMATION
    # --------------------------------------

    print("\nUSER INFORMATION DATA TYPES:")
    print(users_df.dtypes)

    print("\nUSER INFORMATION MISSING VALUES:")
    print(users_df.isnull().sum())

    print("\nUSER INFORMATION TREATMENTS:")
    print(users_df["Treatment"].value_counts())

    print("\nPARTICIPANT-SESSION RECORDS:")
    print(len(users_df))

    # --------------------------------------
    # SAVE DRYAD DATASETS
    # --------------------------------------

    print("\nDRYAD DATA SHAPES:")
    print("Fixed-partner:", fix_df.shape)
    print("Random-partner:", rand_df.shape)
    print("User information:", users_df.shape)

    save_to_csv(fix_df, "dryad_fix.csv")
    save_to_csv(rand_df, "dryad_rand.csv")
    save_to_csv(users_df, "dryad_user_information.csv")

    # --------------------------------------
    # VERIFY PROCESSED DATA
    # --------------------------------------

    verify_saved_data()

    print("\nDATA INGESTION COMPLETED!")


# ==========================================
# 4. SCRIPT EXECUTION
# ==========================================

if __name__ == "__main__":
    main()
