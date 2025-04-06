from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# 🔐 Your Together API key and model
TOGETHER_API_KEY = "2b0cb3216fced71ce25a4f28fe37dbd82e6383dd24b20a7e4ab5047b0b485db7"
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# 📦 Input model for the request
class QueryInput(BaseModel):
    query: str
    assessment_name: str

# 🤖 Recommender logic
def recommend_assessments(query: QueryInput):
    prompt = f"""Given the following job description:

\"\"\"
{query.query}
\"\"\"

Evaluate the relevance of the assessment titled: "{query.assessment_name}"

Respond ONLY in the following JSON format:
{{
  "relevance_score": <integer from 1 to 10>,
  "explanation": "<short explanation>"
}}"""

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
                "temperature": 0.3,
                "stop": ["```"]
            }
        )

        response.raise_for_status()
        result = response.json()['choices'][0]['text'].strip()

        data = json.loads(result)
        return {
            "relevance_score": data["relevance_score"],
            "explanation": data["explanation"]
        }

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": response.text if 'response' in locals() else None
        }

# 🚀 FastAPI endpoint
@app.post("/recommend")
def get_recommendation(query: QueryInput):
    return recommend_assessments(query)