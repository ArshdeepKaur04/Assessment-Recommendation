from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import requests
import os

app = FastAPI()

# Replace with your Mixtral/Together API key
TOGETHER_API_KEY = "2b0cb3216fced71ce25a4f28fe37dbd82e6383dd24b20a7e4ab5047b0b485db7"

headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

mixtral_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

assessment_names = ["Global Skills Development Report",
    ".NET Framework 4.5",
    ".NET MVC (New)",
    ".NET MVVM (New)",
    "ASP.NET Core",
    "Azure DevOps",
    "Angular Development",
    "Agile Methodologies",
    "Team Collaboration Skills",
    "Software Architecture"]

# Request schema
class QueryRequest(BaseModel):
    job_description: str

# API root
@app.get("/")
def root():
    return {"message": "Assessment Recommendation API is running 🚀"}

# Endpoint for recommendations
@app.post("/recommend")
def recommend_assessments(request: QueryRequest):
    job_description = request.job_description
    results = []

    for assessment in assessment_names:
        prompt = f"""
        Job Description: {job_description}
        Assessment: {assessment}

        Evaluate the relevance of the above assessment for the given job description on a scale of 1 to 10.
        Respond ONLY in JSON format like this:
        {{
            "relevance_score": 8,
            "explanation": "Why this assessment is relevant or not."
        }}
        """

        try:
            response = requests.post(
                "https://api.together.xyz/v1/chat/completions",
                headers=headers,
                json={
                    "model": mixtral_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 512,
                    "top_p": 0.9
                }
            )

            # Check if the request failed
            if response.status_code != 200:
                raise Exception(f"API Error {response.status_code}: {response.text}")

            model_response = response.json()["choices"][0]["message"]["content"]

            result_json = eval(model_response) if model_response.strip().startswith("{") else {
                "relevance_score": 0,
                "explanation": "Invalid response format"
            }

        except Exception as e:
            print(f"Error for assessment '{assessment}': {str(e)}")
            result_json = {
                "relevance_score": 0,
                "explanation": f"Error: {str(e)}"
            }

        results.append({
            "assessment": assessment,
            "score": result_json["relevance_score"],
            "explanation": result_json["explanation"]
        })

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)[:10]
    return {"recommendations": sorted_results}