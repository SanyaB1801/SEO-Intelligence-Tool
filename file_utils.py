from bs4 import BeautifulSoup
import requests
import PyPDF2
import docx
import os
import textract
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image

def extract_text_from_file(uploaded_file):
    try:
        filename = uploaded_file.name.lower()

        if filename.endswith(".txt"):                                       # Text file
            return uploaded_file.read().decode("utf-8")

        elif filename.endswith(".pdf"):                                     # PDF file
            try:
                reader = PyPDF2.PdfReader(uploaded_file)                    # Digital text
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    text += extracted if extracted else ""
                if text.strip():
                    return text.strip()
                else:
                    images = convert_from_bytes(uploaded_file.getvalue())   # OCR
                    text = ""
                    for img in images:
                        text += pytesseract.image_to_string(img)
                    return text.strip()
            except Exception as e:
                return f"OCR failed for PDF: {e}"

        elif filename.endswith(".docx"):                                    # Docx file
            doc = docx.Document(uploaded_file)
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text).strip()
        
        elif filename.endswith(".doc"):                                     # Old doc file
            try:
                text = textract.process(uploaded_file)
                return text.decode("utf-8").strip()
            except Exception as e:
                return f"Error processing .doc file: {e}"

        else:
            return "Unsupported file format. Please upload a .txt, .pdf, or .docx file."

    except Exception as e:
        return f"Error reading file: {e}"

def scrape_article_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return ' '.join(soup.stripped_strings)
    except Exception as e:
        return f"Error scraping URL: {e}"