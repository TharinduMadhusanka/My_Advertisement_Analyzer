from io import BytesIO
import pytesseract
from PIL import Image
import spacy
import re
import requests

nlp = spacy.load('en_core_web_sm')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def ocr_image(image_path, mode):
    try:
        # Open the image using Pillow
        image = Image.open(image_path)

        # Perform OCR using pytesseract with the specified mode
        ocr_text = pytesseract.image_to_string(image, config=f'--psm {mode}')

        return ocr_text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return None


def perform_ner(sentence):
    doc = nlp(sentence)

    ner_list = []
    for ent in doc.ents:
        ner_list.append((ent.text, ent.label_))

    return ner_list


def run_ocr(image_path):
    # Perform OCR
    ocr_result = ocr_image(image_path, 3)
    if ocr_result:
        # remove non-ASCII characters
        ocr_result = re.sub(r'[^\x00-\x7f]', r'', ocr_result)

        # Perform NER
        return perform_ner(ocr_result)
    else:
        return False


def ocr_image_url(image_url, mode):
    try:
        # Fetch the image from the provided URL
        response = requests.get(image_url)
        response.raise_for_status()

        # Open the image using Pillow from the response content
        image = Image.open(BytesIO(response.content))

        # Perform OCR using pytesseract with the specified mode
        ocr_text = pytesseract.image_to_string(image, config=f'--psm {mode}')

        if ocr_text:
            # remove non-ASCII characters
            ocr_text = re.sub(r'[^\x00-\x7f]', r'', ocr_text)

            # Perform NER
            return perform_ner(ocr_text)
        else:
            return ["No text found"]

    except Exception as e:
        print(f"Error during OCR from URL: {e}")
        return None

# image_path = "sample4.jpg"
# print(run_ocr(image_path))
