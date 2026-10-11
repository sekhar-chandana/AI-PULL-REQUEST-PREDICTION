# ==========================================================
# AI Pull Request Risk Predictor
# Phase 3 : Model Training
# Part 1
# ==========================================================

import os
import warnings
warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold
)

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve
)

# ==========================================================
# MODELS
# ==========================================================

from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import RandomForestClassifier

# XGBoost

try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except:
    XGB_AVAILABLE = False

# LightGBM

try:
    from lightgbm import LGBMClassifier
    LGBM_AVAILABLE = True
except:
    LGBM_AVAILABLE = False

# ==========================================================
# CREATE OUTPUT FOLDER
# ==========================================================
# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "Models")

os.makedirs(MODEL_DIR, exist_ok=True)

print("BASE_DIR :", BASE_DIR)
print("MODEL_DIR :", MODEL_DIR)


OUTPUT_DIR = MODEL_DIR

print("="*80)
print("PHASE 3 : MODEL TRAINING")
print("="*80)

# ==========================================================
# LOAD DATASET
# ==========================================================

print("\nLoading Dataset...")

df = pd.read_csv("ml_dataset.csv")

print("Dataset Loaded Successfully")

print("Shape :", df.shape)

# ==========================================================
# FEATURES & TARGET
# ==========================================================

TARGET = "bug_label"

X = df.drop(columns=[TARGET])

y = df[TARGET]

print("\nFeatures :", X.shape)

print("Target :", y.shape)

# ==========================================================
# TRAIN TEST SPLIT
# ==========================================================

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# ==========================================================
# SAVE FEATURE NAMES & BACKGROUND DATA FOR SHAP
# ==========================================================

print("Training :", len(X_train))

print("Testing  :", len(X_test))

# ==========================================================
# FEATURE SCALING
# ==========================================================

print("\nScaling Features...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

joblib.dump(

    scaler,

    os.path.join(OUTPUT_DIR, "scaler.pkl")

)

print("Scaler Saved")

# ==========================================================
# METRICS STORAGE
# ==========================================================

results = []

trained_models = {}

# ==========================================================
# EVALUATION FUNCTION
# ==========================================================

def evaluate_model(

    model,

    model_name,

    X_train,

    X_test,

    y_train,

    y_test

):

    print("\n" + "="*70)

    print(model_name)

    print("="*70)

    model.fit(

        X_train,

        y_train

    )

    predictions = model.predict(

        X_test

    )

    probabilities = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(

            X_test

        )[:,1]

    accuracy = accuracy_score(

        y_test,

        predictions

    )

    precision = precision_score(

        y_test,

        predictions,

        zero_division=0

    )

    recall = recall_score(

        y_test,

        predictions,

        zero_division=0

    )

    f1 = f1_score(

        y_test,

        predictions,

        zero_division=0

    )

    if probabilities is not None:

        auc = roc_auc_score(

            y_test,

            probabilities

        )

    else:

        auc = 0

    print("Accuracy :", round(accuracy,4))

    print("Precision :", round(precision,4))

    print("Recall :", round(recall,4))

    print("F1 Score :", round(f1,4))

    print("ROC AUC :", round(auc,4))

    print("\nClassification Report\n")

    print(

        classification_report(

            y_test,

            predictions

        )

    )

    cm = confusion_matrix(

        y_test,

        predictions

    )

    results.append({

        "Model":model_name,

        "Accuracy":accuracy,

        "Precision":precision,

        "Recall":recall,

        "F1":f1,

        "ROC_AUC":auc

    })

    trained_models[model_name] = model

    return model,predictions,probabilities,cm

# ==========================================================
# CROSS VALIDATION FUNCTION
# ==========================================================

def perform_cross_validation(

    model,

    X,

    y

):

    cv = StratifiedKFold(

        n_splits=5,

        shuffle=True,

        random_state=42

    )

    scores = cross_val_score(

        model,

        X,

        y,

        cv=cv,

        scoring="accuracy"

    )

    print("\nCross Validation Accuracy")

    print(scores)

    print("Average :", round(scores.mean(),4))

    return scores.mean()

print("\nInitialization Completed")

print("="*80)

# ==========================================================
# LOGISTIC REGRESSION
# ==========================================================

print("\n")
print("="*80)
print("TRAINING LOGISTIC REGRESSION")
print("="*80)

logistic = LogisticRegression(
    random_state=42,
    max_iter=1000
)

model,predictions,probabilities,cm = evaluate_model(

    logistic,

    "Logistic Regression",

    X_train_scaled,

    X_test_scaled,

    y_train,

    y_test

)

perform_cross_validation(

    logistic,

    X_train_scaled,

    y_train

)

joblib.dump(

    logistic,

    os.path.join(

        OUTPUT_DIR,

        "logistic_regression.pkl"

    )

)

# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

plt.figure(figsize=(5,5))

plt.imshow(cm,cmap="Blues")

plt.title("Logistic Regression")

plt.colorbar()

plt.xticks([0,1],["Safe","Buggy"])

plt.yticks([0,1],["Safe","Buggy"])

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j,i,str(cm[i,j]),
                 ha="center",
                 va="center",
                 fontsize=12)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "logistic_confusion_matrix.png"

    )

)

