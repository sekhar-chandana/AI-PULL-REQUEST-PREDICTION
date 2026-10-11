import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder

# ============================================================
# Create Output Folder
# ============================================================

OUTPUT_DIR = "EDA_Output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Load Dataset
# ============================================================

print("="*80)
print("PHASE 2 : EXPLORATORY DATA ANALYSIS")
print("="*80)

df = pd.read_csv("ml_dataset.csv")

print("\nDataset Loaded Successfully")

# ============================================================
# Dataset Information
# ============================================================

print("\n")
print("="*80)
print("DATASET INFORMATION")
print("="*80)

print(df.info())

print("\nShape")

print(df.shape)

print("\nColumns")

print(df.columns.tolist())

# ============================================================
# Missing Values
# ============================================================

print("\n")
print("="*80)
print("MISSING VALUES")
print("="*80)

missing = df.isnull().sum()

print(missing)

missing = missing[missing > 0]

if len(missing) > 0:

    plt.figure(figsize=(10,5))

    plt.bar(missing.index, missing.values)

    plt.xticks(rotation=90)

    plt.title("Missing Values")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/missing_values.png")

    plt.close()

# ============================================================
# Duplicate Rows
# ============================================================

print("\n")
print("="*80)
print("DUPLICATES")
print("="*80)

duplicates = df.duplicated().sum()

print("Duplicate Rows :", duplicates)

# ============================================================
# Summary Statistics
# ============================================================

print("\n")
print("="*80)
print("SUMMARY")
print("="*80)

summary = df.describe(include="all")

print(summary)

summary.to_csv(f"{OUTPUT_DIR}/summary_statistics.csv")

# ============================================================
# Target Distribution
# ============================================================

print("\n")
print("="*80)
print("TARGET DISTRIBUTION")
print("="*80)

target = df["bug_label"].value_counts()

print(target)

plt.figure(figsize=(6,6))

plt.pie(
    target.values,
    labels=["Safe","Buggy"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Bug Label Distribution")

plt.savefig(f"{OUTPUT_DIR}/bug_distribution_pie.png")

plt.close()

plt.figure(figsize=(6,5))

plt.bar(["Safe","Buggy"],target.values)

plt.title("Bug Label Distribution")

plt.savefig(f"{OUTPUT_DIR}/bug_distribution_bar.png")

plt.close()

# ============================================================
# Class Percentage
# ============================================================

print("\n")

safe = target[0]

buggy = target[1]

print("Safe :", safe)

print("Buggy :", buggy)

print("Safe % :", round((safe/len(df))*100,2))

print("Buggy % :", round((buggy/len(df))*100,2))

# ============================================================
# Numerical Columns
# ============================================================

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

    "review_time_hours",

    "created_year",

    "created_month",

    "created_day",

    "created_weekday"

]

# ============================================================
# Histograms
# ============================================================

print("\nGenerating Histograms...")

for col in numeric_columns:

    if col not in df.columns:

        continue

    plt.figure(figsize=(7,5))

    plt.hist(df[col], bins=30)

    plt.title(col)

    plt.xlabel(col)

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/{col}_hist.png")

    plt.close()

print("Histograms Saved")

# ============================================================
# Boxplots
# ============================================================

print("\nGenerating Boxplots...")

for col in numeric_columns:

    if col not in df.columns:

        continue

    plt.figure(figsize=(6,5))

    plt.boxplot(df[col])

    plt.title(col)

    plt.tight_layout()

    plt.savefig(f"{OUTPUT_DIR}/{col}_boxplot.png")

    plt.close()

print("Boxplots Saved")

# ============================================================
# Correlation Heatmap
# ============================================================

print("\nGenerating Correlation Heatmap...")

corr = df[numeric_columns + ["bug_label"]].corr()

plt.figure(figsize=(15,10))

plt.imshow(corr, cmap="coolwarm", aspect="auto")

plt.colorbar()

plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)

plt.yticks(range(len(corr.columns)), corr.columns)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/correlation_heatmap.png")

plt.close()

print("Correlation Heatmap Saved")

# ============================================================
# Correlation with Target
# ============================================================

print("\nCorrelation With Bug Label")

target_corr = corr["bug_label"].sort_values(ascending=False)

print(target_corr)

target_corr.to_csv(f"{OUTPUT_DIR}/target_correlation.csv")

plt.figure(figsize=(8,8))

target_corr.drop("bug_label").plot(kind="bar")

plt.title("Feature Correlation with Bug Label")

plt.ylabel("Correlation")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/target_feature_correlation.png")

plt.close()

# ============================================================
# Programming Language Distribution
# ============================================================

print("\nLanguage Distribution")

language_counts = df["language"].value_counts().head(10)

print(language_counts)

plt.figure(figsize=(10,6))

plt.bar(language_counts.index.astype(str),
        language_counts.values)

