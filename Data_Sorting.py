import pandas as pd
import numpy as np

# Load Dataset
cb_df = pd.read_csv("yds_cleaned.csv")

# Create season sort column
cb_df["season_year"] = (
    cb_df["game_season"]
    .str[:4]
)

# Convert to numeric
cb_df["season_year"] = pd.to_numeric(
    cb_df["season_year"],
    errors="coerce"
)

# Sort dataset
scb_df = cb_df.sort_values(
    by=["season_year", "date_of_game"],
    ascending=True
)

# Save
scb_df.to_csv("yds_cleaned.csv", index=False)