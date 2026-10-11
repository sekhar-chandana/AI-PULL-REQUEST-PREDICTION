"""
=============================================================
AI Pull Request Risk Predictor

Groq Engine

Loads:
    • prediction.json
    • top_features.csv

Uses:
    • Groq API

Returns:
    • Human Readable Explanation

=============================================================
"""
from dotenv import load_dotenv
import os
import json
import pandas as pd
from datetime import datetime
from groq import Groq


class GroqEngine:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        print("=" * 70)
        print("INITIALIZING GROQ ENGINE")
        print("=" * 70)

        CURRENT_DIR = os.path.dirname(
        os.path.abspath(__file__)
        )

        # Explain_Output is inside explain folder
        self.output_folder = os.path.join(
        CURRENT_DIR,
        "Explain_Output"
            )

                    
        # ---------------------------------------
        # Load Environment Variables
        # ---------------------------------------

        from dotenv import load_dotenv

        env_path = os.path.join(
        CURRENT_DIR,
        ".env"
        )   

        load_dotenv(env_path)

        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:

            raise ValueError(
            "GROQ_API_KEY not found in .env"
            )

        print("Groq API Loaded Successfully")

        self.client = Groq(
            api_key=self.api_key
            )

        # ---------------------------------------
        # File Paths
        # ---------------------------------------

        self.prediction_file = os.path.join(

            self.output_folder,

            "prediction.json"

        )

        self.feature_file = os.path.join(

            self.output_folder,

            "top_features.csv"

        )

        print("Prediction File :")

        print(self.prediction_file)

        print("Feature File :")

        print(self.feature_file)

        print("=" * 70)


    # ======================================================
    # Load Prediction
    # ======================================================

    def load_prediction(self):

        with open(

            self.prediction_file,

            "r",

            encoding="utf-8"

        ) as f:

            prediction = json.load(f)

        return prediction


    # ======================================================
    # Load Top Features
    # ======================================================

    def load_features(self):

        df = pd.read_csv(

            self.feature_file

        )

        return df


    # ======================================================
    # Build Prompt
    # ======================================================

    def build_prompt(
        self,
        prediction,
        features
            ):

        prompt = f"""
        You are a Senior Software Engineer and Code Reviewer.

        Your task is to explain the result of an AI model that predicts
        whether a GitHub Pull Request is likely to introduce bugs.

        ====================================================

        Prediction Summary

        Prediction      : {prediction['label']}

        Risk Score      : {prediction['risk_score']:.4f}

        Confidence      : {prediction['confidence']:.2f}%

        Risk Level      : {prediction['risk_level']}

        ====================================================

        Most Important Factors

        """

    # ------------------------------------------
    # Top Features
    # ------------------------------------------

        for index, row in features.iterrows():

            prompt += f"""

        Feature {index+1}

        Feature Name : {row['feature']}

        Actual Value : {row['value']}

        Model Impact : {row['shap_value']:.5f}

        """

        prompt += """

        ====================================================

        Instructions

        Act like an experienced Software Architect.

        Do NOT mention:

        • SHAP
        • Machine Learning
        • Artificial Intelligence
        • Feature Importance
        • Model Prediction

        Instead explain the result naturally.

        Your explanation must contain these sections.

        1. Overall Assessment

        Describe whether the pull request appears Low Risk,
        Medium Risk or High Risk.

        2. Why?

        Explain why the pull request received this prediction
        using the important factors.
        Talk naturally about

        • code size
        • commits
        • reviews
        • files changed
        • additions
        • deletions

        where applicable.

        3. Risk Analysis

        Explain what could happen if this pull request
        is merged.

        4. Recommendation

        Give practical advice to the developer.

        Examples:

        • merge after testing

        • request another review

        • split large pull requests

        • improve documentation

        • increase automated testing

        5. Summary

        Write one concluding paragraph.

        Use professional English.
 
        Keep the explanation between 180 and 250 words.

        Do not use bullet points except in Recommendation.

        """
        return prompt
        # ======================================================
    # Generate Explanation Using Groq
    # ======================================================

    def generate_explanation(self):

        prediction = self.load_prediction()

        features = self.load_features()

        prompt = self.build_prompt(

            prediction,

            features

        )
        print("\n")
        print("=" * 70)
        print("PROMPT SENT TO GROQ")
        print("=" * 70)
        print(prompt)
        print("=" * 70)

        print("\nGenerating Explanation from Groq...\n")

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {

                    "role": "system",

                    "content":
                    "You are an expert software engineering assistant."

                },

                {

                    "role": "user",

                    "content": prompt

                }

            ],

            temperature=0.2,

            max_tokens=700

        )

        explanation = response.choices[0].message.content
        print("\n")
        print("=" * 70)
        print("AI RESPONSE RECEIVED")
        print("=" * 70)

        return explanation


    # ======================================================
    # Save Explanation
    # ======================================================

    def save_explanation(

        self,

        explanation

    ):

        os.makedirs(

            self.output_folder,

            exist_ok=True

        )

        txt_path = os.path.join(

            self.output_folder,

            "groq_explanation.txt"

        )

        with open(

            txt_path,

            "w",

            encoding="utf-8"

        ) as f:

            f.write(explanation)

        print("\nExplanation Saved")

        print(txt_path)

        return txt_path


    # ======================================================
    # Save Response JSON
    # ======================================================
