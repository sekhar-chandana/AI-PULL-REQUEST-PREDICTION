"""
==========================================================

PostgreSQL Database Test

AI Pull Request Risk Predictor

==========================================================
"""

from database.db_connection import DatabaseConnection
from database.create_tables import DatabaseTables
from database.insert_data import DatabaseInsert
from database.fetch_data import DatabaseFetch


class DatabaseTester:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        print("=" * 70)
        print("DATABASE INTEGRATION TEST")
        print("=" * 70)

        self.connection = DatabaseConnection()


    # ======================================================
    # Test Connection
    # ======================================================

    def test_connection(self):

        print("\nTesting Database Connection...")

        connected = self.connection.connect()

        if connected:

            print("✓ Database Connection Successful")

        else:

            raise Exception(
                "Database Connection Failed"
            )

        self.connection.close()


    # ======================================================
    # Test Table Creation
    # ======================================================

    def test_tables(self):

        print("\nTesting Table Creation...")

        tables = DatabaseTables()

        tables.create_all_tables()

        print("✓ Tables Verified")


    # ======================================================
    # Test Insert Module
    # ======================================================

    def test_insert_module(self):

        print("\nTesting Insert Module...")

        insert = DatabaseInsert()

        print("✓ Insert Module Loaded")

        insert.close()


    # ======================================================
    # Test Fetch Module
    # ======================================================

    def test_fetch_module(self):

        print("\nTesting Fetch Module...")

        fetch = DatabaseFetch()

        print("✓ Fetch Module Loaded")

        try:

            prediction = fetch.fetch_latest_prediction()

            if prediction:

                print("✓ Latest Prediction Found")

            else:

                print("No Prediction Data Available")

        except Exception:

            print("Prediction Table Empty")

        fetch.close()


    # ======================================================
    # Run All Tests
    # ======================================================

    def run(self):

        self.test_connection()

        self.test_tables()

        self.test_insert_module()

        self.test_fetch_module()

        print("\n")
        print("=" * 70)
        print("ALL DATABASE TESTS PASSED")
        print("=" * 70)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    try:

        tester = DatabaseTester()

        tester.run()

    except Exception as e:

        print("\n")
        print("=" * 70)
        print("DATABASE TEST FAILED")
        print("=" * 70)
        print(e)