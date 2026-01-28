import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# Download required NLTK data (first run only)
nltk.download('punkt')

def summarize_text(text, num_sentences=3):
    # Split text into sentences
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Sentence scores
    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

    # Get top N sentence indices
    top_indices = sentence_scores.argsort()[-num_sentences:][::-1]

    # Preserve original order
    top_indices = sorted(top_indices)

    # Build summary
    summary = " ".join([sentences[i] for i in top_indices])
    return summary
