"""
=============================================================
AI Pull Request Risk Predictor

SHAP Engine

Loads:
    • Best ML Model
    • Scaler
    • Feature Names
    • Background Dataset

Performs:
    • Prediction
    • Probability Calculation

Author : AI Pull Request Risk Predictor
=============================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import shap


class SHAPEngine:

    def __init__(self):

        print("=" * 70)
        print("INITIALIZING SHAP ENGINE")
        print("=" * 70)

        # --------------------------------------------------
        # Project Path
        # --------------------------------------------------

        CURRENT_DIR = os.path.dirname(
            os.path.abspath(__file__)
        )

        PROJECT_DIR = os.path.abspath(
            os.path.join(
                CURRENT_DIR,
                ".."
            )
        )

        MODEL_DIR = os.path.join(
            PROJECT_DIR,
            "scripts",
            "Models"
        )

        self.model_path = os.path.join(
            MODEL_DIR,
            "best_model.pkl"
        )

        self.scaler_path = os.path.join(
            MODEL_DIR,
            "scaler.pkl"
        )

        self.feature_path = os.path.join(
            MODEL_DIR,
            "feature_names.pkl"
        )

        self.background_path = os.path.join(
            MODEL_DIR,
            "background_data.pkl"
        )

        print("\nLoading Model...")

        self.model = joblib.load(
            self.model_path
        )

        print("Best Model Loaded")

        print("\nLoading Scaler...")

        self.scaler = joblib.load(
            self.scaler_path
        )

        print("Scaler Loaded")

        print("\nLoading Feature Names...")

        self.feature_names = joblib.load(
            self.feature_path
        )

        print("Feature Names Loaded")

        print("Total Features :", len(self.feature_names))

        print("\nLoading Background Data...")

        self.background = joblib.load(
            self.background_path
        )

        print("Background Loaded")

        print("Background Shape :", self.background.shape)

        print("\nCreating SHAP Explainer...")

        self.explainer = shap.TreeExplainer(
            self.model
        )

        print("SHAP Explainer Ready")

        print("=" * 70)

    # ======================================================
    # Convert Feature Vector to DataFrame
    # ======================================================

    def prepare_features(
        self,
        feature_vector
        ):

    # -------------------------------
    # Dictionary
    # -------------------------------
        if isinstance(feature_vector, dict):

            df = pd.DataFrame([feature_vector])

    # -------------------------------
    # List
    # -------------------------------
        elif isinstance(feature_vector, list):

            df = pd.DataFrame(
            [feature_vector],
            columns=self.feature_names
            )

    # -------------------------------
    # NumPy Array
    # -------------------------------
        elif isinstance(feature_vector, np.ndarray):

            if feature_vector.ndim == 1:

                feature_vector = feature_vector.reshape(1, -1)

            df = pd.DataFrame(
            feature_vector,
            columns=self.feature_names
            )

    # -------------------------------
    # Pandas Series
    # -------------------------------
        elif isinstance(feature_vector, pd.Series):

            df = feature_vector.to_frame().T

    # -------------------------------
    # Pandas DataFrame
    # -------------------------------
        elif isinstance(feature_vector, pd.DataFrame):

            df = feature_vector.copy()

    # -------------------------------
    # Unsupported Type
    # -------------------------------
        else:

            raise TypeError(
                f"Unsupported input type: {type(feature_vector)}"
            )

    # --------------------------------------------------
    # Ensure Correct Feature Order
    # --------------------------------------------------

        df = df[self.feature_names]

        return df

    # ======================================================
    # Prediction
    # ======================================================

    def predict(
        self,
        feature_vector
    ):

        df = self.prepare_features(
            feature_vector
        )

        prediction = self.model.predict(
            df
        )[0]

        probability = self.model.predict_proba(
            df
        )[0][1]

        if prediction == 1:

            label = "Buggy"

        else:

            label = "Safe"

        return {

            "prediction": int(prediction),

            "label": label,

            "risk_score": float(probability)

        }

    # ======================================================
    # Display Prediction
    # ======================================================

    def print_prediction(
        self,
        prediction_result
    ):

        print("\nPrediction")

        print("-" * 40)

        print(
            "Prediction :",
            prediction_result["label"]
        )

        print(
            "Risk Score :",
            round(
                prediction_result["risk_score"],
                4
            )
        )

        print("-" * 40)
            # ======================================================
    # Generate SHAP Values
    # ======================================================

    def generate_shap_values(
        self,
        feature_vector
    ):

        df = self.prepare_features(
            feature_vector
        )

        prediction = self.predict(
            feature_vector
        )

        # ---------------------------------------------
        # SHAP Values
        # ---------------------------------------------

        shap_values = self.explainer.shap_values(df)

        # Binary Classification
        if isinstance(shap_values, list):

            shap_array = shap_values[1][0]

        else:

            shap_array = shap_values[0]

        feature_importance = []

        for feature, value, shap_value in zip(

            self.feature_names,

            df.iloc[0],

            shap_array

        ):

            feature_importance.append({

                "feature": feature,

                "value": float(value),

                "shap_value": float(shap_value),

                "impact": abs(float(shap_value))

            })

        feature_importance = sorted(

            feature_importance,

            key=lambda x: x["impact"],

            reverse=True

        )

        return {

            "prediction": prediction,

            "feature_importance": feature_importance,

            "raw_shap_values": shap_array,

            "input_dataframe": df

        }

    # ======================================================
    # Top Important Features
    # ======================================================

    def get_top_features(

        self,

        shap_result,

        top_n=10

    ):

        return shap_result["feature_importance"][:top_n]

    # ======================================================
    # Print Top Features
    # ======================================================

    def print_top_features(

        self,

        shap_result,

        top_n=10

    ):

        top_features = self.get_top_features(

            shap_result,

            top_n

        )

        print("\n")

        print("=" * 70)

        print("TOP IMPORTANT FEATURES")

        print("=" * 70)

        print(

            "{:<25} {:>12} {:>15}".format(

                "Feature",

                "Value",

                "SHAP Impact"

            )

        )

        print("-" * 70)

        for item in top_features:

            print(

                "{:<25} {:>12.2f} {:>15.5f}".format(

                    item["feature"],

                    item["value"],

                    item["shap_value"]

                )

            )

        print("=" * 70)

    # ======================================================
    # Convert SHAP Result to DataFrame
    # ======================================================

    def feature_dataframe(

        self,

        shap_result

    ):

        return pd.DataFrame(

            shap_result["feature_importance"]

        )

    # ======================================================
    # Save Top Features CSV
    # ======================================================

    def save_top_features(

        self,

        shap_result,

        output_folder="Explain_Output",

        top_n=10

    ):

        os.makedirs(

            output_folder,

            exist_ok=True

        )

        df = self.feature_dataframe(

            shap_result

        )

        df = df.head(top_n)

        csv_path = os.path.join(

            output_folder,

            "top_features.csv"

        )

        df.to_csv(

            csv_path,

            index=False

        )

        print("\nTop Features Saved")

        print(csv_path)

        return csv_path
        # ======================================================
    # SHAP Summary Plot
    # ======================================================

    def summary_plot(
        self,
        shap_result,
        output_folder="Explain_Output"
    ):

        os.makedirs(output_folder, exist_ok=True)

        summary_path = os.path.join(
            output_folder,
            "shap_summary.png"
        )

        try:

            shap.summary_plot(

                shap_result["raw_shap_values"].reshape(1, -1),

                shap_result["input_dataframe"],

                feature_names=self.feature_names,

                show=False

            )

            import matplotlib.pyplot as plt

            plt.tight_layout()

            plt.savefig(
                summary_path,
                dpi=300,
                bbox_inches="tight"
            )

            plt.close()

            print("SHAP Summary Plot Saved")

        except Exception as e:

            print("Summary Plot Error :", e)

        return summary_path


    # ======================================================
    # Feature Importance Bar Chart
    # ======================================================

    def feature_bar_plot(

        self,

        shap_result,

        output_folder="Explain_Output",

        top_n=10

    ):

        import matplotlib.pyplot as plt

        os.makedirs(output_folder, exist_ok=True)

        df = self.feature_dataframe(

            shap_result

        ).head(top_n)

        plt.figure(figsize=(10,6))

        plt.barh(

            df["feature"],

            df["impact"]

        )

        plt.xlabel("Absolute SHAP Value")

        plt.ylabel("Feature")

        plt.title("Top SHAP Features")

        plt.tight_layout()

        path = os.path.join(

            output_folder,

            "feature_importance.png"

        )

        plt.savefig(

            path,

            dpi=300

        )

        plt.close()

        print("Feature Importance Plot Saved")

        return path


    # ======================================================
    # Waterfall Plot
    # ======================================================

    def waterfall_plot(

        self,

        shap_result,

        output_folder="Explain_Output"

    ):

        os.makedirs(output_folder, exist_ok=True)

        path = os.path.join(

            output_folder,

            "waterfall_plot.png"

        )

        try:

            explanation = shap.Explanation(

                values=shap_result["raw_shap_values"],

                base_values=self.explainer.expected_value,

                data=shap_result["input_dataframe"].iloc[0].values,

                feature_names=self.feature_names

            )

            shap.plots.waterfall(

                explanation,

                show=False

            )

            import matplotlib.pyplot as plt

            plt.tight_layout()

            plt.savefig(

                path,

                dpi=300,

                bbox_inches="tight"

            )

            plt.close()

            print("Waterfall Plot Saved")

        except Exception as e:

            print("Waterfall Plot Error :", e)

        return path


    # ======================================================
    # Force Plot
    # ======================================================

    def force_plot(

        self,

        shap_result,

        output_folder="Explain_Output"

    ):

        os.makedirs(output_folder, exist_ok=True)

        html_path = os.path.join(

            output_folder,

            "force_plot.html"

        )

        try:

            force = shap.force_plot(

                self.explainer.expected_value,

                shap_result["raw_shap_values"],

                shap_result["input_dataframe"],

                matplotlib=False

            )

            shap.save_html(

                html_path,

                force

            )

            print("Force Plot Saved")

        except Exception as e:

            print("Force Plot Error :", e)

        return html_path


    # ======================================================
    # Generate All SHAP Outputs
    # ======================================================

    def generate_visualizations(

        self,

        shap_result,

        output_folder="Explain_Output"

    ):

        print("\nGenerating SHAP Visualizations...\n")

        self.summary_plot(

            shap_result,

            output_folder

        )

        self.feature_bar_plot(

            shap_result,

            output_folder

        )

        self.waterfall_plot(

            shap_result,

            output_folder

        )

        self.force_plot(

            shap_result,

            output_folder

        )

        print("\nAll SHAP Visualizations Generated Successfully")
            # ======================================================
    # Save Prediction JSON
    # ======================================================

    def save_prediction_json(
        self,
        shap_result,
        output_folder="Explain_Output"
    ):

        import json

        os.makedirs(output_folder, exist_ok=True)

        prediction = shap_result["prediction"]

        top_features = self.get_top_features(
            shap_result,
            top_n=10
        )

        output = {

            "prediction": prediction["prediction"],

            "label": prediction["label"],

            "risk_score": prediction["risk_score"],

            "top_features": top_features

        }

        json_path = os.path.join(

            output_folder,

            "prediction.json"

        )

        with open(

            json_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                output,

                f,

                indent=4

            )

        print("\nPrediction JSON Saved")

        print(json_path)

        return json_path


    # ======================================================
    # Complete Explanation Pipeline
    # ======================================================

    def explain(

        self,

        feature_vector,

        output_folder="Explain_Output"

    ):

        print("\n")

        print("=" * 70)

        print("GENERATING SHAP EXPLANATION")

        print("=" * 70)

        shap_result = self.generate_shap_values(

            feature_vector

        )

        self.print_prediction(

            shap_result["prediction"]

        )

        self.print_top_features(

            shap_result,

            top_n=10

        )

        self.save_top_features(

            shap_result,

            output_folder

        )

        self.generate_visualizations(

            shap_result,

            output_folder

        )

        self.save_prediction_json(

            shap_result,

            output_folder

        )

        print("\n")

        print("=" * 70)

        print("SHAP EXPLANATION COMPLETED")

        print("=" * 70)

        return shap_result


# ==========================================================
# Example Usage
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)

    print("TESTING SHAP ENGINE")

    print("=" * 70)

    try:

        engine = SHAPEngine()

        background = engine.background

        sample = background.iloc[[0]]

        result = engine.explain(sample)

        print("\n")

        print("Prediction Label :",

              result["prediction"]["label"])

        print("Risk Score :",

              round(

                  result["prediction"]["risk_score"],

                  4

              ))

        print("\nTop 10 Features\n")

        for feature in result["feature_importance"][:10]:

            print(

                feature["feature"],

                "->",

                round(

                    feature["shap_value"],

                    5

                )

            )

        print("\n")

        print("Everything Generated Successfully")

    except Exception as e:

        print("\nERROR OCCURRED")

        print(e)
