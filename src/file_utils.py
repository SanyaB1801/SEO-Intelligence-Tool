from bs4 import BeautifulSoup
import requests
import PyPDF2
import docx
import textract
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

def extract_text_from_file(uploaded_file):
    try:
        filename = uploaded_file.name.lower()

        if filename.endswith(".txt"):
            return uploaded_file.read().decode("utf-8")

        elif filename.endswith(".pdf"):
            try:
                reader = PyPDF2.PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    text += extracted if extracted else ""
                if text.strip():
                    return text.strip()
                else:
                    try:
                        images = convert_from_bytes(uploaded_file.getvalue())
                        text = ""
                        for img in images:
                            text += pytesseract.image_to_string(img)
                        return text.strip()
                    except Exception as ocr_err:
                        return f"OCR image extraction failed: {ocr_err}"
            except Exception as e:
                return f"OCR failed for PDF: {e}"

        elif filename.endswith(".docx"):
            doc = docx.Document(uploaded_file)
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text).strip()

        elif filename.endswith(".doc"):
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
        result = ' '.join(soup.stripped_strings).strip()
        return result if result else "No readable content found at the URL."
    except Exception as e:
        return f"Error scraping URL: {e}"