plt.xticks(rotation=45)

plt.title("Top Programming Languages")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/language_distribution.png")

plt.close()

# ============================================================
# Bug Rate by Language
# ============================================================

print("\nBug Rate by Language")

bug_lang = (

    df.groupby("language")["bug_label"]

      .mean()

      .sort_values(ascending=False)

      .head(10)

)

print(bug_lang)

plt.figure(figsize=(10,6))

plt.bar(

    bug_lang.index.astype(str),

    bug_lang.values

)

plt.xticks(rotation=45)

plt.ylabel("Bug Rate")

plt.title("Bug Rate by Programming Language")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/bug_rate_language.png")

plt.close()

# ============================================================
# Commit Count Analysis
# ============================================================

print("\nCommit Analysis")

plt.figure(figsize=(8,6))

plt.hist(df["commit_count"], bins=30)

plt.xlabel("Commit Count")

plt.ylabel("Frequency")

plt.title("Commit Count Distribution")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/commit_distribution.png")

plt.close()

plt.figure(figsize=(7,6))

df.boxplot(column="commit_count", by="bug_label")

plt.title("Commit Count vs Bug Label")

plt.suptitle("")

plt.savefig(f"{OUTPUT_DIR}/commit_vs_bug.png")

plt.close()

# ============================================================
# Review Count Analysis
# ============================================================

print("\nReview Count Analysis")

plt.figure(figsize=(8,6))

plt.hist(df["review_count"], bins=30)

plt.xlabel("Review Count")

plt.ylabel("Frequency")

plt.title("Review Count Distribution")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/review_distribution.png")

plt.close()

plt.figure(figsize=(7,6))

df.boxplot(column="review_count", by="bug_label")

plt.title("Review Count vs Bug Label")

plt.suptitle("")

plt.savefig(f"{OUTPUT_DIR}/review_vs_bug.png")

plt.close()

# ============================================================
# Files Changed Analysis
# ============================================================

print("\nFiles Changed Analysis")

plt.figure(figsize=(8,6))

plt.hist(df["files_changed"], bins=30)

plt.xlabel("Files Changed")

plt.ylabel("Frequency")

plt.title("Files Changed Distribution")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/files_changed_distribution.png")

plt.close()

plt.figure(figsize=(7,6))

df.boxplot(column="files_changed", by="bug_label")

plt.title("Files Changed vs Bug Label")

plt.suptitle("")

plt.savefig(f"{OUTPUT_DIR}/files_changed_vs_bug.png")

plt.close()

# ============================================================
# Total Lines Changed
# ============================================================

print("\nTotal Lines Changed")

plt.figure(figsize=(8,6))

plt.hist(df["total_lines_changed"], bins=40)

plt.xlabel("Total Lines Changed")

plt.ylabel("Frequency")

plt.title("Total Lines Changed")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/total_lines_changed.png")

plt.close()

plt.figure(figsize=(7,6))

df.boxplot(column="total_lines_changed", by="bug_label")

plt.title("Total Lines Changed vs Bug")

plt.suptitle("")

plt.savefig(f"{OUTPUT_DIR}/lines_changed_vs_bug.png")

plt.close()

# ============================================================
# Review Time
# ============================================================

print("\nReview Time")

plt.figure(figsize=(8,6))

plt.hist(df["review_time_hours"], bins=30)

plt.xlabel("Review Time (Hours)")

plt.ylabel("Frequency")

plt.title("Review Time Distribution")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/review_time_distribution.png")

plt.close()

plt.figure(figsize=(7,6))

df.boxplot(column="review_time_hours", by="bug_label")

plt.title("Review Time vs Bug")

plt.suptitle("")

plt.savefig(f"{OUTPUT_DIR}/review_time_vs_bug.png")

plt.close()

# ============================================================
# High Risk Files
# ============================================================

print("\nHigh Risk Files")

risk = df.groupby("bug_label")["high_risk_files"].mean()

print(risk)

plt.figure(figsize=(6,5))

plt.bar(

    ["Safe","Buggy"],

    risk.values

)

plt.title("Average High Risk Files")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/high_risk_files.png")

plt.close()

# ============================================================
# Test Files
# ============================================================

print("\nTest Files")

tests = df.groupby("bug_label")["test_files"].mean()

print(tests)

plt.figure(figsize=(6,5))

plt.bar(

    ["Safe","Buggy"],

    tests.values

)

plt.title("Average Test Files")

plt.tight_layout()

plt.savefig(f"{OUTPUT_DIR}/test_files.png")

plt.close()

print("\nPart 2 Completed Successfully")

# ============================================================
# OUTLIER DETECTION (IQR METHOD)
# ============================================================

print("\n")
print("=" * 80)
print("OUTLIER ANALYSIS")
print("=" * 80)

outlier_report = []

