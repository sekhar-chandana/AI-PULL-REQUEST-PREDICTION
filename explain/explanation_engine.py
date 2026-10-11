"""
=============================================================

AI Pull Request Risk Predictor

Explanation Engine

This module combines

1. SHAP Engine
2. Groq Engine

and produces one final explanation.

=============================================================
"""

import os
import json
from datetime import datetime
import pandas as pd


import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.insert_data import DatabaseInsert

from explain.shap_engine import SHAPEngine
from explain.groq_engine import GroqEngine


class ExplanationEngine:

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        print("=" * 70)
        print("INITIALIZING EXPLANATION ENGINE")
        print("=" * 70)

        CURRENT_DIR = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.output_folder = os.path.join(
            CURRENT_DIR,
            "Explain_Output"
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

        print("\nLoading SHAP Engine...")

        self.shap_engine = SHAPEngine()

        print("SHAP Engine Loaded")

        print("\nLoading Groq Engine...")

        self.groq_engine = GroqEngine()

        print("Groq Engine Loaded")

        print("\nExplanation Engine Ready")

        print("=" * 70)


    # =====================================================
    # Risk Level
    # =====================================================

    def get_risk_level(

        self,

        risk_score

    ):

        if risk_score < 0.20:

            return "Low"

        elif risk_score < 0.50:

            return "Medium"

        elif risk_score < 0.80:

            return "High"

        else:

            return "Critical"


    # =====================================================
    # Confidence
    # =====================================================

    def get_confidence(

        self,

        risk_score

    ):

        prediction_confidence = max(

            risk_score,

            1 - risk_score

        )

        return round(

            prediction_confidence * 100,

            2

        )


    # =====================================================
    # Current Time
    # =====================================================

    def current_time(self):

        return datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )


    # =====================================================
    # Recommendation
    # =====================================================

    def recommendation(

        self,

        risk_level

    ):

        if risk_level == "Low":

            return (
                "The pull request appears safe. "
                "Continue following the existing "
                "review and testing process."
            )

        elif risk_level == "Medium":

            return (
                "Perform an additional code review "
                "and execute regression tests before merging."
            )

        elif risk_level == "High":

            return (
                "Request a senior developer review "
                "and perform extensive testing before merging."
            )

        else:

            return (
                "Do not merge until all identified risks "
                "have been addressed and validated."
            )
        # =====================================================
    # Generate Complete Explanation
    # =====================================================

    def explain(
        self,
        feature_vector
    ):

        print("\n")
        print("=" * 70)
        print("GENERATING COMPLETE EXPLANATION")
        print("=" * 70)

        # ---------------------------------------------
        # SHAP Prediction
        # ---------------------------------------------

        shap_result = self.shap_engine.explain(
            feature_vector
        )

        prediction = shap_result["prediction"]

        risk_score = prediction["risk_score"]

        confidence = self.get_confidence(
            risk_score
        )

        risk_level = self.get_risk_level(
            risk_score
        )

        # ---------------------------------------------
# Top Features
# ---------------------------------------------

        top_features = self.shap_engine.get_top_features(

        shap_result,

        top_n=10

        )

# ---------------------------------------------
# Prepare CURRENT prediction for Groq
# ---------------------------------------------

        groq_prediction = {

        "label": prediction["label"],

        "risk_score": risk_score,

        "confidence": confidence,

        "risk_level": risk_level

        }

# ---------------------------------------------
# Prepare CURRENT features for Groq
# ---------------------------------------------

        groq_features = pd.DataFrame(

        top_features

        )

