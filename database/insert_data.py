"""
==========================================================

Insert Prediction Data into PostgreSQL

AI Pull Request Risk Predictor

==========================================================
"""

import json

from database.db_connection import DatabaseConnection


class DatabaseInsert:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.db = DatabaseConnection()

        connected = self.db.connect()

        if not connected:

            raise Exception(
                "Unable to connect to PostgreSQL."
            )

        print("\nDatabase Insert Module Ready")


    # ======================================================
    # Insert Repository
    # ======================================================

    def insert_repository(

        self,

        repository

    ):

        query = """

        INSERT INTO repository (

            repository_name,

            language,

            stars,

            forks,

            license

        )

        VALUES (

            %s,

            %s,

            %s,

            %s,

            %s

        )

        RETURNING repo_id;

        """

        values = (

            repository["repository_name"],

            repository["language"],

            repository["stars"],

            repository["forks"],

            repository["license"]

        )

        self.db.cursor.execute(

            query,

            values

        )

        repo_id = self.db.cursor.fetchone()[0]

        self.db.commit()

        print(

            "Repository Saved :",

            repo_id

        )

        return repo_id


    # ======================================================
    # Insert Pull Request
    # ======================================================

    def insert_pull_request(

        self,

        repo_id,

        pull_request

    ):

        query = """

        INSERT INTO pull_request (

            repo_id,

            review_count,

            comment_count,

            commit_count,

            files_changed,

            additions,

            deletions,

            total_changes,

            total_lines_changed,

            merged

        )

        VALUES (

            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s

        )

        RETURNING pr_id;

        """

        values = (

            repo_id,

            pull_request["review_count"],

            pull_request["comment_count"],

            pull_request["commit_count"],

            pull_request["files_changed"],

            pull_request["additions"],

            pull_request["deletions"],

            pull_request["total_changes"],

            pull_request["total_lines_changed"],

            pull_request["merged"]

        )

        self.db.cursor.execute(

            query,

            values

        )

        pr_id = self.db.cursor.fetchone()[0]

        self.db.commit()

        print(

            "Pull Request Saved :",

            pr_id

        )

        return pr_id
        # ======================================================
    # Insert Prediction
    # ======================================================

    def insert_prediction(

        self,

        pr_id,

        prediction

    ):

        query = """

        INSERT INTO prediction (

            pr_id,

            model_name,

            prediction,

            risk_score,

            confidence,

            risk_level

        )

        VALUES (

            %s,%s,%s,%s,%s,%s

        )

        RETURNING prediction_id;

        """

        values = (

            pr_id,

            prediction["model_name"],

            prediction["label"],

            prediction["risk_score"],

            prediction["confidence"],

            prediction["risk_level"]

        )

        self.db.cursor.execute(

            query,

            values

        )

        prediction_id = self.db.cursor.fetchone()[0]

        self.db.commit()

        print(

            "Prediction Saved :",

            prediction_id

        )

        return prediction_id


    # ======================================================
    # Insert Explanation
    # ======================================================

    def insert_explanation(

        self,

        prediction_id,

        explanation

    ):

        query = """

        INSERT INTO explanation (

            prediction_id,

            top_features,

            ai_explanation,

            recommendation

        )

        VALUES (

            %s,%s,%s,%s

        )

        RETURNING explanation_id;

        """

        top_features_json = json.dumps(

            explanation["top_features"],

            indent=4

        )

        values = (

            prediction_id,

            top_features_json,

            explanation["ai_explanation"],

            explanation["recommendation"]

        )

        self.db.cursor.execute(

            query,

            values

        )

        explanation_id = self.db.cursor.fetchone()[0]

        self.db.commit()

        print(

            "Explanation Saved :",

            explanation_id

        )

        return explanation_id
        # ======================================================
    # Insert Complete Result
    # ======================================================

    def insert_complete_result(

        self,

        result

    ):

        print("\n")
        print("=" * 70)
        print("INSERTING COMPLETE RESULT")
        print("=" * 70)

        # ------------------------------------------
        # Repository
        # ------------------------------------------

        repo_id = self.insert_repository(

            result["repository"]

        )

        # ------------------------------------------
        # Pull Request
        # ------------------------------------------

        pr_id = self.insert_pull_request(

            repo_id,

            result["pull_request"]

        )

        # ------------------------------------------
        # Prediction
        # ------------------------------------------

        prediction_id = self.insert_prediction(

            pr_id,

            result["prediction"]

        )

        # ------------------------------------------
        # Explanation
        # ------------------------------------------

        explanation_id = self.insert_explanation(

            prediction_id,

            result["explanation"]

        )

        print("\n")
        print("=" * 70)
        print("DATABASE INSERT COMPLETED")
        print("=" * 70)

        return {

            "repo_id": repo_id,

            "pr_id": pr_id,

            "prediction_id": prediction_id,

            "explanation_id": explanation_id

        }


    # ======================================================
    # Close Database
    # ======================================================

    def close(self):

        self.db.close()
# ==========================================================
# Test Database Insert
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING DATABASE INSERT")
    print("=" * 70)

    try:

        print("\nThis module will be tested")

        print("after integrating with")

        print("Explanation Engine.")

        print("\nDatabase Module Ready.")

    except Exception as e:

        print("\nError")

        print(e)