User Guide for RAG Compliance Chatbot
Introduction
The RAG Compliance Chatbot is a tool designed to analyze the Bank's Information Security Policy v4.0 against PCI-DSS v3.2 and ISO 27001:2013 standards. It ingests the policy PDF, creates a knowledge base with 26 structured chunks, performs semantic searches, and generates responses with compliance details. The minimal UI (Streamlit) allows users to query the policy and view the compliance gap analysis report.
This guide explains how to use the chatbot, interpret responses, and troubleshoot common issues.
Prerequisites

Python 3.10+ installed.
Dependencies from requirements.txt installed (pip install -r requirements.txt).
.env file with GROQ_API_KEY=your_key.
Policy PDF at data/input/information_security_policy_v4.0.pdf.
Knowledge base generated (run Day 2 scripts: python src/pdf_processing/extract_text.py, chunk_text.py, src/rag_pipeline/vector_store.py).
Report generated (run Day 4: python -m src.compliance_analysis.report_generator).

Running the Chatbot

Navigate to project directory: cd C:\Users\Admin\Desktop\rag_compliance_chatbot.
Activate virtual environment: venv\Scripts\activate.
Run the UI: streamlit run src/ui/streamlit_app.py.
Access the UI: Open http://localhost:8501 in a browser.

Using the Chatbot
Querying the Policy

Enter Query: Type a query in the input field (e.g., "How are passwords managed?").
Submit: Click "Submit Query".
Response: The chatbot displays a response (~100–150 words) with policy details, compliance status, and inferred content if sections are missing.
History: Previous queries and responses are listed below.
Report: Expand "Compliance Gap Analysis Report" to view the pre-generated report with queries, sections, responses, status, priority, and gaps.

Example Queries

"What are the access control policies?" (Section 4.4, compliant with PCI-DSS 8.1.6, gaps in 8.1.7).
"How does the policy address encryption?" (Section 4.34, partial compliance, gaps in PCI-DSS 3.6.4).
"What are the vulnerability management procedures?" (Section 4.16, partial compliance, gaps in PCI-DSS 11.2).
"What is the incident response plan?" (Section 4.33, compliant, no gaps).
"How are passwords managed?" (Section 4.5, partial compliance, gaps in PCI-DSS 8.3).

Interpreting Responses

Policy Section: The referenced section (e.g., 4.5).
Response: Policy summary or inferred if missing.
Compliance Status: Compliant, Partial, Non-Compliant.
Audit Priority: High, Medium, Low.
Gaps: Specific missing clauses (e.g., PCI-DSS 8.1.7: Missing lockout duration).

Troubleshooting

Inferred Responses: Indicates missing sections in chunks_structured.json. Re-run Day 2 pipeline.
No Report: Run python -m src.compliance_analysis.report_generator.
Errors: Check logs for Groq/Hugging Face issues; ensure .env key is valid.
Inaccurate Sections: Verify chunks_structured.json for sections like 4.5, 4.34 (use findstr /C:"4.34" data\knowledge_base\chunks_structured.json).

Advanced Usage

Update Policy: Replace PDF and re-run Day 2 scripts.
Custom Queries: Use UI for queries beyond report (e.g., "How is supplier risk managed?").
Export Report: Copy from UI or open data/reports/gap_analysis_report.md.

Support
For issues, contact the developer or review developer_guide.md.