# ======================================================
# Save Response JSON
# ======================================================

    def save_json(

        self,

        explanation

    ):

        prediction = self.load_prediction()

        features = self.load_features()

        response = {

            "model_information": {

            "model_name": "Best Model",

            "generated_at":datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        },

        "prediction": {

            "label": prediction["label"],

            "risk_score": prediction["risk_score"]

        },

            "top_features": features.to_dict(
            orient="records"
            ),

            "ai_explanation": explanation

        }

        json_path = os.path.join(

        self.output_folder,

        "groq_response.json"

        )

        with open(

        json_path,

        "w",

        encoding="utf-8"

        ) as f:

         json.dump(

            response,

            f,

            indent=4

            )

        print("\nJSON Saved")

        print(json_path)

        return json_path

    # ======================================================
    # Complete Pipeline
    # ======================================================

    def run(

        self,

        prediction=None,

        features=None

    ):

    # --------------------------------------------------
    # Use current prediction/features when provided
    # --------------------------------------------------

        if prediction is None:

            prediction = self.load_prediction()

        if features is None:

            features = self.load_features()

    # --------------------------------------------------
    # Build prompt using CURRENT data
    # --------------------------------------------------

        prompt = self.build_prompt(

        prediction,

        features

        )

        print("\n")
        print("=" * 70)
        print("PROMPT SENT TO GROQ")
        print("=" * 70)

        print(prompt)

        print("=" * 70)

        print("\nGenerating Explanation from Groq...\n")

        response = self.client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {

                "role": "system",

                "content":
                "You are an expert software engineering assistant."

            },

            {

                "role": "user",

                "content": prompt

            }

        ],

        temperature=0.2,

        max_tokens=700

        )

        explanation = (

        response

        .choices[0]

        .message

        .content

        )

        print("\n")
        print("=" * 70)
        print("AI RESPONSE RECEIVED")
        print("=" * 70)

    # --------------------------------------------------
    # Save current explanation
    # --------------------------------------------------

        self.save_explanation(

        explanation

        )

        self.save_json(

        explanation

        )

        print("\n")
        print("=" * 70)
        print("GROQ EXPLANATION GENERATED")
        print("=" * 70)

        return explanation
        # ======================================================
    # Print Explanation
    # ======================================================

    def print_explanation(
        self,
        explanation
    ):

        print("\n")
        print("=" * 70)
        print("GROQ AI EXPLANATION")
        print("=" * 70)
        print(explanation)
        print("=" * 70)


# ==========================================================
# Main Function
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING GROQ ENGINE")
    print("=" * 70)

    try:

        engine = GroqEngine()

        explanation = engine.run()

        engine.print_explanation(
            explanation
        )

        print("\n")
        print("Groq Engine Executed Successfully")
        print("\nGenerated Files:")

        print("Explain_Output/groq_explanation.txt")
        print("Explain_Output/groq_response.json")

    except FileNotFoundError as e:

        print("\nFile Not Found")
        print(e)

    except ValueError as e:

        print("\nConfiguration Error")
        print(e)

    except Exception as e:

        print("\nUnexpected Error")
        print(e)