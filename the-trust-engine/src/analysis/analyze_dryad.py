from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Define the project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the path to processed data
DATA_PATH = PROJECT_ROOT / "data" / "processed"


def load_dryad_data():
    """
    Load the processed FIX and RAND datasets.
    """
    fix_df = pd.read_csv(DATA_PATH / "dryad_fix.csv")
    rand_df = pd.read_csv(DATA_PATH / "dryad_rand.csv")

    return fix_df, rand_df

def calculate_cooperation_metrics(df, treatment_name):
    """
    Calculate individual and mutual cooperation rates.
    """

    # Calculate individual cooperation rate
    player_cooperation_rate = (
        df["action_player"] == "C"
    ).mean() * 100

    # Calculate mutual cooperation rate
    mutual_cooperation = (
        (df["action_player"] == "C")
        & (df["action_opponent"] == "C")
    )

    mutual_cooperation_rate = mutual_cooperation.mean() * 100

    # Display results
    print(f"\n{treatment_name} COOPERATION METRICS")
    print("-" * 40)

    print(
        f"Player Cooperation Rate: "
        f"{player_cooperation_rate:.2f}%"
    )

    print(
        f"Mutual Cooperation Rate: "
        f"{mutual_cooperation_rate:.2f}%"
    )

    return {
        "Treatment": treatment_name,
        "Player Cooperation": player_cooperation_rate,
        "Mutual Cooperation": mutual_cooperation_rate
    }

def plot_cooperation_metrics(metrics):
    """
    Create a bar chart comparing FIX and RAND cooperation rates.
    """

    # Convert results into a DataFrame
    metrics_df = pd.DataFrame(metrics)

    # Use treatment names as chart labels
    metrics_df = metrics_df.set_index("Treatment")

    # Create the bar chart
    metrics_df.plot(
        kind="bar",
        figsize=(8, 5)
    )

    # Add chart labels and title
    plt.title("Cooperation Rates: FIX vs RAND")
    plt.ylabel("Percentage (%)")
    plt.xlabel("Experiment Treatment")
    plt.xticks(rotation=0)
    plt.legend(title="Metric")

    # Adjust chart layout
    plt.tight_layout()

    # Create a folder for figures
    figures_path = PROJECT_ROOT / "docs" / "figures"
    figures_path.mkdir(parents=True, exist_ok=True)

    # Save the chart
    plt.savefig(
        figures_path / "dryad_cooperation_comparison.png",
        dpi=300
    )

    # Display the chart
    plt.show()

    plt.close()

def analyze_cooperation_over_rounds(fix_df, rand_df):
    """
    Calculate player cooperation rate for each round.
    """

    # Calculate cooperation rate for each round
    fix_by_round = (
        fix_df.assign(cooperated=fix_df["action_player"] == "C")
        .groupby("round")["cooperated"]
        .mean() * 100
    )

    rand_by_round = (
        rand_df.assign(cooperated=rand_df["action_player"] == "C")
        .groupby("round")["cooperated"]
        .mean() * 100
    )

    # Create a line chart
    plt.figure(figsize=(10, 5))

    plt.plot(
        fix_by_round.index,
        fix_by_round.values,
        label="FIX"
    )

    plt.plot(
        rand_by_round.index,
        rand_by_round.values,
        label="RAND"
    )

    plt.title("Player Cooperation Rate Across 100 Rounds")
    plt.xlabel("Round")
    plt.ylabel("Cooperation Rate (%)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # Save the chart
    figures_path = PROJECT_ROOT / "docs" / "figures"
    figures_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        figures_path / "dryad_cooperation_over_rounds.png",
        dpi=300
    )

    plt.show()
    plt.close()

