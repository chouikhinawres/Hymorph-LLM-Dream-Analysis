import streamlit as st
from langdetect import detect, LangDetectException
from utils import extract_text_from_pdf, vectorize_text

# -----------------------------
# Configuration de la page
# -----------------------------
st.set_page_config(
    page_title="PDF Processing Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CSS Professionnel
# -----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2ff, #fef3c7);
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 12px 35px rgba(0,0,0,0.08);
}

h1 {
    font-weight: 900;
    color: #111827;
    text-align: left;  
    font-size: 36px;
    margin-bottom: 1rem;
    border-left: 6px solid #6366f1;
    padding-left: 12px;
}

/* Sidebar */
.stSidebar {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

/* PDF Cards */
.pdf-card {
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1rem;
    background-color: #f9fafb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: transform 0.2s;
}
.pdf-card:hover {
    transform: translateY(-4px);
}

/* Petit texte explicatif */
.info-text {
    font-size: 14px;
    color: #4b5563;
    margin-top: 6px;
    margin-bottom: 16px;
}

/* Cacher le texte par défaut du file uploader */
div[data-baseweb="file-uploader"] span {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Titre principal
# -----------------------------
st.markdown("<h1>PDF Processing Platform</h1>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("PDF Upload")
    uploaded_files = st.file_uploader(
        "",  # titre supprimé
        type=["pdf"],
        accept_multiple_files=True
    )
    st.markdown("Upload one or more PDF files to process their content automatically.")
    st.markdown("---")

# -----------------------------
# Traitement automatique des PDFs
# -----------------------------
if uploaded_files:
    all_texts = []

    st.subheader("Document Details")
    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        st.markdown(f"<div class='pdf-card'>", unsafe_allow_html=True)
        st.markdown(f"### {uploaded_file.name}", unsafe_allow_html=True)

        text = extract_text_from_pdf(uploaded_file)
        if not text:
            st.warning("Empty or unreadable PDF.")
            st.markdown("</div>", unsafe_allow_html=True)
            continue

        try:
            lang = detect(text)
        except LangDetectException:
            lang = "Unknown"

        lines = text.splitlines()
        title = lines[0] if len(lines) > 0 else uploaded_file.name
        author = lines[1] if len(lines) > 1 else "Unknown author"

        st.markdown(f"**Title:** {title}")
        st.markdown(f"**Author:** {author}")
        st.markdown(f"**Language:** {lang}")
        st.markdown(f"**Text length:** {len(text)} characters")

        all_texts.append(text)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------
    # Traitement automatique avec feedback
    # -----------------------------
    if all_texts:
        st.subheader("Processing PDFs")
        with st.spinner("Processing uploaded PDFs... Please wait."):
            combined_text = "\n".join(all_texts)
            try:
                vectorize_text(combined_text, "data/pdf_vector_multi.pkl")
                st.success("Processing completed successfully.\nFile saved: data/pdf_vector_multi.pkl")
            except ValueError as e:
                st.error(f"Error during processing: {e}")

        st.markdown(
            "<div class='info-text'>All uploaded documents were processed automatically.</div>",
            unsafe_allow_html=True
        )

else:
    st.info("Please upload PDF files from the sidebar.")
