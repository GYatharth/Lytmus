"""
Streamlit entrypoint: takes a user query, runs the pipeline, and displays
the answer with inline citations and per-claim confidence tags.
"""

import streamlit as st

st.set_page_config(page_title="Research Copilot", layout="wide")
st.title("Research Copilot")
st.caption("Search, synthesize, and see how much to trust each claim.")

query = st.text_input("Ask a research question")

if query:
    st.info("Pipeline not yet implemented — see PLAN.md for build status.")
