"""
Bug v3 — Test : la latence doit être mesurée sur >= 5 appels (pas 1 seul).

Applique d'abord le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v3.patch
Lance ensuite : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v3.py -v

Comportement observable avec le bug actif :
  show_latency_summary() affiche une seule valeur par mode — pas de variance observable.
  Le premier appel (cold start) est souvent 2-5x plus long que les suivants.
  En mesurant seulement ce 1er appel, on sur-estime systématiquement la latence.
"""

import ast
import pathlib


def test_compare_modes_uses_multiple_questions():
    """compare_modes() doit itérer sur toutes les questions, pas juste la première."""
    eval_path = pathlib.Path(__file__).resolve().parent.parent / "evaluate_pipeline.py"
    source = eval_path.read_text()

    # Vérifier les signes du bug : utilisation de questions[0] ou boucle cassée
    assert "questions[0]" not in source, (
        "BUG ACTIF : compare_modes() utilise 'questions[0]' — seule la première question "
        "est testée. La latence mesurée sur 1 appel est biaisée par le cold-start. "
        "Le premier appel initialise l'agent, le vectorstore, etc. → 2-5x plus lent. "
        "Fix : itérer sur toutes les questions et ignorer le premier appel dans le calcul."
    )


def test_latencies_list_has_multiple_values():
    """
    Simule un appel à compare_modes() et vérifie que les listes de latences
    contiennent plus d'un élément.
    """
    eval_path = pathlib.Path(__file__).resolve().parent.parent / "evaluate_pipeline.py"
    source = eval_path.read_text()

    # Recherche de "latencies[mode] = [elapsed]" qui écrase au lieu d'accumuler
    assert "latencies[mode] = [elapsed]" not in source, (
        "BUG ACTIF : 'latencies[mode] = [elapsed]' trouvé — l'assignation écrase "
        "les valeurs précédentes au lieu de les accumuler. "
        "Doit être 'latencies[mode].append(elapsed)' pour collecter toutes les mesures."
    )


def test_minimum_sample_size_for_latency():
    """
    Vérifie que compare_modes() est appelé avec >= 5 questions dans main().
    Mesurer la latence sur < 5 appels est insuffisant statistiquement.
    """
    eval_path = pathlib.Path(__file__).resolve().parent.parent / "evaluate_pipeline.py"
    source = eval_path.read_text()

    # Cherche l'appel à compare_modes dans main() — doit passer au moins 5 questions
    # Approximation : on cherche [:5] ou la variable questions avec >= 5 éléments
    if "questions[:1]" in source or "questions[:2]" in source:
        raise AssertionError(
            "BUG ACTIF : compare_modes() est appelé avec moins de 5 questions. "
            "Pour une mesure de latence fiable : >= 5 appels, ignorer le 1er (warm-up). "
            "Recommandé : 10 questions, p50 et p95 calculés sur les 9 dernières."
        )
