📝 Slide 1 : Atelier 02 — RAG Simple FAISS (mission en un coup d'œil)

POURQUOI cet atelier après le LLM baseline (AT01) ?

L'Atelier 01 a chiffré que le LLM seul invente ses réponses sur les documents privés (taux d'hallucination ≥ 80 %). Le RAG (Retrieval-Augmented Generation) est la première réponse : indexer les documents, retrouver les chunks pertinents, et les injecter dans le prompt. Cet atelier construit cette chaîne de bout en bout sur les 5 PDFs HomeButler, avec une métrique chiffrée (Recall@5 + Faithfulness) pour prouver la valeur ajoutée.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| Chargement PDF (déjà fourni) | Extrait le texte page par page avec métadonnées (source, n° page) | Sans métadonnées, impossible de citer la source dans la réponse |
| Chunking (À CODER 3 stratégies) | Découpe les pages en morceaux de ~500 caractères | Un PDF entier dépasse le contexte LLM ; les chunks sont la granularité indexable |
| Embeddings (À CODER) | Transforme chaque chunk en vecteur de 384 dimensions | C'est ce vecteur qui permet la recherche par SENS et non par mot-clé |
| Index FAISS (À CODER) | Stocke les vecteurs dans un index ANN | Sans index, comparer la query à 1000 chunks coûte 1000 multiplications. Avec FAISS : O(log n). |
| Évaluation | Recall@5 + Faithfulness sur 5 questions étalons | La cible **0.80 / 0.85** prouve que le système est utilisable en production |

> 💡 **Branche élève** : `git checkout student/02-rag-simple`. Bloqué > 15 min : `git diff student/02-rag-simple atelier/02-rag-simple -- <fichier>`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI séparer plomberie et concept pédagogique ?

L'atelier dure 3h30. Si tu recodes tout (loader PDF + chunking + embedding + FAISS + retriever), tu dépasses de 2h. La règle de blanking : on garde corrigés les éléments qui ne portent PAS le concept central, et on blanke uniquement ce qui matérialise le concept RAG. Résultat : 2 fichiers Python (~6 fonctions au total) ciblés.

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/llm/provider.py` | ✅ Acquis AT01 (corrigé) | LLM déjà fonctionnel |
| `homebutler/rag/ingestion.py` → `load_pdf`, `load_pdf_with_metadata`, `ingest_all_documents` | ✅ Plomberie fournie | Lecture PDF + orchestration — pas le concept RAG |
| `homebutler/rag/ingestion.py` → `chunk_fixed_size`, `chunk_recursive`, `chunk_semantic` | 🛠️ **À CODER** | Concept central : stratégies de découpage |
| `homebutler/rag/vectorstore_faiss.py` → `get_embeddings`, `build_faiss_index`, `load_faiss_index` | 🛠️ **À CODER** | Concept central : embeddings + vector store |
| `ateliers/atelier-02-rag-simple/exercice.py` | ✅ Cadré par TODOs existants | Wrapper qui orchestre les briques que tu codes |
| `ateliers/atelier-02-rag-simple/evaluate_rag.py` | ✅ LLM-judge fourni clé en main | Évaluation Faithfulness — pas du scope |

> 💡 Les fonctions à coder ont **deux niveaux d'indices** dans leur docstring : *léger* (« quel objet chercher ») et *fort* (« quels arguments / quels appels »). Aucun indice ne révèle directement la solution.


📝 Slide 3 : Concept #1 — Chunking récursif (la pierre angulaire)

POURQUOI le chunking récursif est la stratégie par défaut ?

Un PDF est rarement uniforme : des paragraphes longs, des listes, des titres. Le chunking *fixed-size* (couper tous les 512 caractères) tronque souvent une phrase au milieu d'un concept clé. Le *récursif* tente de couper sur les séparateurs naturels du plus large au plus fin : paragraphe → ligne → phrase → mot. Résultat : un chunk reste sémantiquement cohérent.

**Signature à compléter** :

```python
def chunk_recursive(documents, chunk_size=512, chunk_overlap=50):
    """Découpe une liste de Documents en chunks ~512 caractères en respectant
    les séparateurs naturels (paragraphe → ligne → phrase → espace).
    """
    raise NotImplementedError(
        "Atelier 02 § 2.2 — chunking récursif. "
        "Solution finale : git diff student/02-rag-simple atelier/02-rag-simple -- homebutler/rag/ingestion.py"
    )
