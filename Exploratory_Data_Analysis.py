import pandas as pd
import numpy as np

# 1. Load dataset
b_df = pd.read_csv("yds_data.csv")

# 2. Column names and structure
print("\nDATASET OVERVIEW")
print("Rows:", b_df.shape[0])
print("Columns:", b_df.shape[1])
print("\nColumn names:")
print(b_df.columns.tolist())
print("\nData types:")
print(b_df.dtypes)

# 3. Missing values
print("\nMISSING VALUES")
missing = pd.DataFrame({
    "missing_count": b_df.isnull().sum(),
    "missing_percent": (b_df.isnull().mean() * 100).round(2)
})
print(missing[missing["missing_count"] > 0]
      .sort_values("missing_percent", ascending=False))

# 4. Duplicate rows
print("\nDUPLICATES")
print("Exact duplicate rows:", b_df.duplicated().sum())

# 5. Numerical outliers using the IQR method
print("\nPOTENTIAL NUMERICAL OUTLIERS")

numeric_cols = b_df.select_dtypes(include=np.number).columns

# Exclude likely identifiers and numeric-coded categories
exclude_cols = [
    col for col in b_df.columns
    if any(word in col.lower()
           for word in ["id", "index", "period", "power_of_shot"])
]

for col in numeric_cols:
    if col in exclude_cols or b_df[col].nunique() < 10:
        continue

    values = b_df[col].dropna()

    if values.empty:
        continue

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = values[(values < lower) | (values > upper)]

    print(
        f"{col}: {len(outliers)} potential outliers "
        f"({len(outliers) / len(values) * 100:.2f}%)"
    )

# 6. Categorical values
print("\nCATEGORICAL VALUE CHECK")

categorical_cols = b_df.select_dtypes(
    include=["object", "category", "string"]
).columns

for col in categorical_cols:
    print(f"\n{col}: {b_df[col].nunique(dropna=True)} unique values")
    print(b_df[col].value_counts(dropna=False).head(10))

# 7. Exact duplicate rows for further inspection
duplicates = b_df[b_df.duplicated(keep=False)]
if not duplicates.empty:
    print("\nDuplicate row examples:")
    print(duplicates.head(10))

print("\nEDA checks complete.")
b_df 