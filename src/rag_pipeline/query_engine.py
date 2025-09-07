# src/rag_pipeline/query_engine.py

import json
import logging
import os
import time
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from dotenv import load_dotenv

# ===========================
# Setup logging & environment
# ===========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# ===========================
# Initialize LLMs
# ===========================
try:
    llm_groq = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.5
    )
except Exception as e:
    logger.warning(f"Failed to initialize Groq LLM: {e}")
    llm_groq = None

hf_model_name = "distilbert-base-uncased-distilled-squad"
hf_tokenizer = AutoTokenizer.from_pretrained(hf_model_name)
hf_model = AutoModelForQuestionAnswering.from_pretrained(hf_model_name)

# ===========================
# Prompt template for Groq
# ===========================
template = """
You are a compliance assistant analyzing an Information Security Policy document for PCI-DSS and ISO 27001 compliance.
Use the provided context to answer the query in 100–150 words, focusing on key details and compliance status.
If the context is insufficient or missing, clearly indicate that the answer is inferred and provide a brief general response.
Respond in clear, professional English.

Query: {query}
Context: {context}
"""
prompt = ChatPromptTemplate.from_template(template)
output_parser = StrOutputParser()

if llm_groq:
    chain = ({"query": RunnablePassthrough(), "context": RunnablePassthrough()} 
             | prompt | llm_groq | output_parser)
else:
    chain = None

# ===========================
# Load compliance mapping
# ===========================
MAPPING_PATH = "data/mappings/compliance_mapping.json"
try:
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        compliance_mapping = json.load(f)
    logger.info(f"Loaded compliance mapping from {MAPPING_PATH}")
except Exception as e:
    logger.error(f"Failed to load compliance mapping: {e}")
    compliance_mapping = {}

# ===========================
# Utility functions
# ===========================
def truncate_context(context: str, max_tokens: int = 3000) -> str:
    words = context.split()
    current_tokens = 0
    truncated = []
    for w in words:
        current_tokens += 1.5
        if current_tokens > max_tokens:
            break
        truncated.append(w)
    return " ".join(truncated)

def extract_section(chunk: dict) -> str:
    return chunk.get("section", "Unknown")

def enhance_query(query: str) -> str:
    """Automatically enhance query with mapping keywords"""
    q_lower = query.lower()
    for key, value in compliance_mapping.items():
        if key.lower() in q_lower:
            sections = value.get("sections", "")
            keywords = value.get("keywords", "")
            additions = " ".join(sections + " " + keywords)
            return query + " " + additions
    return query

# ===========================
# Retrieve chunks (deduplicated)
# ===========================
def retrieve_chunks(query: str, index_path: str, chunks_path: str, top_k: int = 20) -> list:
    try:
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)

        index = faiss.read_index(index_path)
        enhanced = enhance_query(query)
        logger.info(f"Enhanced query: {enhanced}")

        model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
        q_embed = model.encode([enhanced], show_progress_bar=False, normalize_embeddings=True)
        distances, indices = index.search(q_embed, top_k)

        # Deduplicate chunks by text
        seen_texts = set()
        relevant_chunks = []
        for idx in indices[0]:
            if idx >= len(chunks):
                continue
            text = chunks[idx]["text"]
            if text not in seen_texts:
                seen_texts.add(text)
                relevant_chunks.append(chunks[idx])

        logger.info(f"Retrieved chunk sections: {[extract_section(c) for c in relevant_chunks]}")
        return [c["text"] for c in relevant_chunks]
    except Exception as e:
        logger.error(f"Error retrieving chunks: {e}")
        return []

# ===========================
# Fallback: scan entire chunks JSON
# ===========================
def scan_chunks_fallback(query: str, chunks_path: str) -> list:
    """Scan all chunks for the query if FAISS retrieval fails"""
    try:
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        matched_chunks = []
        q_lower = query.lower()
        for chunk in chunks:
            text = chunk.get("text", "")
            title = chunk.get("title", "")
            if text.strip() == "[No text extracted]":
                continue
            if q_lower in text.lower() or q_lower in title.lower():
                matched_chunks.append(chunk)
        return [c["text"] for c in matched_chunks]
    except Exception as e:
        logger.error(f"Error scanning chunks: {e}")
        return []

# ===========================
# Query knowledge base
# ===========================
def query_knowledge_base(query: str,
                         index_path="data/knowledge_base/index.faiss",
                         chunks_path="data/knowledge_base/chunks_structured.json",
                         full_scan=False) -> str:
    try:
        # Use full scan for complete coverage
        relevant_chunks = scan_chunks_fallback(query, chunks_path) if full_scan else retrieve_chunks(query, index_path, chunks_path)
        inferred = False  # flag for inferred/fallback answers

        if not relevant_chunks:
            inferred = True
            for key, value in compliance_mapping.items():
                if key.lower() in query.lower():
                    fallback_text = value.get("fallback", "")
                    if fallback_text:
                        return f"[INFERRED] {fallback_text}"
            return "[INFERRED] No relevant information found. Please refine your query."

        context = "\n".join(relevant_chunks)
        context = truncate_context(context, max_tokens=3000)

        # Groq LLM
        if llm_groq and chain:
            try:
                response = chain.invoke({"query": query, "context": context})
                if inferred:
                    response = "[INFERRED] " + response
                return response
            except Exception as e:
                logger.warning(f"Groq error: {e}. Falling back to Hugging Face.")
                inferred = True

        # Hugging Face QA fallback
        context_chunk = truncate_context(relevant_chunks[0], max_tokens=300)
        inputs = hf_tokenizer(query, context_chunk, return_tensors="pt", truncation=True, max_length=512)
        outputs = hf_model(**inputs)
        start_idx = outputs.start_logits.argmax().item()
        end_idx = outputs.end_logits.argmax().item()
        if 0 <= start_idx <= end_idx < len(inputs.input_ids[0]):
            answer = hf_tokenizer.decode(inputs.input_ids[0, start_idx:end_idx+1])
            prefix = "[INFERRED] " if inferred else ""
            return f"{prefix}Based on the policy document: {answer}"

        return "[INFERRED] Unable to extract a precise answer. Please ask a more specific query."
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return "[ERROR] Error processing query. Please try again."


# ===========================
# Run dynamic queries
# ===========================
if __name__ == "__main__":
    while True:
        query = input("\nEnter your query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        response = query_knowledge_base(query, full_scan=True)
        print(f"\nResponse: {response}\n")
        time.sleep(1)
