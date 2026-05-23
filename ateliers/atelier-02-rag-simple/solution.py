"""
═══════════════════════════════════════════════════════════════════════════
Atelier 02 — RAG Simple FAISS (solution corrigée + commentaires)
═══════════════════════════════════════════════════════════════════════════

Pipeline RAG complet : PDF → chunks → embeddings → FAISS → retriever → LLM.

Lancer : python ateliers/atelier-02-rag-simple/solution.py
═══════════════════════════════════════════════════════════════════════════
"""

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from homebutler import config
from homebutler.llm.provider import get_llm
from homebutler.llm.prompts import RAG_QA_TEMPLATE
from homebutler.rag.ingestion import (
    load_pdf_with_metadata,
    chunk_fixed_size,
    chunk_recursive,
)
from homebutler.rag.vectorstore_faiss import build_faiss_index


BENCHMARK_QUESTIONS = [
    ("Quelle est la marque de ma chaudière ?",      "notice_chaudiere.pdf"),
    ("Code erreur F4 chaudière",                    "notice_chaudiere.pdf"),
    ("Comment purger les radiateurs ?",             "notice_chaudiere.pdf"),
    ("Quel est le filtre de la VMC à nettoyer ?",   "notice_vmc.pdf"),
    ("Quelle est la durée du bail ?",               "bail.pdf"),
]


# ═══════════════════════════════════════════════════════════════════════════
# CONCEPT RAG : Pourquoi formatter les documents avec leur source ?
# ───────────────────────────────────────────────────────────────────────────
# On veut que le LLM cite SES sources dans la réponse (vérifiabilité).
# Le format `[source p.X]\n<contenu>` est une convention simple et robuste.
# Le system prompt RAG_QA_TEMPLATE demande au LLM de réutiliser ce format
# pour ses citations.
# ═══════════════════════════════════════════════════════════════════════════
def format_docs(docs: list) -> str:
    return "\n\n".join(
        f"[{d.metadata.get('source')} p.{d.metadata.get('page')}]\n{d.page_content}"
        for d in docs
    )


def main() -> None:
    docs_dir = config.DOCUMENTS_DIR
    if not os.path.exists(docs_dir) or not os.listdir(docs_dir):
        print("PDFs absents — lancer : python scripts/generate_documents.py")
        return

    # ─── Étape 1 : charger les pages PDF ────────────────────────────────
    pages = []
    for f in sorted(os.listdir(docs_dir)):
        if f.endswith(".pdf"):
            pages.extend(load_pdf_with_metadata(os.path.join(docs_dir, f)))
    print(f"  {len(pages)} pages chargées")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : Comparer les stratégies de chunking
    # ──────────────────────────────────────────────────────────────────
    # Fixed-size (CharacterTextSplitter)     → coupe brutalement à N chars
    # Recursive (RecursiveCharacterText...)  → essaie \n\n → \n → . → espace
    # Semantic (SemanticChunker)             → coupe sur rupture de cohérence
    # Recommandé par défaut : recursive.
    # ═══════════════════════════════════════════════════════════════════
    chunks_fixed = chunk_fixed_size(pages, chunk_size=512, chunk_overlap=50)
    chunks_rec   = chunk_recursive(pages, chunk_size=512, chunk_overlap=50)
    print(f"  chunks_fixed     : {len(chunks_fixed)}")
    print(f"  chunks_recursive : {len(chunks_rec)}")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : Index FAISS
    # ──────────────────────────────────────────────────────────────────
    # build_faiss_index() :
    #   1. Calcule un embedding 384-dim pour chaque chunk (modèle multilingual)
    #   2. Construit un index ANN (Approximate Nearest Neighbors)
    #   3. Sauvegarde le tout dans data/faiss_index/ (fichier binaire)
    # Au prochain run, on rechargera l'index sans tout recalculer.
    # ═══════════════════════════════════════════════════════════════════
    faiss_store = build_faiss_index(chunks_rec, force_rebuild=True)

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : Retriever MMR (Maximal Marginal Relevance)
    # ──────────────────────────────────────────────────────────────────
    # similarity_search retourne les k plus proches → risque de doublons.
    # MMR pénalise la redondance : retourne k résultats à la fois pertinents
    # ET diversifiés (utile sur des PDFs où la même info se répète).
    # ═══════════════════════════════════════════════════════════════════
    retriever = faiss_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 20},
    )

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : LCEL — LangChain Expression Language
    # ──────────────────────────────────────────────────────────────────
    # Le pipe `|` compose des "Runnables" : chaque étape transforme la sortie
    # de la précédente. Plus transparent que la chaîne RetrievalQA classique :
    #   {context: retriever→format, question: passthrough}
    #     → injection dans le prompt template
    #     → appel LLM
    #     → parsing en string
    # ═══════════════════════════════════════════════════════════════════
    llm = get_llm(temperature=0.1)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_QA_TEMPLATE | llm | StrOutputParser()
    )

    # ─── Question fil rouge HomeButler ──────────────────────────────────
    q = "Quelle est la marque de ma chaudière ?"
    print(f"\n═══ Question : {q}")
    print(f"\n→ {rag_chain.invoke(q)}")

    # ═══════════════════════════════════════════════════════════════════
    # CONCEPT RAG : Recall@k
    # ──────────────────────────────────────────────────────────────────
    # Sur N questions étalons, combien obtiennent au moins un chunk pertinent
    # dans les k premiers résultats du retriever ? Métrique principale pour
    # comparer chunking strategies, embeddings, retrievers.
    # Objectif : Recall@5 ≥ 80 % pour le projet HomeButler.
    # ═══════════════════════════════════════════════════════════════════
    print(f"\n═══ Évaluation Recall@k sur {len(BENCHMARK_QUESTIONS)} questions")
    for k in (1, 3, 5):
        hits = 0
        for q, expected in BENCHMARK_QUESTIONS:
            results = faiss_store.similarity_search(q, k=k)
            if any(r.metadata.get("source") == expected for r in results):
                hits += 1
        print(f"  Recall@{k} = {hits}/{len(BENCHMARK_QUESTIONS)} = {hits/len(BENCHMARK_QUESTIONS):.0%}")


if __name__ == "__main__":
    main()
