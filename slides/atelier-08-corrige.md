📝 Slide 1 : Atelier 08 — Optimisation du pipeline RAG (mission en un coup d'œil)

POURQUOI cet atelier après le RAG (AT02) et l'agent (AT03) ?

L'Atelier 02 finissait sur une note explicite : « On pourrait améliorer la précision en ajoutant un re-ranker (cross-encoder) après le retriever. Hors-scope de cet atelier mais à mentionner. » AT08 réalise cette promesse. Le retrieval d'AT02/03 trouve souvent la bonne notice, mais le bon passage n'est pas toujours en tête — surtout quand l'utilisateur parle avec ses propres mots. On ajoute 3 techniques 100% locales (CPU) pour améliorer la PRÉCISION, et on le PROUVE avec des métriques.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| Baseline FAISS (fournie) | Recall@1/@3/@5 + MRR du retrieval AT02/03 | Point de comparaison chiffré |
| Reranking cross-encoder (À CODER) | Récupère 20 candidats, en garde 5 reclassés | Remonte le bon chunk vers le sommet (Recall@1, MRR) |
| Multi-query (À CODER) | Le LLM reformule en 3 variantes, union des docs | Couvre le vocabulaire divergent (rappel) |
| HyDE (À CODER, bonus) | Embed une réponse hypothétique au lieu de la question | Meilleur rappel sur questions vagues |
| Mesure | ΔRecall@1, ΔMRR baseline vs reranké | Prouve le gain (≈ +30 pts Recall@1) |

> 💡 **Branche élève** : `git checkout student/08-optimisation` dans `training-rag`. Solution : `git diff student/08-optimisation atelier/08-optimisation -- homebutler/rag/reranking.py`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI un fichier neuf (reranking.py) et pas une modif de retriever.py ?

Règle de NON-RÉGRESSION : `homebutler/rag/retriever.py` est le code d'AT03, réutilisé tel quel. On ne le touche PAS. Tout le code AT08 vit dans un fichier NEUF, `homebutler/rag/reranking.py`. L'élève importe et réutilise `get_faiss_retriever`/`get_ensemble_retriever` d'AT03, sans les modifier.

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/rag/retriever.py` | ✅ Acquis AT03 (corrigé, NON modifié) | Bi-encodeur FAISS/Ensemble — la base |
| `homebutler/rag/reranking.py` → `get_reranked_retriever` | 🛠️ **À CODER** | Concept central : entonnoir + cross-encoder |
| `homebutler/rag/reranking.py` → `get_multiquery_retriever` | 🛠️ **À CODER** | Diversité de requêtes (rappel) |
| `homebutler/rag/reranking.py` → `get_hyde_chain` | 🛠️ **À CODER (bonus)** | Réponse hypothétique |
| `ateliers/atelier-08-optimisation/exercice.py` | ✅ Cadré par TODOs | Orchestration : compare baseline vs reranké |

> 💡 Les fonctions à coder ont **deux niveaux d'indices** dans leur docstring : *léger* (quel objet) et *fort* (quels appels).


📝 Slide 3 : Concept #1 — Bi-encodeur vs Cross-encoder

POURQUOI deux étages au lieu d'un ?

Le bi-encodeur (les embeddings d'AT02) encode question et chunk SÉPARÉMENT, puis compare les vecteurs. C'est rapide et scalable (on pré-calcule les vecteurs des chunks), donc parfait pour ratisser tout le corpus. Mais en encodant séparément, il rate les subtilités d'interaction. Le cross-encoder lit la PAIRE (question, chunk) ENSEMBLE et sort un score de pertinence : bien plus précis, mais lent (un passage modèle par paire). On ne peut donc PAS l'appliquer à tout le corpus — seulement à une shortlist.

> 💡 **Analogie** : le bi-encodeur juge deux CV séparément (rapide, présélection de masse). Le cross-encoder fait passer un ENTRETIEN (question + CV ensemble : précis, mais réservé à la shortlist).
⚠️ **Piège fréquent** — vouloir mettre le cross-encoder en étage 1 : scorer des milliers de chunks à chaque requête est inutilisable en production.


📝 Slide 4 : Concept #2 — L'entonnoir base_k ≫ top_n (la pierre angulaire)

POURQUOI base_k doit être beaucoup plus grand que top_n ?

Le gain du reranking vient de sa capacité à REPÊCHER : un bon chunk mal classé par le bi-encodeur (rang 8-15) est remonté dans le top final. Pour cela, il faut lui donner un large pool de candidats (base_k=20), puis ne garder que les meilleurs (top_n=5). Si base_k == top_n, le reranker n'a plus rien à filtrer : il réordonne le même petit ensemble, le bénéfice disparaît.

**Évolution à apporter** (vue corrigée) :

```python
# AVANT (blank student/08) : NotImplementedError
# APRÈS (atelier/08) :

def get_reranked_retriever(base_k=20, top_n=5, use_ensemble=False):
    # Étage 1 — RAPPEL : on récupère LARGE (base_k=20 candidats).
    base_retriever = get_faiss_retriever(k=base_k, fetch_k=max(base_k, 20))
    # Étage 2 — PRÉCISION : le cross-encoder re-score chaque paire et garde top_n.
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2", top_n=top_n)
    # Le wrapper combine les deux étages :
    return ContextualCompressionRetriever(
        base_compressor=compressor,      # étage 2
        base_retriever=base_retriever,   # étage 1
    )
```

> 💡 Règle de pouce : `base_k` ≈ 4 à 10 × `top_n`. Ici 20 vs 5.


📝 Slide 5 : Concept #3 — Multi-query (la diversité vient du PROMPT)

POURQUOI pas augmenter la température pour diversifier ?

Le MultiQueryRetriever demande au LLM de reformuler la question en N variantes, récupère pour chacune, et prend l'UNION des documents. Point souvent mal compris : la diversité ne vient PAS d'un sampling à température élevée. Les N reformulations sont générées dans UN SEUL appel, pilotées par la CONSIGNE du prompt (« génère 3 reformulations différentes »). On garde donc temperature=0 pour la reproductibilité.

```python
def get_multiquery_retriever(k=4, use_ensemble=False):
    base = get_faiss_retriever(k=k)
    return MultiQueryRetriever.from_llm(
        retriever=base,
        llm=get_llm(temperature=0),   # déterministe ; la diversité vient du prompt
        prompt=MULTIQUERY_PROMPT,     # "génère 3 reformulations DIFFÉRENTES"
    )
```

> 💡 Multi-query = levier de RAPPEL (union de docs). Reranking = levier de PRÉCISION (ordre). On les chaîne souvent : multi-query → reranking.


📝 Slide 6 : Concept #4 — HyDE (Hypothetical Document Embeddings) [bonus]

POURQUOI embedder une réponse plutôt que la question ?

Une question est courte et formulée différemment des chunks (longs, déclaratifs). HyDE demande au LLM de générer une RÉPONSE hypothétique plausible, puis embedde ce paragraphe pour la recherche. L'embedding de la réponse hypothétique ressemble davantage aux vrais chunks → meilleur rappel sur questions vagues. Coût : un appel LLM de plus par requête.

```python
def get_hyde_chain():
    hyde_prompt = ChatPromptTemplate.from_template(
        "Rédige un court paragraphe qui répondrait à : {question}")
    return hyde_prompt | get_llm(temperature=0) | StrOutputParser()
# Usage : hypo = chain.invoke({"question": q}); vectorstore.similarity_search(hypo)
```


📝 Slide 7 : Concept #5 — Mesurer le bon indicateur (Recall@1 et MRR)

POURQUOI pas Recall@5 ?

Sur un petit corpus (6 PDFs HomeButler), le bon document est presque toujours dans le top-5 : Recall@5 SATURE (≈ 90-100 % avant reranking). Le reranking n'augmente pas le rappel — il améliore l'ORDRE. Donc les bonnes métriques sont Recall@1 (le bon doc est-il en TÊTE ?) et MRR (Mean Reciprocal Rank = 1/rang moyen du bon doc). C'est là que le gain se voit.

| Métrique | Baseline FAISS | + Reranking | Gain |
|---|---|---|---|
| Recall@1 | 40% | 70% | **+30 pts** |
| Recall@3 | 90% | 100% | +10 pts |
| Recall@5 | 90% | 100% | +10 pts |
| MRR | 0.617 | 0.833 | **+0.22** |

> 💡 Mesuré sur des questions en langage NATUREL (« mon linge ressort trempé »), pas « mot pour mot » du document — c'est là que le cross-encoder fait la différence.
⚠️ **Piège** — sur des questions calquées sur le document, la baseline est déjà parfaite : le gain serait invisible.


📝 Slide 8 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `langchain_community.document_compressors.FlashrankRerank(model, top_n)` — reranker cross-encoder ONNX (CPU). Paramètres : - `model: str` — `ms-marco-MiniLM-L-12-v2` (~34 Mo) - `top_n: int` — nombre de documents conservés après reclassement
- `langchain.retrievers.ContextualCompressionRetriever(base_compressor, base_retriever)` — combine étage 1 (retriever) + étage 2 (compresseur/reranker)
- `langchain.retrievers.multi_query.MultiQueryRetriever.from_llm(retriever, llm, prompt)` — génère N reformulations en 1 appel, union des docs
- `flashrank` (lib) — runtime ONNX du cross-encoder, 100% CPU, cohérent avec fastembed (AT02)
- `langchain_core.prompts.ChatPromptTemplate`, `langchain_core.output_parsers.StrOutputParser` — briques LCEL pour HyDE

> 💡 Aucun GPU, aucune API tierce pour le reranking : tout tourne en local comme le reste du fil rouge.


📝 Slide 9 : Bug Hunt — les 3 pièges classiques

POURQUOI ces 3 bugs ?

| Bug | Erreur | Symptôme | Leçon |
|-----|--------|----------|-------|
| v1 | `RERANK_BASE_K=5` (== top_n) | Le reranker ne filtre plus | L'entonnoir base_k ≫ top_n est l'essence du reranking |
| v2 | prompt multi-query → 1 reformulation | Plus de diversité de requêtes | La diversité vient du PROMPT, pas de la température |
| v3 | `FlashrankRerank()` sans top_n | Sortie = 3 (défaut) au lieu de 5 | Un paramètre oublié prend une valeur par défaut silencieuse |

> 💡 Chaque bug a un test pytest qui ÉCHOUE avec le bug et PASSE une fois réparé, et un `vN_explanation.md` (QCM vrai/faux) à lire après réparation.


📝 Slide 10 : Récap & transition

CE QU'ON A PROUVÉ : le reranking cross-encoder remonte le bon chunk vers le sommet (Recall@1 +30 pts, MRR +0.22), pour un coût maîtrisé par l'entonnoir, 100% local. Multi-query couvre le vocabulaire divergent ; HyDE aide sur les questions vagues.

PROCHAINES ÉTAPES :
- **AT07** — tu as mesuré UNE fois en CLI ; comment mesurer EN CONTINU en production, tracer chaque requête et noter la qualité ? → Observabilité (Langfuse) + évaluation (RAGAS).
- **AT09** — ton index est local (FAISS) ; comment passer à un vector store MANAGÉ en cloud ? → Azure AI Search.
