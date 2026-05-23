#!/usr/bin/env python3
"""
Checkpoint Final — Atelier 06 Fine-tuning vs RAG / RAFT
5 questions sur FT vs RAG trade-offs, métriques, RAFT, TCO, soutenance.

Usage : python ateliers/atelier-06-finetune-vs-rag/checkpoints/check_final.py
"""

import sys

QUESTIONS = [
    {
        "question": "Dans quel cas recommanderais-tu Fine-Tuning seul (sans RAG) ? "
                    "Cite 2 conditions nécessaires.",
        "keywords": ["style", "ton", "stable", "change", "dataset", "500", "paires", "fixe",
                     "format", "annot", "qualité"],
        "min_hits": 3,
        "explanation": (
            "FT seul est pertinent quand : (1) les données changent peu (< 1 fois/mois) → "
            "pas besoin de la fraîcheur du RAG ; (2) le ton/style est critique (ex: ton juridique, "
            "ton conciergerie 'Merenza') — FT atteint 94% style vs 65% RAG seul ; "
            "(3) on dispose de > 500 paires Q/R annotées de qualité → FT sous-performera sinon. "
            "Contre-indication : données qui évoluent fréquemment → utiliser RAG (ou Hybride)."
        ),
    },
    {
        "question": "Cite 2 métriques qui mesurent la qualité factuelle d'un pipeline RAG "
                    "et 1 métrique qui mesure la qualité du style. Pourquoi ne peut-on pas "
                    "utiliser la même métrique pour les deux ?",
        "keywords": ["recall", "hallucination", "faithfulness", "bleu", "cosine", "embedding",
                     "llm-judge", "lexical", "sémantique", "ton", "style"],
        "min_hits": 3,
        "explanation": (
            "Factualité : Recall@k (% bonnes sources retrouvées), hallucination rate (% réponses inventées), "
            "faithfulness (le LLM cite-t-il les documents ? — mesure RAGAS). "
            "Style : cosine similarity entre embeddings, LLM-judge avec rubric. "
            "Pourquoi pas la même : les métriques factuelles (Recall@k) ne dépendent pas du vocabulaire. "
            "Les métriques style sont sémantiques — BLEU (lexical) est inadapté pour le style car "
            "il pénalise les paraphrases de bonne qualité."
        ),
    },
    {
        "question": "Ton évaluation donne Recall@5 = 0.87 pour 'ensemble' sur le dataset de test. "
                    "Ton chef te demande 'c'est bon ou pas ?'. Comment tu réponds en 2 phrases ?",
        "keywords": ["benchmark", "0.87", "89", "bien", "contexte", "question", "privée", "bonne",
                     "baseline", "compare", "absolu"],
        "min_hits": 2,
        "explanation": (
            "0.87 est un bon score : il correspond au benchmark RAFT 2024 pour RAG seul (89% QA factuel). "
            "Il faut contextulaiser : sur les questions 'privées' (notices HomeButler), est-ce que 87% "
            "signifie que 13% des utilisateurs reçoivent des réponses incorrectes ? Si oui, c'est peut-être "
            "inacceptable pour un service premium. Le chiffre absolu compte moins que son impact métier."
        ),
    },
    {
        "question": "Pourquoi mesurer la latence sur le 1er appel uniquement est biaisé ? "
                    "Comment corriger ce biais ?",
        "keywords": ["cold", "start", "warm", "premier", "initialise", "agent", "vectorstore",
                     "ignore", "10", "5", "appels"],
        "min_hits": 3,
        "explanation": (
            "Le 1er appel initialise l'agent ReAct, charge le vectorstore en mémoire — 2-5x plus lent. "
            "En prod, l'API tourne depuis des heures, les utilisateurs ne voient jamais ce cold-start. "
            "Fix : mesurer sur >= 10 appels, ignorer le 1er (warm-up), calculer p50 et p95 sur les 9 suivants."
        ),
    },
    {
        "question": "Pour HomeButler (notices qui changent peu, ton conciergerie critique, ~10k req/mois, "
                    "pas de GPU dédié), quelle est ta recommandation ? Justifie avec 3 critères chiffrés.",
        "keywords": ["rag", "style", "ton", "0.87", "10k", "api", "hybride", "tco",
                     "prompt", "engineering", "recall", "1700"],
        "min_hits": 3,
        "explanation": (
            "Recommandation typique : RAG seul + system prompt soigné pour le style, pour commencer. "
            "Justification : (1) notices stables → RAG suffit (pas de re-training coûteux) ; "
            "(2) Recall@5 = 0.87 déjà bon — au-dessus du seuil min acceptable ; "
            "(3) TCO an 1 RAG = ~1700€ vs FT = ~3600€ (voir grille_decision.md) — gain qualité "
            "insuffisant à 10k req/mois pour justifier l'investissement FT. "
            "Évolution vers Hybride si on dépasse 50k req/mois ou si les utilisateurs se plaignent "
            "du ton malgré un system prompt optimisé."
        ),
    },
]

SCORE = 0
TOTAL = len(QUESTIONS)

print("=" * 70)
print("CHECKPOINT FINAL — Atelier 06 : FT vs RAG — Synthèse")
print("=" * 70)
print("5 questions. Réponds avec TES données mesurées + les benchmarks théoriques.")
print()

for i, q in enumerate(QUESTIONS, 1):
    print(f"Q{i}. {q['question']}")
    print()
    answer = input("Ta réponse : ").strip().lower()
    print()

    hits = sum(1 for kw in q["keywords"] if kw.lower() in answer)

    if hits >= q["min_hits"]:
        print(f"  OK ({hits}/{len(q['keywords'])} mots-clés, minimum={q['min_hits']})")
        SCORE += 1
    else:
        print(f"  Incomplet ({hits}/{len(q['keywords'])} mots-clés, minimum={q['min_hits']})")

    print(f"  Explication : {q['explanation']}")
    print()

PCT = round(100 * SCORE / TOTAL)
print("=" * 70)
print(f"Score final : {SCORE}/{TOTAL} ({PCT}%)")
print()

if PCT >= 80:
    print("Excellent ! Tu es prêt(e) pour la soutenance.")
    print("Rédige la reco 1 page et utilise le rubric LLM-judge du Wrap-up.")
elif PCT >= 60:
    print("Bien. Relis les points manquants, puis prépare ta reco écrite.")
else:
    print("Score < 60% → pars en SPRINT pour consolider avant la soutenance.")
    print("Relis grille_decision.md et les sections Mesure-toi + TCO du guide.")
    sys.exit(1)
