import pandas as pd
import re

# Load the dataset
df = pd.read_csv("assessment_explanations_output.csv")

def recommend_assessments(query, top_k=5):
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    def match_score(row):
        name_score = bool(pattern.search(str(row['Assessment Name'])))
        explanation_score = bool(pattern.search(str(row['Explanation'])))
        return name_score + explanation_score

    df['score'] = df.apply(match_score, axis=1)
    results = df[df['score'] > 0].sort_values(by='score', ascending=False).head(top_k)
    return results.drop(columns=['score'])