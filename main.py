import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn
from fastapi import FastAPI
from ragchallenge.api.api import app as api_app

# Create a main FastAPI app (wrapper) to add root route
main_app = FastAPI(title="RAG Challenge API")

# Include your existing API routes
main_app.mount("/", api_app)

# Optional: Add a friendly root endpoint to prevent 404
@main_app.get("/")
def read_root():
    return {
        "message": "✅ RAG Challenge API is running!",
        "docs": "Visit /docs for the interactive API documentation",
        "health": "Visit /health to check system status"
    }

if __name__ == '__main__':
    print("🔄 Initializing FastAPI server on http://0.0.0.0:8082 ...")
    uvicorn.run(
        main_app,
        host='0.0.0.0',
        port=8082,
        log_level='info'
    )
