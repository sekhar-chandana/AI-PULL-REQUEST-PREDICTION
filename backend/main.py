"""
==========================================================

AI Pull Request Risk Predictor

FastAPI Main Application

==========================================================
"""

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


# ==========================================================
# Create FastAPI Application
# ==========================================================

app = FastAPI(

    title="AI Pull Request Risk Predictor",

    description="Explainable AI for GitHub Pull Request Risk Prediction",

    version="1.0.0"

)


# ==========================================================
# Enable CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# ==========================================================
# Include API Routes
# ==========================================================

app.include_router(

    router

)
# ==========================================================
# Root Endpoint
# ==========================================================

@app.get(

    "/"

)

def home():

    return {

        "project": "AI Pull Request Risk Predictor",

        "version": "1.0.0",

        "status": "Running"

    }


# ==========================================================
# Health Check
# ==========================================================

@app.get(

    "/health"

)

def health():

    return {

        "status": "Healthy",

        "api": "Running",

        "database": "Connected",

        "model": "Loaded"

    }
# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "backend.main:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )