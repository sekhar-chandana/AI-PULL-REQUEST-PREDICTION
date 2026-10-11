"""
==========================================================

FastAPI Services

AI Pull Request Risk Predictor

==========================================================
"""

import os
import sys

import pandas as pd


# ----------------------------------------------------------
# Add Project Root
# ----------------------------------------------------------

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    CURRENT_DIR
)

if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )


# ----------------------------------------------------------
# Imports
# ----------------------------------------------------------

from explain.explanation_engine import ExplanationEngine

from database.fetch_data import DatabaseFetch

from backend.schemas import PredictionRequest


# ==========================================================
# Prediction Service
# ==========================================================

class PredictionService:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        print("=" * 70)
        print("INITIALIZING PREDICTION SERVICE")
        print("=" * 70)

        self.engine = ExplanationEngine()

        print("Prediction Service Ready")

    # ======================================================
    # Convert Request to DataFrame
    # ======================================================

    def convert_request(

        self,

        request

    ):

        data = {

            "language": request.language,

            "stars": request.stars,

            "forks": request.forks,

            "license": request.license,

            "review_count": request.review_count,

            "approved_reviews": request.approved_reviews,

            "commented_reviews": request.commented_reviews,

            "comment_count": request.comment_count,

            "commit_count": request.commit_count,

            "files_changed": request.files_changed,

            "additions": request.additions,

            "deletions": request.deletions,

            "total_changes": request.total_changes,

            "total_lines_changed": request.total_lines_changed,

            "test_files": request.test_files,

            "high_risk_files": request.high_risk_files,

            "review_time_hours": request.review_time_hours,

            "created_year": request.created_year,

            "created_month": request.created_month,

            "created_day": request.created_day,

            "created_weekday": request.created_weekday,

            "merged": request.merged

        }

        feature_vector = pd.DataFrame(

            [data]

        )

        return feature_vector

    # ======================================================
    # Generate Prediction
    # ======================================================

    def predict(

        self,

        request

    ):

        print("\nGenerating Prediction...")

        feature_vector = self.convert_request(

            request

        )

        print("\nFeature Vector:")

        print(feature_vector)

        result = self.engine.run(

            feature_vector

        )

        print("\nPrediction Generated Successfully")

        return result

    # ======================================================
    # Get Latest Prediction
    # ======================================================
    # ==========================================================
# Predict From GitHub Features
# ==========================================================

    def predict_from_features(

    self,

    features

    ):

        print("\n")
        print("=" * 70)
        print("PREDICTING FROM GITHUB FEATURES")
        print("=" * 70)

    # ------------------------------------------------------
    # Convert GitHub feature dictionary to DataFrame
    # ------------------------------------------------------

        feature_vector = pd.DataFrame(

        [features]

        )

    # ------------------------------------------------------
    # Get exact feature order from trained model
    # ------------------------------------------------------

        feature_names = (

        self.engine
        .shap_engine
        .feature_names

        )

    # ------------------------------------------------------
    # Verify missing features
    # ------------------------------------------------------

        missing_features = [

        feature

        for feature in feature_names

        if feature not in feature_vector.columns

        ]

        if missing_features:

            raise ValueError(

            "Missing model features: "

            + str(missing_features)

            )

    # ------------------------------------------------------
    # Force exact model feature order
    # ------------------------------------------------------

        feature_vector = feature_vector[

        feature_names

        ]

        print("\nFeature Vector")

        print("-" * 70)

        for feature in feature_names:

            print(

            f"{feature:<25}: "

            f"{feature_vector.iloc[0][feature]}"

            )

    # ------------------------------------------------------
    # Run existing prediction pipeline
    # ------------------------------------------------------

        result = self.engine.run(

        feature_vector

        )

        return result


    def get_latest_prediction(

        self

    ):
        database = DatabaseFetch()

        try:

            prediction = database.fetch_latest_prediction()

            if prediction is None:

                return {

                    "message": "No prediction found."

                }

            return prediction

        finally:

            database.close()

    # ======================================================
    # Get Prediction History
    # ======================================================

    def get_prediction_history(

        self

    ):

        database = DatabaseFetch()

        try:

            history = database.fetch_prediction_history()

            return history

        finally:

            database.close()

    # ======================================================
    # Health Check
    # ======================================================

    def health(

        self

    ):

        return {

            "status": "Healthy",

            "api": "Running",

            "database": "Connected",

            "model": type(

                self.engine.shap_engine.model

            ).__name__

        }


