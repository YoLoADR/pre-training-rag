📝 Slide 1 : Atelier 09 — Azure AI Search (mission en un coup d'œil)

POURQUOI cet atelier ?

L'index FAISS d'AT02 est local. En production : moteur MANAGÉ, scalable, cloud. AT09 migre HomeButler vers Azure AI Search. Fil conducteur : le SERVICE se pilote en CLI (`az search`), le CONTENU (index, vecteurs, ingestion, requêtes) en SDK Python.

| Bloc | Plan |
|------|------|
| Provisionner le service (FOURNI, CLI) | control plane |
| Créer le schéma d'index (À CODER, SDK) | data plane |
| Ingérer le corpus (SDK) | data plane |
| Requêter 3 modes (À CODER, SDK) | data plane |

> 💡 **Branche élève** : `git checkout student/09-azure-search`. Service Basic PARTAGÉ, ton index = ton trigramme.


📝 Slide 2 : Le concept central — control plane vs data plane

POURQUOI cette distinction change tout ?

| Plan | Quoi | Outil |
|------|------|-------|
| Control | service, clés, scaling | CLI `az search` |
| Data | index, vecteurs, ingestion, requêtes | SDK Python / REST |

**Il n'existe AUCUNE commande `az search` pour créer un index ou ingérer.** Tout le RAG = SDK → terminal, sans portail.

> 💡 **Analogie** : `az search` construit le bâtiment ; le SDK range les livres.
⚠️ **Piège** — chercher une commande `az search` pour créer un index : elle n'existe pas.


📝 Slide 3 : Le seul élément portail-only

POURQUOI éviter l'assistant graphique ?

Le wizard « Import and vectorize data » (portail, no-code) crée tout d'un coup, mais n'est NI reproductible NI versionnable. On fait l'équivalent en SDK (code dans git, rejouable).

> 💡 Monitoring : portail plus lisible visuellement, mais Azure Monitor reste scriptable.


📝 Slide 4 : Concept — le schéma d'index vectoriel (à coder)

POURQUOI créer le schéma à la main ?

Pour MAÎTRISER les champs (data plane). Champs alignés sur LangChain AzureSearch : id / content / content_vector / metadata.

**Signature à compléter** (`homebutler/rag/vectorstore_azure.py`) :
```python
def build_index_schema(index_name, dim=AZURE_VECTOR_DIM):
    raise NotImplementedError("git diff student/09-azure-search atelier/09-azure-search -- homebutler/rag/vectorstore_azure.py")
```

> 💡 **Indice léger** : `SearchIndex(name, fields=[...], vector_search=VectorSearch(...))`.
> 💡 **Indice fort** : champs id(key), content(SearchField searchable=True), content_vector(Collection(Single), searchable=True, vector_search_dimensions=384, vector_search_profile_name="hnsw-profile"), metadata(SearchableField) ; VectorSearch(algorithms=[HnswAlgorithmConfiguration("hnsw")], profiles=[VectorSearchProfile("hnsw-profile","hnsw")]).
⚠️ **Piège** — déclarer 1536 alors que fastembed fait 384 → upload rejeté (Bug v1).


📝 Slide 5 : Concept — les 3 modes de recherche (à coder)

POURQUOI préférer "hybrid" ?

- **similarity** : vecteur pur.
- **hybrid** : vecteur + BM25 (RRF) → rattrape vocabulaire divergent + termes exacts. Bon défaut.
- **semantic_hybrid** : + semantic ranker (Basic+, semantic config) = reranking managé.

**Signatures à compléter** :
```python
def get_azure_store(index_name=None, search_type="hybrid"): ...
def azure_search(query, index_name=None, k=4, search_type="hybrid"): ...
```

> 💡 **Indice fort** : `AzureSearch(azure_search_endpoint, azure_search_key, index_name, embedding_function=get_embeddings().embed_query, search_type=...)` ; `azure_search` = `get_azure_store(index, search_type).similarity_search(query, k=k, search_type=search_type)`.
> 💡 `searchable=True` sur content = indispensable pour l'hybride (Bug v3).


📝 Slide 6 : Embeddings locaux + coût

POURQUOI fastembed et pas Azure OpenAI ?

fastembed (384d) d'AT02 via `embedding_function` → 0 dépendance Azure OpenAI, 0 coût token. Côté service : Dedicated facturé à l'HEURE dès la création.

| Garde-fou | Pourquoi |
|---|---|
| fastembed local | 0 coût token |
| service Basic PARTAGÉ + index/élève | Free = 1 service/souscription |
| `azure_teardown.sh` en fin | éviter la facturation horaire |


📝 Slide 7 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `azure.search.documents.indexes.SearchIndexClient` — create_or_update_index
- `azure.search.documents.indexes.models` : SearchIndex, SimpleField, SearchableField, SearchField, SearchFieldDataType, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration
- `langchain_community.vectorstores.azuresearch.AzureSearch(embedding_function, search_type)`
- CLI : `az search service create --sku`, `az search admin-key show`, `az group delete`
- Pins : azure-search-documents>=11.5.1, azure-identity>=1.16


📝 Slide 8 : Bug Hunt — à toi de jouer

| Bug | À observer | À trouver |
|-----|-----------|-----------|
| v1 | upload rejeté | dim schéma = dim embedding (384) |
| v2 | recall dégradé | search_type "hybrid" |
| v3 | hybride 0 résultat | content searchable=True |

Cycle : `git apply bugs/vN.patch` → `pytest bugs/test_vN.py` (FAIL, hors-ligne) → `git checkout -- homebutler/rag/vectorstore_azure.py` → `pytest` (PASS) → lis `bugs/vN_explanation.md`.


📝 Slide 9 : Récap & clôture du parcours avancé

Migration FAISS local → Azure AI Search managé. CLI = service, SDK = contenu. Hybrid (vecteur+BM25), embeddings locaux, garde-fous coût.

PARCOURS AVANCÉ : AT07 (MESURER) · AT08 (AMÉLIORER) · AT09 (INDUSTRIALISER).

> 🧹 Ne pars jamais sans `bash ateliers/atelier-09-azure-search/azure_teardown.sh`.
