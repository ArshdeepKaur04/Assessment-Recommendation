from fastapi import FastAPI, Request
from pydantic import BaseModel
import pandas as pd
import requests
import json
from typing import List

app = FastAPI()

# Load your assessments CSV
df = pd.read_csv("assessment_explanations_output.csv")

TOGETHER_API_KEY = "2b0cb3216fced71ce25a4f28fe37dbd82e6383dd24b20a7e4ab5047b0b485db7"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

class QueryInput(BaseModel):
    query: str

@app.post("/evaluate")
def evaluate_assessments(query: QueryInput):
    results = []

    for _, row in df.iterrows():
        prompt = f"""
You are an expert in job analysis and assessment design.

Given the job description:
\"\"\"
{query.query}
\"\"\"

Evaluate the relevance of the following assessment:
Title: {row['Assessment Name']}
Test Type: {row['Test Type']}
Explanation: {row['Explanation']}

Respond with ONLY the following JSON:
{{
  "relevance_score": <integer from 1 to 10>,
  "explanation": "<short explanation>"
}}
"""

        try:
            response = requests.post(
                "https://api.together.xyz/v1/completions",
                headers={
                    "Authorization": f"Bearer {TOGETHER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "max_tokens": 256,
                    "temperature": 0.3
                }
            )
            response.raise_for_status()
            output = json.loads(response.json()['choices'][0]['text'].strip())

            results.append({
                "Assessment Name": row['Assessment Name'],
                "URL": row['URL'],
                "Remote Testing Support": row['Remote Testing Support'],
                "Adaptive/IRT Support": row['Adaptive/IRT Support'],
                "Duration": row['Duration'],
                "Test Type": row['Test Type'],
                "Explanation": output["explanation"],
                "Relevance Score": output["relevance_score"]
            })

        except Exception as e:
            results.append({
                "Assessment Name": row['Assessment Name'],
                "error": str(e)
            })

    # Sort and return top 10
    sorted_results = sorted(results, key=lambda x: x.get("Relevance Score", 0), reverse=True)
    return sorted_results[:10]