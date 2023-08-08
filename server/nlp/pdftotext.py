import re
import fitz
from PIL import Image
import spacy
import re

nlp = spacy.load('en_core_web_sm')


def extract_text_from_pdf(pdf_file_path):
    text = ""
    pdf_document = fitz.open(pdf_file_path)
    num_pages = pdf_document.page_count
    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text


def perform_ner(sentence):
    doc = nlp(sentence)

    ner_list = []
    for ent in doc.ents:
        ner_list.append((ent.text, ent.label_))

    return ner_list


def run_pdf(file_path):
    # Perform OCR
    pdf_result = extract_text_from_pdf(file_path)
    if pdf_result:
        # remove non-ASCII characters
        pdf_result = re.sub(r'[^\x00-\x7f]', r'', pdf_result)

        # Perform NER
        return perform_ner(pdf_result)
    else:
        return False