```

**Indice léger** — LangChain expose une classe dont le nom commence par `Recursive…Splitter`. Le découpage « récursif » signifie : essayer le séparateur le plus large (paragraphe `\n\n`), puis plus fin (ligne `\n`), puis plus fin encore (phrase `.` `!` `?`), puis espace.

**Indice fort** — Instancie le splitter avec `chunk_size`, `chunk_overlap`, et **une liste** de séparateurs ordonnés du plus large au plus fin : `["\n\n", "\n", ".", "!", "?", " ", ""]`. Puis appelle `.split_documents(documents)` — cette méthode (et pas `.split_text()`) préserve les métadonnées (source, page) sur chaque chunk produit.

> 💡 **Analogie cuisine** : tu coupes un gâteau pour servir 8 parts. Tu commences par couper en quart (séparateur large), puis en huitième (plus fin). Tu ne coupes pas au hasard tous les 5 cm — tu respectes les marques naturelles.

⚠️ **Piège fréquent** — passer un seul `separator="\n"` au lieu d'une LISTE : c'est ce que fait `CharacterTextSplitter` (la stratégie *fixed*). Sans la liste, pas de récursivité.

**📚 Dépendances natives utilisées**

- `langchain_text_splitters.RecursiveCharacterTextSplitter(...)` — splitter qui tente ses séparateurs dans l'ordre du plus large au plus fin. Paramètres :
  - `chunk_size: int` — taille cible du chunk en **caractères** (pas tokens). 500-1500 typique pour FR.
  - `chunk_overlap: int` — chevauchement entre chunks consécutifs (10-20 % du `chunk_size`).
  - `separators: list[str]` — liste ORDONNÉE. Le premier séparateur qui produit des chunks ≤ `chunk_size` gagne. Default LangChain : `["\n\n", "\n", " ", ""]`.
  - `length_function: callable` — fonction qui mesure la taille. Default `len` (caractères). Pour mesurer en tokens : `lambda x: len(tokenizer.encode(x))`.
  - `is_separator_regex: bool` — `False` par défaut. Si `True`, les séparateurs sont compilés en regex.
  - `keep_separator: bool` — `True` par défaut. Conserve le séparateur dans le chunk (utile pour ponctuation).

- `splitter.split_documents(documents)` — prend une `list[Document]` et retourne une `list[Document]` chunkée **AVEC métadonnées préservées** (`source`, `page`).
  - À distinguer de `.split_text(str)` qui prend un `str` et retourne `list[str]` — perd les metadata. Toujours préférer `split_documents` quand on part de `Document`.


📝 Slide 4 : Concept #2 — Embeddings (le code-barres sémantique)

POURQUOI on transforme un texte en 384 nombres ?

Un LLM ne sait pas comparer « chaudière à condensation » et « ballon thermodynamique » par leur SENS — il sait seulement comparer caractère par caractère. L'embedding résout ce problème : chaque texte devient un vecteur de N dimensions tel que deux textes proches sémantiquement aient des vecteurs proches géométriquement (cosinus élevé).

**Signature à compléter** :

```python
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# TODO (indice : ce modèle est multilingue FR+EN, quantisé ONNX, ~300 MB de cache,
#                ne nécessite ni torch ni GPU)

def get_embeddings():
    """Retourne un objet embedder LangChain prêt à être passé à FAISS.from_documents."""
    raise NotImplementedError(...)
