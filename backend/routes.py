"""
==========================================================

FastAPI Routes

AI Pull Request Risk Predictor

==========================================================
"""
from backend.schemas import (
    PredictionRequest,
    GitHubPredictionRequest
)
from fastapi import APIRouter

from backend.services import PredictionService

from github.github_service import GitHubService

github_service = GitHubService()

from backend.schemas import (

    PredictionRequest,

    PredictionResponse,

    HealthResponse

)

# ==========================================================
# Create Router
# ==========================================================

router = APIRouter(

    prefix="/api",

    tags=["AI Pull Request Risk Predictor"]

)

# ==========================================================
# Initialize Service
# ==========================================================

service = PredictionService()
# ==========================================================
# Health Check
# ==========================================================

@router.get(

    "/health",

    response_model=HealthResponse

)

def health():

    return service.health()


# ==========================================================
# Get Latest Prediction
# ==========================================================

@router.get(

    "/prediction/latest"

)

def latest_prediction():

    return service.get_latest_prediction()


# ==========================================================
# Get Prediction History
# ==========================================================

@router.get(

    "/predictions"

)

def prediction_history():

    return service.get_prediction_history()
# ==========================================================
# Generate Prediction
# ==========================================================

@router.post(

    "/predict"

)

@router.post(

    "/predict"

)

def predict(

    request: PredictionRequest

):

    result = service.predict(

        request

    )

    return result


# ==========================================================
# GitHub Pull Request Prediction
# ==========================================================

@router.post("/predict/github")
def predict_github(

    request: GitHubPredictionRequest

):

    print("\n")
    print("=" * 70)
    print("GITHUB PREDICTION REQUEST")
    print("=" * 70)

    # ------------------------------------------------------
    # GitHub Service
    # ------------------------------------------------------

    github_service = GitHubService()

    # ------------------------------------------------------
    # Extract GitHub data and 22 features
    # ------------------------------------------------------

    github_result = (

        github_service.analyze_pull_request(

            request.pr_url

        )

    )

    features = github_result["features"]

    # ------------------------------------------------------
    # Prediction Service
    # ------------------------------------------------------

    service = PredictionService()

    result = service.predict_from_features(

        features

    )

    # ------------------------------------------------------
    # Add GitHub information to response
    # ------------------------------------------------------

    return {

        "success": True,

        "repository": (

            github_result["repository"]

            .get(

                "full_name"

            )

        ),

        "pull_request": {

            "number": (

                github_result["pull_request"]

                .get(

                    "number"

                )

            ),

            "title": (

                github_result["pull_request"]

                .get(

                    "title"

                )

            ),

            "state": (

                github_result["pull_request"]

                .get(

                    "state"

                )

            ),

            "merged": (

                github_result["pull_request"]

                .get(

                    "merged"

                )

            )

        },

        "features": features,

        "prediction": result

    }