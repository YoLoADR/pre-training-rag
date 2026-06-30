📝 Slide 1 : Atelier 08 — Optimisation du pipeline RAG (mission en un coup d'œil)

POURQUOI cet atelier après le RAG (AT02) et l'agent (AT03) ?

L'Atelier 02 finissait sur : « On pourrait améliorer la précision en ajoutant un re-ranker (cross-encoder) après le retriever. » AT08 réalise cette promesse. Le retrieval trouve la bonne notice mais pas toujours le bon passage en tête — surtout quand l'utilisateur parle avec ses mots. On ajoute 3 techniques 100% locales (CPU) pour améliorer la PRÉCISION, et on le PROUVE.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| Baseline FAISS (fournie) | Recall@1/@3/@5 + MRR du retrieval AT02/03 | Point de comparaison chiffré |
| Reranking cross-encoder (À CODER) | Récupère 20 candidats, en garde 5 reclassés | Remonte le bon chunk vers le sommet |
| Multi-query (À CODER) | Le LLM reformule, union des docs | Couvre le vocabulaire divergent |
| HyDE (À CODER, bonus) | Embed une réponse hypothétique | Meilleur rappel sur questions vagues |
| Mesure | ΔRecall@1, ΔMRR baseline vs reranké | Prouve le gain |

> 💡 **Branche élève** : `git checkout student/08-optimisation`. Solution : `git diff student/08-optimisation atelier/08-optimisation -- homebutler/rag/reranking.py`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI un fichier neuf (reranking.py) et pas une modif de retriever.py ?

NON-RÉGRESSION : `homebutler/rag/retriever.py` (AT03) est réutilisé tel quel, JAMAIS modifié. Tu codes dans un fichier NEUF, `homebutler/rag/reranking.py`, en important `get_faiss_retriever`/`get_ensemble_retriever` d'AT03.

| Fichier | État |
|---------|------|
| `homebutler/rag/retriever.py` | ✅ Acquis AT03 (NON modifié) |
| `homebutler/rag/reranking.py` → `get_reranked_retriever` | 🛠️ **À CODER** |
| `homebutler/rag/reranking.py` → `get_multiquery_retriever` | 🛠️ **À CODER** |
| `homebutler/rag/reranking.py` → `get_hyde_chain` | 🛠️ **À CODER (bonus)** |
| `ateliers/atelier-08-optimisation/exercice.py` | ✅ Cadré par TODOs |


📝 Slide 3 : Concept #1 — Bi-encodeur vs Cross-encoder

POURQUOI deux étages au lieu d'un ?

Le bi-encodeur (embeddings AT02) encode question et chunk SÉPARÉMENT → rapide, scalable, ratisse tout le corpus, mais grossier. Le cross-encoder lit la PAIRE ensemble → précis mais lent. On combine : bi-encodeur pour la présélection, cross-encoder pour trancher sur la shortlist.

> 💡 **Analogie** : bi-encodeur = juger deux CV séparément (présélection de masse). Cross-encoder = entretien (question + CV ensemble, réservé à la shortlist).
⚠️ **Piège** — mettre le cross-encoder en étage 1 : scorer tout le corpus à chaque requête = inutilisable.


📝 Slide 4 : Concept #2 — L'entonnoir base_k ≫ top_n (à coder)

POURQUOI base_k doit être beaucoup plus grand que top_n ?

Le reranking REPÊCHE un bon chunk mal classé (rang 8-15) pour le remonter dans le top final. Il faut donc un large pool (base_k=20) puis ne garder que le meilleur (top_n=5). Si base_k == top_n, plus rien à filtrer.

**Signature à compléter** (`homebutler/rag/reranking.py`) :

```python
def get_reranked_retriever(base_k=20, top_n=5, use_ensemble=False):
    raise NotImplementedError(
        "git diff student/08-optimisation atelier/08-optimisation -- homebutler/rag/reranking.py")
```

> 💡 **Indice léger** : un `ContextualCompressionRetriever` combine un `base_retriever` (étage 1) et un `base_compressor` (étage 2 = `FlashrankRerank`).
> 💡 **Indice fort** : (1) `base = get_faiss_retriever(k=base_k, fetch_k=max(base_k,20))` ; (2) `compressor = FlashrankRerank(model=RERANK_MODEL, top_n=top_n)` ; (3) `return ContextualCompressionRetriever(base_compressor=compressor, base_retriever=base)`.


📝 Slide 5 : Concept #3 — Multi-query (à coder)

POURQUOI pas augmenter la température pour diversifier ?

La diversité vient de la CONSIGNE du prompt (« génère 3 reformulations »), pas du sampling. Les N variantes sortent d'UN appel → garde temperature=0 (reproductibilité).

**Signature à compléter** :

```python
def get_multiquery_retriever(k=4, use_ensemble=False):
    raise NotImplementedError(...)
```

> 💡 **Indice léger** : `MultiQueryRetriever.from_llm(...)` ; passe le prompt `MULTIQUERY_PROMPT` fourni.
> 💡 **Indice fort** : `base = get_faiss_retriever(k=k)` ; `return MultiQueryRetriever.from_llm(retriever=base, llm=get_llm(temperature=0), prompt=MULTIQUERY_PROMPT)`.


📝 Slide 6 : Concept #4 — HyDE (à coder, bonus)

POURQUOI embedder une réponse plutôt que la question ?

Une question courte ressemble peu aux chunks. HyDE génère une réponse hypothétique, dont l'embedding est plus proche des vrais chunks → meilleur rappel sur questions vagues.

> 💡 **Indice léger** : une chaîne LCEL `prompt | llm | StrOutputParser()` qui retourne le paragraphe.
> 💡 **Indice fort** : `hyde_prompt = ChatPromptTemplate.from_template("... {question}")` ; `return hyde_prompt | get_llm(temperature=0) | StrOutputParser()`.


📝 Slide 7 : Concept #5 — Mesurer le bon indicateur (Recall@1 et MRR)

POURQUOI pas Recall@5 ?

Sur un petit corpus, Recall@5 SATURE (le bon doc est presque toujours dans le top-5). Le reranking améliore l'ORDRE, pas le rappel → regarde Recall@1 (bon doc en tête ?) et MRR (1/rang moyen).

| Métrique | Baseline | + Reranking |
|---|---|---|
| Recall@1 | ___% | ___% |
| MRR | ___ | ___ |

> 💡 Mesure sur des questions en langage NATUREL (« mon linge ressort trempé »).
⚠️ **Piège** — questions calquées sur le document : baseline déjà parfaite, gain invisible.


📝 Slide 8 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `langchain_community.document_compressors.FlashrankRerank(model, top_n)` — reranker cross-encoder ONNX (CPU)
- `langchain.retrievers.ContextualCompressionRetriever(base_compressor, base_retriever)` — combine les 2 étages
- `langchain.retrievers.multi_query.MultiQueryRetriever.from_llm(retriever, llm, prompt)` — reformulations + union
- `flashrank` — runtime ONNX CPU
- `ChatPromptTemplate`, `StrOutputParser` — briques LCEL pour HyDE


📝 Slide 9 : Bug Hunt — à toi de jouer

| Bug | À observer | À trouver |
|-----|-----------|-----------|
| v1 | pool de candidats == sortie | l'entonnoir base_k ≫ top_n |
| v2 | plus de diversité de requêtes | la diversité vient du prompt |
| v3 | sortie de mauvaise taille | top_n non transmis au reranker |

Cycle : `git apply bugs/vN.patch` → `pytest bugs/test_vN.py` (FAIL) → répare → `pytest` (PASS) → lis `bugs/vN_explanation.md`.


📝 Slide 10 : Récap & transition

Le reranking remonte le bon chunk (Recall@1, MRR), coût maîtrisé par l'entonnoir, 100% local. Multi-query = rappel ; HyDE = questions vagues.

PROCHAINES ÉTAPES : AT07 (mesurer EN CONTINU : Langfuse + RAGAS) · AT09 (vector store MANAGÉ : Azure AI Search).
