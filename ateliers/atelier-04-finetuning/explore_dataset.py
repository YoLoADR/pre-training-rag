"""
═══════════════════════════════════════════════════════════════════════════
Atelier 04 — Exploration / quality check du dataset Q/R
═══════════════════════════════════════════════════════════════════════════

Stats : longueurs questions/réponses, paires anormales, équilibre catégories.

Lancer : python ateliers/atelier-04-finetuning/explore_dataset.py
═══════════════════════════════════════════════════════════════════════════
"""

import json
from collections import Counter
from pathlib import Path
from statistics import mean, median

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET = BASE_DIR / "data" / "qa_dataset" / "concierge_qa.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


# ═══════════════════════════════════════════════════════════════════════════
# FT CONCEPT : Quality checks avant fine-tuning
# ───────────────────────────────────────────────────────────────────────────
# Avant de lancer un entraînement coûteux, on inspecte le dataset pour :
#   - détecter les doublons (questions identiques → biais)
#   - vérifier les longueurs (>512 tokens = truncation pendant le training)
#   - détecter les paires courtes/anormales (réponses < 20 tokens = pauvre signal)
#   - équilibrer les catégories (pas 90 % d'une seule classe)
# Un mauvais dataset = aucune amélioration possible, même avec le meilleur GPU.
# ═══════════════════════════════════════════════════════════════════════════
def main() -> None:
    if not DATASET.exists():
        print(f"Dataset absent : {DATASET}")
        print("Lance d'abord : python ateliers/atelier-04-finetuning/prepare_dataset.py")
        return

    pairs = load_jsonl(DATASET)
    print(f"Dataset : {len(pairs)} paires\n")

    # ─── Longueurs (proxy tokens : chars / 4) ──────────────────────────
    q_lens = [len(p["input"]) for p in pairs]
    a_lens = [len(p["output"]) for p in pairs]

    def stats(arr, label, hard_max=None):
        print(f"  {label}")
        print(f"    moy  : {mean(arr):.0f} chars (~{mean(arr)/4:.0f} tokens)")
        print(f"    med  : {median(arr):.0f}")
        print(f"    min  : {min(arr)}    max : {max(arr)}")
        if hard_max:
            n_over = sum(1 for x in arr if x > hard_max)
            print(f"    > {hard_max} chars : {n_over} paires (à vérifier — truncation possible)")

    stats(q_lens, "Longueur QUESTION", hard_max=512)
    print()
    stats(a_lens, "Longueur RÉPONSE",  hard_max=2048)

    # ─── Paires anormales ───────────────────────────────────────────────
    too_short = [p for p in pairs if len(p["output"]) < 80]   # ~20 tokens
    too_long  = [p for p in pairs if len(p["output"]) > 2048] # ~512 tokens
    print(f"\n  Réponses très courtes (<80 chars) : {len(too_short)}")
    print(f"  Réponses très longues (>2048 chars): {len(too_long)}")

    # ─── Doublons ───────────────────────────────────────────────────────
    dup = Counter(p["input"] for p in pairs)
    duplicates = {k: v for k, v in dup.items() if v > 1}
    print(f"  Questions dupliquées : {len(duplicates)}")
    if duplicates:
        for q, n in list(duplicates.items())[:3]:
            print(f"     [{n}×] {q[:80]}")

    # ─── Équilibre instruction ──────────────────────────────────────────
    instructions = Counter(p["instruction"] for p in pairs)
    print(f"\n  Variantes d'instruction (system prompt) : {len(instructions)}")
    for instr, n in instructions.most_common(3):
        print(f"    [{n}×] {instr[:80]}")

    print("\n─── À RETENIR ──────────────────────────────────────────────")
    print("  • Le format Alpaca attend instruction + input + output.")
    print("  • Si certaines paires dépassent 512 tokens : augmenter max_seq_length")
    print("    dans le notebook ou tronquer ces paires.")
    print("  • Pour éviter l'overfitting sur 150 paires : LR=2e-4, epochs=3-5.")


if __name__ == "__main__":
    main()
