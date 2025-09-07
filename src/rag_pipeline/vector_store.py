import faiss  # type: ignore
import numpy as np
import json
from pathlib import Path

def create_vector_store(embeddings: np.ndarray, chunks: list, index_path: Path, chunks_path: Path):
    """
    Create and save a FAISS index with text chunks.
    embeddings: numpy array of shape (num_chunks, embedding_dim)
    chunks: list of structured chunks (dicts)
    index_path: Path to save FAISS index
    chunks_path: Path to save chunks JSON
    """
    try:
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        # Ensure directories exist
        index_path.parent.mkdir(parents=True, exist_ok=True)
        chunks_path.parent.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(index, str(index_path))

        # Save chunks as JSON
        with open(chunks_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        print(f"FAISS index saved to {index_path}")
        print(f"Chunks saved to {chunks_path}")

    except Exception as e:
        print(f"Error creating vector store: {e}")


if __name__ == "__main__":
    from src.pdf_processing.extract_text import extract_pdf_text
    from src.pdf_processing.chunk_text import chunk_text
    from src.rag_pipeline.embeddings import generate_embeddings

    pdf_path = Path("data/input/information_security_policy_v4.0.pdf")
    index_path = Path("data/knowledge_base/index.faiss")
    chunks_path = Path("data/knowledge_base/chunks.json")

    # Extract PDF text
    text = extract_pdf_text(pdf_path)
    if text:
        # Chunk text into structured sections
        chunks = chunk_text(text, max_words=500)

        # Generate embeddings for each chunk
        embeddings = generate_embeddings(chunks)
        if embeddings is not None:
            # Create FAISS index + save chunks
            create_vector_store(embeddings, chunks, index_path, chunks_path)
