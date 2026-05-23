"""
Vectorstore FAISS — documents statiques (notices, bail, DPE).

Concept RAG : FAISS est une bibliothèque de recherche de voisins approximatifs
(ANN — Approximate Nearest Neighbors) développée par Meta. Elle indexe des
vecteurs (embeddings) et retrouve les plus proches en O(log n) au lieu de O(n).
Pour ~10k documents, FAISS répond en quelques millisecondes au lieu de secondes.

Index FAISS = fichier binaire sauvegardé sur disque (data/faiss_index/).
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from homebutler import config

# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT RAG : Modèle d'embeddings
# ───────────────────────────────────────────────────────────────────────────
# Un embedding transforme un texte en vecteur de 384 nombres (dimensions).
# Deux textes proches sémantiquement → vecteurs proches géométriquement.
# Ce modèle multilingue (FR/EN/...) est quantisé ONNX → léger, pas besoin
# de torch ni GPU. Téléchargé une fois dans ~/.cache/fastembed/ (~300 MB).
# ═══════════════════════════════════════════════════════════════════════════
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_embeddings() -> FastEmbedEmbeddings:
    """Retourne le modèle d'embeddings (mis en cache localement)."""
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)


def build_faiss_index(
    documents: list[Document],
    save_path: str | None = None,
    force_rebuild: bool = False,
) -> FAISS:
    """
    Construit (ou recharge) un index FAISS depuis une liste de chunks.

    Concept : `FAISS.from_documents` calcule l'embedding de chaque chunk
    puis l'insère dans l'index. La similarité par défaut = cosinus normalisé.
    """
    path = save_path or config.FAISS_PATH

    if os.path.exists(path) and not force_rebuild:
        print(f"  Index FAISS existant chargé depuis {path}")
        return load_faiss_index(path)

    print(f"  Construction de l'index FAISS ({len(documents)} chunks)...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(path)
    print(f"  ✓ Index FAISS sauvegardé dans {path}")
    return vectorstore


def load_faiss_index(path: str | None = None) -> FAISS:
    """
    Charge un index FAISS depuis le disque.
    `allow_dangerous_deserialization=True` requis depuis LangChain 0.1.x
    (FAISS utilise pickle, qui peut exécuter du code — OK ici car notre propre fichier).
    """
    path = path or config.FAISS_PATH
    embeddings = get_embeddings()
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True,
    )
