from sentence_transformers import SentenceTransformer # type: ignore
import numpy as np

def generate_embeddings(chunks: list) -> np.ndarray:
    """Generate embeddings for text chunks using sentence-transformers."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    try:
        embeddings = model.encode(chunks, show_progress_bar=True)
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return None

if __name__ == "__main__":
    from src.pdf_processing.extract_text import extract_pdf_text
    from src.pdf_processing.chunk_text import chunk_text
    from pathlib import Path
    pdf_path = Path("data/input/information_security_policy_v4.0.pdf")
    text = extract_pdf_text(pdf_path)
    if text:
        chunks = chunk_text(text, chunk_size=500)
        embeddings = generate_embeddings(chunks)
        if embeddings is not None:
            print(f"Generated {len(embeddings)} embeddings with shape: {embeddings.shape}")