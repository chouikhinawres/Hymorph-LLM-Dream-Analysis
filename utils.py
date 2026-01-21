from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from pathlib import Path

def extract_text_from_pdf(file):
    """Lit un PDF et retourne son texte complet"""
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text.strip()

def vectorize_text(text, output_file="pdf_vector.pkl"):
    """Vectorise le texte et sauvegarde le vecteur"""
    vectorizer = TfidfVectorizer(stop_words=None)
    vectors = vectorizer.fit_transform([text])
    with open(Path(output_file), "wb") as f:
        pickle.dump(vectors, f)
    return vectors