```

**Indice léger** — Le projet utilise FastEmbed (lib légère, ONNX, CPU-friendly). LangChain expose un wrapper dont le nom commence par `FastEmbed…`.

**Indice fort** — Une seule ligne suffit : `return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)`. FastEmbed télécharge le modèle au premier appel dans `~/.cache/fastembed/`, puis le réutilise.

| Texte | Vecteur (extrait des 384 dimensions) |
|-------|--------------------------------------|
| « ma chaudière fait du bruit » | `[0.21, -0.04, 0.88, ...]` |
| « le chauffage est bruyant » | `[0.22, -0.03, 0.85, ...]` ← très proche |
| « le bail interdit les animaux » | `[-0.12, 0.71, 0.03, ...]` ← très différent |

> 💡 **Analogie GPS** : un embedding = coordonnées GPS du texte dans un espace à 384 dimensions. Deux concepts proches sont géographiquement voisins.

**📚 Dépendances natives utilisées**

- `langchain_community.embeddings.FastEmbedEmbeddings(...)` — wrapper LangChain autour de `fastembed` (ONNX, CPU). Paramètres :
  - `model_name: str` — modèle d'embedding (ex. `"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"`). Téléchargé au 1er usage dans `~/.cache/fastembed/`.
  - `max_length: int` — tronque les textes plus longs (default 512). Si tu chunkes à 500 chars, c'est confortable.
  - `cache_dir: str | None` — répertoire de cache du modèle. Default `~/.cache/fastembed/`.
  - `threads: int | None` — parallélisation CPU. Default = nb de cœurs.
  - `doc_embed_type: "default" | "passage"` — `"passage"` ajoute un préfixe spécifique pour certains modèles asymétriques query/passage.

- Interface LangChain `Embeddings` (méthodes exposées) :
  - `.embed_documents(texts: list[str]) → list[list[float]]` — embedde N textes en N vecteurs (appelé par FAISS à l'indexation).
  - `.embed_query(text: str) → list[float]` — embedde une seule query (appelé au runtime par `similarity_search`).


📝 Slide 5 : Concept #3 — Construire un index FAISS

POURQUOI FAISS plutôt qu'une boucle Python qui compare tous les chunks ?

Naïvement, retrouver les 4 chunks les plus proches d'une question revient à comparer son embedding à TOUS les chunks (1000 multiplications de vecteurs 384-D pour 1000 chunks). À chaque requête. FAISS précompile un index qui retrouve les voisins en quelques millisecondes via des structures arborescentes. Sur 10 000 chunks : ~1 ms au lieu de 200 ms.

**Signature à compléter** :

```python
def build_faiss_index(documents, save_path=None, force_rebuild=False):
    """Construit un index FAISS à partir d'une liste de Document chunkés.
    Recharge l'index existant si déjà sur disque (sauf si force_rebuild=True).
    """
    raise NotImplementedError(...)
```

**Indice léger** — LangChain expose un constructeur de classe (commence par `FAISS.from_...`) pour bâtir un index directement à partir d'une liste de Documents — pas besoin d'instancier un index vide puis d'appeler `.add_documents()`. L'embedder vient de `get_embeddings()` que tu as déjà écrit.

**Indice fort** — Vérifie d'abord si `save_path` existe et que `force_rebuild` est `False` → recharge via `load_faiss_index(save_path)`. Sinon : `vectorstore = FAISS.from_documents(documents, get_embeddings())` puis `vectorstore.save_local(save_path)` pour persister. La similarité par défaut = cosinus normalisé (le standard du RAG).

> 💡 **Analogie** : FAISS = la BIBLIOTHÈQUE organisée par sens (rayons thématiques, fiches), vs lecture séquentielle (parcourir 10 000 livres un par un).

⚠️ **Piège LangChain ≥ 0.1** — `FAISS.load_local()` exige `allow_dangerous_deserialization=True` (FAISS utilise pickle). C'est OK ici car on charge ton propre fichier, jamais celui d'un tiers.

**📚 Dépendances natives utilisées**

- `langchain_community.vectorstores.FAISS.from_documents(documents, embedding)` — méthode de classe qui bâtit un index FAISS depuis une liste de Documents + un embedder. Paramètres :
  - `documents: list[Document]` — les chunks à indexer.
  - `embedding: Embeddings` — l'objet retourné par `get_embeddings()`.
  - `**kwargs` — options FAISS bas-niveau ; `distance_strategy="COSINE"` par défaut (le standard du RAG).

- `vectorstore.save_local(folder_path, index_name="index")` — persiste l'index sur disque. Produit 2 fichiers : `index.faiss` (binaire FAISS) + `index.pkl` (mapping pickle ID FAISS → Document).

- `FAISS.load_local(folder_path, embeddings, index_name="index", allow_dangerous_deserialization=False)` — recharge depuis disque. Paramètres :
  - `folder_path: str` — où trouver les 2 fichiers.
  - `embeddings: Embeddings` — embedder à attacher (doit être **identique** à celui qui a indexé).
  - ⚠️ `allow_dangerous_deserialization: bool` — **doit être `True`** depuis LangChain 0.1. OK pour ton propre index, jamais pour un index tiers (pickle = code arbitraire exécutable).

- `vectorstore.similarity_search(query, k=4, filter=None, fetch_k=20)` — récupère les k chunks les plus proches. Paramètres :
  - `query: str` — la question (sera embeddée via `.embed_query`).
  - `k: int` — nombre de chunks retournés. 4 = bon compromis contexte/coût.
  - `filter: dict | None` — filtre sur metadata (ex. `{"source": "notice_chaudiere.pdf"}`). FAISS ne filtre pas efficacement — préférer ChromaDB en AT03.
  - `fetch_k: int` — nombre de candidats à fetcher AVANT filtrage (default 20).


📝 Slide 6 : Pipeline complet — du PDF à la réponse citée

POURQUOI vue d'ensemble avant de te lancer ?

L'orchestration `ingest_all_documents` (déjà fournie) appelle tes 3 fonctions dans l'ordre : chargement → chunking → indexation. Le retriever (déjà câblé dans `exercice.py` via `similarity_search`) appelle l'index FAISS. Le LLM (AT01) compose la réponse en citant la source extraite des métadonnées des chunks.

```
PDF (data/raw/notice_chaudiere.pdf)
   │
   ▼  load_pdf_with_metadata (FOURNI)
