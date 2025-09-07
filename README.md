<h2>🗂️ Project Structure</h2>
<pre class="project-structure"><code>
rag_compliance_chatbot/
├── src/
│   ├── pdf_processing/         # PDF extraction & chunking
│   │   ├── extract_text.py     # Extracts text from PDFs (~81k words, pdfplumber / PyPDF2 / OCR)
│   │   └── chunk_text.py       # Splits text into structured chunks (~26 large / ~162 small)
│   ├── rag_pipeline/           # RAG retrieval & LLM integration
│   │   ├── embeddings.py       # Embeddings via SentenceTransformers('multi-qa-MiniLM-L6-cos-v1')
│   │   ├── vector_store.py     # Builds FAISS vector index
│   │   └── query_engine.py     # Query enhancement & LLM response generation
│   ├── compliance_analysis/    # Gap analysis & reporting
│   │   ├── gap_analysis.py     # Compares chunks against PCI-DSS/ISO 27001
│   │   └── report_generator.py # Generates gap_analysis_report.md
│   └── ui/                     # Streamlit UI
│       └── streamlit_app.py    # Query & report interface
├── data/
│   ├── input/                  # Input PDF
│   │   └── information_security_policy_v4.0.pdf
│   ├── knowledge_base/         # Indexed chunks
│   │   ├── index.faiss
│   │   ├── chunks_structured.json
│   │   └── chunks.json          # legacy
│   ├── mappings/               # Compliance mappings
│   │   └── compliance_mapping.json
│   └── reports/                # Generated reports
│       └── gap_analysis_report.md
├── docs/                       # Documentation
│   ├── user_guide.md           # Instructions for end users
│   └── developer_guide.md      # Setup, workflow, troubleshooting
├── requirements.txt
├── .gitignore                  # Exclude .env, logs, virtualenv
└── README.md
</code></pre>

<hr>

<h2>🚀 Project Overview</h2>
<p><strong>RAG Compliance Chatbot</strong> is a fully hardcoded Retrieval-Augmented Generation system for analyzing text-based PDF policies (~81,000 words) against <strong>PCI-DSS v3.2</strong> and <strong>ISO 27001:2013</strong>. It ingests PDFs, creates a semantic knowledge base, retrieves relevant sections, generates LLM-powered answers, and produces compliance gap reports.</p>

<ul>
  <li>PDF ingestion & chunking (~26 large / ~162 small chunks)</li>
  <li>FAISS vector store for similarity search</li>
  <li>LLM Integration: Groq (llama-3.1-8b-instant) with Hugging Face fallback (distilbert-base-uncased-distilled-squad)</li>
  <li>PCI-DSS & ISO 27001 compliance mapping (hardcoded in scripts)</li>
  <li>Gap analysis report generation (Markdown)</li>
  <li>Streamlit UI for interactive queries & reports</li>
</ul>

<hr>

<h2>⚙️ Setup & Installation</h2>
<ol>
  <li><strong>Clone repository</strong>
    <pre><code>git clone https://github.com/your-org/rag_compliance_chatbot.git
cd rag_compliance_chatbot</code></pre>
  </li>
  <li><strong>Create & activate virtual environment</strong>
    <pre><code>python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate</code></pre>
  </li>
  <li><strong>Install dependencies</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Configure environment variables</strong> in <code>.env</code> (excluded from Git)
    <pre><code>GROQ_API_KEY=your_groq_api_key</code></pre>
  </li>
</ol>

<hr>

<h2>📄 PDF Processing & Knowledge Base</h2>
<ul>
  <li>Input: <code>information_security_policy_v4.0.pdf</code> (~81k words)</li>
  <li>Extraction via <code>pdfplumber</code>, <code>PyPDF2</code>, OCR fallback</li>
  <li>Chunking:
    <ul>
      <li>26 large chunks (~3115 words each) or 162 small chunks (~500 words)</li>
      <li>Each chunk contains <code>{section, title, text}</code> for semantic retrieval</li>
    </ul>
  </li>
</ul>

<pre><code>Total chunks example:
1, Section 4.0: 3115 words
2, Section 4.1: 3050 words
3, Section 4.2: 3120 words
...
</code></pre>

<hr>

<h2>💾 FAISS Vector Store</h2>
<ul>
  <li>Embeddings: <code>SentenceTransformers('multi-qa-MiniLM-L6-cos-v1')</code></li>
  <li>Semantic search for top-K relevant chunks</li>
  <li>Deduplication ensures unique chunks for retrieval</li>
  <li>Improves LLM query response quality</li>
</ul>

<hr>

<h2>🤖 LLM Integration</h2>
<ul>
  <li>Primary: Groq LLM (<code>llama-3.1-8b-instant</code>)</li>
  <li>Fallback: Hugging Face QA (<code>distilbert-base-uncased-distilled-squad</code>)</li>
  <li>Top retrieved chunks (~3000 tokens) + query → LLM generates professional answers (100–150 words)</li>
  <li>Inferred responses flagged with <code>[INFERRED]</code> if context is insufficient</li>
</ul>

<hr>

<h2>📝 Compliance Gap Analysis</h2>
<ul>
  <li>Compares retrieved sections to PCI-DSS & ISO 27001 mappings (hardcoded)</li>
  <li>Generates <code>gap_analysis_report.md</code> including:
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
  <li>Query PDF policies (e.g., “How are passwords managed?”)</li>
  <li>View LLM answers + compliance gaps + audit priorities</li>
  <li>Export reports as Markdown</li>
  <li>Run: <code>streamlit run src/ui/streamlit_app.py</code></li>
</ul>

<hr>

<h2>📚 Documentation (docs/)</h2>
<ul>
  <li><code>user_guide.md</code> — Instructions for end users on querying and exporting reports</li>
  <li><code>developer_guide.md</code> — Setup, workflow, troubleshooting, updated for hardcoded scripts</li>
</ul>

<hr>

<h2>🚫 Files to Exclude (.gitignore)</h2>
<pre><code>.env
venv/
*.pyc
__pycache__/
data/reports/*
data/knowledge_base/
data/input/*.pdf
pipeline.log
</code></pre>

<hr>

<h2>🔐 Security & Privacy</h2>
<ul>
  <li>Store API keys in <code>.env</code>, never commit</li>
  <li>User PDF data processed locally; no sensitive data persisted</li>
  <li>Logs redact sensitive information</li>
</ul>

<hr>

<h2>📈 Performance & Roadmap</h2>
<ul>
  <li>Chunking + FAISS + LLM enables < 5s semantic retrieval</li>
  <li>Future improvements:
    <ul>
      <li>Multi-PDF ingestion</li>
      <li>Interactive PDF/Excel export</li>
      <li>Fine-tuned compliance LLM</li>
      <li>Enhanced UI/UX with HTML/CSS</li>
    </ul>
  </li>
</ul>

<hr>

<h2>🙏 Acknowledgments</h2>
<p>Built with pdfplumber, PyPDF2, Tesseract OCR, SentenceTransformers, FAISS, Groq, Hugging Face, LangChain, Streamlit.</p>
