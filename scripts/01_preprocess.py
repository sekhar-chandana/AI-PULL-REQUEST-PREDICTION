"""
==========================================================

PHASE 1 - DATA PREPROCESSING

AI Pull Request Risk Predictor

==========================================================
"""

import os
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder


# ==========================================================
# PROJECT PATH
# ==========================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "final_dataset_labeled.csv"
)

ML_DATASET_PATH = os.path.join(
    PROJECT_ROOT,
    "ml_dataset.csv"
)

ENCODER_PATH = os.path.join(
    PROJECT_ROOT,
    "label_encoders.pkl"
)


# ==========================================================
# START
# ==========================================================

print("=" * 80)
print("PHASE 1 : DATA PREPROCESSING")
print("=" * 80)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("\nLoading Dataset...")

df = pd.read_csv(
    DATASET_PATH
)

print(
    "Original Shape :",
    df.shape
)


# ==========================================================
# CONVERT DATES
# ==========================================================

print("\nConverting Dates...")

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)

df["merged_at"] = pd.to_datetime(
    df["merged_at"],
    errors="coerce"
)


# ==========================================================
# CREATE DATE FEATURES
# ==========================================================

print("\nCreating Date Features...")

df["created_year"] = (
    df["created_at"]
    .dt.year
    .fillna(0)
)

df["created_month"] = (
    df["created_at"]
    .dt.month
    .fillna(0)
)

df["created_day"] = (
    df["created_at"]
    .dt.day
    .fillna(0)
)

df["created_weekday"] = (
    df["created_at"]
    .dt.weekday
    .fillna(0)
)

df["merged"] = (
    ~df["merged_at"].isna()
).astype(int)


# ==========================================================
# FILL MISSING CATEGORICAL VALUES
# ==========================================================

print("\nHandling Categorical Missing Values...")

categorical_columns = [

    "language",

    "license"

]

for col in categorical_columns:

    if col in df.columns:

        df[col] = df[col].fillna(
            "Unknown"
        )


# ==========================================================
# FILL MISSING NUMERIC VALUES
# ==========================================================

print("\nHandling Numeric Missing Values...")

numeric_columns = [

    "stars",

    "forks",

    "review_count",

    "approved_reviews",

    "commented_reviews",

    "comment_count",

    "commit_count",

    "files_changed",

    "additions",

    "deletions",

    "total_changes",

    "total_lines_changed",

    "test_files",

    "high_risk_files",

    "review_time_hours"

]

for col in numeric_columns:

    if col in df.columns:

        df[col] = df[col].fillna(0)


# ==========================================================
# LABEL ENCODING
# ==========================================================

print("\nEncoding Categorical Features...")


# ----------------------------------------------------------
# Language Encoder
# ----------------------------------------------------------

language_encoder = LabelEncoder()

df["language"] = language_encoder.fit_transform(

    df["language"].astype(str)

)


# ----------------------------------------------------------
# License Encoder
# ----------------------------------------------------------

license_encoder = LabelEncoder()

df["license"] = license_encoder.fit_transform(

    df["license"].astype(str)

)


# ==========================================================
# PRINT LANGUAGE ENCODING
# ==========================================================

print("\nLANGUAGE ENCODING")

print("-" * 80)

for index, value in enumerate(

    language_encoder.classes_

):

    print(

        f"{value} -> {index}"

    )


# ==========================================================
# PRINT LICENSE ENCODING
# ==========================================================

print("\nLICENSE ENCODING")

print("-" * 80)

for index, value in enumerate(

    license_encoder.classes_

):

    print(

        f"{value} -> {index}"

    )


# ==========================================================
# SAVE ENCODERS
# ==========================================================

encoders = {

    "language": language_encoder,

    "license": license_encoder

}

joblib.dump(

    encoders,

    ENCODER_PATH

)

print("\n")

print("=" * 80)

print("LABEL ENCODERS SAVED")

print("=" * 80)

print(

    "File :",

    ENCODER_PATH

)


# ==========================================================
# REMOVE UNNECESSARY COLUMNS
# ==========================================================

print("\nRemoving Unnecessary Columns...")

remove_columns = [

    "pr_id",

    "pr_number",

    "title",

    "author",

    "state",

    "repo_id",

    "repository",

    "html_url",

    "created_at",

    "closed_at",

    "merged_at",

    "bug_score",

    "heuristic_score",

    "final_score",

    "risk_level"

]

for col in remove_columns:

    if col in df.columns:

        df.drop(

            columns=col,

            inplace=True

        )


# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

print("\nRemoving Duplicate Rows...")

before = len(df)

df = df.drop_duplicates()

after = len(df)

print(

    "Duplicates Removed :",

    before - after

)


# ==========================================================
# CHECK FEATURES
# ==========================================================

print("\nChecking Final Features...")

expected_features = [

    "language",

    "stars",

    "forks",

    "license",

    "review_count",

    "approved_reviews",

    "commented_reviews",

    "comment_count",

    "commit_count",

    "files_changed",

    "additions",

    "deletions",

    "total_changes",

    "total_lines_changed",

    "test_files",

    "high_risk_files",

    "review_time_hours",

    "created_year",

    "created_month",

    "created_day",

    "created_weekday",

    "merged"

]


print("\nFeature Count :")

print(

    len(expected_features)

)


print("\nFeature Order:")

for index, feature in enumerate(

    expected_features,

    start=1

):

    print(

        f"{index:02d}. {feature}"

    )


# ==========================================================
# VERIFY FEATURES EXIST
# ==========================================================

missing_features = [

    feature

    for feature in expected_features

    if feature not in df.columns

]

if missing_features:

    raise ValueError(

        "Missing expected features: "

        + str(missing_features)

    )


# ==========================================================
# FORCE EXACT FEATURE ORDER
# ==========================================================

df = df[

    expected_features

]


# ==========================================================
# SAVE ML DATASET
# ==========================================================

print("\nSaving ML Dataset...")

df.to_csv(

    ML_DATASET_PATH,

    index=False

)

print(

    "Saved :",

    ML_DATASET_PATH

)


# ==========================================================
# FINAL INFORMATION
# ==========================================================

print("\n")

print("=" * 80)

print("FINAL ML DATASET")

print("=" * 80)

print(

    "Shape :",

    df.shape

)

print(

    "Features :",

    len(df.columns)

)

print("\nColumns:")

for index, col in enumerate(

    df.columns,

    start=1

):

    print(

        f"{index:02d}. {col}"

    )


# ==========================================================
# COMPLETED
# ==========================================================

print("\n")

print("=" * 80)

print("PHASE 1 COMPLETED SUCCESSFULLY")

print("=" * 80)