[Document(page="...", metadata={"source": "notice_chaudiere.pdf", "page": 2}), ...]
   │
   ▼  chunk_recursive (À CODER)
[Document(page="extrait 500 caractères", metadata={"source": ..., "page": 2}), ...]
   │
   ▼  get_embeddings + build_faiss_index (À CODER)
FAISS index sauvegardé sur disque
   │
   ▼  vectorstore.similarity_search("Comment purger un radiateur ?", k=4)
4 chunks les plus pertinents
   │
   ▼  RAG_QA_TEMPLATE | llm  (AT01)
"Pour purger un radiateur, voici la procédure [notice_chaudiere.pdf, p.2]..."
```

**Critère de succès** (commande à lancer) :
```bash
python ateliers/atelier-02-rag-simple/evaluate_rag.py
# 🎯 Cible :  Recall@5 ≥ 0.80  ET  Faithfulness ≥ 0.85
```

> 💡 Si tu n'atteins pas la cible :
> - `Recall@5 < 0.80` → augmente `chunk_overlap` (50 → 100), ou réduis `chunk_size` (512 → 300) pour avoir plus de granularité.
> - `Faithfulness < 0.85` → relis ton system prompt (AT01) ; force la citation entre crochets [nom_du_doc].


📝 Slide 7 : Récap — comment travailler sur la branche `student/02-rag-simple`

POURQUOI ce workflow protège ton apprentissage ?

Les blanks créent une friction productive : tu ne peux PAS te contenter de copier la solution. Tu DOIS lire les 2 niveaux d'indices, verbaliser au checkpoint, puis seulement consulter le diff. Le `.claude/CLAUDE.md` local refuse également les demandes de code complet à Claude Code / Cursor.

```bash
# 1. Récupère la branche élève
git clone <repo> && cd training-rag
git checkout student/02-rag-simple
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Lis le QUICK-START (1 page)
cat ateliers/atelier-02-rag-simple/QUICK-START.md

# 3. Lis le GUIDE-ELEVE (section "Atelier 02 en un coup d'œil")
cat ateliers/atelier-02-rag-simple/GUIDE-ELEVE.md | head -60

# 4. Ouvre les fichiers blankés et lis les docstrings (indice léger + fort)
$EDITOR homebutler/rag/ingestion.py
$EDITOR homebutler/rag/vectorstore_faiss.py

# 5. Code, teste
pytest ateliers/atelier-02-rag-simple/                  # tronc commun
python ateliers/atelier-02-rag-simple/checkpoints/check_1.py  # QCM + verbalisation
python ateliers/atelier-02-rag-simple/evaluate_rag.py   # 🎯 Recall@5 ≥ 0.80

# 6. Bloqué > 15 min : en dernier recours
git diff student/02-rag-simple atelier/02-rag-simple -- homebutler/rag/ingestion.py
```

> 💡 **Règle d'or** : si tu peux **expliquer ton code à voix haute** (« j'ai choisi chunk_overlap=50 parce que… »), tu as compris. Si tu ne peux que **lire ton code**, retourne au carnet de bord.
