import streamlit as st
from recommender import recommend_assessments

st.title("🔍 SHL Assessment Recommender")

query = st.text_input("Enter a job role, skill, or keyword to find assessments")

if query:
    results = recommend_assessments(query)
    if not results.empty:
        st.success(f"Found {len(results)} matching assessments:")
        for _, row in results.iterrows():
            st.markdown(f"### [{row['Assessment Name']}]({row['URL']})")
            st.markdown(f"**Explanation:** {row['Explanation']}")
            st.markdown("---")
    else:
        st.warning("No matching assessments found. Try a different keyword.")