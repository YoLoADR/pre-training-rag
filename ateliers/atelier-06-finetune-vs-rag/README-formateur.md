# Atelier 06 — Fine-tuning vs RAG (J3 après-midi)

> **Chapitre formation** : Fine-tuning vs RAG (synthèse)
> **Branche** : `atelier/06-finetune-vs-rag`
> **Durée** : ~3 heures (demi-journée)

## Objectif pédagogique

Comparer **rigoureusement** les approches RAG, Fine-Tuning et Hybride sur
le projet HomeButler :
- Mesurer Recall@k pour chaque stratégie de chunking
- Comparer la latence et le coût des 3 modes (llm_only / rag_only / agent)
- Construire une **grille de décision** réutilisable
- Comprendre **RAFT** (Retrieval-Augmented Fine-Tuning, Zhang et al. 2024)

## Pré-requis

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt    # version complète (= main)
pip install -e .
cp .env.example .env

# Données + index (idem atelier 05)
python scripts/generate_documents.py
python scripts/generate_energy_data.py
python scripts/generate_producers.py
python scripts/generate_qa_dataset.py    # nécessaire pour evaluate_pipeline.py
python scripts/preload_models.py
# (rebuild des index FAISS + Chroma)

# Démarrer l'API
uvicorn api.main:app --port 8000
```

## RAFT — Retrieval-Augmented Fine-Tuning (Zhang et al. 2024)

> Le projet HomeButler combine RAG et Fine-Tuning, mais **RAFT** va plus loin :
> on entraîne le modèle FT sur des questions avec des **distracteurs**
> (documents non-pertinents mélangés aux vrais) pour le rendre robuste au bruit.

### Résultats benchmarks (Slide 7 Chapitre 6)

| Approche             | QA factuel | Style / Ton | Médical (RAFT paper)  |
|----------------------|-----------:|------------:|----------------------:|
| RAG seul             |     89 %   |    65 %     |        —              |
| Fine-Tuning seul     |     79 %   |    94 %     |        —              |
| **Hybride (RAFT)**   |  **94 %**  |  **95 %**   |     **96 %**          |

→ HomeButler vise l'approche **hybride** pour combiner précision factuelle
ET ton chaleureux.

## Lancer le benchmark complet

```bash
python ateliers/atelier-06-finetune-vs-rag/evaluate_pipeline.py
```

Le script :
1. Charge 20 paires de test depuis `concierge_qa.jsonl`
2. Appelle `/rag/evaluate` → Recall@1/@3/@5 pour les 3 stratégies de chunking
3. Appelle `/chat/compare` sur 5 questions → llm_only vs rag_only vs agent
4. Mesure la latence de chaque mode (time.time())
5. Affiche un tableau récapitulatif + comparaison aux benchmarks

## Questions de réflexion (Slide 2 + 9 Chapitre 6)

1. **Quand choisir RAG seul plutôt qu'hybride ?**
   _(infos changent souvent, pas de GPU, dataset Q/R < 500 paires, MVP)_

2. **Recall@5 = 0.87 signifie quoi pour la chaudière ?**
   _(sur 100 questions sur la chaudière, 87 ont au moins un chunk pertinent
   dans les 5 premiers résultats du retriever → 13 ne trouveront jamais
   la bonne réponse même avec le meilleur LLM en aval)_

3. **Quel budget GPU/API pour passer en production ?**
   _(voir section TCO dans `grille_decision.md`)_

## Critère de succès

- [ ] `evaluate_pipeline.py` affiche un tableau Recall@1/3/5 par stratégie
- [ ] Le mode `agent` est plus précis mais plus lent que `rag_only`
- [ ] Vous savez justifier RAG / FT / Hybride pour 3 cas d'usage concrets

→ **Fin du parcours** — vous avez un projet RAG + FT production-ready !
