import pytesseract
from pdf2image import convert_from_path

# PATHS
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\poppler\poppler-25.12.0\Library\bin"


def extract_text_from_pdf(pdf_path):

    pages = convert_from_path(
        pdf_path,
        dpi=200,
        poppler_path=POPPLER_PATH
    )

    page_data = []

    for i, page in enumerate(pages):

        text = pytesseract.image_to_string(page)

        page_data.append({
            "page": i + 1,
            "text": text
        })

    return page_data


def chunk_text(page_data, chunk_size=300):

    chunks = []

    for page in page_data:

        text = page["text"]

        for i in range(0, len(text), chunk_size):

            chunk = text[i:i + chunk_size]

            chunks.append({
                "page": page["page"],
                "text": chunk
            })

    return chunks