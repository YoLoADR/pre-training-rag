"""
═══════════════════════════════════════════════════════════════════════════
Atelier 02 — Évaluation RAG avec 4 métriques RAGAs (OPTIONNEL)
═══════════════════════════════════════════════════════════════════════════

Aligné sur Slide 8 Chapitre 2 — Métriques RAGAs.

Ce script utilise une évaluation LLM-as-a-judge MINIMALE (pas la lib `ragas`
officielle pour éviter une dépendance lourde). Il calcule 4 métriques sur
quelques questions étalons :

  1. Faithfulness       — le LLM invente-t-il des infos non présentes dans
                          les chunks ? (ancrage factuel)
  2. Answer Relevance   — la réponse répond-elle réellement à la question ?
  3. Context Precision  — les chunks retournés sont-ils pertinents
                          (vs noyés dans du bruit) ?
  4. Context Recall     — les chunks contiennent-ils l'info nécessaire ?

Lancer : python ateliers/atelier-02-rag-simple/evaluate_rag.py

NOTE — Reranking (Slide 7 Chapitre 2) :
On pourrait améliorer la précision en ajoutant un re-ranker (cross-encoder)
après le retriever. Hors-scope de cet atelier mais à mentionner.
═══════════════════════════════════════════════════════════════════════════
"""

from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from homebutler.llm.provider import get_llm
from homebutler.llm.prompts import RAG_QA_TEMPLATE
from homebutler.rag.ingestion import ingest_all_documents
from homebutler.rag.vectorstore_faiss import build_faiss_index


QUESTIONS_ETALONS = [
    {
        "question": "Quelle est la marque de ma chaudière ?",
        "ground_truth": "Viessmann Vitodens 100-W",
    },
    {
        "question": "Comment purger les radiateurs ?",
        "ground_truth": "Ouvrir le robinet de purge en haut du radiateur jusqu'à ce que l'eau coule sans air.",
    },
    {
        "question": "Quelle est la durée du bail ?",
        "ground_truth": "3 ans pour un logement vide loué par un particulier (loi du 6 juillet 1989).",
    },
]


def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata.get('source')} p.{d.metadata.get('page')}]\n{d.page_content}"
        for d in docs
    )


# ─── LLM-as-a-judge : prompts de notation ─────────────────────────────────
JUDGE_FAITHFULNESS = """Tu es un évaluateur strict. Voici une RÉPONSE et son CONTEXTE source.
Note de 0 à 1 si chaque affirmation de la réponse est SUPPORTÉE par le contexte.
1.0 = toutes les affirmations sont dans le contexte. 0.0 = la réponse invente.
Réponds par un seul nombre entre 0 et 1.

CONTEXTE :
{context}

RÉPONSE :
{answer}

Note (0-1) :"""

JUDGE_RELEVANCE = """Note de 0 à 1 à quel point la RÉPONSE répond à la QUESTION.
1.0 = répond directement et complètement. 0.0 = hors-sujet.
Réponds par un seul nombre.

QUESTION : {question}
RÉPONSE : {answer}

Note (0-1) :"""

JUDGE_CONTEXT_RECALL = """Voici la VRAIE RÉPONSE (ground truth) et le CONTEXTE récupéré.
Note de 0 à 1 si le contexte contient l'information nécessaire pour la
vraie réponse.
1.0 = info présente. 0.0 = info absente.
Réponds par un seul nombre.

VRAIE RÉPONSE : {ground_truth}
CONTEXTE : {context}

Note (0-1) :"""


def parse_score(text: str) -> float:
    """Extrait un float entre 0 et 1 du texte du juge."""
    import re
    m = re.search(r"(\d+\.?\d*)", text)
    return min(max(float(m.group(1)), 0.0), 1.0) if m else 0.0


def main() -> None:
    print("Construction de l'index sur les PDFs existants...")
    chunks = ingest_all_documents(strategy="recursive")
    faiss_store = build_faiss_index(chunks, force_rebuild=False)
    retriever = faiss_store.as_retriever(search_kwargs={"k": 4})

    llm = get_llm(temperature=0.1)
    judge = get_llm(temperature=0.0)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_QA_TEMPLATE | llm | StrOutputParser()
    )

    print(f"\nÉvaluation sur {len(QUESTIONS_ETALONS)} questions :\n")
    totals = {"faithfulness": 0.0, "relevance": 0.0, "context_recall": 0.0}

    for item in QUESTIONS_ETALONS:
        q = item["question"]
        gt = item["ground_truth"]
        docs = retriever.invoke(q)
        context = format_docs(docs)
        answer = rag_chain.invoke(q)

        f_score = parse_score(judge.invoke([HumanMessage(content=JUDGE_FAITHFULNESS.format(context=context, answer=answer))]).content)
        r_score = parse_score(judge.invoke([HumanMessage(content=JUDGE_RELEVANCE.format(question=q, answer=answer))]).content)
        cr_score = parse_score(judge.invoke([HumanMessage(content=JUDGE_CONTEXT_RECALL.format(ground_truth=gt, context=context))]).content)

        totals["faithfulness"]   += f_score
        totals["relevance"]      += r_score
        totals["context_recall"] += cr_score

        print(f"  Q: {q}")
        print(f"     Faithfulness={f_score:.2f}  Relevance={r_score:.2f}  ContextRecall={cr_score:.2f}\n")

    n = len(QUESTIONS_ETALONS)
    print("─" * 60)
    print(f"  Moyenne Faithfulness     : {totals['faithfulness']/n:.2f}")
    print(f"  Moyenne Answer Relevance : {totals['relevance']/n:.2f}")
    print(f"  Moyenne Context Recall   : {totals['context_recall']/n:.2f}")
    print("\nContext Precision : non implémenté ici (nécessite annotation manuelle des chunks).")


if __name__ == "__main__":
    main()
