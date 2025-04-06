import streamlit as st
import requests

# 🔁 Replace with your deployed API endpoint once it's live
API_URL = "https://your-api-url.onrender.com/recommend"  # Example placeholder

st.set_page_config(page_title="SHL Assessment Recommendation", layout="centered")

st.title("🧠 SHL Assessment Recommendation Engine")
st.markdown("This tool suggests the **most relevant SHL assessments** based on your job description or query.")
st.markdown("---")

# Input box for job description
job_description = st.text_area("📝 Enter Job Description or Role Requirements:")

# Submit button
if st.button("🔍 Get Recommendations"):
    if not job_description.strip():
        st.warning("Please enter a job description or query.")
    else:
        with st.spinner("Analyzing and generating recommendations..."):
            try:
                response = requests.post(API_URL, json={"job_description": job_description})
                if response.status_code == 200:
                    data = response.json()
                    recommendations = data.get("recommendations", [])
                    
                    if recommendations:
                        st.success("✅ Top 10 Recommended Assessments:")
                        for idx, rec in enumerate(recommendations, 1):
                            st.markdown(f"**{idx}. {rec['assessment']}**")
                            st.markdown(f"- **Relevance Score:** {rec['score']}/10")
                            st.markdown(f"- **Why:** {rec['explanation']}")
                            st.markdown("---")
                    else:
                        st.info("No recommendations found for the given input.")
                else:
                    st.error(f"❌ API Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"⚠️ Failed to connect to API: {e}")

st.markdown("----")
st.caption("Built with ❤️ using Streamlit and Mixtral (Together.ai)")