plt.close()

# ==========================================================
# DECISION TREE
# ==========================================================

print("\n")
print("="*80)
print("TRAINING DECISION TREE")
print("="*80)

decision_tree = DecisionTreeClassifier(

    random_state=42,

    max_depth=10,

    min_samples_split=10

)

model,predictions,probabilities,cm = evaluate_model(

    decision_tree,

    "Decision Tree",

    X_train,

    X_test,

    y_train,

    y_test

)

perform_cross_validation(

    decision_tree,

    X_train,

    y_train

)

joblib.dump(

    decision_tree,

    os.path.join(

        OUTPUT_DIR,

        "decision_tree.pkl"

    )

)

# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

plt.figure(figsize=(5,5))

plt.imshow(cm,cmap="Greens")

plt.title("Decision Tree")

plt.colorbar()

plt.xticks([0,1],["Safe","Buggy"])

plt.yticks([0,1],["Safe","Buggy"])

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j,i,str(cm[i,j]),
                 ha="center",
                 va="center",
                 fontsize=12)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "decision_tree_confusion_matrix.png"

    )

)

plt.close()

# ==========================================================
# RANDOM FOREST
# ==========================================================

print("\n")
print("="*80)
print("TRAINING RANDOM FOREST")
print("="*80)

random_forest = RandomForestClassifier(

    n_estimators=300,

    random_state=42,

    max_depth=20,

    min_samples_split=5,

    n_jobs=-1

)

model,predictions,probabilities,cm = evaluate_model(

    random_forest,

    "Random Forest",

    X_train,

    X_test,

    y_train,

    y_test

)

perform_cross_validation(

    random_forest,

    X_train,

    y_train

)

joblib.dump(

    random_forest,

    os.path.join(

        OUTPUT_DIR,

        "random_forest.pkl"

    )

)

# ----------------------------------------------------------
# Confusion Matrix
# ----------------------------------------------------------

plt.figure(figsize=(5,5))

plt.imshow(cm,cmap="Oranges")

plt.title("Random Forest")

plt.colorbar()

plt.xticks([0,1],["Safe","Buggy"])

plt.yticks([0,1],["Safe","Buggy"])

for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j,i,str(cm[i,j]),
                 ha="center",
                 va="center",
                 fontsize=12)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "random_forest_confusion_matrix.png"

    )

)

plt.close()

# ==========================================================
# RANDOM FOREST FEATURE IMPORTANCE
# ==========================================================

print("\nGenerating Feature Importance...")

importance = pd.DataFrame({

    "Feature":X.columns,

    "Importance":random_forest.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

importance.to_csv(

    os.path.join(

        OUTPUT_DIR,

        "random_forest_feature_importance.csv"

    ),

    index=False

)

plt.figure(figsize=(10,8))

plt.barh(

    importance["Feature"][:15],

    importance["Importance"][:15]

)

plt.title("Random Forest Feature Importance")

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "random_forest_feature_importance.png"

    )

)

plt.close()

print("\nTop 15 Features")

print(

    importance.head(15)

)

print("\n")

print("="*80)

print("PART 2 COMPLETED")

print("="*80)

# ==========================================================
# XGBOOST
# ==========================================================

