<h2>🛠️ Developer Guide: RAG Compliance Chatbot</h2>

<h3>Overview</h3>
<p>The <strong>RAG Compliance Chatbot</strong> is a Python-based system that ingests text-based PDF policy documents, creates a structured knowledge base, performs semantic searches, and generates compliance gap reports for <strong>PCI-DSS v3.2</strong> and <strong>ISO 27001:2013</strong> standards. It uses a Retrieval-Augmented Generation (RAG) pipeline with:</p>

<ul>
  <li>FAISS for vector search</li>
  <li>SentenceTransformers for embeddings</li>
  <li>Groq LLM (<code>llama-3.1-8b-instant</code>) for responses</li>
  <li>Hugging Face fallback (<code>distilbert-base-uncased-distilled-squad</code>)</li>
  <li>Streamlit UI for querying and report visualization</li>
</ul>

<p>All configuration and compliance rules are now fully <strong>hardcoded</strong> in the scripts.</p>

<hr>

<h3>Project Structure</h3>
<pre class="project-structure"><code>
rag_compliance_chatbot/
├── src/pdf_processing/
│   ├── extract_text.py     # Extracts text from PDFs (pdfplumber/PyPDF2/OCR fallback)
│   └── chunk_text.py       # Splits text into structured chunks (~26 large / ~162 small)
├── src/rag_pipeline/
│   ├── embeddings.py       # Embeddings generation (SentenceTransformers)
│   ├── vector_store.py     # Builds FAISS index
│   └── query_engine.py     # Enhances queries, retrieves chunks, generates responses (Groq/Hugging Face)
├── src/compliance_analysis/
│   ├── gap_analysis.py     # Compares retrieved chunks to PCI-DSS/ISO 27001 mappings
│   └── report_generator.py # Generates <code>gap_analysis_report.md</code>
├── src/ui/
│   └── streamlit_app.py    # Streamlit interface for queries and report display
├── data/
│   ├── input/              # Input PDF(s)
│   │   └── information_security_policy_v4.0.pdf
│   ├── knowledge_base/     # Indexed chunks
│   │   ├── index.faiss
│   │   ├── chunks_structured.json
│   │   └── chunks.json      # legacy
│   ├── mappings/
│   │   └── compliance_mapping.json
│   └── reports/
│       └── gap_analysis_report.md
├── docs/
│   ├── user_guide.md
│   └── developer_guide.md
├── requirements.txt
├── .gitignore
└── README.md
</code></pre>

<hr>

<h3>Setup & Installation</h3>
<ol>
  <li><strong>Clone repository:</strong>
    <pre><code>git clone &lt;repo-url&gt;
cd rag_compliance_chatbot</code></pre>
  </li>
  <li><strong>Create virtual environment & activate:</strong>
    <pre><code>python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate</code></pre>
  </li>
  <li><strong>Install dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Configure environment variables (.env):</strong>
    <pre><code>GROQ_API_KEY=your_groq_api_key</code></pre>
  </li>
  <li><strong>Run pipeline:</strong>
    <pre><code>python src/pdf_processing/extract_text.py
python src/pdf_processing/chunk_text.py
python src/rag_pipeline/vector_store.py</code></pre>
  </li>
  <li><strong>Generate report:</strong>
    <pre><code>python -m src.compliance_analysis.report_generator</code></pre>
  </li>
  <li><strong>Run UI:</strong>
    <pre><code>streamlit run src/ui/streamlit_app.py</code></pre>
  </li>
</ol>

<hr>

<h3>Development Workflow</h3>
<ul>
  <li><strong>PDF Ingestion:</strong> extract_text.py extracts text (OCR fallback for scanned PDFs). chunk_text.py splits into structured chunks with metadata (<code>section, title, text</code>).</li>
  <li><strong>Knowledge Base:</strong> vector_store.py generates embeddings and FAISS index (~26 large / 162 small chunks).</li>
  <li><strong>Querying:</strong> query_engine.py enhances queries, retrieves top-K relevant chunks, uses Groq LLM for responses with Hugging Face fallback.</li>
  <li><strong>Report Generation:</strong> report_generator.py queries predefined topics, analyzes gaps using compliance_mapping.json, assigns risk levels, outputs Markdown report.</li>
  <li><strong>UI:</strong> streamlit_app.py provides input, query history, response display, and report viewer.</li>
</ul>

<hr>

<h3>Troubleshooting Retrieval Issues</h3>
<ul>
  <li><strong>Incorrect sections:</strong> e.g., encryption returned as 4.22 instead of 4.34. Verify <code>chunks_structured.json</code> using:
    <pre><code>findstr /C:"4.34" data\knowledge_base\chunks_structured.json</code></pre>
  </li>
  <li><strong>Debug:</strong> Log retrieved chunks in query_engine.py. Test retrieval with:
    <pre><code>python -c "from src.rag_pipeline.query_engine import retrieve_chunks; print(retrieve_chunks('How does the policy address encryption?', 'data/knowledge_base/index.faiss', 'data/knowledge_base/chunks_structured.json', top_k=3))"</code></pre>
  </li>
  <li><strong>Enhancement:</strong> Add more mappings to compliance_mapping.json for new queries (e.g., 4.5 for password management).</li>
</ul>

<hr>

<h3>Maintenance</h3>
<ul>
  <li>Update <code>compliance_mapping.json</code> for new standards or clauses.</li>
  <li>Re-run the pipeline for new PDFs (extract → chunk → index → report).</li>
  <li>Monitor Groq API usage; fallback to Hugging Face when necessary.</li>
  <li>Expand UI for advanced features (file upload for new PDFs, filtering, or export options).</li>
</ul>
