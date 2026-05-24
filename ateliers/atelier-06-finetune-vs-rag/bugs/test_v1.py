"""
Bug v1 — evaluate_pipeline.py charge le train set au lieu du test set (analyse statique).

Le bug : TRAIN_QA_PATH (même fichier que QA_PATH) est utilisé dans load_qa().
Conséquence : le Recall@k paraît parfait (1.00) car les questions ont déjà été
indexées lors de l'entraînement — on mesure la mémorisation, pas la généralisation.

Applique le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v1.patch
Lance ensuite   : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v1.py -v

Le test ECHOUE si le bug est actif (TRAIN_QA_PATH dans evaluate_pipeline.py).
Le test PASSE quand load_qa() utilise QA_PATH (le dataset de test).

Pas d'appel réseau — analyse statique de evaluate_pipeline.py.
"""

import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent.parent
EVAL_PATH = BASE_DIR / "ateliers" / "atelier-06-finetune-vs-rag" / "evaluate_pipeline.py"


def _get_source() -> str:
    return EVAL_PATH.read_text(encoding="utf-8")


def test_no_train_qa_path():
    """evaluate_pipeline.py ne doit pas définir TRAIN_QA_PATH."""
    source = _get_source()

    assert "TRAIN_QA_PATH" not in source, (
        "BUG ACTIF : 'TRAIN_QA_PATH' trouvé dans evaluate_pipeline.py.\n"
        "Le script d'évaluation utilise le train set à la place du test set.\n"
        "Conséquence : Recall@k = 1.00 — illusion de performances parfaites.\n"
        "Fix : utiliser QA_PATH dans load_qa() (supprimer TRAIN_QA_PATH)."
    )


def test_load_qa_uses_qa_path():
    """load_qa() doit ouvrir QA_PATH, pas TRAIN_QA_PATH."""
    source = _get_source()

    # Le bug remplace `with QA_PATH.open()` par `with TRAIN_QA_PATH.open()`
    assert "TRAIN_QA_PATH.open()" not in source, (
        "BUG ACTIF : load_qa() ouvre TRAIN_QA_PATH au lieu de QA_PATH.\n"
        "Remplace 'TRAIN_QA_PATH.open()' par 'QA_PATH.open()' dans load_qa()."
    )


def test_qa_path_defined():
    """QA_PATH doit être défini dans evaluate_pipeline.py."""
    source = _get_source()

    assert "QA_PATH" in source, (
        "QA_PATH absent de evaluate_pipeline.py — le chemin du dataset de test "
        "doit être défini explicitement."
    )