if XGB_AVAILABLE:

    print("\n")
    print("=" * 80)
    print("TRAINING XGBOOST")
    print("=" * 80)

    xgb_model = XGBClassifier(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=8,

        subsample=0.8,

        colsample_bytree=0.8,

        random_state=42,

        eval_metric="logloss"

    )

    model, predictions, probabilities, cm = evaluate_model(

        xgb_model,

        "XGBoost",

        X_train,

        X_test,

        y_train,

        y_test

    )

    perform_cross_validation(

        xgb_model,

        X_train,

        y_train

    )

    joblib.dump(

        xgb_model,

        os.path.join(

            OUTPUT_DIR,

            "xgboost.pkl"

        )

    )

    # --------------------------------------------
    # Confusion Matrix
    # --------------------------------------------

    plt.figure(figsize=(6,5))

    plt.imshow(cm,cmap="Purples")

    plt.title("XGBoost")

    plt.colorbar()

    plt.xticks([0,1],["Safe","Buggy"])

    plt.yticks([0,1],["Safe","Buggy"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j,i,str(cm[i,j]),
                     ha="center",
                     va="center",
                     fontsize=12)

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_DIR,

            "xgboost_confusion_matrix.png"

        )

    )

    plt.close()

    # --------------------------------------------
    # Feature Importance
    # --------------------------------------------

    importance = pd.DataFrame({

        "Feature":X.columns,

        "Importance":xgb_model.feature_importances_

    })

    importance = importance.sort_values(

        by="Importance",

        ascending=False

    )

    importance.to_csv(

        os.path.join(

            OUTPUT_DIR,

            "xgboost_feature_importance.csv"

        ),

        index=False

    )

    plt.figure(figsize=(10,8))

    plt.barh(

        importance["Feature"][:15],

        importance["Importance"][:15]

    )

    plt.title("XGBoost Feature Importance")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_DIR,

            "xgboost_feature_importance.png"

        )

    )

    plt.close()

else:

    print("\nXGBoost Not Installed")

# ==========================================================
# LIGHTGBM
# ==========================================================

if LGBM_AVAILABLE:

    print("\n")
    print("=" * 80)
    print("TRAINING LIGHTGBM")
    print("=" * 80)

    lgb_model = LGBMClassifier(

        n_estimators=300,

        learning_rate=0.05,

        max_depth=8,

        random_state=42

    )

    model,predictions,probabilities,cm = evaluate_model(

        lgb_model,

        "LightGBM",

        X_train,

        X_test,

        y_train,

        y_test

    )

    perform_cross_validation(

        lgb_model,

        X_train,

        y_train

    )

    joblib.dump(

        lgb_model,

        os.path.join(

            OUTPUT_DIR,

            "lightgbm.pkl"

        )

    )

    # --------------------------------------------
    # Confusion Matrix
    # --------------------------------------------

    plt.figure(figsize=(6,5))

    plt.imshow(cm,cmap="Reds")

    plt.title("LightGBM")

    plt.colorbar()

    plt.xticks([0,1],["Safe","Buggy"])

    plt.yticks([0,1],["Safe","Buggy"])

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j,i,str(cm[i,j]),
                     ha="center",
                     va="center",
                     fontsize=12)

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_DIR,

            "lightgbm_confusion_matrix.png"

        )

    )

    plt.close()

    # --------------------------------------------
    # Feature Importance
    # --------------------------------------------

    importance = pd.DataFrame({

        "Feature":X.columns,

        "Importance":lgb_model.feature_importances_

    })

    importance = importance.sort_values(

        by="Importance",

        ascending=False

    )

    importance.to_csv(

        os.path.join(

            OUTPUT_DIR,

            "lightgbm_feature_importance.csv"

        ),

        index=False

    )

    plt.figure(figsize=(10,8))

    plt.barh(

        importance["Feature"][:15],

        importance["Importance"][:15]

    )

    plt.title("LightGBM Feature Importance")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_DIR,

            "lightgbm_feature_importance.png"

        )

    )

    plt.close()

else:

    print("\nLightGBM Not Installed")

print("\n")
print("="*80)
print("PART 3 COMPLETED")
print("="*80)

# ==========================================================
# MODEL COMPARISON
# ==========================================================

print("\n")
print("="*80)
print("MODEL COMPARISON")
print("="*80)

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="Accuracy",
    ascending=False
)

