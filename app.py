import streamlit as st
import re
from nlp_utils import extract_keywords, extract_entities_topics, generate_meta_title, generate_meta_description
from file_utils import extract_text_from_file, scrape_article_from_url

#Checking if url is valid
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' #  ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' #  ipv6
        r'(?::\d+)?' #  port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def analyse_text(text):
    st.markdown("## 🧠 Analysis Results")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔑 Top Keywords")
        keywords = extract_keywords(text)
        for i, kw in enumerate(keywords, start=1):
            st.markdown(f"- **{i}.** {kw}")

    with col2:
        st.markdown("### 🏷️ Named Entities")
        entities, _ = extract_entities_topics(text)
        if entities:
            for ent in entities:
                st.markdown(f"- {ent}")
        else:
            st.markdown("*No named entities found.*")

    # Expandable section for Topics
    _, topics = extract_entities_topics(text)
    with st.expander("📂 View Detected Topics (noun chunks)"):
        if topics:
            for topic in topics:
                st.markdown(f"- {topic}")
        else:
            st.write("No topics found.")

    # Meta title and description
    st.markdown("### 📌 Suggested Meta Title")
    meta_title = generate_meta_title(text)
    st.success(f"**{meta_title}**")

    st.markdown("### 📝 Suggested Meta Description")
    meta_desc = generate_meta_description(text)
    st.info(meta_desc)


# Main Streamlit UI starts


st.title("SEO Content Intelligence Tool 🧠🔍")
st.text('This tool should extract relevant keywords, entities, and topics from an article or blog post, and optionally generate SEO meta title and description suggestions.')

selection = st.segmented_control("Drop a file here, or paste text (URL or raw text)",["Raw Text","Upload File", "Paste URL"])

if selection == "Upload File":
    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx"], help="Drag and drop a file here")
    if st.button("Analyse"):
        file_text = extract_text_from_file(uploaded_file)
        analyse_text(file_text)

elif selection == "Paste URL":
    url_input = st.text_area("Paste the article/blog URL", height=75, help="Paste URL here")
    if st.button("Analyse") and is_valid_url(url_input):
        page_text = scrape_article_from_url(url_input)
        analyse_text(page_text)

elif selection == "Raw Text":
    text_input = st.text_area("Paste raw text here", height=150, help="Paste raw text here")
    if st.button("Analyse"):
        analyse_text(text_input)