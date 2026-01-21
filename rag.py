# rag.py
# Gestion du VectorStore et RAG (Retrieval-Augmented Generation)

import streamlit as st
from langchain_community.llms import Ollama

from dream_app import read_pdf_bytes, build_faiss_store, detect_lang


# ---------- Gestionnaire du VectorStore ----------
class VectorStoreManager:
    # Clé utilisée pour stocker l'instance dans st.session_state
    KEY = "vector_store_mgr"

    def __init__(self):
        self.store = None  # Instance FAISS
        self.pdf_name = ""  # Nom du PDF chargé
        self.pdf_lang = ""  # Langue du PDF
        self.doc_count = 0  # Nombre de segments/documents dans le VectorStore

    @classmethod
    def get(cls):
        """
        Retourne l'instance unique du VectorStoreManager.
        Si elle n'existe pas encore dans st.session_state, on la crée.
        """
        if cls.KEY not in st.session_state:
            st.session_state[cls.KEY] = VectorStoreManager()
        return st.session_state[cls.KEY]

    def reset(self):
        """Réinitialise le VectorStore et les métadonnées."""
        self.store = None
        self.pdf_name = ""
        self.pdf_lang = ""
        self.doc_count = 0

    def load_pdf(self, pdf_bytes: bytes, name: str):
        """
        Charge un PDF, détecte sa langue, crée le VectorStore et stocke les métadonnées.
        """
        text = read_pdf_bytes(pdf_bytes)
        self.pdf_lang = detect_lang(text[:2000])  # Détecte la langue des premiers caractères
        self.store = build_faiss_store(text)  # Création des embeddings et du FAISS
        self.pdf_name = name
        self.doc_count = len(self.store.index_to_docstore_id)

    def is_ready(self) -> bool:
        """Retourne True si le VectorStore est prêt à être utilisé."""
        return self.store is not None


# ---------- RAG (Retrieval-Augmented Generation) ----------
def run_rag(query: str, vectorstore, k: int = 3) -> str:
    """
    Exécute une requête RAG sur le VectorStore.

    Paramètres :
    - query : texte à rechercher / interpréter
    - vectorstore : instance FAISS
    - k : nombre de documents similaires à récupérer

    Retourne :
    - La réponse générée par le modèle LLM (Ollama)
    """
    # Recherche des k documents les plus similaires
    docs = vectorstore.similarity_search(query, k=k)
    # Concaténation du contenu des documents pour le contexte
    context = "\n\n".join(doc.page_content for doc in docs)

    # Prompt pour le LLM
    prompt = f"""
Vous êtes un interprète de rêves expert.
Utilisez uniquement les informations présentes dans le CONTEXTE.
Répondez dans la même langue que le CONTEXTE.

CONTEXTE :
{context}

RÊVE :
{query}

INTERPRÉTATION :
"""

    llm = Ollama(model="mistral")
    return llm(prompt).strip()
