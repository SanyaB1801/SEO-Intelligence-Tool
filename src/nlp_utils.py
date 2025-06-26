import os
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
os.environ["HF_HOME"] = "/tmp/huggingface"

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import spacy

sentence_model = SentenceTransformer("src/models/all-MiniLM-L6-v2")
kw_model = KeyBERT(model=SentenceTransformer("src/models/all-MiniLM-L6-v2"))
nlp = spacy.load("en_core_web_sm")

title_gen = pipeline("text2text-generation", model="google/flan-t5-base")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def extract_keywords(text, num=10):
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=num * 2,
        use_mmr=True,
        diversity=0.7
    )
    seen = set()
    unique_keywords = []
    for kw, _ in keywords:
        if kw.lower() not in seen:
            unique_keywords.append(kw)
            seen.add(kw.lower())
        if len(unique_keywords) >= num:
            break
    return unique_keywords

    
def extract_entities_topics(text, top_n=15):
    doc = nlp(text)

    # Extracting raw candidates
    raw_ents = [ent.text.strip() for ent in doc.ents 
                if ent.label_ not in ("DATE", "TIME", "QUANTITY") and not ent.text.strip().isdigit()]
    
    raw_chunks = [chunk.text.strip() for chunk in doc.noun_chunks 
                  if len(chunk.text.strip().split()) > 1]

    # Removing duplicates
    unique_ents = list(set(raw_ents))
    unique_chunks = list(set(raw_chunks))

    def rank_by_relevance(items):
        if not items:
            return []
        doc_embedding = sentence_model.encode(text, convert_to_tensor=True)
        item_embeddings = sentence_model.encode(items, convert_to_tensor=True)
        similarities = util.cos_sim(doc_embedding, item_embeddings)[0].cpu().numpy()
        ranked = sorted(zip(items, similarities), key=lambda x: x[1], reverse=True)
        return [item for item, _ in ranked[:top_n]]

    top_entities = rank_by_relevance(unique_ents)
    top_chunks = rank_by_relevance(unique_chunks)

    return top_entities, top_chunks


def generate_meta_title(text):
    try:
        input_text = text.strip().replace("\n", " ")[:512]
        prompt = f"Generate a short headline for this article: {input_text}"
        title = title_gen(prompt, max_length=15, min_length=5, do_sample=False)
        return title[0]["generated_text"].strip()
    except Exception as e:
        return "Untitled"

def generate_meta_description(text):
    try:
        input_text = text.strip().replace("\n", " ")[:1024]
        summary = summarizer(input_text, max_length=60, min_length=30, do_sample=False)
        return summary[0]["summary_text"].strip()
    except Exception:
        return "Summary not available"
