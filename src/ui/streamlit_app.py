import sys
import os
from pathlib import Path

# ✅ Ensure project root is in sys.path so "src" can be imported
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from src.rag_pipeline.query_engine import query_knowledge_base

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Compliance Chatbot", page_icon="🔒")
st.title("🔒 Compliance Chatbot")
st.write("Query the Information Security Policy for **PCI-DSS** and **ISO 27001** compliance.")

# Initialize session state for query history
if "query_history" not in st.session_state:
    st.session_state.query_history = []

# Query input box
query = st.text_input("Enter your query:", placeholder="e.g., What are the access control policies?")

# Submit button
if st.button("Submit Query", disabled=not query):
    if query:
        response = query_knowledge_base(query)
        st.session_state.query_history.append({"query": query, "response": response})
        st.success("✅ Query processed!")
        st.write("### Response:")
        st.write(response)
    else:
        st.error("⚠️ Please enter a query.")

# Display query history
if st.session_state.query_history:
    st.subheader("📜 Query History")
    for item in st.session_state.query_history[::-1]:  # newest first
        with st.expander(f"🔍 Query: {item['query']}"):
            st.write(f"**Response:** {item['response']}")

# Show compliance report if available
# Fixed code (correct path)
report_path = Path("data/output/compliance_report.md")
if report_path.exists():
    with open(report_path, 'r', encoding='utf-8') as f:
        report_content = f.read()
    with st.expander("📑 Compliance Gap Analysis Report", expanded=False):
        st.markdown(report_content)
else:
    st.warning("⚠️ Compliance report not found. Run `report_generator.py` to generate it.")
