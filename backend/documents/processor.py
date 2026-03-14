from typing import List, Tuple
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[str, int]:
    """Extract all text from a PDF and return (full_text, page_count)."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text())
    doc.close()
    return "\n".join(pages_text), len(pages_text)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks of approximately chunk_size characters."""
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        # Try to break at a sentence or word boundary
        if end < text_length:
            last_period = chunk.rfind(". ")
            last_newline = chunk.rfind("\n")
            break_point = max(last_period, last_newline)
            if break_point > chunk_size // 2:
                chunk = chunk[: break_point + 1]

        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)

        start = start + len(chunk) - overlap if len(chunk) > overlap else start + chunk_size

    return chunks
