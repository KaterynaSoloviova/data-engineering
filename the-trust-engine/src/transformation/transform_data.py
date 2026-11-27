
import pandas as pd


def transform_bitcoin_data(df):
    """
    Convert Unix timestamps into readable UTC datetime values.
    """

    df = df.copy()

    df["datetime"] = pd.to_datetime(
        df["timestamp"],
        unit="s",
        utc=True
    )

    return df


def transform_dryad_data(df):
    """
    Create readable labels for player actions and interaction types.
    """

    df = df.copy()

    # Create readable labels for player actions
    df["action_label"] = df["action_player"].map({
        "C": "Cooperation",
        "D": "Defection"
    })

    # Create readable labels for opponent actions
    df["opponent_action_label"] = df["action_opponent"].map({
        "C": "Cooperation",
        "D": "Defection"
    })

    # Describe the interaction between player and opponent
    df["interaction_type"] = (
        df["action_player"] + "_" + df["action_opponent"]
    ).map({
        "C_C": "Mutual Cooperation",
        "C_D": "Player Cooperates, Opponent Defects",
        "D_C": "Player Defects, Opponent Cooperates",
        "D_D": "Mutual Defection"
    })

    # Check that all actions were mapped
    if (
        df["action_label"].isnull().any()
        or df["opponent_action_label"].isnull().any()
        or df["interaction_type"].isnull().any()
    ):
        raise ValueError("Unknown action or interaction found!")

    return df

