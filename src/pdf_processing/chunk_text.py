import re
import json
from pathlib import Path
from typing import List

def chunk_text(text: str, max_words: int = 500) -> List[dict]:
    """
    Split policy text by section headings (e.g., 4, 4.1, 4.1.1) and keep sections intact.
    Very long sections are split into ~max_words word chunks.
    Returns a list of dicts: {"section": ..., "title": ..., "text": ...}
    """
    # Regex to match section number + title (allowing optional trailing numbers/page artifacts)
    section_pattern = r'(\d+(\.\d+){0,2})\s+([^\n]+)'

    # Find all section headings
    matches = list(re.finditer(section_pattern, text))

    chunks = []

    for i, match in enumerate(matches):
        section_num = match.group(1)
        title = match.group(3).strip()

        # Determine text range for this section
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)

        # Extract section text
        section_text = text[start:end]

        # Clean text: remove page numbers, multiple newlines, and extra spaces
        section_text = re.sub(r'page\s*\d+\s*of\s*\d+', '', section_text, flags=re.IGNORECASE)
        section_text = re.sub(r'\n+', ' ', section_text)  # replace newlines with space
        section_text = section_text.strip()

        # Skip sections with no text
        if not section_text:
            section_text = "[No text extracted]"  # optional placeholder

        # Split long sections into smaller chunks
        words = section_text.split()
        if len(words) > max_words:
            for j in range(0, len(words), max_words):
                chunk_text_str = " ".join(words[j:j+max_words])
                chunks.append({"section": section_num, "title": title, "text": chunk_text_str})
        else:
            chunks.append({"section": section_num, "title": title, "text": section_text})

    # Save structured chunks
    output_path = Path("data/input/chunks_structured.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Structured chunks saved to {output_path}")
    return chunks

# -------------------------------
# Run script
# -------------------------------
if __name__ == "__main__":
    from extract_text import extract_pdf_text  # your existing PDF extractor

    pdf_path = Path("data/input/information_security_policy_v4.0.pdf")
    text = extract_pdf_text(pdf_path)

    if text:
        chunks = chunk_text(text, max_words=500)
        print(f"Created {len(chunks)} structured chunks.")
        if chunks:
            print(f"First chunk:\n{chunks[0]['section']} - {chunks[0]['title']}\n{chunks[0]['text'][:500]}")
