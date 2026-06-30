📝 Slide 1 : Atelier 07 — Observabilité & Évaluation (mission en un coup d'œil)

POURQUOI cet atelier après le déploiement (AT05) et le benchmark (AT06) ?

AT05 a câblé Langfuse pour VOIR les traces. AT06 a comparé des stratégies une fois. En production, il faut MESURER EN CONTINU : combien ça coûte, combien de temps, et surtout — les réponses sont-elles bonnes ? AT07 transforme « on croit que ça marche » en « on sait, chiffres à l'appui » : tracer chaque appel, noter sa qualité (LLM-as-judge), évaluer en batch (RAGAS).

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| Tracing Langfuse (À CÂBLER) | handler en callback → prompt, latence, tokens, coût | Visibilité ops, debug, suivi des coûts |
| LLM-as-judge (À CÂBLER) | note 1-5 chaque réponse, score poussé dans la trace | Qualité mesurée par requête, suivie dans le temps |
| RAGAS (À CÂBLER) | faithfulness, answer_relevancy, context_precision/recall | Évaluation automatique standardisée |
| homebutler/eval/ (FOURNI) | tracing.py / ragas_eval.py / judge.py | La bibliothèque réutilisable — l'élève l'orchestre |

> 💡 **Branche élève** : `git checkout student/07-observabilite`. On MESURE le RAG, on ne le modifie pas.


📝 Slide 2 : Observabilité ≠ Évaluation

POURQUOI distinguer les deux ?

Ce sont deux questions différentes. L'OBSERVABILITÉ répond à « QUE s'est-il passé ? » (latence, tokens, coût, étapes du raisonnement). L'ÉVALUATION répond à « est-ce BON ? » (la réponse est-elle fidèle, pertinente ?). On a besoin des deux : tracer en continu pour la prod, et noter la qualité régulièrement pour détecter une dérive.

> 💡 **Analogie** : l'observabilité dit « le plat est sorti de cuisine en 8 minutes » ; l'évaluation dit « le plat est-il bon ? ». Un service qui ne mesure que le temps sert vite… de la mauvaise nourriture.
⚠️ **Piège** — croire qu'une latence faible = qualité. Un RAG rapide peut halluciner ; seule l'évaluation le révèle.


📝 Slide 3 : Concept #1 — Tracer avec Langfuse (SDK v2)

POURQUOI un handler en callback ?

LangChain expose un mécanisme de callbacks : on passe un handler à chaque `invoke`, et il capture automatiquement tout l'arbre d'exécution (prompt, sous-appels, latence, tokens, coût) et l'envoie à Langfuse. Aucune instrumentation manuelle. Point de version CRUCIAL : le projet est sur le SDK Langfuse v2.

```python
# homebutler/eval/tracing.py (fourni)
from langfuse.callback import CallbackHandler   # SDK v2 — PAS langfuse.langchain (v3)

handler = get_langfuse_handler()                 # None si pas de clés (no-op)
rag_chain.invoke(q, config={"callbacks": [handler]})   # ← l'appel est tracé
flush_traces(handler)                            # envoi asynchrone → flush en fin
```

> 💡 Sans clés Langfuse, le tracing devient un no-op : le reste (RAGAS, judge) fonctionne.


📝 Slide 4 : Concept #2 — RAGAS, les 4 métriques (et la référence)

POURQUOI certaines métriques exigent-elles une réponse de référence ?

RAGAS note la qualité automatiquement via un LLM juge. Deux métriques jugent la RÉPONSE seule, deux jugent les CONTEXTES par rapport à une vérité terrain :

| Métrique | Mesure | Référence requise ? |
|---|---|---|
| faithfulness | réponse ancrée dans les contextes (pas d'invention) | Non |
| answer_relevancy | la réponse répond à la question | Non |
| context_precision | les contextes récupérés sont pertinents | **Oui** |
| context_recall | les contextes couvrent la réponse de référence | **Oui** |

Schéma RAGAS 0.2.x : `{user_input, response, retrieved_contexts, reference}`.

> 💡 `reference` vient du champ `output` du dataset Alpaca (`concierge_qa.jsonl`). Mapping : input→user_input, output→reference.
⚠️ **Piège** — sans `reference`, context_recall/precision renvoient **NaN** (≠ 0). C'est le Bug v2.


📝 Slide 5 : Concept #3 — LLM-as-judge déterministe

POURQUOI temperature=0 pour le juge ?

On demande à un LLM de noter la qualité d'une réponse (1-5). Si le juge est à température élevée, il échantillonne : le même couple (question, réponse) reçoit 3/5 puis 5/5. L'évaluation n'est plus reproductible — impossible de comparer deux exécutions ou de suivre une dérive.

```python
# homebutler/eval/judge.py (fourni)
def llm_as_judge(question, answer, contexts):
    judge = get_llm(temperature=0)   # DÉTERMINISTE — jamais > 0 pour un juge
    ...                              # prompt 1-5, normalisé en [0,1]
```

> 💡 La température contrôle l'ALÉA, pas la compétence. Pour un juge, on veut zéro aléa.


📝 Slide 6 : Concept #4 — Attacher le score à la trace

POURQUOI pousser le score du judge dans Langfuse ?

Un score isolé dans un terminal se perd. Attaché à la trace, il devient filtrable et suivable : « montre-moi les requêtes avec llm_judge < 0.5 cette semaine ». C'est la boucle observabilité + évaluation fermée.

```python
score = llm_as_judge(q, answer, contexts)
trace_id = handler.get_trace_id()
score_trace(trace_id, name="llm_judge", value=score)
```

> 💡 RAGAS injecte EXPLICITEMENT le juge et les embeddings du projet (get_llm + fastembed) — sinon RAGAS appelle OpenAI par défaut et réclame une clé absente.


📝 Slide 7 : Garde-fous de production

POURQUOI faire attention en salle / en prod ?

- **Rate-limit** : RAGAS = dizaines d'appels LLM (4 métriques × N questions) + le judge. On évalue 6 questions en Core, 20 en bonus, et on bascule `LLM_PROVIDER=ollama` pour les gros runs.
- **Coût** : chaque évaluation consomme des tokens. On mesure, on ne gaspille pas.
- **RGPD** : les traces peuvent contenir des données personnelles → masquer (scrubbing) avant envoi (bonus).

| Garde-fou | Pourquoi |
|---|---|
| N_EVAL=6 en Core | éviter le mur de rate-limit en classe |
| Ollama pour gros runs | 0 rate-limit, 0 coût API |
| LLM/embeddings injectés | éviter l'appel OpenAI implicite |


📝 Slide 8 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `langfuse.callback.CallbackHandler(public_key, secret_key, host)` — handler de tracing (SDK v2). Méthode clé : `get_trace_id()`
- `langfuse.Langfuse(...).score(trace_id, name, value)` — attache un score à une trace ; `.flush()` force l'envoi
- `ragas.evaluate(dataset, metrics, llm, embeddings)` — lance l'évaluation. Paramètres : - `llm` — `LangchainLLMWrapper(get_llm(temperature=0))` - `embeddings` — `LangchainEmbeddingsWrapper(fastembed)`
- `ragas.EvaluationDataset` + `ragas.SingleTurnSample(user_input, response, retrieved_contexts, reference)` — schéma 0.2.x
- `ragas.metrics` : `faithfulness, answer_relevancy, context_precision, context_recall`

> 💡 Pins : `langfuse==2.57.1` (v2), `ragas==0.2.15`. Ne pas migrer sans raison.


📝 Slide 9 : Bug Hunt — les 3 pièges classiques

| Bug | Erreur | Symptôme | Leçon |
|-----|--------|----------|-------|
| v1 | import `langfuse.langchain` (v3) | ImportError du handler → 0 trace | le bon import dépend de la version du SDK |
| v2 | `reference` omis du dataset | context_recall/precision = NaN | NaN ≠ 0 ; la référence est obligatoire pour ces métriques |
| v3 | judge `temperature=1.0` | scores non reproductibles | un juge doit être déterministe |

> 💡 Tests déterministes (analyse statique + construction de dataset) : pas besoin de clé LLM ni de Langfuse live pour les jouer.


📝 Slide 10 : Récap & transition

CE QU'ON A CONSTRUIT : un RAG MESURABLE — chaque appel tracé (latence, coût), chaque réponse notée (judge attaché à la trace), et un rapport RAGAS (faithfulness, context_recall…). On est passé de « ça marche » à « voici la preuve ».

PROCHAINES ÉTAPES :
- **AT08** — maintenant qu'on sait MESURER, AMÉLIORONS le retrieval (reranking) et prouvons le gain avec ces mêmes métriques.
- **AT09** — passer l'index local à un vector store MANAGÉ en cloud (Azure AI Search).
