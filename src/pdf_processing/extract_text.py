import pdfplumber # type: ignore
import PyPDF2 # type: ignore
from pathlib import Path

def extract_pdf_text(pdf_path: Path):
    """Extract text from a PDF using pdfplumber first, then PyPDF2 fallback."""
    text = ""
    try:
        # pdfplumber extraction
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # Fallback to PyPDF2 if text is too short
        if len(text.strip()) < 500:
            print("pdfplumber extracted insufficient text, trying PyPDF2...")
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        # Save extracted text
        debug_path = Path("data/input/extracted_text.txt")
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        with open(debug_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Extracted text saved to {debug_path}")

        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

if __name__ == "__main__":
    pdf_path = Path("data/input/information_security_policy_v4.0.pdf")
    if not pdf_path.exists():
        print(f"PDF file not found at {pdf_path}")
    else:
        extracted_text = extract_pdf_text(pdf_path)
        if extracted_text:
            print("Text extracted successfully.")
            print(f"First 500 characters:\n{extracted_text[:500]}")
            print(f"Total characters extracted: {len(extracted_text)}")
