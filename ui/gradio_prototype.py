"""
Prototype Gradio — Interface chat minimaliste (~50 lignes).
Démonstration rapide J1-J2 de la formation RAFT.
Pré-requis : API FastAPI lancée sur http://localhost:8000
"""

import os
import requests
import gradio as gr

API_URL = os.getenv("API_URL", "http://localhost:8000")


def chat_with_butler(message: str, history: list) -> str:
    """Envoie le message à l'API HomeButler et retourne la réponse."""
    try:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"message": message, "session_id": "gradio"},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("response", "Pas de réponse.")
    except requests.exceptions.ConnectionError:
        return "❌ API non disponible. Lancez d'abord : `uvicorn api.main:app --port 8000`"
    except Exception as e:
        return f"❌ Erreur : {e}"


demo = gr.ChatInterface(
    fn=chat_with_butler,
    title="🏠 HomeButler AI",
    description=(
        "Votre conciergerie domestique intelligente. "
        "Posez vos questions sur votre logement, votre énergie ou les producteurs locaux."
    ),
    examples=[
        "Quelle température régler sur ma chaudière la nuit ?",
        "Ma consommation électrique de juin était-elle anormale ?",
        "Trouve-moi un producteur de légumes bio à moins de 15 km",
        "Il va faire -5°C demain, comment préparer ma maison et que manger de chaud ?",
        "Mon lave-linge fait un bruit bizarre en essorage, que faire ?",
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    print(f"HomeButler Gradio — API : {API_URL}")
    demo.launch(server_port=7860, share=False, show_error=True)
