"""
==========================================================

GitHub Pull Request Service

AI Pull Request Risk Predictor

==========================================================
"""
import os
import sys


# ----------------------------------------------------------
# Add Project Root to Python Path
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
from github.github_client import GitHubClient
from github.feature_extractor import GitHubFeatureExtractor


# ==========================================================
# GitHub Service
# ==========================================================

class GitHubService:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(self, token=None):

        print("=" * 70)
        print("INITIALIZING GITHUB SERVICE")
        print("=" * 70)

        self.client = GitHubClient(

            token=token

        )

        self.extractor = GitHubFeatureExtractor()

        print("GitHub Service Ready")

    # ======================================================
    # Analyze Pull Request
    # ======================================================

    def analyze_pull_request(

        self,

        pr_url

    ):

        print("\n")
        print("=" * 70)
        print("ANALYZING GITHUB PULL REQUEST")
        print("=" * 70)

        # --------------------------------------------------
        # Parse URL
        # --------------------------------------------------

        parsed = self.client.parse_pr_url(

            pr_url

        )

        owner = parsed["owner"]

        repository_name = parsed["repository"]

        pull_number = parsed["pull_number"]

        print("\nPull Request")

        print(

            "Owner      :",

            owner

        )

        print(

            "Repository :",

            repository_name

        )

        print(

            "PR Number  :",

            pull_number

        )

        # --------------------------------------------------
        # Get Repository
        # --------------------------------------------------

        print("\nLoading Repository...")

        repository = self.client.get_repository(

            owner,

            repository_name

        )

        print(

            "Repository Loaded :",

            repository.get(

                "full_name"

            )

        )

        # --------------------------------------------------
        # Get Pull Request
        # --------------------------------------------------

        print("\nLoading Pull Request...")

        pull_request = self.client.get_pull_request(

            owner,

            repository_name,

            pull_number

        )

        print(

            "Title :",

            pull_request.get(

                "title"

            )

        )

        print(

            "State :",

            pull_request.get(

                "state"

            )

        )

        print(

            "Merged:",

            pull_request.get(

                "merged"

            )

        )

        # --------------------------------------------------
        # Get Reviews
        # --------------------------------------------------

        print("\nLoading Reviews...")

        reviews = self.client.get_reviews(

            owner,

            repository_name,

            pull_number

        )

        print(

            "Reviews Loaded :",

            len(reviews)

        )

        # --------------------------------------------------
        # Get Comments
        # --------------------------------------------------

        print("\nLoading Comments...")

        comments = self.client.get_comments(

            owner,

            repository_name,

            pull_number

        )

        print(

            "Comments Loaded :",

            len(comments)

        )

        # --------------------------------------------------
        # Get Commits
        # --------------------------------------------------

        print("\nLoading Commits...")

        commits = self.client.get_commits(

            owner,

            repository_name,

            pull_number

        )

        print(

            "Commits Loaded :",

            len(commits)

        )

        # --------------------------------------------------
        # Get Changed Files
        # --------------------------------------------------

        print("\nLoading Changed Files...")

        changed_files = self.client.get_changed_files(

            owner,

            repository_name,

            pull_number

        )

        print(

            "Changed Files Loaded :",

            len(changed_files)

        )

        # --------------------------------------------------
        # Extract Features
        # --------------------------------------------------

        print("\nExtracting Features...")

        features = self.extractor.extract_features(

            repository=repository,

            pull_request=pull_request,

            reviews=reviews,

            comments=comments,

            commits=commits,

            changed_files=changed_files

        )

        # --------------------------------------------------
        # Final Result
        # --------------------------------------------------

        result = {

            "repository": repository,

            "pull_request": pull_request,

            "reviews": reviews,

            "comments": comments,

            "commits": commits,

            "changed_files": changed_files,

            "features": features

        }

        print("\n")

        print("=" * 70)
        print("GITHUB PULL REQUEST ANALYSIS COMPLETED")
        print("=" * 70)

        return result

    # ======================================================
    # Print Analysis
    # ======================================================

    def print_analysis(

        self,

        result

    ):

        repository = result["repository"]

        pull_request = result["pull_request"]

        features = result["features"]

        print("\n")
        print("=" * 70)
        print("GITHUB PULL REQUEST DATA")
        print("=" * 70)

        print(

            "\nRepository :",

            repository.get(

                "full_name"

            )

        )

        print(

            "PR Number  :",

            pull_request.get(

                "number"

            )

        )

        print(

            "Title      :",

            pull_request.get(

                "title"

            )

        )

        print(

            "State      :",

            pull_request.get(

                "state"

            )

        )

        print(

            "Merged     :",

            pull_request.get(

                "merged"

            )

        )

        print("\n")

        print("=" * 70)
        print("EXTRACTED ML FEATURES")
        print("=" * 70)

        for name, value in features.items():

            print(

                f"{name:<25}: {value}"

            )


# ==========================================================
# Test GitHub Service
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING GITHUB SERVICE")
    print("=" * 70)

    try:

        service = GitHubService()

        pr_url = input(

            "\nEnter GitHub Pull Request URL: "

        ).strip()

        result = service.analyze_pull_request(

            pr_url

        )

        service.print_analysis(

            result

        )

        print("\n")

        print("=" * 70)
        print("GITHUB SERVICE TEST COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\n")

        print("=" * 70)
        print("GITHUB SERVICE TEST FAILED")
        print("=" * 70)

        print(

            type(e).__name__,

            ":",

            str(e)

        )

        print("=" * 70)