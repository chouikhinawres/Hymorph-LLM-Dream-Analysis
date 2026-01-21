import streamlit as st
from langdetect import detect, LangDetectException
from utils import extract_text_from_pdf, vectorize_text

# -----------------------------
# Configuration générale
# -----------------------------
st.set_page_config(
    page_title="PDF Vectorisation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("📂 Gestion des PDFs")
    st.markdown("Téléversez un ou plusieurs fichiers PDF.")

    uploaded_files = st.file_uploader(
        "📄 Choisir des fichiers PDF",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")

# -----------------------------
# Header principal
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>📑 PDF Uploader & Vectorisation</h1>
    <p style='text-align: center; color: grey;'>
        Extraction automatique, détection de langue et vectorisation multi-documents
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------
# Traitement des PDFs
# -----------------------------
if uploaded_files:
    all_texts = []
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📘 Informations des PDFs")

        for uploaded_file in uploaded_files:
            with st.container(border=True):
                st.markdown(f"### 📄 {uploaded_file.name}")

                text = extract_text_from_pdf(uploaded_file)

                if not text:
                    st.warning("⚠️ Texte vide ou non extractible.")
                    continue

                try:
                    lang = detect(text)
                except LangDetectException:
                    lang = "Inconnue"

                lines = text.splitlines()
                titre = lines[0] if len(lines) > 0 else uploaded_file.name
                auteur = lines[1] if len(lines) > 1 else "Auteur inconnu"

                st.markdown(f"**📝 Titre :** {titre}")
                st.markdown(f"**👤 Auteur :** {auteur}")
                st.markdown(f"**🌍 Langue :** {lang}")
                st.markdown(f"**📊 Taille texte :** {len(text)} caractères")

                all_texts.append(text)

    with col2:
        st.subheader("📈 Résumé")
        st.metric("Nombre de PDFs", len(uploaded_files))
        st.metric("PDFs valides", len(all_texts))

        if all_texts:
            st.success("✔️ Tous les fichiers sont prêts pour la vectorisation")

    st.markdown("---")

    # -----------------------------
    # Vectorisation
    # -----------------------------
    if all_texts:
        st.subheader("⚙️ Vectorisation TF-IDF")

        if st.button("🚀 Lancer la vectorisation", use_container_width=True):
            with st.spinner("Vectorisation en cours..."):
                combined_text = "\n".join(all_texts)
                try:
                    vectorize_text(combined_text, "data/pdf_vector_multi.pkl")
                    st.success(
                        "✅ Vectorisation terminée avec succès\n\n"
                        "📁 Fichier sauvegardé : `data/pdf_vector_multi.pkl`"
                    )
                except ValueError as e:
                    st.error(f"❌ Erreur lors de la vectorisation : {e}")

else:
    st.info("👈 Veuillez importer des fichiers PDF depuis la sidebar.")
