"""
==========================================================

FastAPI Schemas

AI Pull Request Risk Predictor

==========================================================
"""

from typing import List

from pydantic import BaseModel


# ==========================================================
# Repository Information
# ==========================================================

class RepositorySchema(BaseModel):

    repository_name: str

    language: str

    stars: int

    forks: int

    license: str


# ==========================================================
# Pull Request Information
# ==========================================================

class PullRequestSchema(BaseModel):

    review_count: int

    comment_count: int

    commit_count: int

    files_changed: int

    additions: int

    deletions: int

    total_changes: int

    total_lines_changed: int

    merged: bool
# ==========================================================
# Prediction Information
# ==========================================================

class PredictionSchema(BaseModel):

    model_name: str

    label: str

    prediction_code: int

    risk_score: float

    confidence: float

    risk_level: str


# ==========================================================
# Feature Explanation
# ==========================================================

class FeatureSchema(BaseModel):

    feature: str

    value: float

    shap_value: float
# ==========================================================
# AI Explanation
# ==========================================================

class ExplanationSchema(BaseModel):

    top_features: List[FeatureSchema]

    ai_explanation: str

    recommendation: str


# ==========================================================
# Complete Response
# ==========================================================

class PredictionResponse(BaseModel):

    repository: RepositorySchema

    pull_request: PullRequestSchema

    prediction: PredictionSchema

    explanation: ExplanationSchema
# ==========================================================
# Health Response
# ==========================================================

class HealthResponse(BaseModel):

    status: str

    api: str

    database: str

    model: str
# ==========================================================
# Prediction Request
# ==========================================================

class PredictionRequest(BaseModel):

    language: int

    stars: int

    forks: int

    license: int

    review_count: int

    approved_reviews: int

    commented_reviews: int

    comment_count: int

    commit_count: int

    files_changed: int

    additions: int

    deletions: int

    total_changes: int

    total_lines_changed: int

    test_files: int

    high_risk_files: int

    review_time_hours: float

    created_year: int

    created_month: int

    created_day: int

    created_weekday: int

    merged: int
# ==========================================================
# GitHub Pull Request Prediction Request
# ==========================================================

class GitHubPredictionRequest(BaseModel):

    pr_url: str