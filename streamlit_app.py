import streamlit as st
import requests

st.set_page_config(page_title="Assessment Recommendation", layout="centered")

st.title("🧠 Assessment Recommendation Engine")
st.write("Enter a job description to get relevant SHL assessments.")

job_description = st.text_area("Job Description", height=200)

if st.button("Get Recommendation"):
    if not job_description:
        st.warning("Please enter a job description.")
    else:
        try:
            API_URL = "https://assessment-recommendation.onrender.com/evaluate"
            response = requests.post(API_URL, json={"query": job_description})

            if response.status_code == 200:
                data = response.json()
                st.success("Recommended Assessment")

                st.write("**Assessment Name:**", data["assessment_name"])
                st.markdown(f"**URL:** [Click here]({data['url']})")
                st.write("**Remote Testing Support:**", data["remote_testing_support"])
                st.write("**Adaptive/IRT Support:**", data["adaptive_irt_support"])
                st.write("**Duration:**", data["duration"])
                st.write("**Test Type:**", data["test_type"])
                st.write("**Explanation:**", data["explanation"])
            else:
                st.error(f"API Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")