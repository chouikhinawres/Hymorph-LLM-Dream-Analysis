# Hymorph-LLM-Dream-Analysis

## Description
Hymorph est une application d’IA générative pour l’interprétation automatique des rêves. Le projet combine **Streamlit**, un **Large Language Model (LLM) via Ollama**,
et une approche **RAG (Retrieval-Augmented Generation)** pour analyser le texte des rêves.  
Il comprend deux interfaces principales :  
1. **Interface Admin / Livre** : permet de déposer et gérer les documents que le modèle utilisera pour apprendre et enrichir ses interprétations.  
2. **Interface Utilisateur** : permet à l’utilisateur de saisir la description de son rêve et de recevoir une interprétation générée par le modèle, enrichie par le contenu des livres déposés.  

## Architecture
Flux global du projet :

Admin (upload livre) -> RAG -> LLM -> Streamlit -> Output pour User
User (saisie du rêve) -> Streamlit -> LLM (avec RAG) -> Output

- **User** : saisie de la description du rêve dans l’interface Streamlit
- **Admin** : dépôt du livre pour enrichir le modèle  
- **Streamlit** : application web qui reçoit et envoie les données  
- **Ollama** : API qui interagit avec le LLM  
- **LLM** : modèle génératif qui analyse le texte et produit une interprétation  
- **Output** : retour de l’interprétation dans l’interface utilisateur  

## Installation
1. Cloner le dépôt :
git clone https://github.com/ton-compte/Hymorph-LLM-Dream-Analysis.git ``

1.Installer les dépendances :
pip install -r requirements.txt

2.Lancer l’application Streamlit :
admin : streamlit run app/main.py
user  : streamlit run app/dream_app.py



streamlit run app/dream_app.py

