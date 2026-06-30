📝 Slide 1 : Atelier 07 — Observabilité & Évaluation (mission en un coup d'œil)

POURQUOI cet atelier après le déploiement (AT05) et le benchmark (AT06) ?

AT05 a câblé Langfuse pour VOIR les traces. En production, il faut MESURER EN CONTINU : coût, latence, et surtout la QUALITÉ des réponses. AT07 : tracer chaque appel, noter sa qualité (LLM-as-judge), évaluer en batch (RAGAS).

| Bloc | Ce qu'il fait |
|------|---------------|
| Tracing Langfuse (À CÂBLER) | handler en callback → prompt, latence, tokens, coût |
| LLM-as-judge (À CÂBLER) | note chaque réponse, score poussé dans la trace |
| RAGAS (À CÂBLER) | faithfulness, answer_relevancy, context_precision/recall |
| homebutler/eval/ (FOURNI) | la bibliothèque que tu orchestres |

> 💡 **Branche élève** : `git checkout student/07-observabilite`. On MESURE le RAG, on ne le modifie pas.


📝 Slide 2 : Observabilité ≠ Évaluation

POURQUOI distinguer les deux ?

OBSERVABILITÉ = « QUE s'est-il passé ? » (latence, tokens, coût). ÉVALUATION = « est-ce BON ? » (fidélité, pertinence). Les deux sont nécessaires : tracer en continu + noter la qualité régulièrement.

> 💡 **Analogie** : l'observabilité dit « plat sorti en 8 min » ; l'évaluation dit « le plat est-il bon ? ».
⚠️ **Piège** — latence faible ≠ qualité. Un RAG rapide peut halluciner.


📝 Slide 3 : Concept #1 — Tracer avec Langfuse (à câbler)

POURQUOI un handler en callback ?

On passe un handler à `invoke` ; il capture tout l'arbre d'exécution et l'envoie à Langfuse. Version CRUCIALE : SDK Langfuse **v2**.

**À câbler** (dans evaluate_observability.py) :
```python
handler = get_langfuse_handler()
rag_chain.invoke(q, config={"callbacks": [...]})   # ← passe le handler
flush_traces(handler)                              # envoi async → flush en fin
```

> 💡 **Indice** : le handler vient de `homebutler/eval/tracing.py` (fourni). SDK v2 = `from langfuse.callback import CallbackHandler`.


📝 Slide 4 : Concept #2 — RAGAS, les 4 métriques (et la référence)

POURQUOI certaines métriques exigent-elles une référence ?

| Métrique | Mesure | Référence requise ? |
|---|---|---|
| faithfulness | réponse ancrée dans les contextes | Non |
| answer_relevancy | la réponse répond à la question | Non |
| context_precision | contextes pertinents | **Oui** |
| context_recall | contextes couvrent la réponse de référence | **Oui** |

Schéma 0.2.x : `{user_input, response, retrieved_contexts, reference}`.

> 💡 **Indice** : `reference` vient du champ `output` du dataset (input→user_input, output→reference).
⚠️ **Piège** — sans `reference`, context_recall/precision = **NaN** (Bug v2).


📝 Slide 5 : Concept #3 — LLM-as-judge déterministe (à câbler)

POURQUOI temperature=0 ?

Un juge à température > 0 donne des scores variables → évaluation non reproductible. On met temperature=0.

**À câbler** :
```python
score = llm_as_judge(q, answer, contexts)   # fourni dans homebutler/eval/judge.py
```

> 💡 **Indice** : la température contrôle l'aléa, pas la compétence. Pour un juge, zéro aléa.


📝 Slide 6 : Concept #4 — Attacher le score à la trace (à câbler)

POURQUOI pousser le score dans Langfuse ?

Attaché à la trace, le score devient filtrable/suivable : « requêtes avec llm_judge < 0.5 ».

**À câbler** :
```python
trace_id = handler.get_trace_id()
score_trace(trace_id, name="llm_judge", value=score)
```

> 💡 **Indice** : RAGAS injecte explicitement get_llm + fastembed — sinon il appelle OpenAI par défaut.


📝 Slide 7 : Garde-fous de production

- **Rate-limit** : RAGAS = dizaines d'appels LLM → 6 questions en Core, 20 en bonus, `LLM_PROVIDER=ollama` pour les gros runs.
- **Coût** : chaque éval consomme des tokens.
- **RGPD** : masquer les données personnelles (scrubbing) avant envoi des traces (bonus).


📝 Slide 8 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `langfuse.callback.CallbackHandler(...)` — tracing (v2). `get_trace_id()`
- `langfuse.Langfuse(...).score(trace_id, name, value)` / `.flush()`
- `ragas.evaluate(dataset, metrics, llm, embeddings)`
- `ragas.EvaluationDataset` + `ragas.SingleTurnSample(user_input, response, retrieved_contexts, reference)`
- `ragas.metrics` : faithfulness, answer_relevancy, context_precision, context_recall


📝 Slide 9 : Bug Hunt — à toi de jouer

| Bug | À observer | À trouver |
|-----|-----------|-----------|
| v1 | ImportError du handler / 0 trace | le bon import du SDK (v2) |
| v2 | context_recall = NaN | `reference` manquante |
| v3 | scores non reproductibles | juge non déterministe |

Cycle : `git apply bugs/vN.patch` → `pytest bugs/test_vN.py` (FAIL) → `git checkout -- homebutler/eval/<fichier>` → `pytest` (PASS) → lis `bugs/vN_explanation.md`.


📝 Slide 10 : Récap & transition

Un RAG MESURABLE : chaque appel tracé, chaque réponse notée (judge attaché à la trace), rapport RAGAS. De « ça marche » à « voici la preuve ».

PROCHAINES ÉTAPES : AT08 (AMÉLIORER le retrieval : reranking) · AT09 (vector store MANAGÉ : Azure AI Search).
