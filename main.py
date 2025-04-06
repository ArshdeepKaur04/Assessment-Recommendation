from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

class InputData(BaseModel):
    query: str

# Allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    job_description: str

@app.post("/recommend")
def recommend_assessments(req: JobRequest):
    # Dummy response logic
    return {
        "recommended_assessments": [
            "Cognitive Ability Test",
            "Personality Assessment",
            "Technical Skills Test"
        ]
    }

@app.post("/evaluate")
def evaluate_query(data: InputData):
    # Dummy logic for now
    return {
        "query": data.query,
        "relevance_score": 8,
        "explanation": "This is a mock explanation based on the input."
    }