# streamlit_app.py ################################
import streamlit as st
from main import run_pipeline
import tempfile
#import pandas as pd
#:office:
st.set_page_config(page_title="AI  Job  Search Assistant", page_icon=":star2:", layout="wide")
st.title(":office: AI  Job  Search Assistant")
st.write("**Upload your resume and get AI-matched job recommendations with explanations.**")

# File uploader
uploaded_file = st.file_uploader("Upload Resume only in (PDF) :page_with_curl:",  type=["pdf"])

# Location input
location = st.text_input("Preferred Job Location", value="bangalore")

# Number of results
#top_n = st.slider("Number of jobs to explain", min_value=1, max_value=5, value=3)

if st.button("Find Jobs :mag:", type="primary"):
    if uploaded_file is None:
        st.warning("Please upload a resume first.")
    else:
        with st.spinner("Processing your resume and searching for jobs..."):
            # Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            try:
                print("Try")
                jobs, explanations = run_pipeline(
                    file_path=temp_path,
                    location=location
                   #top_n=top_n
                )

                #st.success(f"Found {len(jobs)} jobs. Showing top {top_n} matches.")
                st.success(f"Found {len(jobs)} jobs. ")

                for job, exp in zip(jobs, explanations):
                    st.subheader(job.title)
                    st.write(f"Company: {job.company}")
                    st.write(f"Location: {job.location}")
                    st.markdown(f"[Apply Here]({job.url})")

                    st.write("This job matches you because:")
                    st.markdown(exp)
                   
            except Exception as e:
                st.error(f"An error occurred: {e}")
