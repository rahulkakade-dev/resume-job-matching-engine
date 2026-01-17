import streamlit as st
import requests

st.title("Resume ↔ Job Matching Engine")

resume_text = st.text_area("Paste your resume text")

if st.button("Find Matching Jobs"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/match",
            json={"resume_text": resume_text},
            timeout=30
        )
        results = response.json()

        for job in results:
            st.write(f"### {job['job_title']}")
            st.write(f"Company: {job['company']}")
            st.write(f"Score: {job['score']}")
            st.markdown("---")

    except Exception as e:
        st.error(f"Backend not reachable: {e}")
