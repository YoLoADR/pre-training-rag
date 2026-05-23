"""
Bug v1 — Test : le dataset de test doit être distinct du dataset d'entraînement.

Applique d'abord le patch : git apply ateliers/atelier-06-finetune-vs-rag/bugs/v1.patch
Lance ensuite : pytest ateliers/atelier-06-finetune-vs-rag/bugs/test_v1.py -v

Le test ECHOUE si le bug est actif (train set = test set).
Le test PASSE quand tu utilises un fichier de test distinct.

Comportement observable avec le bug actif :
  evaluate_strategies() retourne Recall@1 = 1.00 pour toutes les stratégies.
  C'est "trop beau pour être vrai" — les questions ont été indexées avec leurs réponses.
"""

import json
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE / "data" / "qa_dataset"


def test_train_test_split_exists():
    """Des fichiers distincts train/test doivent exister dans data/qa_dataset/."""
    train_path = DATA_DIR / "concierge_qa_train.jsonl"
    test_path = DATA_DIR / "concierge_qa_test.jsonl"

    # Au moins un des deux doit exister pour que l'évaluation soit valide
    # Si un seul fichier existe, evaluate_pipeline.py doit utiliser une fraction test
    main_path = DATA_DIR / "concierge_qa.jsonl"

    if not main_path.exists() and not test_path.exists():
        # Dataset pas encore généré — skip le test
        import pytest
        pytest.skip("Dataset non généré — lance scripts/generate_qa_dataset.py d'abord")

    if test_path.exists() and train_path.exists():
        # Vérifier que les contenus sont différents
        train_data = [json.loads(l) for l in train_path.open() if l.strip()]
        test_data = [json.loads(l) for l in test_path.open() if l.strip()]

        train_questions = {d.get("input", d.get("question", "")) for d in train_data}
        test_questions = {d.get("input", d.get("question", "")) for d in test_data}

        overlap = train_questions & test_questions
        overlap_rate = len(overlap) / len(test_questions) if test_questions else 1.0

        assert overlap_rate < 0.3, (
            f"BUG ACTIF : {overlap_rate:.0%} des questions de test sont dans le train set ! "
            f"Un overlap > 30% signifie que l'évaluation mesure la mémorisation, pas la généralisation. "
            f"Questions en commun : {list(overlap)[:3]}"
        )


def test_evaluate_pipeline_uses_correct_path():
    """evaluate_pipeline.py ne doit pas utiliser TRAIN_QA_PATH comme source de test."""
    eval_path = pathlib.Path(__file__).resolve().parent.parent / "evaluate_pipeline.py"
    source = eval_path.read_text()

    assert "TRAIN_QA_PATH" not in source or "# BUG" not in source, (
        "BUG ACTIF : evaluate_pipeline.py contient TRAIN_QA_PATH utilisé pour charger les données. "
        "Le script d'évaluation doit utiliser QA_PATH (le dataset de test), pas le train set."
    )
