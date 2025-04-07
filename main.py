from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from recommender import recommend_assessments
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def get_recommendations(query: str = Query(..., description="Enter your search query")):
    results = recommend_assessments(query)
    return results.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
