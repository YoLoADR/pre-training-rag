"""
═══════════════════════════════════════════════════════════════════════════
Atelier 04 — Préparation du dataset Q/R pour le fine-tuning
═══════════════════════════════════════════════════════════════════════════

Génère le dataset, vérifie le format Alpaca, montre un split 80/10/10.

Pré-requis : pandas, numpy (déjà dans requirements_atelier04.txt).

Lancer : python ateliers/atelier-04-finetuning/prepare_dataset.py
═══════════════════════════════════════════════════════════════════════════
"""

import json
import os
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET = BASE_DIR / "data" / "qa_dataset" / "concierge_qa.jsonl"


def ensure_dataset() -> None:
    """Génère le dataset s'il n'existe pas."""
    if DATASET.exists():
        return
    print(f"Dataset absent — génération via scripts/generate_qa_dataset.py")
    subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "generate_qa_dataset.py")],
                   check=True)


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def categorize(pair: dict) -> str:
    """Classifie une paire par mot-clé dans la question (heuristique simple)."""
    q = pair["input"].lower()
    if any(k in q for k in ("chaudière", "radiateur", "vmc", "lave-linge", "frigo", "chauffe-eau")):
        return "équipements"
    if any(k in q for k in ("bail", "loyer", "préavis", "caution", "syndic", "copropriété", "droits")):
        return "droits"
    if any(k in q for k in ("consommation", "énergie", "kwh", "facture", "dpe", "électricité")):
        return "énergie"
    if any(k in q for k in ("producteur", "artisan", "plombier", "légumes", "marketplace", "boulanger")):
        return "marketplace"
    return "autres"


# ═══════════════════════════════════════════════════════════════════════════
# FT CONCEPT : Format Alpaca / Instruction
# ───────────────────────────────────────────────────────────────────────────
# Format standard pour fine-tuner un modèle "instruction-following" :
#   {"instruction": "...",   ← consigne système ("Tu es HomeButler...")
#    "input":       "...",   ← entrée utilisateur (la question)
#    "output":      "..."}   ← sortie attendue (la réponse "ton conciergerie")
# Le trainer transforme ça en prompt brut :
#   <s>[INST] {instruction}\n{input} [/INST] {output} </s>
# ═══════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════
# FT CONCEPT : Split 80/10/10 (train / val / test)
# ───────────────────────────────────────────────────────────────────────────
# train : optimiser les poids LoRA
# val   : détecter l'overfitting (val_loss qui remonte = stop training)
# test  : évaluer le modèle final (PPL, F1) — JAMAIS vu pendant l'entraînement
# Le split aléatoire est suffisant pour 150 paires homogènes.
# ═══════════════════════════════════════════════════════════════════════════
def split_train_val_test(pairs: list[dict], seed: int = 42):
    rng = random.Random(seed)
    shuffled = pairs[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_train = int(n * 0.8)
    n_val   = int(n * 0.1)
    return (
        shuffled[:n_train],
        shuffled[n_train : n_train + n_val],
        shuffled[n_train + n_val :],
    )


def main() -> None:
    ensure_dataset()
    pairs = load_jsonl(DATASET)
    print(f"Dataset : {DATASET}")
    print(f"Total : {len(pairs)} paires Q/R")

    # ─── Format Alpaca — vérifier les clés ──────────────────────────────
    required = {"instruction", "input", "output"}
    ok = all(required.issubset(p.keys()) for p in pairs)
    print(f"Format Alpaca complet : {'✓' if ok else '✗'}")

    # ─── Distribution par catégorie ─────────────────────────────────────
    cats = Counter(categorize(p) for p in pairs)
    print("\nDistribution par catégorie :")
    for cat, n in cats.most_common():
        bar = "█" * int(n * 30 / max(cats.values()))
        print(f"  {cat:14s} {n:3d}  {bar}")

    # ─── Échantillon (1 paire) ──────────────────────────────────────────
    print("\nExemple de paire (format Alpaca) :")
    print(json.dumps(pairs[0], indent=2, ensure_ascii=False))
    print("\nForme brute attendue par le trainer :")
    print(f"  <s>[INST] {pairs[0]['instruction']}\\n{pairs[0]['input']} [/INST] {pairs[0]['output'][:60]}... </s>")

    # ─── Split 80/10/10 ─────────────────────────────────────────────────
    train, val, test = split_train_val_test(pairs)
    print(f"\nSplit 80/10/10 : train={len(train)}  val={len(val)}  test={len(test)}")

    # ─── Sauvegarde des splits pour le notebook FT ─────────────────────
    out_dir = DATASET.parent
    for name, subset in (("train", train), ("val", val), ("test", test)):
        out = out_dir / f"concierge_qa_{name}.jsonl"
        with out.open("w") as f:
            for p in subset:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        print(f"  → {out.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
