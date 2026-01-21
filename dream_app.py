import streamlit as st
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
import ollama

st.set_page_config(page_title="Analyse de Rêve avec ", layout="wide")
st.title("💭 Analyse de Rêve (Ollama + Mistral)")

dream_text = st.text_area("Entrez votre rêve ici :", height=200)

if st.button("Analyser le rêve"):
    if dream_text.strip() == "":
        st.warning("Veuillez entrer un rêve avant de cliquer sur 'Analyser'.")
    else:
        try:
            lang = detect(dream_text)
        except LangDetectException:
            lang = "inconnue"

        # Ne traduire que si nécessaire, sinon garder la langue d’origine
        if lang != "en":
            translated_text = GoogleTranslator(source='auto', target='en').translate(dream_text)
        else:
            translated_text = dream_text

        prompt = f"Analyse ce rêve et explique-le de façon claire, détaillée et empathique :\n\n{translated_text}"

        try:
            response = ollama.chat(
                model="mistral:latest",  # modèle que tu as installé
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that interprets dreams."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.subheader("Résultat de l'analyse :")
            # Afficher dans la langue d’origine
            if lang != "en":
                # traduire la réponse en français si le rêve était en français
                final_output = GoogleTranslator(source='en', target=lang).translate(response["message"]["content"])
            else:
                final_output = response["message"]["content"]
            st.write(final_output)

        except Exception as e:
            st.error(f"Erreur lors de la communication avec Ollama : {e}")
