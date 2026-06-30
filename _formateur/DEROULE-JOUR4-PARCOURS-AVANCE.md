# Déroulé — Jour 4 « RAG avancé & industrialisation » (parcours optionnel)

> Complément à `DEROULE-FORMATION.md` (Jours 1-3 / AT01-06). Ce 4e jour regroupe les 3 modules
> AVANCÉS et OPTIONNELS — détachables, jouables à la carte. **Cadrage honnête** : le programme
> officiel Ambient IT = 14 h ; l'existant fait déjà ~21 h ; ces 3 ateliers ajoutent ~10 h. Ce ne
> sont donc PAS un comblement de la fiche 14 h, mais un « advanced track » (industrialisation).

## Fil narratif du Jour 4 : mesurer → améliorer → industrialiser

| Demi-journée | Atelier | Question répondue | Prolonge |
|---|---|---|---|
| J4 matin | **AT07 Observabilité & Éval** | « Mes réponses sont-elles bonnes ? À quel coût ? » | AT05 (Langfuse), AT06 (dataset) |
| J4 a.-m. | **AT08 Optimisation pipeline** | « Comment améliorer le retrieval, et le prouver ? » | AT02/03 (retrieval) |
| (J4+) | **AT09 Azure AI Search** | « Comment passer au cloud managé ? » | AT02 (FAISS → managé) |

> Ordre d'ENSEIGNEMENT : 07 → 08 → 09. Ordre de CONSTRUCTION (formateur) : 08 → 07 → 09
> (AT08 le plus autonome valide la mécanique). Les 3 branches partent de `atelier/06` (parallèles,
> pas une chaîne) : chacune = atelier/06 + son seul delta.

## Honnêteté de couverture PDF (à ne pas survendre)
- ch.4 « observabilité » nomme LangSmith → on enseigne **Langfuse** (déjà câblé). Équivalent.
- ch.2 « Deep Memory » est une feature propriétaire Activeloop → AT08 (reranking/multi-query) est
  une **substitution pédagogique** de « optimisation du pipeline », pas une implémentation de Deep Memory.
- ch.5 « Azure AI Search » → couvert tel quel (AT09).

---

## Structure invariante (identique aux Jours 1-3)

```
00:00 Slides (30) → 00:30 Démo live (20) → 00:50 Relais (5) → 00:55 Core (1h40)
→ 02:35 Bug Hunt (30) → 03:05 Bonus (25) → 03:30 Fin
```

---

## AT07 — Observabilité & Évaluation

**Mission élève :** rendre le RAG mesurable — tracer (Langfuse), noter (LLM-judge), évaluer (RAGAS).
**L'élève câble** (TODO inline, style AT06) : `ateliers/atelier-07-observabilite/evaluate_observability.py`.
**Fourni :** `homebutler/eval/` (tracing/ragas_eval/judge).

### Démo live (T+30)
```bash
git checkout atelier/07-observabilite
python ateliers/atelier-07-observabilite/evaluate_observability.py   # nécessite clé LLM + LANGFUSE_*
```
Pointe une trace Langfuse (latence/tokens/coût + score `llm_judge`) et le rapport RAGAS
(`context_recall` PAS NaN car `reference` = champ `output`).

### Passage de relais
```bash
git checkout student/07-observabilite
grep -n "TODO" ateliers/atelier-07-observabilite/evaluate_observability.py
```
Critère : traces + score + RAGAS sans NaN. **6 questions en Core** (rate-limit), 20 en bonus.

### Bug Hunt (cible homebutler/eval/, tests SANS clé LLM)
```bash
git apply ateliers/atelier-07-observabilite/bugs/v1.patch   # import langfuse.langchain (v3)
pytest ateliers/atelier-07-observabilite/bugs/test_v1.py -v
git checkout -- homebutler/eval/tracing.py
# v2 : reference omis → context_recall NaN (homebutler/eval/ragas_eval.py)
# v3 : judge temperature=1.0 (homebutler/eval/judge.py)
```

### Pannes typiques
| Symptôme | Cause | Réponse |
|---|---|---|
| `context_recall = NaN` | `reference` manquante | mapping output→reference |
| RAGAS réclame clé OpenAI | LLM/embeddings non injectés | run_ragas_eval passe get_llm + fastembed |
| 429 rate limit | RAGAS = dizaines d'appels | `LLM_PROVIDER=ollama`, N_EVAL=6 |
| Traces invisibles | API non flush / .env non rechargé | flush_traces, relancer |
| ImportError CallbackHandler | langfuse v3 vs v2 | `from langfuse.callback import CallbackHandler` |

