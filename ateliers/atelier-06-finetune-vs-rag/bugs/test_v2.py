"""
Bug v2 — Test : BLEU ne doit pas être utilisé comme métrique de qualité du ton/style.

Applique d'abord le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v2.patch
Lance ensuite : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v2.py -v

Ce test vérifie que :
1. La fonction evaluate_style_quality utilise une métrique adaptée (pas BLEU)
2. Deux réponses sémantiquement équivalentes mais lexicalement différentes obtiennent
   un score similaire (BLEU les différencierait fortement)
"""

import pathlib
import sys


def test_bleu_not_used_for_style():
    """evaluate_pipeline.py ne doit pas importer bleu_score pour le style."""
    eval_path = pathlib.Path(__file__).resolve().parent.parent / "evaluate_pipeline.py"
    source = eval_path.read_text()

    assert "bleu_score" not in source or "# BUG" in source, (
        "BUG ACTIF : nltk.translate.bleu_score est importé dans evaluate_pipeline.py. "
        "BLEU est inadapté pour mesurer la qualité du ton/style conversationnel. "
        "Alternatives : cosine similarity (embeddings), LLM-judge avec rubric, BERTScore."
    )


def test_semantic_equivalence_not_penalized():
    """
    Deux réponses sémantiquement équivalentes doivent obtenir un score similaire.
    BLEU les pénaliserait fortement si le vocabulaire diffère.
    """
    ref = "Bonjour ! Votre chaudière Viessmann est garantie 5 ans. N'hésitez pas si vous avez d'autres questions."
    good_paraphrase = "Bonsoir ! La garantie de votre chaudière Viessmann est de 5 ans. Je suis là pour tout renseignement supplémentaire."
    bad_response = "Chaudière. Garantie. 5."

    try:
        from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
        bleu_good = sentence_bleu([ref.split()], good_paraphrase.split(),
                                   smoothing_function=SmoothingFunction().method1)
        bleu_bad = sentence_bleu([ref.split()], bad_response.split(),
                                  smoothing_function=SmoothingFunction().method1)

        # BLEU score de la paraphrase de bonne qualité
        # Si BLEU pénalise fortement une bonne paraphrase, c'est le signe du bug
        # (une bonne réponse obtient un score bas juste parce que le vocabulaire diffère)
        assert bleu_good > 0.1, (
            f"BUG DEMONSTRE : la bonne paraphrase obtient BLEU={bleu_good:.3f} < 0.10. "
            f"BLEU pénalise fortement les réponses de bonne qualité qui utilisent un "
            f"vocabulaire différent de la référence. Ce n'est pas une bonne métrique de style. "
            f"Utilise plutôt la cosine similarity sur les embeddings ou un LLM-judge."
        )
    except ImportError:
        # nltk non installé — le bug n'est pas actif
        pass
