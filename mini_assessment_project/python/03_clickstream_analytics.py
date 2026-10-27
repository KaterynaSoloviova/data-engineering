
from pathlib import Path
import pandas as pd

project_dir = Path("/Users/katerynasoloviova/Documents/ironhack_DE/mini_assessment_project/")
data_dir = project_dir / "data"
cleaned_data_dir = project_dir / "data" / "cleaned_data"


clickstream = pd.read_csv(
    cleaned_data_dir / "clickstream_cleaned.csv"
)
print("Cleaned clickstream loaded successfully!")
print(clickstream.head())

print(f"\n{'=' * 60}")
print("Most visited pages")
print("=" * 60)

# Find the most visited pages
page_visits = (
    clickstream["page_url"]
    .value_counts()
    .reset_index()
)

page_visits.columns = ["page_url", "visit_count"]

page_visits = page_visits.sort_values(
    by="visit_count",
    ascending=False
)

print("\nMost visited pages:")
print(page_visits.head(10))

output_dir = data_dir / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

page_visits.to_csv(
    output_dir / "most_visited_pages.csv",
    index=False
)

print("\nResults saved successfully!")

print(f"\n{'=' * 60}")
print("Calculate session counts.")
print("=" * 60)

# Calculate session counts. 

#1 Check that the time is in the correct format
clickstream["event_timestamp"] = pd.to_datetime(
    clickstream["event_timestamp"],
    errors="coerce",
    utc=True
)

#2 Remove rows that cannot be used for calculation
session_data = clickstream.dropna(
    subset=["customer_id", "event_timestamp"]
).copy()

#3 Sorting events
session_data = session_data.sort_values(
    ["customer_id", "event_timestamp"]
)

#4 Calculating the time between events
session_data["time_diff"] = (
    session_data.groupby("customer_id")["event_timestamp"].diff()
)

#5 Determining the start of a new session
session_data["new_session"] = (
    session_data["time_diff"].isna()
    | (session_data["time_diff"] > pd.Timedelta(minutes=30))
)

#6 Count sessions for each client
sessions_per_customer = (
    session_data.groupby("customer_id")["new_session"]
    .sum()
    .reset_index(name="session_count")
)

#7 Total sessions
total_sessions = int(
    sessions_per_customer["session_count"].sum()
)

print("\nSessions per customer:")
print(sessions_per_customer.to_string(index=False))

print(f"\nTotal sessions: {total_sessions}")


output_dir = project_dir / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

sessions_per_customer.to_csv(
    output_dir / "session_counts.csv",
    index=False
)

print("\nSession results saved successfully!")



print(f"\n{'=' * 60}")
print("Mobile vs Desktop Traffic Percentage")
print("=" * 60)

# Find mobile vs desktop traffic percentage

# Step 1: Standardize device names
clickstream["device_type"] = (
    clickstream["device_type"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Step 2: Keep only mobile and desktop events
device_data = clickstream[
    clickstream["device_type"].isin(["mobile", "desktop"])
].copy()

# Step 3: Count events for each device type
device_counts = device_data["device_type"].value_counts()

# Step 4: Calculate percentages
device_percentages = (
    device_counts / device_counts.sum() * 100
).round(2)

# Step 5: Create a results table
device_report = pd.DataFrame({
    "event_count": device_counts,
    "percentage": device_percentages
})

print("\nDevice traffic report:")
print(device_report)

# Step 6: Save the report
device_report.to_csv(
    output_dir / "device_traffic_report.csv",
    index_label="device_type"
)

print("\nDevice traffic report saved successfully!")
