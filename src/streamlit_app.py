import streamlit as st
import re
from nlp_utils import extract_keywords, extract_entities_topics, generate_meta_title, generate_meta_description
from file_utils import extract_text_from_file, scrape_article_from_url

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def clean_desc(text):
   return re.sub(r"[*_`]", "", text)

def analyse_text(text):
    st.markdown("## 🔎 Analysis Results")

    st.markdown("### Top Keywords")
    with st.spinner("Extracting keywords..."):
        
        keywords = extract_keywords(text)
        if keywords:
            st.markdown(" ".join([f"`🟢 {kw}`" for kw in keywords]))
        else:
            st.info("No keywords found.")

    st.markdown("### Named Entities")
    with st.spinner("Extracting named entities..."):
        entities, _ = extract_entities_topics(text)
        with st.expander("Named Entities"):
            if entities:
                st.markdown(" ".join([f"`📃 {ent}`" for ent in entities]))
            else:
                st.write("No named entities found.")
        
    st.markdown("### Detected Topics")
    _, topics = extract_entities_topics(text)
    with st.spinner("Identifying topics..."):
        with st.expander("Detected Topics (noun chunks)"):
            if topics:
                st.markdown(" ".join([f"`⭐ {topic}`" for topic in topics]))
            else:
                st.write("No topics found.")

    st.markdown("### 📌 Suggested Meta Title")
    with st.spinner("Generating meta title..."):
        meta_title = generate_meta_title(text)
        st.success(f"**{meta_title}**")

    st.markdown("### 📝 Suggested Meta Description")
    with st.spinner("Generating meta description..."):
        meta_desc = generate_meta_description(text)
        cleaned = clean_desc(meta_desc)
        st.info(cleaned)


# Streamlit UI
st.title("SEO Intelligence Tool 🧠🔍")
st.write("This tool extracts relevant keywords, entities, and topics from text or a URL, and suggests SEO meta tags.")

selection = st.selectbox("Choose input type:", ["Raw Text", "Upload File", "Paste URL"])

text_input = None
uploaded_file = None
url_input = None

if selection == "Upload File":
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx"])
    
    if st.button("Analyse"):
        if uploaded_file:
            file_text = extract_text_from_file(uploaded_file)
            analyse_text(file_text)
        else:
            st.warning("Please upload a file before analyzing.")

elif selection == "Paste URL":
    url_input = st.text_area("Paste the article/blog URL", height=75)
    
    if st.button("Analyse"):
        if url_input and is_valid_url(url_input):
            page_text = scrape_article_from_url(url_input)
            analyse_text(page_text)
        else:
            st.warning("Invalid URL.")

elif selection == "Raw Text":
    text_input = st.text_area("Paste raw text here", height=150)
    
    if st.button("Analyse"):
        if text_input.strip():
            analyse_text(text_input)
        else:
            st.warning("Please enter some text to analyze.")
