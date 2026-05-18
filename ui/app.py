"""
Point d'entrée Streamlit multi-pages HomeButler AI.
Les pages sont dans ui/pages/ — Streamlit les détecte automatiquement.
"""

import streamlit as st

st.set_page_config(
    page_title="HomeButler AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🏠 HomeButler AI")
    st.caption("Votre conciergerie domestique intelligente")
    st.divider()
    st.markdown(
        """
        **Navigation :**
        - 💬 Chat — Posez vos questions
        - ⚡ Énergie — Tableau de bord
        - 🛒 Marketplace — Producteurs locaux
        - 🏠 Logement — Documents
        """
    )
    st.divider()

    import os
    from homebutler import config
    provider_emoji = "🤖" if config.LLM_PROVIDER == "anthropic" else "🦙"
    st.caption(f"{provider_emoji} LLM : `{config.LLM_PROVIDER}` / `{config.ANTHROPIC_MODEL if config.LLM_PROVIDER == 'anthropic' else config.OLLAMA_MODEL}`")

# ── Page d'accueil ─────────────────────────────────────────────────────────────
st.title("🏠 Bienvenue sur HomeButler AI")
st.markdown(
    """
    Votre conciergerie domestique intelligente — ici pour vous aider au quotidien.

    ### Ce que je peux faire pour vous

    | 💬 Chat | ⚡ Énergie | 🛒 Marketplace | 🏠 Logement |
    |---|---|---|---|
    | Questions sur votre logement | Analyse de consommation | Producteurs locaux | Vos documents |
    | Notices d'équipements | Détection d'anomalies | Artisans de quartier | DPE et conseils |
    | Droits et obligations | Conseils économies | Commande en ligne | Règlement copro |

    ### Pour commencer
    Utilisez le menu de navigation à gauche pour accéder aux différentes fonctionnalités.
    """
)

col1, col2 = st.columns(2)
with col1:
    st.info(
        "💡 **Astuce** : Posez une question complexe au chat comme\n\n"
        "*« Il va faire -5°C demain, que puis-je faire pour préparer ma maison "
        "et commander un bon repas chaud ? »*\n\n"
        "L'agent orchestre automatiquement météo, notices et producteurs locaux !"
    )
with col2:
    st.success(
        "✅ **Formation RAFT** : Ce projet couvre 100% du programme :\n"
        "- Jour 1 : RAG documentaire (FAISS + ChromaDB)\n"
        "- Jour 2 : Agent ReAct + Fine-tuning QLoRA\n"
        "- Jour 3 : Déploiement + Supervision LangSmith"
    )
