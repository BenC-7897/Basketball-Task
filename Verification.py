import pandas as pd

# LOAD SAVED FILES
b_df = pd.read_csv("yds_cleaned.csv")
train_df = pd.read_csv("yds_train.csv")
test_df = pd.read_csv("yds_test.csv")
dashboard_df = pd.read_csv("yds_dashboard.csv")

print("DATASET VERIFICATION REPORT")

# SHAPES
print("\nDATASET SHAPES")
print("-" * 30)

print(f"Cleaned Dataset: {b_df.shape}")
print(f"Training Dataset: {train_df.shape}")
print(f"Test Dataset: {test_df.shape}")
print(f"Dashboard Dataset: {dashboard_df.shape}")

# DUPLICATES
print("\nDUPLICATE CHECK")
print("-" * 30)

print("Cleaned Dataset Duplicates:", b_df.duplicated().sum())

print("Train Dataset Duplicates:", train_df.duplicated().sum())

print("Test Dataset Duplicates:", test_df.duplicated().sum())

# MISSING VALUES
print("\nMISSING VALUES")
print("-" * 30)

print(b_df.isnull().sum().sort_values(
    ascending=False
).head(15))

# TRAIN / TEST VALIDATION
print("\nTRAIN / TEST SPLIT CHECK")
print("-" * 30)

print(
    "Missing is_goal in training set:",
    train_df["is_goal"].isnull().sum()
)

print(
    "Missing is_goal in test set:",
    test_df["is_goal"].isnull().sum()
)

print(
    "Known outcomes in training:",
    train_df["is_goal"].notna().sum()
)

print(
    "Unknown outcomes in test:",
    test_df["is_goal"].isna().sum()
)

# TARGET DISTRIBUTION
print("\nTARGET DISTRIBUTION")
print("-" * 30)

print(
    train_df["is_goal"]
    .value_counts(normalize=True)
    .round(4)
)

# DATA TYPES
print("\nDATA TYPES")
print("-" * 30)

print(b_df.dtypes)

# KEY FEATURE CHECK
print("\nKEY FEATURES")
print("-" * 30)

feature_list = [
    "shot_type",
    "power_of_shot",
    "opponent",
    "game_season",
    "distance_of_shot",
    "area_of_shot",
    "range_of_shot",
    "is_goal"
]

for col in feature_list:
    if col in b_df.columns:
        print(
            f"{col}: {b_df[col].nunique()} unique values"
        )

# TEAM NAME CHECK
print("\nTEAM NAME")
print("-" * 30)

if "team_name" in b_df.columns:
    print(
        "Unique values:",
        b_df["team_name"].nunique()
    )
else:
    print("team_name successfully removed")

# DASHBOARD VALIDATION
print("\nDASHBOARD DATASET CHECK")
print("-" * 30)

print(
    "Missing is_goal:",
    dashboard_df["is_goal"].isnull().sum()
)

print(
    "Missing goal_rate:",
    dashboard_df["goal_rate"].isnull().sum()
)

# SAVE REPORT
verification_summary = pd.DataFrame({
    "Metric": [
        "Cleaned Rows",
        "Train Rows",
        "Test Rows",
        "Dashboard Rows",
        "Duplicate Rows",
        "Missing is_goal Train",
        "Missing is_goal Test"
    ],
    "Value": [
        len(b_df),
        len(train_df),
        len(test_df),
        len(dashboard_df),
        b_df.duplicated().sum(),
        train_df["is_goal"].isnull().sum(),
        test_df["is_goal"].isnull().sum()
    ]
})

verification_summary.to_csv(
    "verification_report.csv",
    index=False
)

print("\nVerification report saved as:")
print("verification_report.csv")

print("\nVerification Complete")