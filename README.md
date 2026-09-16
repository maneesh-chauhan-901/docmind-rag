# DocMind

DocMind is a small AI research and document intelligence assistant. Upload one or more PDF research documents, ask questions, and receive answers grounded in the uploaded text with document and page citations.

## Features

- Upload multiple PDFs
- Extract text page by page
- Split text into simple overlapping chunks
- Create CPU-friendly embeddings with `all-MiniLM-L6-v2`
- Store chunks and metadata in a local ChromaDB index
- Retrieve relevant chunks for each question
- Generate answers with the Gemini API
- Show source document names and page numbers
- Keep chat history during the current Streamlit session
- Clear the local document index

## Technology Stack

- Python
- Streamlit
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Gemini API
- python-dotenv

LangChain and other RAG frameworks are intentionally not used. The RAG steps are implemented directly in `rag.py`.

## Architecture

- `app.py`: Streamlit interface, uploads, chat, and source display.
- `pdf_utils.py`: PDF extraction and simple text chunking.
- `rag.py`: Embeddings, ChromaDB storage, retrieval, and Gemini generation.

## How RAG Works

```text
PDF upload
  -> PyMuPDF page text extraction
  -> overlapping text chunks
  -> Sentence Transformer embeddings
  -> local ChromaDB storage
  -> question embedding
  -> top-K similarity retrieval
  -> Gemini prompt with retrieved context
  -> answer and source pages
```

Gemini is instructed to answer only from the retrieved context. When the context does not contain the answer, the application asks it to say that the information was not found in the uploaded documents.


## Limitations

- Text-based PDFs work best; scanned PDFs need OCR, which is not included.
- Retrieval uses simple top-K similarity search only.
- The local index skips a PDF if another document with the same filename is already indexed.
- Answers depend on the quality of the extracted text, retrieved chunks, and Gemini response.
- Chat history lasts only for the current Streamlit session.
