Developer Guide for RAG Compliance Chatbot
Overview
The RAG Compliance Chatbot is a Python-based project designed to ingest text-based PDF policy documents, create a structured knowledge base, perform semantic searches, and generate compliance gap analysis reports for PCI-DSS v3.2 and ISO 27001:2013 standards. It uses a Retrieval-Augmented Generation (RAG) pipeline with FAISS for vector search, SentenceTransformers for embeddings, Groq's llama-3.1-8b-instant for LLM responses, and Hugging Face's distilbert-base-uncased-distilled-squad as a fallback. The project includes a Streamlit UI for querying and displaying reports, with all components in the provided structure.
Project Structure

requirements.txt: Dependencies (e.g., pdfplumber, sentence-transformers, langchain-groq).
.gitignore: Excludes .env, data/knowledge_base/, venv/, etc.
README.md: Project overview (generated below).
src/pdf_processing/: PDF extraction and chunking.
extract_text.py: Extracts text from PDF using pdfplumber/PyPDF2/OCR fallback.
chunk_text.py: Splits text into chunks (~500 words) with metadata (section, title).


src/rag_pipeline/: RAG core.
embeddings.py: Generates embeddings using SentenceTransformer.
vector_store.py: Builds FAISS index from chunks.
query_engine.py: Enhances queries, retrieves chunks, generates responses with Groq/Hugging Face.


src/compliance_analysis/: Gap analysis and reporting.
mapping.py: Loads compliance_mapping.json (manual in Day 1, optional automation).
report_generator.py: Generates gap_analysis_report.md with queries, status, gaps.


src/ui/: Minimal UI.
streamlit_app.py: Streamlit interface for querying and report display.


data/input/: PDF input (e.g., information_security_policy_v4.0.pdf).
data/knowledge_base/: Indexed chunks ( index.faiss, chunks_structured.json).
data/mappings/: compliance_mapping.json for PCI-DSS/ISO 27001 mappings.
data/reports/: gap_analysis_report.md output.
docs/: Guides (user/developer).
tests/: Unit tests (optional, not covered).
config/: config.yaml (chunk size, etc.), compliance_rules.json (rules).

Setup and Installation

Clone the repository: git clone <repo-url>.
Create virtual environment: python -m venv venv; venv\Scripts\activate.
Install dependencies: pip install -r requirements.txt.
Add .env: GROQ_API_KEY=your_key.
Run Day 2 pipeline: python src\pdf_processing\extract_text.py, chunk_text.py, src\rag_pipeline\vector_store.py.
Generate report: python -m src.compliance_analysis.report_generator.
Run UI: streamlit run src\ui\streamlit_app.py.

Development Workflow

PDF Ingestion: Run extract_text.py for text extraction (supports OCR for scanned PDFs). chunk_text.py splits into 26 chunks with section metadata.
Knowledge Base: vector_store.py generates embeddings (multi-qa-MiniLM-L6-cos-v1) and FAISS index.
Querying: query_engine.py enhances queries (keywords/sections), retrieves chunks, uses Groq for responses, Hugging Face fallback.
Report: report_generator.py queries predefined topics, analyzes gaps using compliance_mapping.json, assigns risks, generates Markdown report.
UI: streamlit_app.py provides input, history, response display, report viewer.

Troubleshooting Retrieval Issues

Issue: Incorrect sections (e.g., 4.22 for encryption instead of 4.34).
Fix: Verify chunks_structured.json for sections using findstr /C:"4.34" data\knowledge_base\chunks_structured.json. Re-run Day 2 if missing.
Debug: Log retrieved sections in query_engine.py (already included). Test with python -c "from src.rag_pipeline.query_engine import retrieve_chunks; print(retrieve_chunks('How does the policy address encryption?', 'data/knowledge_base/index.faiss', 'data/knowledge_base/chunks_structured.json', top_k=3))".
Enhancement: Add more mappings to compliance_mapping.json for new queries (e.g., 4.5 for password management).

Maintenance

Update compliance_mapping.json for new standards.
Re-run Day 2 for new PDFs.
Monitor Groq API credits; fallback to Hugging Face if needed.
Expand UI for advanced features (e.g., file upload for new PDFs).
