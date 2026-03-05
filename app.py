from process_pdf import extract_text_from_pdf, chunk_text
from rag_engine import create_vector_store


def process_pdf(pdf_path):

    print("Reading PDF...")

    pages = extract_text_from_pdf(pdf_path)

    print("Chunking text...")

    chunks = chunk_text(pages)

    print("Creating embeddings...")

    index = create_vector_store(chunks)

    return index, chunks