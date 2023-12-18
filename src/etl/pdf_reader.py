import fitz
from tqdm import tqdm


def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    content = []

    for page_number in tqdm(range(pdf_document.page_count)):
        page = pdf_document[page_number]
        content.append(page.get_text())

    pdf_document.close()

    return content
