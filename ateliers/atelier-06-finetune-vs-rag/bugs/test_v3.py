"""
Bug v3 — Mesure de latence sur 1 seul appel, biais cold-start (analyse statique).

Le bug :
  1. compare_modes() utilise questions[0] — seule la 1ère question est traitée.
  2. latencies[mode] = [elapsed] écrase au lieu d'accumuler (append).
Conséquence : la latence affichée est celle du 1er appel (cold-start), souvent
2-5x plus lente que la latence réelle. Les résultats semblent toujours mauvais.

Applique le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v3.patch
Lance ensuite   : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v3.py -v

Le test ECHOUE si questions[0] ou latencies[mode] = [elapsed] sont présents.
Le test PASSE quand la boucle itère sur toutes les questions et accumule les latences.

Pas d'appel réseau — analyse statique de evaluate_pipeline.py.
"""

import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
EVAL_PATH = BASE_DIR / "ateliers" / "atelier-06-finetune-vs-rag" / "evaluate_pipeline.py"


def _get_source() -> str:
    return EVAL_PATH.read_text(encoding="utf-8")


def test_no_single_question_selection():
    """compare_modes() ne doit pas utiliser questions[0] — seule la 1ère question."""
    source = _get_source()

    assert "questions[0]" not in source, (
        "BUG ACTIF : 'questions[0]' trouvé dans evaluate_pipeline.py.\n"
        "compare_modes() mesure uniquement la 1ère question — biais cold-start.\n"
        "Le premier appel initialise l'agent, le vectorstore, etc. → 2-5x plus lent.\n"
        "Fix : utiliser 'for q in questions:' pour itérer sur toutes les questions."
    )


def test_no_latency_overwrite():
    """latencies[mode] doit utiliser .append(), pas une assignation = [elapsed]."""
    source = _get_source()

    assert "latencies[mode] = [elapsed]" not in source, (
        "BUG ACTIF : 'latencies[mode] = [elapsed]' trouvé dans evaluate_pipeline.py.\n"
        "L'assignation écrase les valeurs précédentes — on ne conserve que la dernière mesure.\n"
        "Fix : remplacer par 'latencies[mode].append(elapsed)' pour accumuler toutes les mesures."
    )


def test_latencies_use_append():
    """latencies[mode].append() doit être utilisé pour accumuler les latences."""
    source = _get_source()

    assert "latencies[mode].append(elapsed)" in source, (
        "latencies[mode].append(elapsed) absent de evaluate_pipeline.py.\n"
        "La boucle doit accumuler les latences pour calculer moyenne et médiane "
        "sur l'ensemble des questions testées."
    )
