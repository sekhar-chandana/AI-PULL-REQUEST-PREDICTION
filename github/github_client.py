"""
==========================================================

GitHub API Client

AI Pull Request Risk Predictor

==========================================================
"""

import os
import re
import requests


# ==========================================================
# GitHub Client
# ==========================================================

class GitHubClient:

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(

        self,

        token=None

    ):

        print("=" * 70)
        print("INITIALIZING GITHUB CLIENT")
        print("=" * 70)

        # --------------------------------------------------
        # Get GitHub Token
        # --------------------------------------------------

        self.token = (

            token

            or os.getenv(

                "GITHUB_TOKEN"

            )

        )

        # --------------------------------------------------
        # GitHub API Base URL
        # --------------------------------------------------

        self.base_url = (

            "https://api.github.com"

        )

        # --------------------------------------------------
        # HTTP Session
        # --------------------------------------------------

        self.session = requests.Session()

        # --------------------------------------------------
        # Headers
        # --------------------------------------------------

        self.session.headers.update({

            "Accept":
                "application/vnd.github+json",

            "X-GitHub-Api-Version":
                "2022-11-28"

        })

        if self.token:

            self.session.headers.update({

                "Authorization":
                    f"Bearer {self.token}"

            })

            print(

                "GitHub Token Loaded"

            )

        else:

            print(

                "GitHub Token Not Provided"

            )

            print(

                "Using public GitHub API access"

            )

        print(

            "GitHub Client Ready"

        )

    # ======================================================
    # Parse Pull Request URL
    # ======================================================

    def parse_pr_url(

        self,

        pr_url

    ):

        if not pr_url:

            raise ValueError(

                "Pull Request URL cannot be empty."

            )

        pattern = (

            r"^https?://github\.com/"

            r"([^/]+)/"

            r"([^/]+)/"

            r"pull/"

            r"(\d+)"

            r"/?$"

        )

        match = re.match(

            pattern,

            pr_url.strip()

        )

        if not match:

            raise ValueError(

                "Invalid GitHub Pull Request URL. "

                "Expected format: "

                "https://github.com/owner/repository/pull/123"

            )

        owner = match.group(1)

        repository = match.group(2)

        pull_number = int(

            match.group(3)

        )

        return {

            "owner": owner,

            "repository": repository,

            "pull_number": pull_number

        }

    # ======================================================
    # Generic GET Request
    # ======================================================

    def get(

        self,

        endpoint,

        params=None

    ):

        url = (

            self.base_url

            + endpoint

        )

        response = self.session.get(

            url,

            params=params,

            timeout=30

        )

        if response.status_code != 200:

            raise RuntimeError(

                f"GitHub API request failed: "

                f"{response.status_code} - "

                f"{response.text}"

            )

        return response.json()

    # ======================================================
    # Get Repository
    # ======================================================

    def get_repository(

        self,

        owner,

        repository

    ):

        endpoint = (

            f"/repos/{owner}/{repository}"

        )

        return self.get(

            endpoint

        )

    # ======================================================
    # Get Pull Request
    # ======================================================

    def get_pull_request(

        self,

        owner,

        repository,

        pull_number

    ):

        endpoint = (

            f"/repos/"

            f"{owner}/"

            f"{repository}/"

            f"pulls/"

            f"{pull_number}"

        )

        return self.get(

            endpoint

        )

    # ======================================================
    # Get Pull Request Reviews
    # ======================================================

    def get_reviews(

        self,

        owner,

        repository,

        pull_number

    ):

        endpoint = (

            f"/repos/"

            f"{owner}/"

            f"{repository}/"

            f"pulls/"

            f"{pull_number}/reviews"

        )

        return self.get(

            endpoint,

            params={

                "per_page": 100

            }

        )

    # ======================================================
    # Get Pull Request Comments
    # ======================================================

    def get_comments(

        self,

        owner,

        repository,

        pull_number

    ):

        endpoint = (

            f"/repos/"

            f"{owner}/"

            f"{repository}/"

            f"issues/"

            f"{pull_number}/comments"

        )

        return self.get(

            endpoint,

            params={

                "per_page": 100

            }

        )

    # ======================================================
    # Get Pull Request Commits
    # ======================================================

    def get_commits(

        self,

        owner,

        repository,

        pull_number

    ):

        endpoint = (

            f"/repos/"

            f"{owner}/"

            f"{repository}/"

            f"pulls/"

            f"{pull_number}/commits"

        )

        return self.get(

            endpoint,

            params={

                "per_page": 100

            }

        )

    # ======================================================
    # Get Changed Files
    # ======================================================

    def get_changed_files(

        self,

        owner,

        repository,

        pull_number

    ):

        endpoint = (

            f"/repos/"

            f"{owner}/"

            f"{repository}/"

            f"pulls/"

            f"{pull_number}/files"

        )

        return self.get(

            endpoint,

            params={

                "per_page": 100

            }

        )


# ==========================================================
# Test GitHub Client
# ==========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("TESTING GITHUB CLIENT")
    print("=" * 70)

    try:

        client = GitHubClient()

        test_url = input(

            "\nEnter GitHub Pull Request URL: "

        ).strip()

        parsed = client.parse_pr_url(

            test_url

        )

        print("\nParsed Pull Request")

        print("-" * 70)

        print(

            "Owner      :",

            parsed["owner"]

        )

        print(

            "Repository :",

            parsed["repository"]

        )

        print(

            "PR Number  :",

            parsed["pull_number"]

        )

        repository = client.get_repository(

            parsed["owner"],

            parsed["repository"]

        )

        print("\nRepository Loaded")

        print(

            "Name :",

            repository.get("full_name")

        )

        pull_request = client.get_pull_request(

            parsed["owner"],

            parsed["repository"],

            parsed["pull_number"]

        )

        print("\nPull Request Loaded")

        print(

            "Title :",

            pull_request.get("title")

        )

        print(

            "State :",

            pull_request.get("state")

        )

        print(

            "Merged:",

            pull_request.get("merged")

        )

        print("\n")

        print("=" * 70)

        print("GITHUB CLIENT TEST COMPLETED")

        print("=" * 70)

    except Exception as e:

        print("\n")

        print("=" * 70)

        print("GITHUB CLIENT TEST FAILED")

        print("=" * 70)

        print(

            type(e).__name__,

            ":",

            str(e)

        )

        print("=" * 70)