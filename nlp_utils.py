from keybert import KeyBERT
import spacy

kw_model = KeyBERT(model='all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, num=10):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=num)
    return [kw[0] for kw in keywords]

def extract_entities_topics(text):
    doc = nlp(text)
    named_ents = list(set([ent.text for ent in doc.ents]))
    noun_chunks = list(set([chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1]))
    return named_ents, noun_chunks

def generate_meta_title(text):
    keywords = extract_keywords(text, num=1)
    return keywords[0].title() if keywords else "Untitled"

def generate_meta_description(text):
    sentences = text.split(".")
    desc = ". ".join(sentences[:2]) + "." if len(sentences) >= 2 else text
    return desc.strip()