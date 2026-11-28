import pandas as pd
import networkx as nx

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Load processed Bitcoin OTC data
df = pd.read_csv("data/processed/bitcoin_otc.csv")

# Create a directed graph
G = nx.DiGraph()

# Add users and ratings as directed edges
for _, row in df.iterrows():
    G.add_edge(
        row["source"],
        row["target"],
        weight=row["rating"]
    )

# Display basic network information
print("\nBITCOIN OTC NETWORK OVERVIEW")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())


# Calculate in-degree and out-degree
in_degree = dict(G.in_degree())
out_degree = dict(G.out_degree())

# Create a DataFrame with network metrics
degree_df = pd.DataFrame({
    "user_id": list(G.nodes()),
    "in_degree": [in_degree[user] for user in G.nodes()],
    "out_degree": [out_degree[user] for user in G.nodes()]
})

# Calculate total degree
degree_df["total_degree"] = (
    degree_df["in_degree"] + degree_df["out_degree"]
)

# Sort users by total degree
degree_df = degree_df.sort_values(
    by="total_degree",
    ascending=False
)

print("\nTOP 10 USERS BY TOTAL DEGREE")
print(degree_df.head(10))



# Identify positive ratings
df["is_positive"] = (df["rating"] > 0).astype(int)

# Calculate reputation metrics for each user
rating_summary = df.groupby("target").agg(
    mean_rating=("rating", "mean"),
    positive_rate=("is_positive", "mean")
).reset_index()

# Convert positive rate into percentage
rating_summary["positive_rate"] *= 100

# Combine network metrics with reputation metrics
network_reputation = degree_df.merge(
    rating_summary,
    left_on="user_id",
    right_on="target",
    how="left"
)

# Display the most connected users and their reputation
print("\nNETWORK ACTIVITY VS REPUTATION")
print(
    network_reputation[
        [
            "user_id",
            "in_degree",
            "out_degree",
            "total_degree",
            "mean_rating",
            "positive_rate"
        ]
    ].head(10).round(2)
)

# Keep users who have received at least one rating
correlation_data = network_reputation.dropna(
    subset=["mean_rating"]
).copy()

# Calculate Spearman correlation
correlation = correlation_data[
    ["total_degree", "mean_rating"]
].corr(method="spearman")

print("\nCONNECTIVITY VS REPUTATION CORRELATION")
print(correlation)

print(
    "\nSpearman correlation:",
    correlation.loc["total_degree", "mean_rating"].round(3)
)


# Calculate correlations between network activity and reputation
correlations = network_reputation[
    [
        "in_degree",
        "out_degree",
        "mean_rating",
        "positive_rate"
    ]
].corr(method="spearman")

print("\nDETAILED NETWORK AND REPUTATION CORRELATIONS")
print(correlations.round(3))


# Create correlation heatmap
plt.figure(figsize=(8, 6))

sns.heatmap(
    correlations,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f"
)

plt.title("Bitcoin OTC: Network Activity and Reputation Correlations")
plt.tight_layout()

# Save the figure
output_dir = Path("docs/figures")
output_dir.mkdir(parents=True, exist_ok=True)

plt.savefig(
    output_dir / "bitcoin_network_reputation_correlation.png",
    dpi=300
)

plt.close()

print("\nCorrelation heatmap saved successfully!")