print(results_df)

results_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "model_metrics.csv"
    ),
    index=False
)

# ==========================================================
# BEST MODEL
# ==========================================================

best_model_name = results_df.iloc[0]["Model"]

print("\nBest Model :", best_model_name)

best_model = trained_models[best_model_name]

joblib.dump(
    best_model,
    os.path.join(
        OUTPUT_DIR,
        "best_model.pkl"
    )
)

print("Best Model Saved")

# ==========================================================
# BAR CHART COMPARISON
# ==========================================================

metrics = ["Accuracy","Precision","Recall","F1","ROC_AUC"]

for metric in metrics:

    plt.figure(figsize=(8,5))

    plt.bar(
        results_df["Model"],
        results_df[metric]
    )

    plt.xticks(rotation=20)

    plt.ylabel(metric)

    plt.title(metric + " Comparison")

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_DIR,

            metric.lower()+"_comparison.png"

        )

    )

    plt.close()

# ==========================================================
# ROC CURVES
# ==========================================================

print("\nGenerating ROC Curves...")

plt.figure(figsize=(8,6))

models = {

    "Logistic Regression": logistic,

    "Decision Tree": decision_tree,

    "Random Forest": random_forest

}

if XGB_AVAILABLE:
    models["XGBoost"] = xgb_model

if LGBM_AVAILABLE:
    models["LightGBM"] = lgb_model

for name, model in models.items():

    if name == "Logistic Regression":

        probs = model.predict_proba(X_test_scaled)[:,1]

    else:

        probs = model.predict_proba(X_test)[:,1]

    fpr, tpr, _ = roc_curve(
        y_test,
        probs
    )

    plt.plot(
        fpr,
        tpr,
        label=name
    )

plt.plot([0,1],[0,1],"k--")

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "roc_curve.png"

    )

)

plt.close()

# ==========================================================
# PRECISION RECALL CURVES
# ==========================================================

print("Generating Precision Recall Curves...")

plt.figure(figsize=(8,6))

for name, model in models.items():

    if name == "Logistic Regression":

        probs = model.predict_proba(X_test_scaled)[:,1]

    else:

        probs = model.predict_proba(X_test)[:,1]

    precision, recall, _ = precision_recall_curve(
        y_test,
        probs
    )

    plt.plot(
        recall,
        precision,
        label=name
    )

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title("Precision Recall Curve")

plt.legend()

plt.tight_layout()

plt.savefig(

    os.path.join(

        OUTPUT_DIR,

        "precision_recall_curve.png"

    )

)

plt.close()

# ==========================================================
# SAVE CLASSIFICATION REPORTS
# ==========================================================

print("Saving Classification Reports...")

report_file = open(

    os.path.join(

        OUTPUT_DIR,

        "classification_reports.txt"

    ),

    "w",

    encoding="utf-8"

)

for name, model in models.items():

    if name == "Logistic Regression":

        preds = model.predict(X_test_scaled)

    else:

        preds = model.predict(X_test)

    report_file.write("="*80+"\n")

    report_file.write(name+"\n")

    report_file.write("="*80+"\n\n")

    report_file.write(

        classification_report(

            y_test,

            preds

        )

    )

    report_file.write("\n\n")

report_file.close()

# ==========================================================
# FINAL SUMMARY
# ==========================================================

print("\n")
print("="*80)
print("TRAINING COMPLETED")
print("="*80)

print("\nModels Trained")

for m in results_df["Model"]:
    print("✔",m)

print("\nBest Model")

print(best_model_name)

print("\nAccuracy")

print(round(results_df.iloc[0]["Accuracy"]*100,2),"%")

print("\nSaved Files")

print("-----------------------------------")

print("best_model.pkl")

print("scaler.pkl")

print("model_metrics.csv")

print("classification_reports.txt")

print("roc_curve.png")

print("precision_recall_curve.png")

print("accuracy_comparison.png")

print("precision_comparison.png")

print("recall_comparison.png")

print("f1_comparison.png")

print("roc_auc_comparison.png")

print("\nEverything Saved Inside")

print("Models/")

print("\n")

print("="*80)
print("PHASE 3 COMPLETED SUCCESSFULLY")
print("="*80)