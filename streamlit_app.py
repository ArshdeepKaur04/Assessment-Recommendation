import streamlit as st
import requests

st.set_page_config(page_title="Assessment Recommendation", layout="centered")

st.title("🧠 Assessment Recommendation Engine")
st.write("Enter a job description to get recommended assessments.")

job_description = st.text_area("Job Description", height=200)

if st.button("Get Recommendations"):
    if job_description.strip():
        with st.spinner("Querying API..."):
            try:
                response = requests.post(
                    "https://assessment-recommendation.onrender.com/evaluate",
                    json={"job_description": job_description},
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("Recommended Assessments:")
                    for i, rec in enumerate(result["recommended_assessments"], 1):
                        st.markdown(f"**{i}. {rec}**")
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a job description.")