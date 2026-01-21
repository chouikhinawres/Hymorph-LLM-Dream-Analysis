import streamlit as st
from langdetect import detect, LangDetectException
import ollama

# -----------------------------
# Configuration page
# -----------------------------
st.set_page_config(
    page_title="Analyse de Rêve",
    layout="wide"
)

# -----------------------------
# CSS pour design pro
# -----------------------------
st.markdown("""
<style>
body { background-color: #ffffff; }
.block-container {
    background-color: #ffffff;
    color: #1f2937;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.08);
}
h1 { color: #111827; font-weight: 700; }
textarea {
    border-radius: 12px !important;
    border: 1px solid #d1d5db !important;
    padding: 12px !important;
    font-size: 15px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #3b82f6);
    color: white; border: none; border-radius: 14px;
    padding: 0.6em 1.6em; font-size: 16px; font-weight: 600;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 6px 18px rgba(99,102,241,0.35);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 10px 24px rgba(59,130,246,0.45);
    background: linear-gradient(135deg, #4f46e5, #2563eb);
}
.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<h1 style="text-align:center; font-weight:800; color:#111827;">
🔓✨ Découvrez la Signification de Vos Rêves 🌙💭
</h1>
<p style="text-align:center; font-size:18px; color:#6b7280;">
Interprétation symbolique dans la même langue que votre rêve
</p>
""", unsafe_allow_html=True)

# -----------------------------
# Input du rêve
# -----------------------------
dream_text = st.text_area(
    "Entrez votre rêve ici :",
    height=200,
    placeholder="Exemple : حلمت اللي سنّي طاح وحطيتو في بلاصتو..."
)

# -----------------------------
# Bouton Analyse
# -----------------------------
if st.button("✨ Analyser le rêve"):
    if not dream_text.strip():
        st.warning("Veuillez entrer un rêve avant de cliquer sur 'Analyser'.")
    else:
        # Détection langue
        try:
            lang = detect(dream_text)
        except LangDetectException:
            lang = "unknown"

        # Prompt optimisé pour rêves absurdes et symboliques
        prompt = f"""
You are an expert dream interpreter. The dream may be illogical or absurd. 
Focus on **symbolic meaning only**. Do not invent unrelated stories.
Reply in the **same language as the dream**.

Dream text:
{dream_text}
"""

        # Spinner pendant traitement
        with st.spinner("Analyse en cours... Cela peut prendre quelques secondes."):
            try:
                response = ollama.chat(
                    model="mistral:latest",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that interprets dreams."},
                        {"role": "user", "content": prompt}
                    ]
                )

                st.subheader("🧠 Résultat de l'analyse")
                st.write(response["message"]["content"])

            except Exception as e:
                st.error(f"Erreur lors de la communication avec Ollama : {e}")
