"""
==========================================================

Database Connection

AI Pull Request Risk Predictor

==========================================================
"""

import psycopg2


class DatabaseConnection:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        self.host = "localhost"

        self.port = "5432"

        self.database = "pr_risk_prediction"

        self.user = "postgres"

        self.password = "Sekhar@1866"

        self.connection = None

        self.cursor = None


    # ======================================================
    # Connect
    # ======================================================

    def connect(self):

        try:

            print("=" * 70)

            print("CONNECTING TO POSTGRESQL DATABASE")

            print("=" * 70)

            self.connection = psycopg2.connect(

                host=self.host,

                port=self.port,

                database=self.database,

                user=self.user,

                password=self.password

            )

            self.cursor = self.connection.cursor()

            print("Database Connected Successfully")

            return True

        except Exception as e:

            print("\nDatabase Connection Failed")

            print(e)

            return False


    # ======================================================
    # Commit
    # ======================================================

    def commit(self):

        if self.connection:

            self.connection.commit()


    # ======================================================
    # Close
    # ======================================================

    def close(self):

        if self.cursor:

            self.cursor.close()

        if self.connection:

            self.connection.close()

        print("Database Connection Closed")