---

## AT08 — Optimisation du pipeline RAG

**Mission élève :** reranking cross-encoder (flashrank) + multi-query, prouver le gain (Recall@1, MRR).
**L'élève code :** `homebutler/rag/reranking.py` (get_reranked_retriever, get_multiquery_retriever, get_hyde_chain).

### Démo live (T+30)
```bash
git checkout atelier/08-optimisation
python ateliers/atelier-08-optimisation/solution.py
```
Seuils figés (corpus HomeButler, questions en langage naturel) :
**baseline Recall@1=40% MRR=0.617 → reranké Recall@1=70% MRR=0.833** (ΔRecall@1 +30pts).
Insiste : Recall@5 sature → regarder Recall@1 et MRR.

### Bug Hunt (cible homebutler/rag/reranking.py)
```bash
# v1 base_k==top_n (entonnoir cassé) ; v2 prompt multi-query → 1 reformulation ; v3 top_n non passé
git apply ateliers/atelier-08-optimisation/bugs/v1.patch
pytest ateliers/atelier-08-optimisation/bugs/test_v1.py -v
git checkout -- homebutler/rag/reranking.py
```

### Pannes typiques
| Symptôme | Cause | Réponse |
|---|---|---|
| ΔRecall@1 ≈ 0 | base_k==top_n OU questions "mot pour mot" | entonnoir + questions naturelles |
| flashrank ne télécharge pas | réseau au 1er run | `scripts/preload_models.py` la veille |
| sortie ≠ 5 docs | top_n non passé | `FlashrankRerank(top_n=top_n)` |

---

## AT09 — Azure AI Search

**Mission élève :** migrer FAISS → Azure AI Search managé. Concept : control plane (CLI) vs data plane (SDK).
**L'élève code :** `homebutler/rag/vectorstore_azure.py` (build_index_schema, get_azure_store, azure_search).

### Setup (LA VEILLE)
```bash
az login
AZ_SEARCH_SKU=basic bash ateliers/atelier-09-azure-search/azure_provision.sh   # 1 service Basic PARTAGÉ
```
En classe : chaque élève met `AZURE_SEARCH_INDEX=<trigramme>` dans `.env` (1 service, N index).

### Démo live (T+30)
```bash
git checkout atelier/09-azure-search
az search service show --name <svc> --resource-group rg-atelier-rag -o table   # control plane
python ateliers/atelier-09-azure-search/solution.py                            # data plane
```
Projette `CLI-VS-PORTAIL.md`. Martèle : « `az search` ≠ RAG ». Montre le portail (monitoring).

### Bug Hunt (cible vectorstore_azure.py, tests HORS-LIGNE)
```bash
# v1 dim 1536≠384 ; v2 default similarity vs hybrid ; v3 content searchable=False
git apply ateliers/atelier-09-azure-search/bugs/v1.patch
pytest ateliers/atelier-09-azure-search/bugs/test_v1.py -v
git checkout -- homebutler/rag/vectorstore_azure.py
```

### Pannes typiques
| Symptôme | Cause | Réponse |
|---|---|---|
| `quota exceeded` à la création | Free = 1 service/souscription | service Basic PARTAGÉ + index par trigramme |
| upload rejeté (dimension) | dim schéma ≠ embedding | `AZURE_VECTOR_DIM=384` |
| hybride 0 résultat | content non searchable OU index vide | searchable=True + ingestion faite |
| add_documents champ manquant | schéma non aligné LangChain | champs id/content/content_vector/metadata |
| facture qui court | tier Dedicated horaire | `azure_teardown.sh` en fin |

> 🧹 **Clôture J4** : faire lancer `azure_teardown.sh` à TOUS les élèves (coût).

---

## Pré-vol J4 (à ajouter au pré-vol)
- AT07 : `LANGFUSE_*` dans `.env` (Cloud) ; `pip install -r requirements_atelier07.txt`.
- AT08 : `python scripts/preload_models.py` (télécharge flashrank ~34 Mo).
- AT09 : `az version` + `az login` validés la veille ; `requirements_atelier09.txt`.

## Vérification formateur (sans clé/Azure)
```bash
# Bug tests déterministes des 3 ateliers (aucune clé requise) :
.venv/bin/python -m pytest ateliers/atelier-0{7,8,9}-*/bugs/ -q
# AT08 a besoin de l'index FAISS (généré) ; AT07/AT09 schéma/static OK sans clé.
```
