
import pandas as pd
from pathlib import Path


# ==========================================
# 1. PROJECT PATH: Project Setup
# ==========================================

# Find the root folder of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the path to the Dryad dataset
DRYAD_PATH = PROJECT_ROOT / "data" / "raw" / "dryad"



# ==========================================
# 2. LOAD DATA: Data Ingestion
# ==========================================

def load_dryad_data():

    # Load the fixed-partner experiment
    fix_df = pd.read_csv(DRYAD_PATH / "fix.csv", sep=";")

    # Load the random-partner experiment
    rand_df = pd.read_csv(DRYAD_PATH / "rand.csv", sep=";")

    # Load participant survey information
    users_df = pd.read_csv(DRYAD_PATH / "UserInformation.csv", sep=";")

    return fix_df, rand_df, users_df

if __name__ == "__main__":

# Load all three datasets
    fix_df, rand_df, users_df = load_dryad_data()


# ==========================================
# 3. INSPECT THE DATA: Data Discovery
# ==========================================

# Display the first 5 rows of each dataset
    print("\nFIXED-PARTNER DATA:")
    print(fix_df.head())

    print("\nRANDOM-PARTNER DATA:")
    print(rand_df.head())

    print("\nUSER INFORMATION:")
    print(users_df.head())


# ==========================================
# 4. CHECK DATASET SIZES: Data Discovery
# ==========================================

# Display the number of rows and columns
    print("\nDATASET SHAPES:")
    print("Fix:", fix_df.shape)
    print("Rand:", rand_df.shape)
    print("User information:", users_df.shape)


# ==========================================
# 5. CHECK COLUMN INFORMATION: Data Discovery
# ==========================================

# Display column names, data types and non-null values
    print("\nFIXED-PARTNER INFO:")
    fix_df.info()

    print("\nRANDOM-PARTNER INFO:")
    rand_df.info()

    print("\nUSER INFORMATION INFO:")
    users_df.info()

# ==========================================
# 6. MISSING VALUES CHECK: Data Quality / Validation
# ==========================================

# Count missing values in each dataset
    print("\nMISSING VALUES IN FIX:")
    print(fix_df.isnull().sum())

    print("\nMISSING VALUES IN RAND:")
    print(rand_df.isnull().sum())

    print("\nMISSING VALUES IN USER INFORMATION:")
    print(users_df.isnull().sum())

# ==========================================
# 7. CHECK IMPORTANT GAME COLUMNS: Data Quality / Validation
# ==========================================

# Check missing values in the main game columns
    important_columns = [
        "action_player",
        "action_opponent",
        "payoff"
    ]

    print("\nIMPORTANT COLUMNS IN FIX:")
    print(fix_df[important_columns].isnull().sum())

    print("\nIMPORTANT COLUMNS IN RAND:")
    print(rand_df[important_columns].isnull().sum())

# ==========================================
# 8. CHECK UNIQUE VALUES: Data Quality / Validation
# ==========================================

# Display all unique actions and payoffs
    print("\nUNIQUE VALUES IN FIX:")
    print("Player actions:", fix_df["action_player"].unique())
    print("Opponent actions:", fix_df["action_opponent"].unique())
    print("Payoffs:", sorted(fix_df["payoff"].unique()))

    print("\nUNIQUE VALUES IN RAND:")
    print("Player actions:", rand_df["action_player"].unique())
    print("Opponent actions:", rand_df["action_opponent"].unique())
    print("Payoffs:", sorted(rand_df["payoff"].unique()))

# ==========================================
# 9. CHECK ROUNDS PER PLAYER: Data Quality / Validation
# ==========================================

# Count the number of rounds for each player
    fix_rounds = fix_df.groupby("player")["round"].count()
    rand_rounds = rand_df.groupby("player")["round"].count()

    print("\nROUNDS PER PLAYER IN FIX:")
    print(fix_rounds.describe())

    print("\nROUNDS PER PLAYER IN RAND:")
    print(rand_rounds.describe())


# ==========================================
# 10. EXTRACT PARTICIPANT ID: Data Discovery
# ==========================================

# Get the first player ID
    player_id = fix_df["player"].iloc[0]

# Find where "usuario" starts
    start_position = player_id.find("usuario")

# Extract the participant ID
    participant_id = player_id[start_position:]

# Display the results
    print("\nPLAYER ID EXAMPLE:")
    print("Original ID:", player_id)
    print("Participant ID:", participant_id)

# ==========================================
# 11. COMPARE PARTICIPANT IDs: Data Discovery
# ==========================================

# Get all participant IDs from User Information
    user_ids = users_df["UserID"]

# Check if the extracted ID exists in User Information
    participant_id = "usuario1"

    if participant_id in user_ids.values:
        print("Participant found!")
    else:
        print("Participant not found!")

# ==========================================
# 11. CHECK ALL PARTICIPANTS: Data Discovery
# ==========================================

# Get all participant IDs from User Information
    user_ids = users_df["UserID"].values

# Extract participant IDs from the game datasets
    fix_players = fix_df["player"].str.extract(r"(usuario\d+)")[0]
    rand_players = rand_df["player"].str.extract(r"(usuario\d+)")[0]

# Check Fixed Partner participants
    missing_fix = []

    for player in fix_players.unique():
        if player not in user_ids:
            missing_fix.append(player)

# Check Random Partner participants
    missing_rand = []

    for player in rand_players.unique():
        if player not in user_ids:
            missing_rand.append(player)

