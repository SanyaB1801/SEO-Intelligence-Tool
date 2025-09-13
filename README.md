
## 📘 SEO Content Intelligence Tool

**An AI-powered web application that analyzes web articles and blog content to generate SEO insights — including keyword extraction, topic detection, and meta tag suggestions.**


### 📌 Problem Statement

In the digital marketing and content publishing space, optimizing content for search engines is critical for visibility. However, identifying relevant keywords, extracting topics, and generating effective meta titles/descriptions is often time-consuming and manual.

**Challenge:** Build a lightweight, deployable SEO tool that can automate this process using modern NLP techniques.


### ✅ Solution Overview

This tool enables users to extract SEO-relevant insights from:

* Raw text content
* Uploaded documents (`.txt`, `.pdf`, `.doc`, `.docx`)
* Blog/article URLs (via web scraping)

It performs the following:

* **Keyword extraction** using KeyBERT (transformer-based)
* **Named Entity Recognition (NER)** and **noun chunk detection** via spaCy
* **SEO meta title and description generation**
* Support for **OCR-based scanned PDFs** using Tesseract
* Unified interface built with **Streamlit**, deployed on **Hugging Face Spaces**


### 🛠️ How It Works

#### 👇 Input Options

* **Raw Text**: Direct paste input
* **File Upload**: Accepts `.txt`, `.pdf`, `.doc`, `.docx`
* **URL Input**: Scrapes article content using BeautifulSoup

#### 🧠 AI-Powered Analysis

| Feature                      | Description                                                            |
| ---------------------------- | ---------------------------------------------------------------------- |
| **Top Keywords**             | Extracted via `KeyBERT` using transformer embeddings                   |
| **Named Entities**           | Extracted via `spaCy`                                                  |
| **Topics / Noun Phrases**    | Based on noun chunks from spaCy’s parser                               |
| **Meta Title & Description** | Heuristically generated from top-ranked keywords and leading sentences |


### 🖼️ Application Demo

> 🔗 **Live Demo**: [https://huggingface.co/spaces/sanyab/seo-intelligence-tool](https://huggingface.co/spaces/sanyab/seo-intelligence-tool)

[streamlit-streamlit_app-2025-06-26-11-06-30.webm](https://github.com/user-attachments/assets/df7a8cf5-9a84-416b-a924-615ccf04127c)



### 📁 Project Structure

```bash
.
├── src
|     ├── app.py           # Streamlit UI and main controller
|     ├── nlp_utils.py     # NLP functions for keyword, entity, and meta extraction
|     ├── file_utils.py    # File/URL scraping and OCR handling
├── requirements.txt       # Python package dependencies
├── .huggingface.yml       # Config for installing system packages (OCR support)
└── README.md              # Project documentation
```


### ⚙️ Installation & Local Setup

```bash
# Clone the repository
git clone https://github.com/sanyab1801/seo-intelligence-tool.git
cd seo-intelligence-tool

# Install Python dependencies
pip install -r requirements.txt

# Optional: install OCR dependencies (for .pdf scans, .doc support)
sudo apt install tesseract-ocr poppler-utils

# Run the app
streamlit run app.py
```

> 📝 On Windows, install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/wiki) and [Poppler](https://github.com/oschwartz10612/poppler-windows) manually, and add to PATH.


### 📦 Requirements

```txt
streamlit
spacy
keybert
sentence-transformers
PyPDF2
python-docx
textract
pytesseract
pdf2image
beautifulsoup4
requests
```

> The app uses the `en_core_web_sm` spaCy model. It will auto-download on first run.


### 📂 Supported File Types

| Format         | Support | Notes                                   |
| -------------- | ------- | --------------------------------------- |
| `.txt`         | ✅       | Direct text read                        |
| `.pdf`         | ✅       | Uses PyPDF2 or Tesseract OCR if scanned |
| `.docx`        | ✅       | Parsed using `python-docx`              |
| `.doc`         | ✅       | Extracted using `textract`              |
| Scanned `.pdf` | ✅       | OCR performed via `pytesseract`         |


### 🧠 Future Improvements (Optional Enhancements)

* ✅ Export results to `.csv` or `.json`
* ✅ Keyword density and readability scoring
* ✅ SEO similarity comparison with competitor URLs
* ✅ Language detection and support for multilingual input


### 👨‍💻 Author

Developed by **\[Sanya Behera]**
GitHub: [github.com/sanyab1801](https://github.com/sanyab1801)
Deployed on: [Hugging Face Spaces](https://huggingface.co/spaces)

---
