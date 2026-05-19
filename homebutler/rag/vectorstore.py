"""
Gestion des bases vectorielles :
  - FAISS  : documents statiques (notices, bail, DPE) — index fichier, perf maximale
  - ChromaDB : FAQ dynamiques — métadonnées, filtres, persistance JSON
"""

import os
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_core.documents import Document
from homebutler import config

# Modèle d'embeddings multilingue — ONNX quantisé via fastembed (pas de torch requis)
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_embeddings() -> FastEmbedEmbeddings:
    """Retourne le modèle d'embeddings (mis en cache dans ~/.cache/fastembed/)."""
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)


# ── FAISS ─────────────────────────────────────────────────────────────────────

def build_faiss_index(
    documents: list[Document],
    save_path: str | None = None,
    force_rebuild: bool = False,
) -> FAISS:
    """
    Construit (ou charge si existant) un index FAISS.
    force_rebuild=True recrée l'index même si un index existe déjà.
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
    allow_dangerous_deserialization=True requis depuis LangChain 0.1.x
    """
    path = path or config.FAISS_PATH
    embeddings = get_embeddings()
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True,  # requis depuis langchain 0.1.x
    )


# ── ChromaDB ──────────────────────────────────────────────────────────────────

def build_chroma_db(
    documents: list[Document],
    collection: str = "homebutler_docs",
    persist_dir: str | None = None,
) -> Chroma:
    """
    Crée ou met à jour une collection ChromaDB persistante.
    ChromaDB >= 0.4.x : utiliser PersistentClient (géré par le wrapper LangChain).
    """
    persist_dir = persist_dir or config.CHROMA_PATH
    print(f"  Construction ChromaDB ({len(documents)} chunks) → {persist_dir}")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection,
        persist_directory=persist_dir,
    )
    print(f"  ✓ ChromaDB sauvegardé dans {persist_dir}")
    return vectorstore


def load_chroma_db(
    collection: str = "homebutler_docs",
    persist_dir: str | None = None,
) -> Chroma:
    """Charge une collection ChromaDB existante."""
    persist_dir = persist_dir or config.CHROMA_PATH
    embeddings = get_embeddings()
    return Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
