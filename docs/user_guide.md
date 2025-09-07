<h2>📘 User Guide: RAG Compliance Chatbot</h2>

<h3>Introduction</h3>
<p>The <strong>RAG Compliance Chatbot</strong> analyzes the Bank's Information Security Policy v4.0 against <strong>PCI-DSS v3.2</strong> and <strong>ISO 27001:2013</strong>. It ingests the policy PDF, creates a knowledge base with 26 structured chunks, performs semantic searches, and generates responses with compliance details. The minimal <strong>Streamlit UI</strong> allows users to query the policy and view the compliance gap analysis report.</p>

<p>This guide explains how to use the chatbot, interpret responses, and troubleshoot common issues.</p>

<hr>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.10+ installed</li>
  <li>Dependencies installed: <code>pip install -r requirements.txt</code></li>
  <li>.env file with <code>GROQ_API_KEY=your_key</code></li>
  <li>Policy PDF located at <code>data/input/information_security_policy_v4.0.pdf</code></li>
  <li>Knowledge base generated (Day 2 scripts):
    <pre><code>python src/pdf_processing/extract_text.py
python src/pdf_processing/chunk_text.py
python src/rag_pipeline/vector_store.py</code></pre>
  </li>
  <li>Report generated (Day 4 script):
    <pre><code>python -m src.compliance_analysis.report_generator</code></pre>
  </li>
</ul>

<hr>

<h3>Running the Chatbot</h3>
<ol>
  <li>Navigate to project directory:
    <pre><code>cd C:\Users\Admin\Desktop\rag_compliance_chatbot</code></pre>
  </li>
  <li>Activate virtual environment:
    <pre><code>venv\Scripts\activate</code></pre>
  </li>
  <li>Run the Streamlit UI:
    <pre><code>streamlit run src/ui/streamlit_app.py</code></pre>
  </li>
  <li>Access the UI in a browser:
    <pre><code>http://localhost:8501</code></pre>
  </li>
</ol>

<hr>

<h3>Using the Chatbot</h3>

<h4>Querying the Policy</h4>
<ol>
  <li><strong>Enter Query:</strong> Type a question in the input field (e.g., "How are passwords managed?").</li>
  <li><strong>Submit:</strong> Click "Submit Query".</li>
  <li><strong>Response:</strong> The chatbot returns a response (~100–150 words) with policy details, compliance status, and inferred content if sections are missing.</li>
  <li><strong>History:</strong> Previous queries and responses are listed below the input field.</li>
  <li><strong>Report:</strong> Expand "Compliance Gap Analysis Report" to view pre-generated report with queries, sections, responses, status, priority, and gaps.</li>
</ol>

<h4>Example Queries</h4>
<ul>
  <li>"What are the access control policies?" – Section 4.4, compliant with PCI-DSS 8.1.6, gaps in 8.1.7</li>
  <li>"How does the policy address encryption?" – Section 4.34, partial compliance, gaps in PCI-DSS 3.6.4</li>
  <li>"What are the vulnerability management procedures?" – Section 4.16, partial compliance, gaps in PCI-DSS 11.2</li>
  <li>"What is the incident response plan?" – Section 4.33, compliant, no gaps</li>
  <li>"How are passwords managed?" – Section 4.5, partial compliance, gaps in PCI-DSS 8.3</li>
</ul>

<hr>

<h3>Interpreting Responses</h3>
<ul>
  <li><strong>Policy Section:</strong> The referenced section (e.g., 4.5)</li>
  <li><strong>Response:</strong> Policy summary or inferred content if missing</li>
  <li><strong>Compliance Status:</strong> Compliant, Partial, Non-Compliant</li>
  <li><strong>Audit Priority:</strong> High, Medium, Low</li>
  <li><strong>Gaps:</strong> Specific missing clauses (e.g., PCI-DSS 8.1.7: Missing lockout duration)</li>
</ul>

<hr>

<h3>Troubleshooting</h3>
<ul>
  <li><strong>Inferred Responses:</strong> Indicates missing sections in <code>chunks_structured.json</code>. Re-run Day 2 pipeline.</li>
  <li><strong>No Report:</strong> Run <code>python -m src.compliance_analysis.report_generator</code>.</li>
  <li><strong>Errors:</strong> Check logs for Groq/Hugging Face issues; ensure .env key is valid.</li>
  <li><strong>Inaccurate Sections:</strong> Verify <code>chunks_structured.json</code> for sections like 4.5, 4.34:
    <pre><code>findstr /C:"4.34" data\knowledge_base\chunks_structured.json</code></pre>
  </li>
</ul>

<hr>

<h3>Advanced Usage</h3>
<ul>
  <li><strong>Update Policy:</strong> Replace PDF and re-run Day 2 scripts.</li>
  <li><strong>Custom Queries:</strong> Use UI for queries beyond report (e.g., "How is supplier risk managed?").</li>
  <li><strong>Export Report:</strong> Copy from UI or open <code>data/reports/gap_analysis_report.md</code>.</li>
</ul>

<hr>

<h3>Support</h3>
<p>For issues, contact the developer or review <code>docs/developer_guide.md</code>.</p>