# ==========================================================
# Test Prediction Service
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING PREDICTION SERVICE")
    print("=" * 70)

    try:

        # --------------------------------------------------
        # Create Service
        # --------------------------------------------------

        service = PredictionService()

        # --------------------------------------------------
        # Load Sample Pull Request
        # --------------------------------------------------

        print(
            "\nLoading Sample Pull Request...\n"
        )

        sample = (

            service

            .engine

            .shap_engine

            .background

            .iloc[0]

        )

        # --------------------------------------------------
        # Convert Sample into PredictionRequest
        # --------------------------------------------------

        request_data = {

            "language": int(
                sample["language"]
            ),

            "stars": int(
                sample["stars"]
            ),

            "forks": int(
                sample["forks"]
            ),

            "license": int(
                sample["license"]
            ),

            "review_count": int(
                sample["review_count"]
            ),

            "approved_reviews": int(
                sample["approved_reviews"]
            ),

            "commented_reviews": int(
                sample["commented_reviews"]
            ),

            "comment_count": int(
                sample["comment_count"]
            ),

            "commit_count": int(
                sample["commit_count"]
            ),

            "files_changed": int(
                sample["files_changed"]
            ),

            "additions": int(
                sample["additions"]
            ),

            "deletions": int(
                sample["deletions"]
            ),

            "total_changes": int(
                sample["total_changes"]
            ),

            "total_lines_changed": int(
                sample["total_lines_changed"]
            ),

            "test_files": int(
                sample["test_files"]
            ),

            "high_risk_files": int(
                sample["high_risk_files"]
            ),

            "review_time_hours": float(
                sample["review_time_hours"]
            ),

            "created_year": int(
                sample["created_year"]
            ),

            "created_month": int(
                sample["created_month"]
            ),

            "created_day": int(
                sample["created_day"]
            ),

            "created_weekday": int(
                sample["created_weekday"]
            ),

            "merged": int(
                sample["merged"]
            )

        }

        request = PredictionRequest(

            **request_data

        )

        # --------------------------------------------------
        # Generate Prediction
        # --------------------------------------------------

        result = service.predict(

            request

        )

        # --------------------------------------------------
        # Display Prediction
        # --------------------------------------------------

        print("\n")
        print("=" * 70)
        print("PREDICTION GENERATED")
        print("=" * 70)

        print(

            "Prediction :",

            result["prediction"]["label"]

        )

        print(

            "Risk Score :",

            result["prediction"]["risk_score"]

        )

        print(

            "Confidence :",

            result["prediction"]["confidence"]

        )

        print(

            "Risk Level :",

            result["prediction"]["risk_level"]

        )

        # --------------------------------------------------
        # Latest Database Record
        # --------------------------------------------------

        print(

            "\nLatest Database Record"

        )

        latest = (

            service

            .get_latest_prediction()

        )

        print(latest)

        # --------------------------------------------------
        # Prediction History
        # --------------------------------------------------

        print(

            "\nPrediction History"

        )

        history = (

            service

            .get_prediction_history()

        )

        print(

            "Total Records :",

            len(history)

        )

        # --------------------------------------------------
        # Health Status
        # --------------------------------------------------

        print(

            "\nHealth Status"

        )

        print(

            service.health()

        )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        print("\n")

        print("=" * 70)
        print("SERVICE TEST COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\n")

        print("=" * 70)
        print("SERVICE TEST FAILED")
        print("=" * 70)

        print(

            type(e).__name__,

            ":",

            str(e)

        )

        print("=" * 70)
    def predict_from_features(

    self,

    features

    ):

        print("\n")
        print("=" * 70)
        print("PREDICTING FROM GITHUB FEATURES")
        print("=" * 70)

    # --------------------------------------------------
    # Convert dictionary to DataFrame
    # --------------------------------------------------

        feature_vector = pd.DataFrame(

        [features]

        )

    # --------------------------------------------------
    # Ensure exact model feature order
    # --------------------------------------------------

        feature_names = (

        self.engine
        .shap_engine
        .feature_names

        )

        feature_vector = feature_vector[

        feature_names

        ]

        print("\nFeature Vector")

        print("-" * 70)

        print(

        feature_vector.to_string(

            index=False

        )

        )

    # --------------------------------------------------
    # Run Existing Prediction Pipeline
    # --------------------------------------------------

        result = self.engine.run(

        feature_vector

        )

        return result