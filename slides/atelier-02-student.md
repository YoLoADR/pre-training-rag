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

> 💡 **Branche élève** : `git checkout student/02-rag-simple` dans `training-rag`. Solution : `git diff student/02-rag-simple atelier/02-rag-simple -- <fichier>`.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI séparer plomberie et concept pédagogique ?

L'atelier dure 3h30. Si l'élève recode tout (loader PDF + chunking + embedding + FAISS + retriever), il dépasse de 2h. La règle de blanking : on garde corrigés les éléments qui ne portent PAS le concept central, et on blanke uniquement ce qui matérialise le concept RAG. Résultat : 2 fichiers Python (~6 fonctions au total) ciblés.

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/llm/provider.py` | ✅ Acquis AT01 (corrigé) | LLM déjà fonctionnel |
| `homebutler/rag/ingestion.py` → `load_pdf`, `load_pdf_with_metadata`, `ingest_all_documents` | ✅ Plomberie fournie | Lecture PDF + orchestration — pas le concept RAG |
| `homebutler/rag/ingestion.py` → `chunk_fixed_size`, `chunk_recursive`, `chunk_semantic` | 🛠️ **À CODER** | Concept central : stratégies de découpage |
| `homebutler/rag/vectorstore_faiss.py` → `get_embeddings`, `build_faiss_index`, `load_faiss_index` | 🛠️ **À CODER** | Concept central : embeddings + vector store |
| `ateliers/atelier-02-rag-simple/exercice.py` | ✅ Cadré par TODOs existants | Wrapper qui orchestre les briques codées par l'élève |
| `ateliers/atelier-02-rag-simple/evaluate_rag.py` | ✅ LLM-judge fourni clé en main | Évaluation Faithfulness — pas du scope élève |

> 💡 Les fonctions à coder ont **deux niveaux d'indices** dans leur docstring : *léger* (« quel objet chercher ») et *fort* (« quels arguments / quels appels »). Aucun indice ne révèle directement la solution.


📝 Slide 3 : Concept #1 — Chunking récursif (la pierre angulaire)

POURQUOI le chunking récursif est la stratégie par défaut ?

Un PDF est rarement uniforme : des paragraphes longs, des listes, des titres. Le chunking *fixed-size* (couper tous les 512 caractères) tronque souvent une phrase au milieu d'un concept clé. Le *récursif* tente de couper sur les séparateurs naturels du plus large au plus fin : paragraphe → ligne → phrase → mot. Résultat : un chunk reste sémantiquement cohérent.

**Évolution à apporter** (vue corrigée) :

```python
# AVANT (blank dans student/02) : la fonction lève NotImplementedError
# APRÈS (atelier/02) :

def chunk_recursive(documents, chunk_size=512, chunk_overlap=50):
    # AVANTAGE pédagogique : le SPLITTER RECURSIF essaie d'abord le séparateur
    # le plus "large" (paragraphe \n\n), puis plus fin (ligne \n), puis encore
    # plus fin (phrase via . ! ?), puis espace, puis vide. Au moment où ça tient
    # dans chunk_size, il s'arrête. Conséquence : on coupe TRÈS rarement au
    # milieu d'une phrase utile.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,        # ~500 caractères : assez gros pour porter
                                       #   une idée, assez petit pour 4 chunks/réponse
        chunk_overlap=chunk_overlap,  # ~10-20 % du chunk_size — un overlap de 50
                                       #   préserve les phrases coupées entre 2 chunks
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        #  ↑ ORDRE CRITIQUE : du plus large au plus fin. LangChain essaie ces
        #    séparateurs DANS CET ORDRE — c'est la "récursivité" du nom.
        length_function=len,           # on mesure en caractères, pas en tokens
    )
    return splitter.split_documents(documents)
    #  ↑ .split_documents() préserve les métadonnées (source, page) sur
    #    chaque chunk produit — indispensable pour citer la source plus tard.