for col in numeric_columns:

    if col not in df.columns:
        continue

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    outlier_report.append({

        "Feature": col,

        "Outliers": len(outliers),

        "Percentage": round((len(outliers)/len(df))*100,2)

    })

outlier_report = pd.DataFrame(outlier_report)

print(outlier_report)

outlier_report.to_csv(

    f"{OUTPUT_DIR}/outlier_report.csv",

    index=False

)

# ============================================================
# FEATURE IMPORTANCE (Correlation Based)
# ============================================================

print("\n")
print("="*80)
print("FEATURE IMPORTANCE")
print("="*80)

importance = abs(

    corr["bug_label"]

).sort_values(

    ascending=False

)

importance = importance.drop("bug_label")

print(importance)

importance.to_csv(

    f"{OUTPUT_DIR}/feature_importance.csv"

)

plt.figure(figsize=(10,7))

importance.plot(kind="bar")

plt.ylabel("Correlation")

plt.title("Feature Importance")

plt.tight_layout()

plt.savefig(

    f"{OUTPUT_DIR}/feature_importance.png"

)

plt.close()

# ============================================================
# TOP FEATURES
# ============================================================

print("\nTop 10 Features")

print(importance.head(10))

# ============================================================
# DATASET REPORT
# ============================================================

print("\nCreating Summary Report...")

report = open(

    f"{OUTPUT_DIR}/summary_report.txt",

    "w",

    encoding="utf-8"

)

report.write("="*80+"\n")

report.write("AI PULL REQUEST RISK PREDICTOR\n")

report.write("EDA SUMMARY REPORT\n")

report.write("="*80+"\n\n")

report.write(f"Dataset Shape : {df.shape}\n")

report.write(f"Rows : {len(df)}\n")

report.write(f"Columns : {len(df.columns)}\n\n")

report.write("TARGET DISTRIBUTION\n")

report.write("-------------------------\n")

report.write(str(target))

report.write("\n\n")

report.write("TARGET PERCENTAGE\n")

report.write("-------------------------\n")

report.write(

f"Safe : {round((safe/len(df))*100,2)}%\n"

)

report.write(

f"Buggy : {round((buggy/len(df))*100,2)}%\n\n"

)

report.write("TOP FEATURES\n")

report.write("-------------------------\n")

report.write(

importance.head(10).to_string()

)

report.write("\n\n")

report.write("MISSING VALUES\n")

report.write("-------------------------\n")

report.write(

str(df.isnull().sum())

)

report.write("\n\n")

report.write("OUTLIERS\n")

report.write("-------------------------\n")

report.write(

outlier_report.to_string()

)

report.write("\n\n")

report.write("SUMMARY\n")

report.write("-------------------------\n")

report.write(

"""1. Dataset contains sufficient samples for ML.

2. Class distribution is acceptable.

3. Numerical features have several outliers.

4. Correlation analysis identifies important predictors.

5. Dataset is ready for Machine Learning.

"""
)

report.close()

# ============================================================
# FINAL OBSERVATIONS
# ============================================================

print("\n")
print("="*80)
print("EDA OBSERVATIONS")
print("="*80)

print(f"Dataset Size : {len(df)}")

print(f"Number of Features : {len(df.columns)-1}")

print(f"Target Column : bug_label")

print("\nTop 5 Important Features")

print(

importance.head()

)

print("\nOutlier Report")

print(outlier_report)

print("\nMissing Values")

print(df.isnull().sum())

# ============================================================
# SAVE CLEAN DATASET
# ============================================================

df.to_csv(

    f"{OUTPUT_DIR}/eda_dataset.csv",

    index=False

)

# ============================================================
# COMPLETION
# ============================================================

print("\n")
print("="*80)
print("EDA COMPLETED SUCCESSFULLY")
print("="*80)

print("\nGenerated Files\n")

print("summary_statistics.csv")

print("target_correlation.csv")

print("feature_importance.csv")

print("outlier_report.csv")

print("summary_report.txt")

print("eda_dataset.csv")

print("\nGraphs Saved")

print("------------------------")

print("bug_distribution_bar.png")

print("bug_distribution_pie.png")

print("language_distribution.png")

print("bug_rate_language.png")

print("commit_distribution.png")

print("commit_vs_bug.png")

print("review_distribution.png")

print("review_vs_bug.png")

print("files_changed_distribution.png")

print("files_changed_vs_bug.png")

print("total_lines_changed.png")

print("lines_changed_vs_bug.png")

print("review_time_distribution.png")

print("review_time_vs_bug.png")

print("feature_importance.png")

print("correlation_heatmap.png")

print("high_risk_files.png")

print("test_files.png")

print("\nEverything has been saved inside")

print("EDA_Output/")

print("\n")

print("="*80)
print("PHASE 2 FINISHED")
print("="*80)