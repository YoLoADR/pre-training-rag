📝 Slide 1 : Atelier 09 — Azure AI Search (mission en un coup d'œil)

POURQUOI cet atelier ?

L'index FAISS d'AT02 est local : parfait pour apprendre, mais en production on veut un moteur de recherche MANAGÉ, scalable, en cloud. AT09 migre HomeButler vers Azure AI Search. Le fil conducteur : comprendre QUI fait QUOI — le SERVICE se pilote en CLI (`az search`), le CONTENU (index, vecteurs, ingestion, requêtes) se pilote en SDK Python. C'est ce qui rend l'atelier 100% faisable au terminal.

| Bloc | Ce qu'il fait | Plan |
|------|---------------|------|
| Provisionner le service (FOURNI, CLI) | `az search service create` + clés → .env | control plane |
| Créer le schéma d'index (À CODER, SDK) | champs id/content/content_vector(384)/metadata | data plane |
| Ingérer le corpus (SDK) | embeddings fastembed 384d + push API | data plane |
| Requêter 3 modes (À CODER, SDK) | similarity / hybrid / semantic_hybrid | data plane |

> 💡 **Branche élève** : `git checkout student/09-azure-search`. En classe : service Basic PARTAGÉ, ton index = ton trigramme.


📝 Slide 2 : Le concept central — control plane vs data plane

POURQUOI cette distinction change tout ?

Azure AI Search expose DEUX plans d'API. Le control plane gère le SERVICE (créer, scaler, clés, réseau) → CLI `az search`, ARM/Bicep. Le data plane gère le CONTENU (index, champs vectoriels, ingestion, requêtes) → SDK `azure-search-documents` / REST. Conséquence capitale : **il n'existe AUCUNE commande `az search` pour créer un index ou ingérer**. Tout le RAG est en SDK → scriptable au terminal, sans portail.

| Plan | Quoi | Outil |
|------|------|-------|
| Control | service, clés, scaling | CLI `az search` |
| Data | index, vecteurs, ingestion, requêtes | SDK Python / REST |

> 💡 **Analogie** : `az search` construit le BÂTIMENT de la bibliothèque ; le SDK range les LIVRES et répond aux lecteurs. On ne range pas des livres avec une grue.
⚠️ **Piège** — chercher une commande `az search` pour créer un index : elle n'existe pas.


📝 Slide 3 : Le seul élément portail-only (et pourquoi on l'évite)

POURQUOI ne pas utiliser l'assistant graphique ?

Le portail Azure propose un wizard « Import and vectorize data » (no-code) qui crée d'un coup data source + index + indexer + skillset. Pratique pour bricoler, mais NON reproductible et NON versionnable. En atelier (et en prod), on fait l'équivalent en SDK : du code dans git, rejouable. Tout ce que le wizard fait est faisable en REST/SDK.

> 💡 Monitoring : le portail (Overview du service : latence, QPS, throttling) est plus lisible VISUELLEMENT, mais Azure Monitor reste scriptable. Le portail est un confort, pas une obligation.


📝 Slide 4 : Concept — le schéma d'index vectoriel (data plane)

POURQUOI créer le schéma à la main ?

LangChain peut créer l'index automatiquement (en inférant la dimension). On le fait À LA MAIN pour MAÎTRISER les champs — et comprendre ce qui se passe. Les champs sont alignés sur ceux qu'attend LangChain `AzureSearch` : id / content / content_vector / metadata.

```python
# homebutler/rag/vectorstore_azure.py
AZURE_VECTOR_DIM = 384   # = dimension de fastembed MiniLM (DOIT matcher l'embedding)

fields = [
    SimpleField(name="id", type=String, key=True),
    SearchField(name="content", type=String, searchable=True),         # BM25 hybride
    SearchField(name="content_vector", type=Collection(Single),
                searchable=True, vector_search_dimensions=384,
                vector_search_profile_name="hnsw-profile"),
    SearchableField(name="metadata", type=String),                     # source/page JSON
]
```

⚠️ **Piège** — déclarer 1536 (dim OpenAI) alors que fastembed fait 384 → upload rejeté (Bug v1).


📝 Slide 5 : Concept — les 3 modes de recherche

POURQUOI préférer "hybrid" ?

- **similarity** : recherche vectorielle pure (le sens).
- **hybrid** : vecteur + BM25 (mots-clés), fusionnés par RRF → rattrape le vocabulaire divergent ET les termes exacts (codes erreur, marques) que le vecteur seul rate. C'est le bon défaut.
- **semantic_hybrid** : hybrid + semantic ranker d'Azure (tier Basic+, semantic config) → l'équivalent managé du reranking d'AT08.

```python
def get_azure_store(index_name=None, search_type="hybrid"):
    return AzureSearch(azure_search_endpoint=..., azure_search_key=...,
                       index_name=index_name,
                       embedding_function=get_embeddings().embed_query,  # fastembed 384d
                       search_type=search_type)
```

> 💡 `searchable=True` sur `content` est INDISPENSABLE pour le volet BM25 de l'hybride (Bug v3).


📝 Slide 6 : Embeddings locaux + coût

POURQUOI fastembed et pas Azure OpenAI ?

On réutilise fastembed (384d) d'AT02 via `embedding_function` : zéro dépendance Azure OpenAI, zéro coût token. Le contenu est vectorisé en Python puis poussé. Côté service : un tier Dedicated (Free/Basic/…) est facturé à l'HEURE dès la création (pas à l'usage).

| Garde-fou | Pourquoi |
|---|---|
| fastembed local | 0 coût token, cohérent avec le fil rouge |
| service Basic PARTAGÉ + index/élève | Free = 1 service/souscription |
| `azure_teardown.sh` en fin | éviter la facturation horaire qui court |

> 💡 `az group delete` supprime le service ET tout son contenu.


📝 Slide 7 : 📚 Dépendances natives utilisées

**📚 Dépendances natives utilisées**
- `azure.search.documents.indexes.SearchIndexClient(endpoint, credential)` — gestion des index (create_or_update_index)
- `azure.search.documents.indexes.models` : `SearchIndex, SimpleField, SearchableField, SearchField, SearchFieldDataType, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration`
- `langchain_community.vectorstores.azuresearch.AzureSearch(...)` — vector store. Paramètres : - `embedding_function` — `get_embeddings().embed_query` (fastembed) - `search_type` — "similarity" | "hybrid" | "semantic_hybrid"
- CLI `az search service create --sku`, `az search admin-key show`, `az group delete` — control plane
- Pins : `azure-search-documents>=11.5.1`, `azure-identity>=1.16`


📝 Slide 8 : Bug Hunt — les 3 pièges classiques

| Bug | Erreur | Symptôme | Leçon |
|-----|--------|----------|-------|
| v1 | dim schéma 1536 ≠ embedding 384 | upload rejeté par Azure | dim champ = dim embedding |
| v2 | search_type "similarity" | recall dégradé (pas de BM25) | "hybrid" rattrape le vocabulaire |
| v3 | `content` searchable=False | hybride renvoie 0 résultat (silencieux) | un flag de champ ne plante pas, il dégrade |

> 💡 Tests HORS-LIGNE (construction de schéma + analyse statique) : jouables sans service Azure.


📝 Slide 9 : Récap & clôture du parcours avancé

CE QU'ON A FAIT : migré le retrieval local (FAISS) vers un service MANAGÉ (Azure AI Search), en distinguant ce qui se pilote en CLI (le service) de ce qui se code en SDK (le contenu). Recherche hybride (vecteur + BM25), embeddings locaux, garde-fous coût.

LE PARCOURS AVANCÉ COMPLET :
- **AT07** : MESURER (observabilité Langfuse + évaluation RAGAS)
- **AT08** : AMÉLIORER (reranking, multi-query)
- **AT09** : INDUSTRIALISER (vector store managé en cloud)

> 🧹 Ne pars jamais sans `bash ateliers/atelier-09-azure-search/azure_teardown.sh`.