```

> 💡 **Analogie cuisine** : tu coupes un gâteau pour servir 8 parts. Tu commences par couper en quart (séparateur large), puis en huitième (plus fin). Tu ne coupes pas au hasard tous les 5 cm — tu respectes les marques naturelles.

⚠️ **Piège fréquent** — passer un seul séparateur (`separator="\n"`) au lieu d'une LISTE : c'est ce que fait `CharacterTextSplitter` (la stratégie *fixed*). Sans la liste, pas de récursivité.


📝 Slide 4 : Concept #2 — Embeddings (le code-barres sémantique)

POURQUOI on transforme un texte en 384 nombres ?

Un LLM ne sait pas comparer « chaudière à condensation » et « ballon thermodynamique » par leur SENS — il sait seulement comparer caractère par caractère. L'embedding résout ce problème : chaque texte devient un vecteur de N dimensions tel que deux textes proches sémantiquement aient des vecteurs proches géométriquement (cosinus élevé). On peut alors faire une recherche par proximité.

**Évolution à apporter** :

```python
# AVANT : NotImplementedError
# APRÈS :

EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# AVANTAGE : modèle MULTILINGUE (FR + EN + autres) — important pour HomeButler
# qui mélange du français bail et de l'anglais technique. Modèle quantisé ONNX :
# pas besoin de torch ni de GPU, tourne en CPU sur Mac M1, ~300 MB de cache.

def get_embeddings():
    # Une seule ligne. On instancie le modèle, FastEmbed le télécharge la
    # première fois dans ~/.cache/fastembed/ puis le réutilise.
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
```

| Texte | Vecteur (extrait des 384 dimensions) |
|-------|--------------------------------------|
| « ma chaudière fait du bruit » | `[0.21, -0.04, 0.88, ...]` |
| « le chauffage est bruyant » | `[0.22, -0.03, 0.85, ...]` ← très proche |
| « le bail interdit les animaux » | `[-0.12, 0.71, 0.03, ...]` ← très différent |

> 💡 **Analogie GPS** : un embedding = coordonnées GPS du texte dans un espace à 384 dimensions. Deux concepts proches sont géographiquement voisins.


📝 Slide 5 : Concept #3 — Construire un index FAISS

POURQUOI FAISS plutôt qu'une boucle Python qui compare tous les chunks ?

Naïvement, retrouver les 4 chunks les plus proches d'une question revient à comparer son embedding à TOUS les chunks (1000 multiplications de vecteurs 384-D pour 1000 chunks). À chaque requête. FAISS (Facebook AI Similarity Search) précompile un index qui retrouve les voisins en quelques millisecondes via des structures arborescentes (LSH, IVF, HNSW). Sur 10 000 chunks : ~1 ms au lieu de 200 ms.

**Évolution à apporter** :

```python
# AVANT : NotImplementedError
# APRÈS :

def build_faiss_index(documents, save_path=None, force_rebuild=False):
    path = save_path or config.FAISS_PATH

    # AVANTAGE : on RECHARGE si l'index existe — pas besoin de re-vectoriser
    # toutes les pages à chaque démarrage de l'API. Gain : 30 s → instantané.
    if os.path.exists(path) and not force_rebuild:
        print(f"  Index FAISS existant chargé depuis {path}")
        return load_faiss_index(path)

    # Sinon on construit : `FAISS.from_documents` calcule l'embedding de chaque
    # chunk via `embeddings.embed_documents(...)` puis insère dans l'index.
    # Similarité par défaut = cosinus normalisé (le standard du RAG).
    print(f"  Construction de l'index FAISS ({len(documents)} chunks)...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    # IMPORTANT : on sauve sur disque. L'index FAISS = 2 fichiers binaires
    # (.faiss + .pkl). Sans save_local, l'index serait perdu à chaque restart.
    vectorstore.save_local(path)
    print(f"  ✓ Index FAISS sauvegardé dans {path}")
    return vectorstore
```

> 💡 **Analogie** : FAISS = la BIBLIOTHÈQUE organisée par sens (rayons thématiques, fiches), vs lecture séquentielle (parcourir 10 000 livres un par un).

⚠️ **Piège LangChain ≥ 0.1** — `FAISS.load_local()` exige désormais `allow_dangerous_deserialization=True` (FAISS utilise pickle). C'est OK ici car on charge NOTRE propre fichier, jamais celui d'un tiers.


📝 Slide 6 : Pipeline complet — du PDF à la réponse citée

POURQUOI vue d'ensemble avant de se lancer ?

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
# Cible :  Recall@5 ≥ 0.80  ET  Faithfulness ≥ 0.85
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

> 💡 **Règle d'or** : si tu peux **expliquer ton code à voix haute** au formateur (« j'ai choisi chunk_overlap=50 parce que… »), tu as compris. Si tu ne peux que **lire ton code**, retourne au carnet de bord.