# ---------------------------------------------
# Groq Explanation
# ---------------------------------------------

        ai_explanation = self.groq_engine.run(

        prediction=groq_prediction,

        features=groq_features

        )

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        recommendation = self.recommendation(
            risk_level
        )

        # ---------------------------------------------
        # Final Result
        # ---------------------------------------------



        result = {

            "repository": {

            "repository_name": "Unknown Repository",

            "language": "Unknown",

            "stars": 0,

            "forks": 0,

            "license": "Unknown"

            },

        "pull_request": {

        "review_count": 0,

        "comment_count": 0,

        "commit_count": 0,

        "files_changed": 0,

        "additions": 0,

        "deletions": 0,

        "total_changes": 0,

        "total_lines_changed": 0,

        "merged": False

        },

        "prediction": {

        "model_name": type(
            self.shap_engine.model
        ).__name__,

        "label": prediction["label"],

        "prediction_code": prediction["prediction"],

        "risk_score": round(
            risk_score,
            4
        ),

        "confidence": confidence,

        "risk_level": risk_level,

        "generated_at": self.current_time()

            },

        "explanation": {

        "top_features": top_features,

        "ai_explanation": ai_explanation,

        "recommendation": recommendation

            }

        }



        return result


    # =====================================================
    # Print Final Result
    # =====================================================

    def print_result(
    self,
    result
    ):

        print("\n")
        print("=" * 70)
        print("FINAL EXPLANATION")
        print("=" * 70)

    # -------------------------------------------------
    # Prediction Information
    # -------------------------------------------------

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
        str(result["prediction"]["confidence"]) + "%"
        )

        print(
        "Risk Level :",
        result["prediction"]["risk_level"]
        )

        print(
        "Model :",
        result["prediction"]["model_name"]
        )

        print("\nTop Features")

        print("-" * 70)

        for item in result["explanation"]["top_features"]:

            print(

                item["feature"],

                ":",

                round(

                    item["shap_value"],

                    5

                )

            )

        print("\nRecommendation")

        print("-" * 70)

        print(

        result["explanation"]["recommendation"]

        )

        print("\nAI Explanation")

        print("-" * 70)

        print(

            result["explanation"]["ai_explanation"]

        )

        print("=" * 70)


    # =====================================================
    # Save Final JSON
    # =====================================================

    def save_result(
        self,
        result
    ):

        file_path = os.path.join(

            self.output_folder,

            "final_explanation.json"

        )

        with open(

            file_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                result,

                file,

                indent=4

            )

        print("\nFinal JSON Saved")

        print(file_path)

        return file_path
        # =====================================================
    # Complete Pipeline
    # =====================================================

    def run(self, feature_vector):

        result = self.explain(feature_vector)

        self.print_result(result)

        self.save_result(result)

        # ------------------------------------
        # Save into PostgreSQL
        # ------------------------------------

        try:

            database = DatabaseInsert()

            database.insert_complete_result(result)

            database.close()

            print("\nResult Saved to PostgreSQL")

        except Exception as e:

                print("\nDatabase Insert Failed")

                print(e)

        return result

# ==========================================================
# Test Explanation Engine
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING EXPLANATION ENGINE")
    print("=" * 70)

    try:

        engine = ExplanationEngine()

        print("\nLoading Sample Pull Request...\n")

        background = engine.shap_engine.background

        sample = background.iloc[[0]]

        result = engine.run(sample)

        print("\n")
        print("=" * 70)
        print("FINAL RESULT")
        print("=" * 70)

        print(
            "Prediction   :",
            result["prediction"]["label"]
        )

        print(
            "Risk Score   :",
            result["prediction"]["risk_score"]
        )

        print(
            "Confidence   :",
            str(result["prediction"]["confidence"]) + "%"
        )

        print(
            "Risk Level   :",
            result["prediction"]["risk_level"]
        )

        print(
            "Model        :",
            result["prediction"]["model_name"]
        )

        print("\nTop Features")

        print("-" * 70)

        for feature in result["explanation"]["top_features"]:

            print(

                "{:<25} {:>12.5f}".format(

                    feature["feature"],

                    feature["shap_value"]

                )

            )

        print("\nAI Explanation")

        print("-" * 70)

        print(

            result["explanation"]["ai_explanation"]

        )

        print("\nRecommendation")

        print("-" * 70)

        print(

            result["explanation"]["recommendation"]

        )

        print("\n")

        print("=" * 70)
        print("PHASE 4C COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("ERROR OCCURRED")
        print("=" * 70)
        print(e)