# Display results
    print("\nPARTICIPANT MATCHING:")
    print("Missing participants in FIX:", missing_fix)
    print("Missing participants in RAND:", missing_rand)

# ==========================================
# 12. CHECK EXPERIMENT TREATMENTS: Data Discovery
# ==========================================

# Check treatment values in each dataset
    print("\nTREATMENTS IN FIX:")
    print(fix_df["treatment"].unique())

    print("\nTREATMENTS IN RAND:")
    print(rand_df["treatment"].unique())

    print("\nTREATMENTS IN USER INFORMATION:")
    print(users_df["Treatment"].value_counts())

# ==========================================
# 13. CHECK TREATMENT CONSISTENCY: Data Discovery
# ==========================================

# Extract participant IDs from each game dataset
    fix_ids = fix_df["player"].str.extract(r"(usuario\d+)")[0].unique()
    rand_ids = rand_df["player"].str.extract(r"(usuario\d+)")[0].unique()

# Check treatments for FIX participants
    print("\nFIX PARTICIPANTS:")
    print(users_df[users_df["UserID"].isin(fix_ids)]["Treatment"].value_counts())

# Check treatments for RAND participants
    print("\nRAND PARTICIPANTS:")
    print(users_df[users_df["UserID"].isin(rand_ids)]["Treatment"].value_counts())

# Check the number of unique participant IDs
    print("\nRAND ID CHECK:")
    print("Number of unique IDs:", len(rand_ids))
    print("First 10 IDs:", rand_ids[:10])

# Count matched participants
    matched_users = users_df[users_df["UserID"].isin(rand_ids)]

    print("Number of matched users:", len(matched_users))
    print("\nMatched treatments:")
    print(matched_users["Treatment"].value_counts())

# ==========================================
# 14. INVESTIGATE PARTICIPANT IDs: Data Discovery
# ==========================================

# Extract participant IDs from RAND
    rand_ids = rand_df["player"].str.extract(r"(usuario\d+)")[0].unique()

# Find matching users
    matched_users = users_df[users_df["UserID"].isin(rand_ids)]

    print("\nID INVESTIGATION:")

    print("Unique RAND IDs:", len(rand_ids))

    print("Matched rows:", len(matched_users))

    print("Unique matched UserIDs:", matched_users["UserID"].nunique())

    print("\nFIRST 20 PLAYER IDs:")
    print(rand_df["player"].drop_duplicates().head(20).to_list())

    print("\nFIRST 20 USER IDs:")
    print(users_df["UserID"].head(20).to_list())

# ==========================================
# 15. INVESTIGATE SESSION IDENTIFIERS: Data Discovery
# ==========================================

# Display information about participant usuario1
    print("\nUSER INFORMATION FOR usuario1:")
    print(
        users_df[users_df["UserID"] == "usuario1"][
            ["UserID", "Experiment Session", "Treatment"]
        ].to_string(index=False)
    )

# Display player IDs and sessions from RAND
    print("\nRAND PLAYER SESSIONS:")
    print(
        rand_df[["player", "session", "treatment"]]
        .drop_duplicates()
        .head(15)
        .to_string(index=False)
    )

# ==========================================
# 16. CHECK SESSION AND USER ID MATCHING: Data Quality / Validation
# ==========================================

# Extract participant IDs from player column
    rand_df["UserID"] = rand_df["player"].str.split("usuario").str[-1]

# Add the "usuario" prefix
    rand_df["UserID"] = "usuario" + rand_df["UserID"]

# Get unique participants and sessions
    rand_participants = rand_df[["session", "UserID"]].drop_duplicates()

# Check matching with User Information
    matched_rand = rand_participants.merge(
        users_df,
        left_on=["session", "UserID"],
        right_on=["Experiment Session", "UserID"],
        how="left",
        indicator=True
    )

# Display results
    print("\nSESSION AND USER ID MATCHING:")
    print(matched_rand["_merge"].value_counts())

# ==========================================
# 17. CHECK FIXED-PARTNER SESSION MATCHING: Data Quality / Validation
# ==========================================

# Extract participant IDs from player column
    fix_df["UserID"] = "usuario" + fix_df["player"].str.split("usuario").str[-1]

# Get unique participants and sessions
    fix_participants = fix_df[["session", "UserID"]].drop_duplicates()

# Match participants with User Information
    matched_fix = fix_participants.merge(
        users_df,
        left_on=["session", "UserID"],
        right_on=["Experiment Session", "UserID"],
        how="left",
        indicator=True
    )

# Display matching results
    print("\nFIXED-PARTNER SESSION AND USER ID MATCHING:")
    print(matched_fix["_merge"].value_counts())


# ==========================================
# 18. VALIDATE PAYOFF VALUES: Data Quality / Validation
# ==========================================

# Define the expected payoff for each action combination
    payoff_rules = {
        ("C", "C"): 3,
        ("C", "D"): 0,
        ("D", "C"): 4,
        ("D", "D"): 1
    }

# Check payoff values in both datasets
    for name, df in [("FIX", fix_df), ("RAND", rand_df)]:

        # Calculate the expected payoff
        expected_payoff = [
            payoff_rules[(player, opponent)]
            for player, opponent in zip(
                df["action_player"],
                df["action_opponent"]
            )
        ]

    # Compare actual and expected payoffs
        matches = df["payoff"].values == expected_payoff

        print(f"\nPAYOFF VALIDATION IN {name}:")
        print("Correct payoffs:", matches.sum())
        print("Incorrect payoffs:", (~matches).sum())
