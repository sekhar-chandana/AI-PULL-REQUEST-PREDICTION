"""
==========================================================

Create PostgreSQL Tables

AI Pull Request Risk Predictor

==========================================================
"""

from database.db_connection import DatabaseConnection


class DatabaseTables:

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

    # ======================================================
    # Repository Table
    # ======================================================

    def create_repository_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS repository (

            repo_id SERIAL PRIMARY KEY,

            repository_name VARCHAR(255),

            language VARCHAR(100),

            stars INTEGER,

            forks INTEGER,

            license VARCHAR(100),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

        """

        self.db.cursor.execute(query)

        self.db.commit()

        print("Repository Table Created")


    # ======================================================
    # Pull Request Table
    # ======================================================

    def create_pull_request_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS pull_request (

            pr_id SERIAL PRIMARY KEY,

            repo_id INTEGER REFERENCES repository(repo_id),

            review_count INTEGER,

            comment_count INTEGER,

            commit_count INTEGER,

            files_changed INTEGER,

            additions INTEGER,

            deletions INTEGER,

            total_changes INTEGER,

            total_lines_changed INTEGER,

            merged BOOLEAN,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

        """

        self.db.cursor.execute(query)

        self.db.commit()

        print("Pull Request Table Created")


    # ======================================================
    # Prediction Table
    # ======================================================

    def create_prediction_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS prediction (

            prediction_id SERIAL PRIMARY KEY,

            pr_id INTEGER REFERENCES pull_request(pr_id),

            model_name VARCHAR(100),

            prediction VARCHAR(30),

            risk_score FLOAT,

            confidence FLOAT,

            risk_level VARCHAR(50),

            prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

        """

        self.db.cursor.execute(query)

        self.db.commit()

        print("Prediction Table Created")


    # ======================================================
    # Explanation Table
    # ======================================================

    def create_explanation_table(self):

        query = """

        CREATE TABLE IF NOT EXISTS explanation (

            explanation_id SERIAL PRIMARY KEY,

            prediction_id INTEGER REFERENCES prediction(prediction_id),

            top_features TEXT,

            ai_explanation TEXT,

            recommendation TEXT,

            created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );

        """

        self.db.cursor.execute(query)

        self.db.commit()

        print("Explanation Table Created")


    # ======================================================
    # Create All Tables
    # ======================================================

    def create_all_tables(self):

        print("\nCreating Tables...\n")

        self.create_repository_table()

        self.create_pull_request_table()

        self.create_prediction_table()

        self.create_explanation_table()

        print("\nAll Tables Created Successfully")

        self.db.close()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    database = DatabaseTables()

    database.create_all_tables()