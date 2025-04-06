# 🧠 SHL Assessment Recommendation Engine
A smart recommendation system that analyzes a job description and recommends the 10 most relevant SHL individual assessment tests using an LLM-powered backend (Mixtral via Together API).

## Features:
- Accepts job description input (via API or Streamlit UI)
- Evaluates relevance of SHL assessments from a CSV dataset
- Uses Mixtral (via Together API) to generate relevance scores and explanations
- Ranks and returns the top 10 most relevant assessments
- Fully deployable as a public API (FastAPI + Render)
- Optional Streamlit UI for interactive demo

## Demo:
- Live API: https://your-api-url.onrender.com/recommend
- Streamlit App: https://your-streamlit-app-url.streamlit.app

### Endpoint: `/recommend`
**Method**: `POST`

**Request Body (JSON)**:
```json
{
  "job_description": "Senior .NET Developer with Azure DevOps and Angular experience"
}
