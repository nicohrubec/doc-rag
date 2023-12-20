import fitz
from tqdm import tqdm
from llama_index.node_parser import SentenceSplitter


def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    content = []

    text_parser = SentenceSplitter(
        chunk_size=1024
    )

    for page_number in tqdm(range(pdf_document.page_count)):
        page_text = pdf_document[page_number].get_text()
        cur_text_chunks = text_parser.split_text(page_text)
        content.extend(cur_text_chunks)

    pdf_document.close()

    return content
