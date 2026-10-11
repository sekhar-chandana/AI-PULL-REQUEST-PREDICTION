"""
==========================================================

GitHub Pull Request Feature Extractor

AI Pull Request Risk Predictor

==========================================================
"""
import os
import joblib
from datetime import datetime, timezone


class GitHubFeatureExtractor:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self):

        print("=" * 70)
        print("INITIALIZING GITHUB FEATURE EXTRACTOR")
        print("=" * 70)

        # --------------------------------------------------
        # Project Root
        # --------------------------------------------------

        current_dir = os.path.dirname(
        os.path.abspath(__file__)
        )

        project_root = os.path.dirname(
        current_dir
        )

        encoder_path = os.path.join(
        project_root,
        "label_encoders.pkl"
        )

    # --------------------------------------------------
    # Load Encoders
    # --------------------------------------------------

        print("\nLoading Label Encoders...")

        if   not os.path.exists(
        encoder_path
        ):

            raise FileNotFoundError(

            "label_encoders.pkl not found: "

            + encoder_path

            )

        encoders = joblib.load(

        encoder_path

        )

        self.language_encoder = encoders[

        "language"

        ]

        self.license_encoder = encoders[

        "license"

        ]

        print(

        "Language Encoder Loaded"

        )

        print(

        "License Encoder Loaded"

        )

        print(

        "GitHub Feature Extractor Ready"

        )

    # ======================================================
    # Safe Integer
    # ======================================================

    def safe_int(

        self,

        value,

        default=0

    ):

        if value is None:

            return default

        try:

            return int(value)

        except (

            TypeError,

            ValueError

        ):

            return default

    # ======================================================
    # Calculate Review Time
    # ======================================================

    def calculate_review_time(

        self,

        created_at,

        updated_at

    ):

        if not created_at or not updated_at:

            return 0.0

        try:

            created = datetime.fromisoformat(

                created_at.replace(

                    "Z",

                    "+00:00"

                )

            )

            updated = datetime.fromisoformat(

                updated_at.replace(

                    "Z",

                    "+00:00"

                )

            )

            seconds = (

                updated - created

            ).total_seconds()

            hours = seconds / 3600

            return max(

                0.0,

                round(hours, 2)

            )

        except (

            ValueError,

            TypeError

        ):

            return 0.0

    # ======================================================
    # Extract Created Date Features
    # ======================================================

    def extract_date_features(

        self,

        created_at

    ):

        if not created_at:

            now = datetime.now(

                timezone.utc

            )

        else:

            try:

                now = datetime.fromisoformat(

                    created_at.replace(

                        "Z",

                        "+00:00"

                    )

                )

            except (

                ValueError,

                TypeError

            ):

                now = datetime.now(

                    timezone.utc

                )

        return {

            "created_year":

                now.year,

            "created_month":

                now.month,

            "created_day":

                now.day,

            "created_weekday":

                now.weekday()

        }

    # ======================================================
    # Count Reviews
    # ======================================================

    def extract_review_features(

        self,

        reviews

    ):

        if not reviews:

            reviews = []

        review_count = len(

            reviews

        )

        approved_reviews = 0

        commented_reviews = 0

        for review in reviews:

            state = (

                review.get(

                    "state",

                    ""

                )

                or ""

            ).upper()

            if state == "APPROVED":

                approved_reviews += 1

            if state in (

                "COMMENTED",

                "CHANGES_REQUESTED"

            ):

                commented_reviews += 1

        return {

            "review_count":

                review_count,

            "approved_reviews":

                approved_reviews,

            "commented_reviews":

                commented_reviews

        }

    # ======================================================
    # Count Test Files
    # ======================================================

    def count_test_files(

        self,

        changed_files

    ):

        count = 0

        for file_data in (

            changed_files or []

        ):

            filename = (

                file_data.get(

                    "filename",

                    ""

                )

                or ""

            ).lower()

            if (

                "test" in filename

                or "spec" in filename

            ):

                count += 1

        return count

    # ======================================================
    # Count High Risk Files
    # ======================================================

    def count_high_risk_files(

        self,

        changed_files

    ):

        count = 0

        high_risk_extensions = {

            ".env",

            ".pem",

            ".key",

            ".crt",

            ".sql",

            ".sh",

            ".bat",

            ".ps1"

        }

        high_risk_names = {

            "dockerfile",

            "package.json",

            "requirements.txt",

            "pom.xml",

            "build.gradle"

        }

        for file_data in (

            changed_files or []

        ):

            filename = (

                file_data.get(

                    "filename",

                    ""

                )

                or ""

            )

            lower_filename = filename.lower()

            name = lower_filename.split(

                "/"

            )[-1]

            extension = ""

            if "." in name:

                extension = (

                    "."

                    + name.rsplit(

                        ".",

                        1

                    )[1]

                )

            if (

                extension in high_risk_extensions

                or name in high_risk_names

            ):

                count += 1

        return count

    # ======================================================
    # Encode Language
    # ======================================================
    def encode_language(

    self,

    language

    ):

        if language is None:

            language = "Unknown"

        language = str(

            language

        ).strip()

    # --------------------------------------------------
    # Known Language
    # --------------------------------------------------

        if language in self.language_encoder.classes_:

            return int(

                self.language_encoder.transform(

                [language]

                )[0]

            )

    # --------------------------------------------------
    # Unknown Language
    # --------------------------------------------------

        print(

        f"Warning: Unknown language '{language}'. "

        "Using Unknown encoding."

        )

        return int(

        self.language_encoder.transform(

            ["Unknown"]

        )[0]

        )

    # ======================================================
    # Encode License
    # ======================================================

    def encode_license(

    self,

    license_data

    ):

    # --------------------------------------------------
    # No License
    # --------------------------------------------------

        if not license_data:

            license_name = "Unknown"

    # --------------------------------------------------
    # GitHub License Object
    # --------------------------------------------------

        elif isinstance(

            license_data,

            dict

        ):

            license_name = (

                license_data.get(

                "spdx_id"

                )

            or license_data.get(

                "name"

                )

            or "Unknown"

            )

        else:

            license_name = str(

            license_data

            )

        license_name = str(

        license_name

        ).strip()

    # --------------------------------------------------
    # Known License
    # --------------------------------------------------

        if license_name in self.license_encoder.classes_:

            return int(

            self.license_encoder.transform(

                [license_name]

                )[0]

            )

    # --------------------------------------------------
    # Unknown License
    # --------------------------------------------------

        print(

        f"Warning: Unknown license "

        f"'{license_name}'. "

        "Using Unknown encoding."

        )

        return int(

        self.license_encoder.transform(

            ["Unknown"]

        )[0]

        )
    # ======================================================
    # Extract All 22 Features
    # ======================================================

    def extract_features(

        self,

        repository,

        pull_request,

        reviews,

        comments,

        commits,

        changed_files

    ):

        print("\nExtracting GitHub Features...")

        # --------------------------------------------------
        # Repository Features
        # --------------------------------------------------

        language = self.encode_language(

            repository.get(

                "language"

            )

        )

        stars = self.safe_int(

            repository.get(

                "stargazers_count"

            )

        )

        forks = self.safe_int(

            repository.get(

                "forks_count"

            )

        )

        license_value = self.encode_license(

            repository.get(

                "license"

            )

        )

        # --------------------------------------------------
        # Review Features
        # --------------------------------------------------

        review_features = (

            self.extract_review_features(

                reviews

            )

        )

        review_count = (

            review_features[

                "review_count"

            ]

        )

        approved_reviews = (

            review_features[

                "approved_reviews"

            ]

        )

        commented_reviews = (

            review_features[

                "commented_reviews"

            ]

        )

        # --------------------------------------------------
        # Comment Features
        # --------------------------------------------------

        comment_count = len(

            comments or []

        )

        # --------------------------------------------------
        # Commit Features
        # --------------------------------------------------

        commit_count = len(

            commits or []

        )

        # --------------------------------------------------
        # Changed File Features
        # --------------------------------------------------

        files_changed = len(

            changed_files or []

        )

        additions = 0

        deletions = 0

        for file_data in (

            changed_files or []

        ):

            additions += self.safe_int(

                file_data.get(

                    "additions"

                )

            )

            deletions += self.safe_int(

                file_data.get(

                    "deletions"

                )

            )

        # --------------------------------------------------
        # Total Changes
        # --------------------------------------------------

        total_changes = (

            additions

            + deletions

        )

        total_lines_changed = (

            additions

            + deletions

        )

        # --------------------------------------------------
        # Test Files
        # --------------------------------------------------

        test_files = (

            self.count_test_files(

                changed_files

            )

        )

        # --------------------------------------------------
        # High Risk Files
        # --------------------------------------------------

        high_risk_files = (

            self.count_high_risk_files(

                changed_files

            )

        )

        # --------------------------------------------------
        # Review Time
        # --------------------------------------------------

        review_time_hours = (

            self.calculate_review_time(

                pull_request.get(

                    "created_at"

                ),

                pull_request.get(

                    "updated_at"

                )

            )

        )

        # --------------------------------------------------
        # Date Features
        # --------------------------------------------------

        date_features = (

            self.extract_date_features(

                pull_request.get(

                    "created_at"

                )

            )

        )

        # --------------------------------------------------
        # Merged
        # --------------------------------------------------

        merged = 1 if (

            pull_request.get(

                "merged"

            )

        ) else 0

        # --------------------------------------------------
        # Final Feature Dictionary
        # --------------------------------------------------

        features = {

            "language":

                language,

            "stars":

                stars,

            "forks":

                forks,

            "license":

                license_value,

            "review_count":

                review_count,

            "approved_reviews":

                approved_reviews,

            "commented_reviews":

                commented_reviews,

            "comment_count":

                comment_count,

            "commit_count":

                commit_count,

            "files_changed":

                files_changed,

            "additions":

                additions,

            "deletions":

                deletions,

            "total_changes":

                total_changes,

            "total_lines_changed":

                total_lines_changed,

            "test_files":

                test_files,

            "high_risk_files":

                high_risk_files,

            "review_time_hours":

                review_time_hours,

            "created_year":

                date_features[

                    "created_year"

                ],

            "created_month":

                date_features[

                    "created_month"

                ],

            "created_day":

                date_features[

                    "created_day"

                ],

            "created_weekday":

                date_features[

                    "created_weekday"

                ],

            "merged":

                merged

        }

        print("\n22 Features Extracted")

        print("-" * 70)

        for name, value in features.items():

            print(

                f"{name:<25}: {value}"

            )

        return features


# ==========================================================
# Test Feature Extractor
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING GITHUB FEATURE EXTRACTOR")
    print("=" * 70)

    extractor = GitHubFeatureExtractor()

    print("\nFeature extractor initialized successfully.")

    print("\n22 expected features:")

    expected_features = [

        "language",

        "stars",

        "forks",

        "license",

        "review_count",

        "approved_reviews",

        "commented_reviews",

        "comment_count",

        "commit_count",

        "files_changed",

        "additions",

        "deletions",

        "total_changes",

        "total_lines_changed",

        "test_files",

        "high_risk_files",

        "review_time_hours",

        "created_year",

        "created_month",

        "created_day",

        "created_weekday",

        "merged"

    ]

    for index, feature in enumerate(

        expected_features,

        start=1

    ):

        print(

            f"{index:02d}. {feature}"

        )

    print("\n")

    print("=" * 70)

    print("FEATURE EXTRACTOR TEST COMPLETED")

    print("=" * 70)