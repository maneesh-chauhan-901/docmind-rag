"""Small PDF helpers for extracting page-aware text chunks."""

import fitz


CHUNK_SIZE = 450
CHUNK_OVERLAP = 75


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into word-based chunks with a small overlap."""
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += step

    return chunks


def extract_pdf_chunks(pdf_bytes: bytes, document_name: str) -> list[dict]:
    """Extract text page by page and attach the original page number."""
    chunks = []
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

    try:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text").strip()
            for chunk_number, text in enumerate(chunk_text(page_text)):
                chunks.append(
                    {
                        "text": text,
                        "document": document_name,
                        "page": page_number,
                        "chunk_number": chunk_number,
                    }
                )
    finally:
        pdf.close()

    return chunks