def compare_early_and_late_cooperation(fix_df, rand_df):
    """
    Compare cooperation rates in the first and last 10 rounds.
    """

    datasets = {
        "FIX": fix_df,
        "RAND": rand_df
    }

    for treatment, df in datasets.items():

        # Select the first 10 rounds
        early_rounds = df[df["round"] <= 10]

        # Select the last 10 rounds
        late_rounds = df[df["round"] >= 91]

        # Calculate cooperation rates
        early_rate = (
            (early_rounds["action_player"] == "C").mean() * 100
        )

        late_rate = (
            (late_rounds["action_player"] == "C").mean() * 100
        )

        # Calculate the difference
        change = late_rate - early_rate

        print(f"\n{treatment} — EARLY vs LATE")
        print("-" * 40)
        print(f"First 10 rounds: {early_rate:.2f}%")
        print(f"Last 10 rounds:  {late_rate:.2f}%")
        print(f"Change:          {change:+.2f} percentage points") 

def analyze_response_to_previous_opponent_action(fix_df, rand_df):
    """
    Compare player cooperation rates based on the opponent's
    previous action.
    """

    datasets = {
        "FIX": fix_df,
        "RAND": rand_df
    }

    for treatment, df in datasets.items():

        # Remove first-round records without previous actions
        valid_df = df.dropna(subset=["prev_opp"]).copy()

        # Calculate cooperation rate for each previous opponent action
        results = (
            valid_df.groupby("prev_opp")["action_player"]
            .apply(lambda actions: (actions == "C").mean() * 100)
        )

        # Count observations for each previous action
        counts = valid_df["prev_opp"].value_counts()

        print(f"\n{treatment} — RESPONSE TO PREVIOUS OPPONENT ACTION")
        print("-" * 50)

        for previous_action in ["C", "D"]:
            rate = results.get(previous_action, float("nan"))
            count = counts.get(previous_action, 0)

            print(
                f"Previous opponent action: {previous_action} | "
                f"Observations: {count} | "
                f"Player cooperation: {rate:.2f}%"
            )

def plot_response_to_previous_action(fix_df, rand_df):
    """
    Visualize cooperation rates after previous opponent actions.
    """

    fix_rates = (
        fix_df.dropna(subset=["prev_opp"])
        .groupby("prev_opp")["action_player"]
        .apply(lambda actions: (actions == "C").mean() * 100)
    )

    rand_rates = (
        rand_df.dropna(subset=["prev_opp"])
        .groupby("prev_opp")["action_player"]
        .apply(lambda actions: (actions == "C").mean() * 100)
    )

    results = pd.DataFrame({
        "FIX": fix_rates,
        "RAND": rand_rates
    })

    results.index = [
        "Previous opponent: C",
        "Previous opponent: D"
    ]

    results.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title("Cooperation After Previous Opponent Action")
    plt.xlabel("Previous Opponent Action")
    plt.ylabel("Player Cooperation Rate (%)")
    plt.xticks(rotation=0)
    plt.legend(title="Treatment")
    plt.tight_layout()

    figures_path = PROJECT_ROOT / "docs" / "figures"
    figures_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(
        figures_path / "dryad_response_to_previous_action.png",
        dpi=300
    )

    plt.show()
    plt.close()

def main():
    # Load both datasets
    fix_df, rand_df = load_dryad_data()

    # Display basic information
    print("FIX DATASET")
    print("Shape:", fix_df.shape)
    print("Columns:", fix_df.columns.tolist())
    print()

    print("RAND DATASET")
    print("Shape:", rand_df.shape)
    print("Columns:", rand_df.columns.tolist())

    # Calculate cooperation metrics
    fix_metrics = calculate_cooperation_metrics(fix_df, "FIX")
    rand_metrics = calculate_cooperation_metrics(rand_df, "RAND")

    # Create comparison chart
    plot_cooperation_metrics([fix_metrics, rand_metrics])

    # Create comparison chart over rounds
    analyze_cooperation_over_rounds(fix_df, rand_df)

    compare_early_and_late_cooperation(fix_df, rand_df)

    analyze_response_to_previous_opponent_action(fix_df, rand_df)

    plot_response_to_previous_action(fix_df, rand_df)






if __name__ == "__main__":
    main()