import streamlit as st
import requests

st.set_page_config(page_title="Assessment Recommendation", layout="centered")

st.title("🧠 Assessment Recommendation Engine")
st.write("Enter a job description and an assessment name to get a relevance score.")

# User inputs
job_description = st.text_area("Job Description", height=200)
assessment_name = st.text_input("Assessment Name", placeholder="e.g., Critical Thinking Test")

# Trigger recommendation
if st.button("Get Recommendation"):
    if not job_description or not assessment_name:
        st.warning("Please fill in both fields.")
    else:
        try:
            API_URL = "https://assessment-recommendation.onrender.com/recommend"
            payload = {
                "query": job_description,
                "assessment_name": assessment_name
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success("✅ Recommendation received!")
                st.write("**Relevance Score:**", data.get("relevance_score", "N/A"))
                st.write("**Explanation:**", data.get("explanation", "No explanation provided."))
            else:
                st.error(f"❌ API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
