import pandas as pd
import numpy as np

# Load Dataset
b_df = pd.read_csv("yds_data.csv")

# Remove Duplicate Columns
duplicate_cols = [
    "remaining_min.1",
    "remaining_sec.1",
    "power_of_shot.1",
    "knockout_match.1",
    "distance_of_shot.1"
]

b_df.drop(columns=duplicate_cols, errors="ignore", inplace=True)

# Create Unified Shot Type
b_df["shot_type"] = (
    b_df["type_of_shot"]
    .fillna(b_df["type_of_combined_shot"])
)

b_df.drop(
    columns=["type_of_shot", "type_of_combined_shot"],
    inplace=True
)

# Create Opponent Feature
b_df["opponent"] = (
    b_df["home/away"]
    .str.extract(r'(?:@|vs\.)\s*(\w+)', expand=False)
)

# Date Conversion
b_df["date_of_game"] = pd.to_datetime(
    b_df["date_of_game"],
    errors="coerce"
)

# Fill Numerical Missing Values
numeric_cols = [
    "location_x",
    "location_y",
    "remaining_min",
    "remaining_sec",
    "distance_of_shot",
    "power_of_shot",
    "match_event_id",
    "shot_id_number"
]

for col in numeric_cols:
    if col in b_df.columns:
        b_df[col] = b_df[col].fillna(b_df[col].median())

# Fill Categorical Missing Values
categorical_cols = [
    "game_season",
    "area_of_shot",
    "shot_basics",
    "range_of_shot",
    "shot_type",
    "opponent",
    "home/away",
    "lat/lng"
]

for col in categorical_cols:
    if col in b_df.columns:
        b_df[col] = b_df[col].fillna("Unknown")

# Remove Low Information Feature
if "team_name" in b_df.columns:
    if b_df["team_name"].nunique() <= 1:
        b_df.drop(columns=["team_name"], inplace=True)

# Train/Test Split
# Training data = known outcome
train_df = b_df[b_df["is_goal"].notna()].copy()

# Prediction data = unknown outcome
test_df = b_df[b_df["is_goal"].isna()].copy()

# Dashboard Dataset
dashboard_df = train_df.copy()

dashboard_df["goal_rate"] = (
    dashboard_df["is_goal"]
    .astype(int)
)

# Save Files
b_df.to_csv(
    "yds_clean.csv",
    index=False
)

train_df.to_csv(
    "yds_train.csv",
    index=False
)

test_df.to_csv(
    "yds_test.csv",
    index=False
)

dashboard_df.to_csv(
    "yds_dashboard.csv",
    index=False
)

# Summary
print("DATASET SUMMARY")

print(f"Full Cleaned Dataset: {b_df.shape}")
print(f"Training Dataset: {train_df.shape}")
print(f"Test Dataset: {test_df.shape}")
print(f"Dashboard Dataset: {dashboard_df.shape}")

print("\nTop Remaining Missing Values:")
print(
    b_df.isnull()
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

print("\nFiles Saved:")
print("- yds_clean.csv")
print("- yds_train.csv")
print("- yds_test.csv")
print("- yds_dashboard.csv")