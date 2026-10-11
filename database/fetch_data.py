"""
==========================================================

Fetch Data from PostgreSQL

AI Pull Request Risk Predictor

==========================================================
"""

from database.db_connection import DatabaseConnection


class DatabaseFetch:

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

        print("\nDatabase Fetch Module Ready")


    # ======================================================
    # Fetch Repository
    # ======================================================

    def fetch_repository(

        self,

        repo_id

    ):

        query = """

        SELECT *

        FROM repository

        WHERE repo_id = %s;

        """

        self.db.cursor.execute(

            query,

            (repo_id,)

        )

        return self.db.cursor.fetchone()


    # ======================================================
    # Fetch Pull Request
    # ======================================================

    def fetch_pull_request(

        self,

        pr_id

    ):

        query = """

        SELECT *

        FROM pull_request

        WHERE pr_id = %s;

        """

        self.db.cursor.execute(

            query,

            (pr_id,)

        )

        return self.db.cursor.fetchone()
        # ======================================================
    # Fetch Prediction
    # ======================================================

    def fetch_prediction(

        self,

        prediction_id

    ):

        query = """

        SELECT *

        FROM prediction

        WHERE prediction_id = %s;

        """

        self.db.cursor.execute(

            query,

            (prediction_id,)

        )

        return self.db.cursor.fetchone()


    # ======================================================
    # Fetch Explanation
    # ======================================================

    def fetch_explanation(

        self,

        explanation_id

    ):

        query = """

        SELECT *

        FROM explanation

        WHERE explanation_id = %s;

        """

        self.db.cursor.execute(

            query,

            (explanation_id,)

        )

        return self.db.cursor.fetchone()


    # ======================================================
    # Fetch Latest Prediction
    # ======================================================

    def fetch_latest_prediction(

        self

    ):

        query = """

        SELECT *

        FROM prediction

        ORDER BY prediction_time DESC

        LIMIT 1;

        """

        self.db.cursor.execute(

            query

        )

        return self.db.cursor.fetchone()


    # ======================================================
    # Fetch Latest Explanation
    # ======================================================

    def fetch_latest_explanation(

        self

    ):

        query = """

        SELECT *

        FROM explanation

        ORDER BY created_time DESC

        LIMIT 1;

        """

        self.db.cursor.execute(

            query

        )

        return self.db.cursor.fetchone()
        # ======================================================
    # Fetch All Predictions
    # ======================================================

    def fetch_all_predictions(

        self

    ):

        query = """

        SELECT *

        FROM prediction

        ORDER BY prediction_time DESC;

        """

        self.db.cursor.execute(

            query

        )

        return self.db.cursor.fetchall()


    # ======================================================
    # Fetch Prediction History
    # ======================================================

    def fetch_prediction_history(

        self

    ):

        query = """

        SELECT

            prediction.prediction_id,

            prediction.model_name,

            prediction.prediction,

            prediction.risk_score,

            prediction.confidence,

            prediction.risk_level,

            explanation.ai_explanation

        FROM prediction

        INNER JOIN explanation

        ON prediction.prediction_id = explanation.prediction_id

        ORDER BY prediction.prediction_time DESC;

        """

        self.db.cursor.execute(

            query

        )

        return self.db.cursor.fetchall()
        # ======================================================
    # Close Database
    # ======================================================

    def close(

        self

    ):

        self.db.close()
# ==========================================================
# Test Database Fetch
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING DATABASE FETCH")
    print("=" * 70)

    try:

        database = DatabaseFetch()

        print("\nLatest Prediction")

        print("-" * 70)

        latest_prediction = database.fetch_latest_prediction()

        print(latest_prediction)

        print("\nLatest Explanation")

        print("-" * 70)

        latest_explanation = database.fetch_latest_explanation()

        print(latest_explanation)

        print("\nPrediction History")

        print("-" * 70)

        history = database.fetch_prediction_history()

        for row in history:

            print(row)

        database.close()

        print("\n")
        print("=" * 70)
        print("DATABASE FETCH TEST COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("ERROR")
        print("=" * 70)
        print(e)