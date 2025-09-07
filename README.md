<h2>🗂️ Project Structure</h2>
<pre class="project-structure"><code>
rag_compliance_chatbot/
├── src/
│   ├── pdf_processing/       # PDF extraction & chunking
│   │   ├── extract_text.py   # Extracts text from PDFs (pdfplumber / PyPDF2 / OCR)
│   │   ├── chunk_text.py     # Splits text into structured chunks
│   ├── rag_pipeline/         # RAG pipeline & retrieval
│   │   ├── embeddings.py     # Embeddings generation via SentenceTransformers
│   │   ├── vector_store.py   # Builds FAISS index
│   │   ├── query_engine.py   # Enhances query, retrieves chunks, generates response
│   ├── compliance_analysis/  # Gap analysis & reporting
│   │   ├── report_generator.py # Generates compliance gap reports
│   ├── ui/                   # Streamlit UI
│   │   ├── streamlit_app.py
├── data/
│   ├── input/                # PDF input
│   │   ├── information_security_policy_v4.0.pdf
│   ├── knowledge_base/       # Indexed chunks
│   │   ├── index.faiss        # FAISS vector index
│   │   ├── chunks_structured.json
│   ├── mappings/             # Compliance mapping
│   │   ├── compliance_mapping.json
│   ├── reports/              # Generated gap reports
│   │   ├── gap_analysis_report.md
├── config/
│   ├── config.yaml           # Pipeline settings (chunk size, models, etc.)
│   ├── compliance_rules.json # Compliance rules mapping
├── tests/
│   ├── test_pdf_processing.py
│   ├── test_rag_pipeline.py
│   ├── test_compliance_analysis.py
├── requirements.txt
├── .gitignore                # Exclude .env, logs, virtualenv
└── README.md                 # This overview
</code></pre>

<hr>

<h2>🚀 Project Overview</h2>

<p><strong>RAG Compliance Chatbot</strong> is a Retrieval-Augmented Generation (RAG) system for analyzing text-based PDF policies (Information Security Policy v4.0) against <strong>PCI-DSS v3.2</strong> and <strong>ISO 27001:2013</strong>. It ingests PDFs, creates a knowledge base, retrieves relevant sections via semantic search, generates LLM-powered responses, and produces compliance gap reports.</p>

<ul>
  <li>PDF ingestion & chunking (~81k characters → 251 structured chunks)</li>
  <li>FAISS vector store for similarity search</li>
  <li>Groq LLM (llama-3.1-8b-instant) with Hugging Face fallback</li>
  <li>PCI-DSS & ISO 27001 compliance mapping</li>
  <li>Compliance gap report generation</li>
  <li>Streamlit UI for query and report display</li>
</ul>

<hr>

<h2>⚙️ Setup & Installation</h2>

<ol>
  <li><strong>Clone repository</strong>
    <pre><code>git clone https://github.com/your-org/rag_compliance_chatbot.git
cd rag_compliance_chatbot</code></pre>
  </li>
  <li><strong>Create virtual environment & activate</strong>
    <pre><code>python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate</code></pre>
  </li>
  <li><strong>Install dependencies</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Configure environment variables</strong> in <code>.env</code> (excluded from Git):
    <pre><code>GROQ_API_KEY=your_groq_api_key</code></pre>
  </li>
  <li><strong>Configure pipeline</strong> in <code>config/config.yaml</code>:
    <pre><code>pdf_processing:
  chunk_size: 500
  embedding_model: 'sentence-transformers/all-MiniLM-L6-v2'
llm:
  model: 'distilbert-base-uncased'
  groq_api_key_env: 'GROQ_API_KEY'
vector_store:
  index_path: 'data/knowledge_base/index.faiss'</code></pre>
  </li>
</ol>

<hr>

<h2>📄 PDF Processing & Knowledge Base</h2>

<ul>
  <li>Input: <code>information_security_policy_v4.0.pdf</code> (~81k characters)</li>
  <li>Extraction via <code>pdfplumber</code> / <code>PyPDF2</code> / OCR for scanned PDFs</li>
  <li>Chunking:
    <ul>
      <li>251 structured chunks (dictionary format: <code>{section, title, text}</code>)</li>
      <li>Each chunk used for semantic retrieval</li>
    </ul>
  </li>
</ul>

<pre><code>Total chunks: 251
1, Section 4.0: 68 words
2, Section 0: 7 words
3, Section 4.0: 18 words
...</code></pre>

<hr>

<h2>💾 FAISS Vector Store</h2>

<ul>
  <li>Embeddings: <code>SentenceTransformers('multi-qa-MiniLM-L6-cos-v1')</code></li>
  <li>Semantic search with FAISS for top-K chunks</li>
  <li>Deduplication ensures unique chunks in retrieval</li>
  <li>Enhances RAG LLM query response quality</li>
</ul>

<hr>

<h2>🤖 LLM Integration</h2>

<ul>
  <li>Primary: Groq LLM (<code>llama-3.1-8b-instant</code>)</li>
  <li>Fallback: Hugging Face QA (<code>distilbert-base-uncased-distilled-squad</code>)</li>
  <li>Query + retrieved chunks (truncated ~3000 tokens) → LLM generates concise, professional answers (100–150 words)</li>
  <li>Inferred responses flagged with <code>[INFERRED]</code> if context insufficient</li>
</ul>

<hr>

<h2>📝 Compliance Gap Analysis</h2>

<ul>
  <li>Compares retrieved policy sections against PCI-DSS & ISO 27001</li>
  <li>Generates Markdown report with:
    <ul>
      <li>Compliance status</li>
      <li>Missing clauses</li>
      <li>Audit priority & risk levels</li>
      <li>Fallback notes for inferred answers</li>
    </ul>
  </li>
</ul>

<hr>

<h2>🖥️ Streamlit UI</h2>

<ul>
  <li>Query with policy questions (e.g., “What are the access control policies?”)</li>
  <li>View responses + compliance gaps + audit priorities</li>
  <li>Export reports as Markdown</li>
  <li>Run: <code>streamlit run src/ui/streamlit_app.py</code></li>
</ul>

<hr>

<h2>🔧 Testing & Verification</h2>

<pre><code>pytest tests/unit/
pytest tests/integration/</code></pre>

<hr>

<h2>🚫 Files to Exclude (.gitignore)</h2>

<pre><code>.env
venv/
*.pyc
__pycache__/
data/reports/*
pipeline.log
</code></pre>

<hr>

<h2>🔐 Security & Privacy</h2>

<ul>
  <li>Environment variables store API keys (.env)</li>
  <li>User PDF data is processed locally; no sensitive data persisted</li>
  <li>Logs redact sensitive info</li>
</ul>

<hr>

<h2>📈 Performance & Roadmap</h2>

<ul>
  <li>Chunking + FAISS + LLM allows fast semantic retrieval</li>
  <li>Future improvements:
    <ul>
      <li>Multi-PDF ingestion</li>
      <li>Interactive PDF/Excel exports</li>
      <li>Fine-tuned compliance LLM</li>
      <li>Enhanced UI/UX with HTML/CSS</li>
    </ul>
  </li>
</ul>

<hr>

<h2>🙏 Acknowledgments</h2>

<p>Built with pdfplumber, PyPDF2, Tesseract OCR, SentenceTransformers, FAISS, Groq, Hugging Face, LangChain, Streamlit.</p>
