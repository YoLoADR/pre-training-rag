"""
Bug v2 — BLEU score utilisé comme métrique de qualité du ton/style (analyse statique).

Le bug : evaluate_style_quality() utilise nltk BLEU pour mesurer la qualité des réponses.
BLEU est conçu pour la traduction automatique (chevauchement de n-grammes).
Il pénalise fortement les bonnes paraphrases qui utilisent un vocabulaire différent.
Pour le style conversationnel HomeButler, il vaut mieux : cosine similarity (embeddings),
BERTScore, ou un LLM-judge avec rubrique.

Applique le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v2.patch
Lance ensuite   : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v2.py -v

Le test ECHOUE si bleu_score est importé dans evaluate_pipeline.py.
Le test PASSE quand la fonction BLEU est supprimée (ou remplacée par une métrique adaptée).

Pas d'appel réseau — analyse statique de evaluate_pipeline.py.
"""

import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
EVAL_PATH = BASE_DIR / "ateliers" / "atelier-06-finetune-vs-rag" / "evaluate_pipeline.py"


def _get_source() -> str:
    return EVAL_PATH.read_text(encoding="utf-8")


def test_bleu_not_used_for_style():
    """evaluate_pipeline.py ne doit pas importer bleu_score."""
    source = _get_source()

    assert "bleu_score" not in source, (
        "BUG ACTIF : 'bleu_score' (nltk) trouvé dans evaluate_pipeline.py.\n"
        "BLEU est une métrique de traduction automatique — elle mesure le chevauchement\n"
        "de n-grammes, pas la qualité conversationnelle ni le ton.\n"
        "Une bonne réponse avec un vocabulaire différent de la référence obtient\n"
        "un BLEU très bas malgré une excellente qualité.\n"
        "Alternatives adaptées : cosine similarity (embeddings), BERTScore, LLM-judge."
    )


def test_no_sentence_bleu():
    """sentence_bleu ne doit pas être utilisé dans evaluate_pipeline.py."""
    source = _get_source()

    assert "sentence_bleu" not in source, (
        "BUG ACTIF : 'sentence_bleu' trouvé dans evaluate_pipeline.py.\n"
        "Supprime la fonction evaluate_style_quality() basée sur BLEU\n"
        "ou remplace-la par une métrique sémantique (ex: cosine similarity)."
    )
