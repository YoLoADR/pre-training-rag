"""
Page Chat — Interface conversationnelle avec l'agent ReAct HomeButler.
"""

import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("💬 Chat avec HomeButler")
st.caption("Posez vos questions sur votre logement, votre énergie ou les producteurs locaux")

# ── Initialisation de l'historique ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Bonjour ! Je suis HomeButler, votre conciergerie domestique intelligente. "
                "Je peux vous aider avec :\n"
                "- Les équipements de votre logement (chaudière, VMC, lave-linge...)\n"
                "- Votre consommation énergétique\n"
                "- Les producteurs et artisans locaux\n\n"
                "Comment puis-je vous aider aujourd'hui ?"
            ),
        }
    ]

# ── Affichage de l'historique ─────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Exemples rapides ─────────────────────────────────────────────────────────
with st.expander("💡 Exemples de questions", expanded=False):
    examples = [
        "Quelle température régler sur ma chaudière la nuit ?",
        "Ma consommation électrique de juin était-elle anormale ?",
        "Trouve-moi un producteur de légumes bio à moins de 15 km",
        "Il va faire -5°C demain, comment préparer ma maison ?",
        "Mon lave-linge affiche E18, que faire ?",
        "Quel est mon préavis pour quitter l'appartement ?",
        "Quelles aides pour rénover mon logement ?",
    ]
    cols = st.columns(2)
    for i, ex in enumerate(examples):
        if cols[i % 2].button(f"📝 {ex[:50]}...", key=f"ex_{i}", use_container_width=True):
            st.session_state._pending_message = ex

# ── Traitement du message ─────────────────────────────────────────────────────
if prompt := st.chat_input("Posez votre question...") or st.session_state.pop("_pending_message", None):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appeler l'API et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("HomeButler réfléchit..."):
            try:
                resp = requests.post(
                    f"{API_URL}/chat",
                    json={"message": prompt, "session_id": "streamlit"},
                    timeout=120,
                )
                resp.raise_for_status()
                response_text = resp.json().get("response", "Pas de réponse.")
            except requests.exceptions.ConnectionError:
                response_text = (
                    "❌ Je ne peux pas joindre l'API. "
                    "Vérifiez que `uvicorn api.main:app --port 8000` est lancé."
                )
            except Exception as e:
                response_text = f"❌ Erreur : {e}"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# ── Bouton reset ──────────────────────────────────────────────────────────────
if st.button("🗑 Effacer la conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()
