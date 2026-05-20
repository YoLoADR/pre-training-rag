# Plan : Slides formation RAFT — RAG et Fine Tuning d'un LLM

## Contexte

Yohann est formateur IA/ML. Il donne une formation PLB (réf. RAFT) de 3 jours "RAG et Fine
Tuning d'un LLM" (Data Scientists / ingénieurs IA / dev Python). Il crée ses supports dans
gamma.app à partir d'un fichier `.md` unique. Ce fichier contient les 10 slides × 6 chapitres
= **60 slides** de la formation, en français, **sans blocs de code** (Gamma gère mal),
intégrant des insights de recherche internet (historique, chiffres clés, bonnes/mauvaises
pratiques) et faisant progresser le projet fil rouge **HomeButler AI** au fil des chapitres.

---

## Fichier de sortie

`/Users/yohannravino/Factory/pre-training-rag/slides-formation-raft.md`

---

## Règles de format (extraites des exemples validés)

**Inspirés de `slides-inspiration-1.md` et `slides-inspiration-2.md` :**

- **Pas de bloc de code** — remplacer par tableaux comparatifs, listes numérotées, pseudo-flux
  textuel ou description d'architecture en prose.
- Titre de chapitre : `Chapitre X : [Titre] — [Jour]` (plain text, H1 implicite)
- Objectif : `🎯 Objectif du chapitre` suivi d'un paragraphe unique
- Slides : `📝 Slide N : [Titre]` (plain text, pas de `#`)
- Ouverture de chaque slide : `POURQUOI [question] ?` en gras ou majuscules
- Tables : format markdown `|col|col|` — jamais de listes à puces là où une table convient
- Callout positif : `> 💡 [texte]`
- Avertissement : `⚠️ **Titre** — description`
- Recap final : `🎓 Ce que vous devez retenir` + table `| Concept | Pourquoi c'est important |`
- Transition : `➡️ Prochain chapitre` suivi d'une phrase de teaser
- Séparateur horizontal `---` entre chaque chapitre

---

## Progression du fil rouge HomeButler AI (vue globale)

```
Chapitre 1 → Vision du projet : conciergerie IA, architecture cible, pourquoi RAG + FT
Chapitre 2 → Les 6 PDFs → PyMuPDF → 3 stratégies de découpage → FAISS → premier Q&A
Chapitre 3 → Pipeline LangChain + 4 outils ReAct + traces LangSmith/Langfuse
Chapitre 4 → Les 150 Q&A pairs synthétiques → fine-tuning LoRA sur base HomeButler
Chapitre 5 → FastAPI (4 routes) + Streamlit (4 pages) + Docker Compose → déploiement VPS
Chapitre 6 → Architecture finale : FastEmbed + FAISS (RAG) + LoRA FT = système hybride
```

---

## CHAPITRE 1 — Introduction aux LLM et concepts RAG (Jour 1)

**🎯 Objectif** : Comprendre pourquoi les LLM ont transformé l'IA en 3 ans, identifier leurs
limites fondamentales (hallucination, knowledge cutoff), situer RAG et Fine Tuning comme les
deux réponses complémentaires, et découvrir le projet fil rouge HomeButler AI qui sera construit
sur 3 jours.

---

**Slide 1 — L'explosion des LLM 2017-2024 : pourquoi maintenant ?**
- POURQUOI : "Pourquoi les LLM ont-ils transformé l'IA en seulement 3 ans ?"
- Contenu : Timeline des ruptures — table chronologique
- Table (colonnes : Année | Modèle / Événement | Rupture) :
  - 2017 — Transformer (Vaswani et al.) — Self-attention remplace RNN/CNN
  - 2018 — BERT + GPT-1 — Pré-entraînement + fine-tuning devient le paradigme
  - 2020 — GPT-3 175B — Few-shot learning sans réentraînement
  - 2022 mars — InstructGPT (RLHF) — 1,3B paramètres surpasse GPT-3 175B en qualité
  - 2022 nov — ChatGPT — 100 millions d'utilisateurs en 2 mois (record absolu)
  - 2023 — LLaMA (Meta) + Mistral (Paris) — Open-source démocratise l'accès
- ⚠️ **Idée reçue n°1** — "Plus grand = meilleur" : InstructGPT 1,3B > GPT-3 175B après RLHF
- Stat clé : ChatGPT → application la plus vite adoptée de l'histoire du numérique

**Slide 2 — L'architecture Transformer : l'attention est tout**
- POURQUOI : "Pourquoi toutes les IA de langage partagent-elles la même architecture depuis 2017 ?"
- Contenu : L'intuition du mécanisme d'attention (chaque token "regarde" tous les autres)
- Table (Critère | Avant Transformer : RNN | Après : Transformer) :
  - Parallélisme : séquentiel | massif (GPU-friendly)
  - Dépendances longues : difficile | natif
  - Entraînement : slow | fast at scale
  - Texte + images + code : non | oui (multimodal)
- Composants clés à retenir : Tokenizer → Embedding → Self-Attention → Feed-Forward → Output
- Callout : > 💡 Un LLM ne "comprend" pas — il prédit le prochain token le plus probable

**Slide 3 — Forces et faiblesses d'un LLM : connaître les limites avant de coder**
- POURQUOI : "Pourquoi anticiper les limites d'un LLM évite des bugs coûteux en production ?"
- Contenu : Table des forces vs faiblesses avec impact concret
- Table (Dimension | Force | Limite) :
  - Connaissance générale | Vaste corpus d'entraînement | Cutoff date (figée) 
  - Génération | Fluide, cohérente | Hallucinations : 8-42% selon domaine
  - Polyvalence | Code, traduction, résumé | Raisonnement formel fragile
  - Personnalisation | Fine-tuning possible | Catastrophic forgetting sans précautions
- Stat clé : taux d'hallucination 8% (questions factuelles générales) → 42% (domaines techniques sans contexte)
- ⚠️ **Piège** — Tester un LLM uniquement sur des cas favorables : en production, les cas-limites révèlent les failles

**Slide 4 — L'écosystème Python LLM : la carte des outils**
- POURQUOI : "Pourquoi connaître l'écosystème avant d'ouvrir un notebook ?"
- Contenu : Vue d'ensemble des 4 couches
- Table (Couche | Outils | Rôle) :
  - Modèles & API | HuggingFace Hub, Anthropic API, Ollama | Accéder au LLM
  - Orchestration | LangChain 0.3, LlamaIndex | Enchaîner les appels
  - Vectorstores | FAISS (local), ChromaDB (persistant), Pinecone (cloud) | Stocker les embeddings
  - Évaluation / Observabilité | LangSmith, Langfuse, MLflow | Tracer et optimiser
- Callout : > 💡 Dans ce cours, l'outil correspond toujours à un rôle — on n'installe rien "au cas où"

**Slide 5 — Open-source vs modèles fermés : le bon choix selon le contexte**
- POURQUOI : "Pourquoi le choix du modèle est une décision d'architecture, pas de préférence ?"
- Contenu : Comparaison sur 5 critères décisifs
- Table (Critère | Open-source (Mistral, Llama 3) | Fermé (GPT-4, Claude, Gemini)) :
  - Coût d'inférence | Hébergement propre = $0/token | $0,01-0,06 par 1k tokens
  - Confidentialité | Données restent on-premise | Données envoyées au provider
  - Personnalisation | Fine-tuning total | Fine-tuning limité ou payant
  - Performance SOTA | Proche (Mistral dépasse GPT-3.5) | Légèrement supérieure
  - Maintenance | À votre charge | Gérée par le provider
- ⚠️ **Piège** — Choisir open-source par principe sans GPU : un modèle 7B quantisé en CPU peut prendre 30s/réponse

**Slide 6 — Qu'est-ce que le RAG ? L'origine du problème**
- POURQUOI : "Pourquoi le RAG est-il né d'un problème de dates, pas d'un problème de taille ?"
- Contenu : Le problème du knowledge cutoff + la solution RAG
- Table (Problème | Sans RAG | Avec RAG) :
  - Données récentes (post-entraînement) | Hallucination ou "je ne sais pas" | Récupérées en temps réel
  - Données propriétaires (contrats, notices) | Inconnues du modèle | Indexées et retrouvables
  - Source de l'info | Opaque (paramètres) | Citée (chunk source)
  - Mise à jour | Réentraînement coûteux | Réindexation rapide
- Origine : Lewis et al. 2020, Meta AI — "RAG for Knowledge-Intensive NLP Tasks"
- Callout : > 💡 RAG = mémoire externe non-paramétrique — le modèle reste gelé, seule la base de données évolue

**Slide 7 — Qu'est-ce que le Fine Tuning ? Apprendre vs mémoriser**
- POURQUOI : "Pourquoi fine-tuner un modèle quand on peut déjà lui passer du contexte ?"
- Contenu : Cas d'usage où le FT surpasse le RAG (style, raisonnement spécialisé)
- Table (Technique | Mécanisme | Modifie les poids ? | Coût mise en œuvre) :
  - Prompting | Instructions dans le prompt | Non | Quasi nul
  - RAG | Contexte injecté dynamiquement | Non | Moyen (indexation)
  - Fine-tuning complet | Tous les paramètres réentraînés | Oui | Élevé (GPU A100)
  - LoRA/QLoRA | Petites matrices ajoutées aux poids gelés | Partiellement | Faible/modéré
- Évolution : BERT full FT (2018) → LoRA Hu et al. (2021) → QLoRA Dettmers (2023) → RAFT Zhang et al. (2024)

**Slide 8 — RAG vs Fine Tuning : première comparaison**
- POURQUOI : "Pourquoi choisir le bon outil dès le départ évite des semaines de refactorisation ?"
- Contenu : Vue d'ensemble des critères de choix (chapitre 6 approfondit)
- Table (Critère | RAG gagne | Fine Tuning gagne) :
  - Données qui changent souvent | ✓ | ✗
  - Ton / style de marque | ✗ | ✓
  - Budget GPU limité | ✓ | ✗
  - Latence critique < 500ms | ✗ | ✓
  - Citations / traçabilité | ✓ | ✗
  - < 500 exemples d'entraînement | ✓ | ✗
- Callout : > 💡 90% des projets commencent par le RAG — le FT vient compléter, rarement remplacer

**Slide 9 — 5 idées reçues à démystifier**
- POURQUOI : "Pourquoi les idées reçues sur les LLM génèrent-elles des erreurs de conception coûteuses ?"
- Contenu : 5 mythe vs réalité (format tableau)
- Table (Idée reçue | Réalité) :
  - "Plus grand = meilleur" | InstructGPT 1,3B > GPT-3 175B grâce au RLHF
  - "Les LLM comprennent" | Prédiction de token suivant — pas de modèle du monde
  - "Fine Tuning suffit" | Knowledge cutoff + coût de réentraînement continu
  - "Le RAG est complexe à mettre en place" | 50 lignes Python avec LangChain
  - "Les hallucinations sont rares" | 8-42% sans RAG selon le domaine testé
- ⚠️ **Piège** — Exposer un LLM en production sans évaluation d'hallucination : coût réputationnel réel

**Slide 10 — HomeButler AI : le projet fil rouge des 3 jours**
- POURQUOI : "Pourquoi construire une vraie application de bout en bout plutôt que des exemples isolés ?"
- Contenu : Présentation de HomeButler AI
- Table (Composant | Technologie | Chapitre qui le construit) :
  - 6 PDFs notices + CSV énergie | PyMuPDF + Pandas | Chapitre 2
  - Pipeline RAG + vectorstore | FAISS + ChromaDB + FastEmbed | Chapitre 2
  - Agent ReAct 4 outils | LangChain 0.3 + hwchase17/react | Chapitre 3
  - Dataset 150 Q&A | Scripts génération + format JSONL | Chapitre 4
  - API + UI | FastAPI + Streamlit + Gradio | Chapitre 5
  - Déploiement | Docker Compose + VPS Linux | Chapitre 5
- Architecture cible : Utilisateur → Streamlit → FastAPI → Agent ReAct → RAG + Services
- Callout : > 💡 L'application sera opérationnelle sur Mac Intel (Python 3.13) et VPS Linux (Docker)

🎓 **Ce que vous devez retenir — Chapitre 1**
| Concept | Pourquoi c'est important |
|---|---|
| Timeline 2017-2024 | ChatGPT = disruption en 2 mois — le contexte explique l'urgence |
| Architecture Transformer | Base commune à tous les LLM — pas besoin de la coder, juste de la comprendre |
| Hallucinations 8-42% | Chiffre à citer en projet pour justifier le RAG |
| Écosystème 4 couches | Choisir le bon outil pour le bon rôle |
| Open-source vs fermé | Décision d'architecture avec conséquences coût/confidentialité |
| RAG = mémoire externe | Répond au problème du knowledge cutoff sans réentraînement |
| Fine Tuning = adaptation | Pour le style, le ton, le raisonnement spécialisé |
| RAG d'abord, FT ensuite | 90% des projets suivent cet ordre |
| 5 idées reçues | Prévenir les erreurs de conception courantes |
| HomeButler AI | Ce qu'on construit ensemble sur 3 jours |

➡️ **Prochain chapitre** : On passe de la théorie à la pratique — découvrir les 5 composantes
d'un RAG (embedding, vectorstore, chunking, retrieval, génération) en les appliquant immédiatement
aux 6 PDFs notices de HomeButler.

---

## CHAPITRE 2 — Création d'un RAG simple avec Python (Jour 1)

**🎯 Objectif** : Comprendre les 5 composantes d'un RAG (chargement, découpage, embedding,
stockage vectoriel, récupération + génération), identifier la stratégie de chunking adaptée
à son cas d'usage, et appliquer ces concepts aux notices PDF de HomeButler AI.

---

**Slide 1 — Les 5 composantes d'un RAG : le flux de bout en bout**
- POURQUOI : "Pourquoi comprendre chaque étape avant de copier un tutoriel ?"
- Contenu : Flux linéaire en 5 étapes avec rôle de chacune
- Table (Étape | Ce que ça fait | Outil typique dans HomeButler) :
  - 1. Chargement | Lire les PDFs, CSV, JSON | PyMuPDF (fitz), Pandas
  - 2. Découpage (chunking) | Diviser en segments cohérents | LangChain TextSplitter
  - 3. Embedding | Convertir en vecteurs numériques | FastEmbed (paraphrase-multilingual-MiniLM)
  - 4. Stockage vectoriel | Indexer les vecteurs | FAISS (local) + ChromaDB (persistant)
  - 5. Récupération + Génération | Retrouver les chunks + répondre | EnsembleRetriever + LLM
- Callout : > 💡 Les étapes 1-4 sont faites une seule fois (indexation). L'étape 5 s'exécute à chaque question

**Slide 2 — Les embeddings : transformer du texte en vecteurs**
- POURQUOI : "Pourquoi la similitude sémantique n'est pas un simple calcul de mots-clés ?"
- Contenu : L'intuition vectorielle + comparaison des modèles
- Analogie : "chien" et "labrador" → vecteurs proches ; "chien" et "voiture" → vecteurs éloignés
- Table (Modèle | Dimension | Taille | Multilingue | Usage idéal) :
  - paraphrase-multilingual-MiniLM-L12-v2 | 384 | 100 Mo (ONNX) | ✓ | Notre formation (CPU)
  - BAAI/bge-base-en-v1.5 | 768 | 270 Mo | ✗ (anglais) | Projets anglophones
  - text-embedding-ada-002 | 1536 | API cloud | ✗ | Production OpenAI
  - mxbai-embed-large | 1024 | 350 Mo | ~ | Qualité SOTA locale
- ⚠️ **Piège** — Premier chargement = 100-470 Mo téléchargés en cache (~/.cache) : prévoir avant le TP

**Slide 3 — Bases de données vectorielles : FAISS, ChromaDB, Pinecone**
- POURQUOI : "Pourquoi ne pas stocker les embeddings dans un DataFrame Pandas ?"
- Contenu : Différences fondamentales + choix selon contexte
- Table (Critère | FAISS | ChromaDB | Pinecone) :
  - Type | Bibliothèque in-memory | DB locale persistante | SaaS cloud
  - Persistance | Sauvegarde manuelle (.index) | Automatique (dossier) | Automatique (cloud)
  - Filtrage métadonnées | Limité | Natif | Natif + avancé
  - Scalabilité | Limité (RAM) | Millions de chunks | Milliards
  - Coût | Gratuit | Gratuit | Payant au-delà du free tier
  - Usage HomeButler | ✓ (recherche principale) | ✓ (persistance) | ✗
- Note FAISS : charger avec `allow_dangerous_deserialization=True` (requis, expliqué en TP)

**Slide 4 — Chunking : l'art de découper les documents**
- POURQUOI : "Pourquoi la qualité du découpage détermine la qualité du RAG ?"
- Contenu : 3 stratégies avec avantages/inconvénients
- Table (Stratégie | Principe | Avantage | Inconvénient | Quand l'utiliser) :
  - Fixed-size | 400 tokens, 50 overlap | Simple, prévisible | Coupe les phrases | Données non structurées
  - Recursive Character | Séparateurs hiérarchiques (\n\n > \n > . > espace) | Respecte structure | Taille variable | PDFs structurés (notre cas)
  - Semantic (SemanticChunker) | Découpe aux ruptures sémantiques | Très cohérent | Lent, coûteux | Corpus premium, petits volumes
- Stat : 400-512 tokens avec 10-20% overlap = consensus industrie 2024-2026
- Callout : > 💡 HomeButler utilise les 3 stratégies en parallèle — comparer leur rappel est l'objectif du TP

**Slide 5 — Bonnes pratiques de chunking (et les erreurs à éviter)**
- POURQUOI : "Pourquoi 80% de la qualité d'un RAG se joue au moment du découpage ?"
- Contenu : Tableau pratique des décisions clés
- Table (Décision | Bonne pratique | Mauvaise pratique) :
  - Taille de chunk | 400-512 tokens (contexte lisible) | Chunks de 50 tokens (trop fragmentés) ou 2000 (context overflow)
  - Overlap | 10-20% (40-100 tokens) | 0% overlap (perd les transitions)
  - Métadonnées | Ajouter source, page, date dans chaque chunk | Pas de métadonnées (pas de filtrage possible)
  - Séparateurs | Adapter au format (PDF ≠ Markdown ≠ CSV) | Même stratégie pour tous
- ⚠️ **Piège** — Réindexer FAISS accumule les chunks : utiliser `force_rebuild=False` ou supprimer l'index avant réindexation

**Slide 6 — Recherche sémantique et récupération**
- POURQUOI : "Pourquoi retrouver les bons documents est plus difficile qu'il n'y paraît ?"
- Contenu : Mécanismes de récupération + hybridation
- Table (Méthode | Principe | Force | Limite) :
  - Dense (cosine similarity) | Vecteur requête vs vecteurs corpus | Sémantique, synonymes | Lent sur gros corpus
  - Sparse (BM25) | Fréquence des mots-clés | Exact, rapide | Ignore la sémantique
  - Hybride (EnsembleRetriever) | Dense (0.6) + BM25 (0.4) | Le meilleur des deux | Plus complexe
  - MMR (Max Marginal Relevance) | Diversité + pertinence | Évite les doublons | Trade-off qualité/vitesse
- HomeButler : EnsembleRetriever avec FAISS (0.6) + ChromaDB (0.4) + MMR activé

**Slide 7 — Reranking : pourquoi les 5 premiers ne suffisent pas**
- POURQUOI : "Pourquoi récupérer 10 chunks pour n'en garder que 3 ?"
- Contenu : Pipeline retrieve → rerank → generate
- Table (Étape | Modèle type | Vitesse | Précision) :
  - Retrieval initial (bi-encoder) | Embedding model | Rapide (ms) | Bonne
  - Reranking (cross-encoder) | cross-encoder/ms-marco | Modéré (100ms) | Très bonne
  - Sans reranking | — | Rapide | Variable (bruit possible)
- Callout : > 💡 Le reranking est souvent la seule optimisation qui donne un gain immédiatement visible sur la qualité des réponses
- Stat : reranking peut améliorer la précision de 15-30% selon les benchmarks RAGAs 2024

**Slide 8 — Métriques d'évaluation d'un RAG**
- POURQUOI : "Pourquoi mesurer un RAG autrement qu'avec 'ça marche' ou 'ça marche pas' ?"
- Contenu : 4 métriques RAGAs + interprétation
- Table (Métrique | Ce qu'elle mesure | Bonne valeur | Symptôme si faible) :
  - Faithfulness | La réponse est-elle fidèle au contexte récupéré ? | > 0.85 | Hallucination post-retrieval
  - Answer Relevance | La réponse répond-elle à la question ? | > 0.80 | Prompt mal formulé
  - Context Precision | Les chunks récupérés sont-ils pertinents ? | > 0.75 | Chunking ou embedding à revoir
  - Context Recall | Le bon chunk a-t-il été récupéré ? | > 0.70 | Top-k trop petit ou mauvais index
- ⚠️ **Piège** — Évaluer uniquement avec des exemples que vous avez vous-même écrits : biais de confirmation

**Slide 9 — Anti-patterns RAG : les erreurs classiques**
- POURQUOI : "Pourquoi la majorité des projets RAG en production échouent sur des détails d'implémentation ?"
- Contenu : Tableau des 5 anti-patterns les plus fréquents
- Table (Anti-pattern | Symptôme | Correction) :
  - Chunking naïf fixe sans overlap | Réponses tronquées, contexte manquant | Recursive splitter + 10-20% overlap
  - Pas de reranking | Réponses génériques, bruit | Ajouter cross-encoder
  - Contexte window débordé | Erreur de tokens, réponse incohérente | Limiter chunk_size × top_k
  - Pas de métadonnées | Impossible de filtrer par date/source | Enrichir les chunks à l'indexation
  - FAISS rechargé sans flag | Erreur silencieuse ou crash | Toujours allow_dangerous_deserialization=True

**Slide 10 — HomeButler RAG : construire la première brique**
- POURQUOI : "Comment les concepts RAG s'appliquent concrètement aux données HomeButler ?"
- Contenu : Les données sources et la pipeline d'indexation
- Table (Source | Format | Nb documents | Stratégie chunking) :
  - Notices équipements | 6 PDFs (PyMuPDF/fitz) | ~150 pages | Recursive Character
  - Données énergie | CSV 365 jours | 1 fichier | Fixed-size (lignes)
  - Catalogue producteurs | JSON 30 entrées | 1 fichier | Document entier
  - Q&A paires | JSONL 150 paires | Dataset FT | Indexation séparée
- Résultat après indexation : 49 chunks → FAISS (recherche principale) + ChromaDB (persistance)
- Embedding : paraphrase-multilingual-MiniLM-L12-v2, 384 dimensions, 100 Mo (ONNX/FastEmbed)
- Callout : > 💡 PyMuPDF s'installe `pip install pymupdf` mais s'importe `import fitz` — c'est un piège documenté

🎓 **Ce que vous devez retenir — Chapitre 2**
| Concept | Pourquoi c'est important |
|---|---|
| 5 composantes RAG | Indexation = une fois. Retrieval+Génération = à chaque requête |
| Embedding ≠ keywords | Similitude sémantique capture synonymes et paraphrases |
| FAISS vs ChromaDB | FAISS = vitesse, ChromaDB = persistance — HomeButler utilise les deux |
| Chunking stratégique | Recursive splitter adapté aux PDFs structurés |
| 400-512 tokens + 10% overlap | Consensus industrie pour le meilleur rappel |
| EnsembleRetriever | Dense (0.6) + BM25 (0.4) = meilleur des deux mondes |
| Reranking | +15-30% de précision pour un coût modeste |
| 4 métriques RAGAs | Faithfulness / Answer Relevance / Context Precision / Context Recall |
| allow_dangerous_deserialization | Requis pour charger un index FAISS local |
| pymupdf → import fitz | Piège de nommage documenté dans HomeButler |

➡️ **Prochain chapitre** : Maintenant que nos données sont indexées, on assemble un pipeline
complet avec LangChain, on crée un agent ReAct avec 4 outils, et on trace tout avec LangSmith.

---

## CHAPITRE 3 — Intégration dans un pipeline RAG (Jour 2)

**🎯 Objectif** : Comprendre pourquoi utiliser un framework d'orchestration, comparer LangChain,
LlamaIndex et Haystack, assembler un pipeline RAG complet, implémenter le pattern ReAct pour les
agents, et connecter l'observabilité via LangSmith/Langfuse.

---

**Slide 1 — Pourquoi un framework ? API directes vs orchestration**
- POURQUOI : "Pourquoi ne pas simplement appeler l'API d'Anthropic directement ?"
- Contenu : Comparaison appels directs vs framework
- Table (Critère | Appels API directs | Framework LangChain) :
  - Gestion des chaînes d'étapes | Code manuel | Natif (LCEL)
  - Changement de LLM | Réécriture | Changer 1 variable d'env
  - Memory / historique | À coder | Intégré (ConversationMemory)
  - Traçabilité | Logs custom | LangSmith natif
  - RAG complet | 200 lignes | 20 lignes
- ⚠️ **Piège** — Utiliser LangChain pour un simple appel LLM sans chaîne : sur-engineering nuisible

**Slide 2 — LangChain : histoire, architecture et état en 2026**
- POURQUOI : "Pourquoi LangChain est-il devenu le standard de fait en 18 mois ?"
- Contenu : Genèse + architecture modulaire
- Timeline : Octobre 2022 (lancement) → 2023 (framework le plus étoilé GitHub) → 0.3.x (LCEL)
- Table (Module LangChain | Rôle | Exemple HomeButler) :
  - Document Loaders | Charger PDFs, JSON, CSV | PyMuPDFLoader
  - Text Splitters | Découper les documents | RecursiveCharacterTextSplitter
  - Vectorstores | Indexer + rechercher | FAISS, Chroma
  - Chains (LCEL) | Assembler des étapes | retrieval_chain
  - Agents | Décider quelle action faire | AgentExecutor ReAct
  - Callbacks | Observer les appels | LangSmithCallbackHandler
- Note : LangChain 0.3.x = LCEL (LangChain Expression Language) remplace les anciennes Chain classes

**Slide 3 — LangChain vs LlamaIndex vs Haystack : choisir le bon outil**
- POURQUOI : "Pourquoi le choix du framework impacte la maintenabilité du projet sur 2 ans ?"
- Contenu : Comparaison des 3 frameworks
- Table (Critère | LangChain 0.3 | LlamaIndex 0.10 | Haystack 2.x) :
  - Lancé | Oct 2022 | Nov 2022 | 2019 (deepset)
  - Focus | Orchestration générale | RAG + indexation | Pipelines NLP/RAG
  - Courbe d'apprentissage | Modérée | Faible (RAG focus) | Modérée
  - Agents | ✓ (natif, ReAct) | ✓ (QueryEngine) | ✓ (Pipeline)
  - Observabilité | LangSmith (natif) | Phoenix/LlamaDebugger | Hayhooks
  - Communauté | Très large | Large | Moyenne
  - Notre choix | ✓ | ✗ | ✗
- Callout : > 💡 LlamaIndex excelle pour les projets purement RAG sans agent. LangChain est meilleur pour les agents complexes.

**Slide 4 — Pipeline RAG complet avec LangChain**
- POURQUOI : "Pourquoi visualiser le pipeline complet avant de coder évite les refactorisations ?"
- Contenu : Flux de bout en bout
- Table (Étape | Composant LangChain | Ce qu'il fait) :
  - 1. Chargement | PyMuPDFLoader | Lit les 6 PDFs
  - 2. Découpage | RecursiveCharacterTextSplitter | 400 tokens, 50 overlap
  - 3. Embedding | FastEmbedEmbeddings | paraphrase-multilingual-MiniLM
  - 4. Indexation | FAISS.from_documents() | Crée l'index vectoriel
  - 5. Retrieval | EnsembleRetriever | Dense + BM25 + MMR
  - 6. Chain | create_retrieval_chain() | Retriever → Prompt → LLM → Réponse
- ⚠️ **Piège** — LCEL (opérateur `|`) vs chaînes legacy : ne pas mélanger les deux styles dans un projet

**Slide 5 — Tool Chains : orchestrer plusieurs sources de données**
- POURQUOI : "Pourquoi HomeButler a besoin de combiner plusieurs sources (PDFs, énergie, météo) ?"
- Contenu : Concept de tool routing + composition
- Table (Source | Outil LangChain | Ce qu'il retourne) :
  - Notices PDF | search_docs (RAG retriever) | Chunks pertinents + source
  - Données énergie | analyze_energy (service Python) | Anomalies détectées, stats
  - Catalogue producteurs | find_products (haversine search) | Producteurs locaux triés
  - Météo | weather_tool (API externe + cache TTL) | Météo actuelle + prévision
- Note : RouterChain ou Agent décide quel outil appeler selon la question
- Callout : > 💡 Chaque outil est une fonction Python wrappée dans un `@tool` LangChain — pas de dépendance à un LLM

**Slide 6 — Agents LLM : du chaîne à la décision autonome**
- POURQUOI : "Pourquoi un agent répond mieux à 'ma consommation est-elle normale ce mois-ci ?' qu'une simple chaîne ?"
- Contenu : Différence fondamentale chain vs agent
- Table (Dimension | Chain | Agent) :
  - Flux | Prédéfini, séquentiel | Dynamique, décisionnel
  - Outils | Toujours les mêmes dans l'ordre | Choisis selon la question
  - Correction d'erreur | Impossible (linéaire) | Réessaie avec une autre approche
  - Coût en tokens | Prévisible | Variable (plus élevé)
  - Cas d'usage | Q&A simple, résumé | Multi-étapes, sources multiples
- ⚠️ **Piège** — Un agent sans `max_iterations` peut boucler indéfiniment (surtout avec Ollama) : toujours limiter à 8 tours

**Slide 7 — Pattern ReAct : Thought → Action → Observation**
- POURQUOI : "Pourquoi ReAct est le pattern d'agent le plus robuste pour les LLM open-source ?"
- Contenu : Les 3 phases du pattern + boucle
- Table (Phase | Ce que le LLM écrit | Exemple HomeButler) :
  - Thought | Raisonnement interne | "La question concerne l'énergie, je dois appeler analyze_energy"
  - Action | Nom de l'outil + paramètre | analyze_energy("juillet 2026")
  - Observation | Résultat de l'outil | "Anomalie détectée : +200% en juin"
  - Thought (suite) | Décision suivante | "Résultat obtenu, je peux répondre à l'utilisateur"
- Origine : Yao et al. 2022 — "ReAct: Synergizing Reasoning and Acting in Language Models"
- Callout : > 💡 `hwchase17/react` (LangChain Hub) est le prompt le plus robuste — il fonctionne avec Claude ET Ollama

**Slide 8 — Observabilité : tracer chaque appel avec LangSmith/Langfuse**
- POURQUOI : "Pourquoi un système non tracé est un système impossible à optimiser ?"
- Contenu : Ce qu'on trace et pourquoi
- Table (Donnée tracée | Pourquoi c'est utile | Outil) :
  - Prompt complet envoyé | Débugger les mauvaises réponses | LangSmith / Langfuse
  - Réponse brute du LLM | Voir si le parsing échoue | LangSmith / Langfuse
  - Latence par étape | Identifier le goulot (retrieval vs LLM) | LangSmith
  - Coût en tokens | Estimer la facture mensuelle | LangSmith
  - Chunks récupérés | Vérifier la qualité du retrieval | LangSmith
- Note HomeButler : support dual LangSmith (formation) + Langfuse (prod) via `TRACING_PROVIDER` env var

**Slide 9 — Erreurs communes dans les pipelines LangChain**
- POURQUOI : "Pourquoi les pipelines LangChain tombent souvent pour des raisons évitables ?"
- Contenu : Top 5 erreurs documentées
- Table (Erreur | Cause | Solution) :
  - Agent en boucle infinie | max_iterations absent avec Ollama | handle_parsing_errors=True + max_iterations=8
  - Réponses de mauvaise qualité | Prompt hwchase17/react mal adapté | Utiliser le prompt hub, ne pas le modifier
  - Lenteur au démarrage | Agent/vectorstore rechargé à chaque requête | @st.cache_resource + lifespan FastAPI
  - Chunks non retrouvés | Top-k trop petit | Augmenter k + activer reranking
  - Erreur de parsing JSON | Réponse Ollama mal formatée | Augmenter max_iterations + parser robuste
- ⚠️ **Piège** — Ignorer les warnings LangChain sur les classes dépréciées : ils cassent en 0.4.x

**Slide 10 — HomeButler Pipeline : l'agent ReAct avec 4 outils**
- POURQUOI : "Comment la logique ReAct orchestre les 4 sources de données de HomeButler ?"
- Contenu : Architecture de l'agent HomeButler
- Table (Outil | Fichier | Description | Données source) :
  - search_docs | agent/tools.py | Recherche RAG dans les notices | 6 PDFs FAISS/ChromaDB
  - analyze_energy | agent/tools.py | Détecte anomalies énergie | CSV 365j (3 anomalies injectées)
  - find_products | agent/tools.py | Trouve producteurs locaux (haversine) | JSON 30 producteurs
  - weather_tool | agent/tools.py | Météo actuelle + cache TTL | API externe + cachetools.TTLCache
- Fichiers concernés : `homebutler/agent/tools.py`, `homebutler/agent/react_agent.py`
- Callout : > 💡 L'agent est initialisé une seule fois au démarrage de l'API (FastAPI lifespan) — pas à chaque requête

🎓 **Ce que vous devez retenir — Chapitre 3**
| Concept | Pourquoi c'est important |
|---|---|
| Framework = accélérateur | LangChain > API directe dès qu'il y a une chaîne ou un agent |
| LangChain 0.3 LCEL | Syntaxe opérateur \| — ne pas mélanger avec legacy chains |
| LangChain vs LlamaIndex | LangChain pour agents, LlamaIndex pour RAG pur |
| 5 étapes pipeline RAG | Load → Split → Embed → Index → Retrieve+Generate |
| 4 outils HomeButler | search_docs / analyze_energy / find_products / weather |
| Chain vs Agent | Chain = séquentiel fixe. Agent = décisionnel dynamique |
| ReAct (Yao 2022) | Thought → Action → Observation — le pattern le plus robuste |
| max_iterations=8 | Éviter les boucles infinies avec Ollama |
| Observabilité LangSmith | Tracer prompt + réponse + latence + coût à chaque appel |
| lifespan FastAPI | Initialiser l'agent une fois, pas à chaque requête |

➡️ **Prochain chapitre** : Le pipeline RAG est opérationnel. Maintenant on explore quand et
comment fine-tuner le modèle de base — LoRA, QLoRA, préparation des données, et les pièges
à éviter sur GPU limité.

---

## CHAPITRE 4 — Fine-tuning avec HuggingFace (Jour 2)

**🎯 Objectif** : Comprendre quand le fine-tuning surpasse le RAG, distinguer Full FT / LoRA /
QLoRA, savoir préparer un dataset de qualité, estimer les ressources nécessaires, et appliquer
ces concepts aux 150 Q&A pairs du projet HomeButler.

---

**Slide 1 — Quand le RAG ne suffit pas : 4 cas d'usage du fine-tuning**
- POURQUOI : "Pourquoi fine-tuner alors qu'on a déjà un RAG qui fonctionne ?"
- Contenu : Les 4 situations où le FT apporte une valeur différente
- Table (Cas d'usage | Pourquoi RAG est insuffisant | Solution FT) :
  - Ton et style de marque | Le contexte ne modifie pas le comportement général du LLM | Fine-tuner le ton/style
  - Raisonnement spécialisé | Le LLM générique raisonne autrement qu'un expert métier | LoRA sur corpus expert
  - Latence critique < 500ms | RAG ajoute 500ms de retrieval incompressible | FT = réponse directe
  - Format de sortie contraint | Le LLM ignore les instructions de format complexes | FT sur examples formatés
- Callout : > 💡 Fine-tuner ne remplace pas le RAG — les deux sont complémentaires (voir chapitre 6)

**Slide 2 — Full Fine Tuning vs PEFT : la révolution de l'efficacité**
- POURQUOI : "Pourquoi 99% des praticiens utilisent PEFT plutôt que le fine-tuning complet ?"
- Contenu : Comparaison des ressources requises
- Table (Méthode | Paramètres entraînés | GPU requis | Coût estimé | Qualité relative) :
  - Full Fine Tuning | 100% | 4× A100 80GB (280GB) | $2 000-5 000 | Référence (100%)
  - LoRA (rank 16) | 0,1-1% | 1× A100 40GB | $200-500 | 95-98%
  - QLoRA (4-bit + LoRA) | 0,1-1% | 1× RTX 4090 24GB | $100-300 | 92-96%
  - Prompting seul | 0% | Aucun | $0 | Variable
- Stat clé : LoRA (Hu et al., juin 2021) — 99% de réduction des paramètres entraînables

**Slide 3 — LoRA : l'intuition des matrices de rang faible**
- POURQUOI : "Pourquoi LoRA fonctionne-t-il malgré si peu de paramètres entraînés ?"
- Contenu : L'hypothèse des faibles dimensions + paramètres pratiques
- Intuition : Les changements de poids lors d'un fine-tuning ont une dimension intrinsèque faible
- Fonctionnement (sans code) : On ajoute deux petites matrices A et B à chaque couche. Pendant l'entraînement, seules A et B sont modifiées. Les poids originaux restent gelés.
- Table (Hyperparamètre | Valeur usuelle | Effet) :
  - Rank (r) | 8-16 (début) → 32-64 (avancé) | Plus élevé = plus de capacité + risque d'overfitting
  - Alpha | 2× rank généralement | Échelle des adaptateurs
  - Target modules | q_proj, v_proj | Couches d'attention visées
  - Dropout | 0.05-0.1 | Régularisation
- ⚠️ **Piège** — Rank trop élevé sur peu de données = mémorisation, pas généralisation

**Slide 4 — QLoRA : fine-tuner sur un GPU grand public**
- POURQUOI : "Pourquoi QLoRA a démocratisé le fine-tuning en mai 2023 ?"
- Contenu : Les 3 innovations de QLoRA + impact pratique
- Table (Innovation | Ce que ça fait | Impact mémoire) :
  - Quantification 4-bit (NF4) | Le modèle de base est chargé en 4-bit | Divisé par 4
  - Paged Optimizers | Gestion CPU/GPU swap pendant l'entraînement | Évite OOM
  - LoRA adapters en bf16 | Les adaptateurs restent en précision haute | Gradients stables
- Avant QLoRA : fine-tuner un 70B = 4× A100 80GB
- Après QLoRA : fine-tuner un 70B = 2× A100 48GB ; fine-tuner un 7B = 1× RTX 4090 24GB
- Callout : > 💡 Dettmers et al., mai 2023 — une seule publication a rendu le fine-tuning accessible à des milliers d'équipes

**Slide 5 — Préparation des données : le facteur numéro 1**
- POURQUOI : "Pourquoi 500 exemples de qualité surpassent 5 000 exemples bruyants ?"
- Contenu : Principes de construction d'un bon dataset de fine-tuning
- Table (Critère | Bonne pratique | Anti-pattern) :
  - Volume | 500-2 000 paires de qualité | 10 000 paires auto-générées sans relecture
  - Format | Instruction / Réponse (Alpaca) ou Chat (ShareGPT) | Format incohérent entre exemples
  - Diversité | Couvrir tous les cas d'usage cibles | 80% du dataset sur le même type de question
  - Bruit | Corriger les fautes, valider les réponses | Laisser les réponses incorrectes
  - Split | 80/10/10 train/validation/test | Pas de validation set = overfitting invisible
- Stat : Dans les benchmarks HuggingFace 2024, la qualité des données explique 60% de la variance de performance finale

**Slide 6 — Hyperparamètres clés du fine-tuning LoRA**
- POURQUOI : "Quels hyperparamètres surveiller en priorité pour éviter les résultats décevants ?"
- Contenu : Guide des hyperparamètres critiques
- Table (Hyperparamètre | Valeur de départ recommandée | Symptôme si mal réglé) :
  - Learning rate | 1e-4 à 5e-4 | Trop élevé : catastrophic forgetting. Trop bas : pas d'apprentissage
  - Batch size | 4-8 (avec gradient accumulation) | Trop petit : convergence lente. Trop grand : OOM
  - Nombre d'epochs | 1-3 | > 3 : overfitting sur petit dataset
  - Warmup steps | 10% des steps totaux | Sans warmup : instabilité au démarrage
  - Gradient accumulation | 4 si petit batch | Sans : gradients bruités
- ⚠️ **Piège** — Entraîner 10 epochs sur 150 exemples = mémorisation parfaite, généralisation nulle

**Slide 7 — GPU et ressources : estimations pour un projet réel**
- POURQUOI : "Pourquoi estimer les ressources AVANT de lancer l'entraînement ?"
- Contenu : Matrice ressources / coûts par scénario
- Table (Modèle | Méthode | GPU minimum | Durée estimée | Coût cloud 2026) :
  - 7B paramètres | QLoRA | RTX 4090 24GB | 1-2h / 1k steps | $5-15
  - 7B paramètres | LoRA | A100 40GB | 30min / 1k steps | $10-20
  - 13B paramètres | QLoRA | 2× RTX 4090 | 2-4h / 1k steps | $20-40
  - 70B paramètres | QLoRA | 2× A100 48GB | 8-16h / 1k steps | $100-300
  - Mac Intel | ❌ | Aucun GPU CUDA | — | Formation uniquement |
- Callout : > 💡 Pour la formation, on prépare le dataset et les configs sur Mac — l'entraînement s'exécute sur GPU cloud ou VPS

**Slide 8 — Évaluation : comment savoir si le fine-tuning a fonctionné ?**
- POURQUOI : "Pourquoi 'ça répond mieux' n'est pas une métrique d'évaluation ?"
- Contenu : Métriques objectives + évaluation humaine
- Table (Métrique | Ce qu'elle mesure | Limite) :
  - Perplexité (PPL) | Fluidité des réponses générées | Ne mesure pas la justesse factuelle
  - BLEU | Similarité n-gram avec réf. humaine | Pénalise la créativité, dépassé
  - F1 (token overlap) | Couverture des tokens attendus | Bonne pour QA extractif
  - Semantic Similarity | Distance cosinus avec réponse référence | Bonne pour paraphrase
  - Évaluation humaine (50-100 ex.) | Qualité globale réelle | Coûteux mais seul gold standard
- Bonne pratique : automatiser avec 3-4 métriques + valider 50 exemples humainement avant déploiement

**Slide 9 — 5 pièges classiques du fine-tuning**
- POURQUOI : "Pourquoi la plupart des premiers fine-tunings échouent pour des raisons évitables ?"
- Contenu : Top 5 pièges avec diagnostic
- Table (Piège | Symptôme | Correction) :
  - Catastrophic forgetting | Le modèle oublie l'anglais ou le code après FT sur données françaises | Mélanger 20-30% de données générales
  - Overfitting sur < 500 exemples | Train loss → 0, val loss ↑ | LoRA rank faible + early stopping
  - Mauvais base model | Modèle anglophone FT sur données françaises = accent | Choisir Mistral pour le français
  - Learning rate trop élevé | Réponses incohérentes dès l'epoch 1 | LR 1e-4, warmup 10%
  - Pas de split validation | Overfitting invisible, découvert en prod | Toujours 80/10/10
- ⚠️ **Piège spécifique Mac Intel** — onnxruntime 1.26+ n'a pas de wheel pour macOS x86_64 : utiliser Python 3.13.5 + onnxruntime 1.23.2

**Slide 10 — HomeButler Dataset : les 150 Q&A pairs pour le fine-tuning**
- POURQUOI : "Comment préparer le dataset HomeButler pour un fine-tuning LoRA ?"
- Contenu : Structure et construction du dataset
- Table (Type de question | Nb paires | Exemple de sujet | Source) :
  - Notices équipements | ~50 | "Comment réinitialiser le thermostat ?" | 6 PDFs
  - Analyse énergie | ~30 | "Ma consommation de juin est-elle anormale ?" | CSV anomalies
  - Producteurs locaux | ~30 | "Quels fromagers sont à moins de 20km ?" | JSON producteurs
  - Conciergerie générale | ~40 | "Recommande un plombier ce week-end" | Génération synthétique
- Format : JSONL avec champs `instruction`, `input`, `output` (format Alpaca)
- Script générateur : `scripts/generate_qa_dataset.py`
- Callout : > 💡 Ces 150 paires sont générées synthétiquement — en production, on préfère 500+ paires validées par des humains

🎓 **Ce que vous devez retenir — Chapitre 4**
| Concept | Pourquoi c'est important |
|---|---|
| 4 cas d'usage FT | Ton, raisonnement spécialisé, latence, format — RAG ne couvre pas ces cas |
| LoRA = 99% de params gelés | Fine-tuner sans modifier les poids originaux |
| QLoRA = 4-bit + LoRA | Fine-tuner un 7B sur un RTX 4090 24GB |
| Qualité > quantité des données | 500 bons exemples > 5 000 bruyants |
| Learning rate 1e-4 à 5e-4 | Trop élevé = catastrophic forgetting |
| Rank 8-16 pour démarrer | Augmenter seulement si la validation stagne |
| Split 80/10/10 | Sans validation set, overfitting invisible |
| Mac Intel + Python 3.14 | Incompatible onnxruntime — utiliser Python 3.13.5 + onnxruntime 1.23.2 |
| Dataset HomeButler | 150 paires JSONL, 4 types de questions |
| Évaluation automatique + humaine | 3-4 métriques + 50 exemples humains avant déploiement |

➡️ **Prochain chapitre** : Le modèle est entraîné. Comment le déployer, le quantiser pour
l'inférence CPU/GPU, l'exposer via FastAPI, et superviser son comportement en production ?

---

## CHAPITRE 5 — Déploiement, bonnes pratiques, optimisation et supervision (Jour 3)

**🎯 Objectif** : Maîtriser les étapes du passage en production (quantisation, API, interface),
choisir entre Ollama et Jan.ai pour le déploiement local, implémenter la supervision avec
LangSmith ou MLflow, anticiper les risques de sécurité, et déployer HomeButler AI sur VPS.

---

**Slide 1 — Du prototype à la production : les 5 étapes**
- POURQUOI : "Pourquoi un modèle qui marche dans un notebook ne marche pas forcément en production ?"
- Contenu : Roadmap de mise en production
- Table (Étape | Ce qui se passe | Piège courant) :
  - 1. Notebook | Test rapide, itération | Pas reproductible, pas scalable
  - 2. API locale (FastAPI) | Exposer le modèle | Modèle rechargé à chaque requête sans cache
  - 3. API sécurisée | Rate limiting, auth, injection filter | Oublier les headers CORS et sécurité
  - 4. Interface utilisateur | Streamlit ou Gradio | @st.cache_resource oublié = crash sur rechargement
  - 5. Conteneurisation | Docker Compose | dépendances OS (onnxruntime, CUDA) non gérées
- Callout : > 💡 HomeButler parcourt ces 5 étapes — chaque piège a été rencontré et documenté

**Slide 2 — Quantisation : GGUF, GPTQ, AWQ**
- POURQUOI : "Pourquoi quantiser un modèle avant déploiement sur GPU limité ?"
- Contenu : Les 3 formats de quantisation avec leurs caractéristiques
- Table (Format | Algorithme | Qualité conservée | Vitesse | Compatibilité) :
  - GGUF (llama.cpp) | Format fichier universel | 92% | Bonne | CPU + GPU partiel (Ollama) ✓
  - GPTQ | Quantif. 4-bit par colonne | 90% | Rapide | GPU uniquement (RTX 3060+)
  - AWQ | Activation-Aware Weight Quant. | 95% | Modérée | GPU (RTX 4080+)
- Recommandation : GGUF Q4_K_M = meilleur ratio qualité/vitesse pour 8-16GB RAM (format Ollama)
- Callout : > 💡 AWQ > GPTQ en qualité, mais GGUF reste le format le plus universel pour déploiement hybride CPU/GPU

**Slide 3 — Déploiement local : Ollama vs Jan.ai**
- POURQUOI : "Quand choisir Ollama, quand choisir Jan.ai ?"
- Contenu : Comparaison des deux solutions
- Table (Critère | Ollama | Jan.ai) :
  - Interface | CLI + API REST | Interface graphique desktop
  - Lancement | `ollama run mistral` | Clic dans l'application
  - Accélération | NVIDIA CUDA + Apple Metal + AMD ROCm | NVIDIA + Metal
  - Support d'outils | Limité (sans framework) | Limité
  - Format modèles | GGUF natif | GGUF natif
  - Logs de debug | Faciles (CLI) | Opaques (GUI)
  - Intégration LangChain | ✓ (ChatOllama) | ✗ (pas d'API standard)
  - Cas HomeButler | LLM_PROVIDER=ollama sur VPS | Démonstration élève débutant
- ⚠️ **Piège** — ChatOllama vs ChatAnthropic : `max_tokens` (Anthropic) vs `num_predict` (Ollama) — paramètre différent

**Slide 4 — API avec FastAPI : les patterns de production**
- POURQUOI : "Pourquoi FastAPI est le standard de fait pour exposer un LLM en Python ?"
- Contenu : Patterns clés d'une API LLM robuste
- Table (Pattern | Rôle | Détail HomeButler) :
  - Lifespan (startup) | Initialiser agent + vectorstores une fois | `@asynccontextmanager` dans `api/main.py`
  - Streaming (StreamingResponse) | Réponse en temps réel token par token | Endpoint `/chat`
  - Rate limiting | Limiter les abus | 100 tokens/min ou 10 req/min par IP
  - Timeout | Éviter les requêtes qui durent | 30-120s selon taille modèle
  - Middleware injection filter | Bloquer les prompt injections | Regex FR+EN avant parsing body
- Endpoints HomeButler : `/health`, `/chat`, `/consumption/analyze`, `/products/search`, `/orders`

**Slide 5 — Interfaces utilisateur : Gradio vs Streamlit**
- POURQUOI : "Quelle interface pour quel public ?"
- Contenu : Comparaison des deux frameworks UI
- Table (Critère | Gradio 5.x | Streamlit 1.x) :
  - Démarrage | ~10 lignes | ~30 lignes
  - Public | Démonstration rapide, chercheur | Application multi-pages, data scientist
  - Multi-pages | Tabs uniquement | Pages natives (st.navigation)
  - Cache ressources | Non | @st.cache_resource (indispensable avec LLM)
  - Authentification | Simple (username/password) | Optionnel (tiers)
  - Usage HomeButler | Prototype (gradio_prototype.py) | App de prod (4 pages Streamlit)
- ⚠️ **Piège Streamlit** — Sans `pip install -e .` sur le package homebutler, Streamlit ne trouve pas les imports locaux

**Slide 6 — Supervision LLM : LangSmith vs MLflow**
- POURQUOI : "Pourquoi l'observabilité LLM est différente de l'observabilité ML classique ?"
- Contenu : Ce qu'on supervise et comment
- Table (Critère | LangSmith | MLflow 2.x) :
  - Tracing natif LLM | ✓ (prompt + réponse + tokens + latence) | Partiellement (plugin)
  - Courbe d'apprentissage | Faible (auto avec LangChain) | Modérée
  - Coût | Gratuit (limité) → payant | Gratuit (self-hosted)
  - Débug chains | ✓ (replay pas-à-pas) | ✗
  - Métriques ML classiques | ✗ | ✓ (loss, accuracy, confusion matrix)
  - Usage HomeButler | Formation RAFT (TRACING_PROVIDER=langsmith) | — |
- Note : Langfuse est l'alternative production (self-hostable, RGPD, `TRACING_PROVIDER=langfuse`)

**Slide 7 — Sécurité : 5 risques critiques d'exposition d'un LLM**
- POURQUOI : "Pourquoi sécuriser un LLM est différent de sécuriser une API REST classique ?"
- Contenu : Les 5 risques OWASP Gen AI 2025
- Table (Risque | Description | Mitigation HomeButler) :
  - Prompt injection | L'utilisateur écrit "Ignore les instructions et..." | Middleware regex + validation input
  - Exfiltration via RAG | Requête malicieuse récupère des données sensibles du vectorstore | Contrôle d'accès sur les collections
  - Credentials exposés | Token API hardcodé dans le code | Variables d'environnement + .env gitignored
  - Absence rate limiting | Coût API illimité = facture explosive | 10 req/min par IP minimum
  - Logs insuffisants | Impossible de détecter un abus | LangSmith/Langfuse : tout tracer
- ⚠️ **Piège** — Tester uniquement en local cache les problèmes de latence, de timeout et de concurrence qui apparaissent en prod

**Slide 8 — Bonnes pratiques de production**
- POURQUOI : "Quelles pratiques différencient un POC d'une application maintenue 6 mois ?"
- Contenu : Checklist de mise en production
- Table (Pratique | Pourquoi | Implémentation) :
  - Cache résultats fréquents | Réduire latence et coût API | cachetools.TTLCache (météo 1h)
  - Variables d'environnement | Sécurité + portabilité | .env.example versionné, .env gitignored
  - Retry avec backoff | Résistance aux pannes transitoires | tenacity ou httpx retry
  - Graceful degradation | L'app reste utilisable si un service est indisponible | Fallback texte si RAG échoue
  - Health check | Monitoring infra | Endpoint `/health` retourne statut de tous les composants

**Slide 9 — Erreurs courantes au déploiement**
- POURQUOI : "Pourquoi les déploiements LLM échouent souvent pour des raisons non-ML ?"
- Contenu : Top 5 erreurs opérationnelles
- Table (Erreur | Symptôme | Solution) :
  - Modèle rechargé à chaque requête | Latence 10-30s, OOM | lifespan FastAPI + @st.cache_resource
  - CORS mal configuré | Erreur bloquante depuis le frontend | Configurer CORSMiddleware avec origins
  - Pas de rate limiting | Coût API explosif | SlowAPI ou middleware custom
  - python-multipart trop ancien | Gradio crash au démarrage | python-multipart >= 0.0.18
  - Homebutler non installé en editable | ModuleNotFoundError dans Streamlit | pip install -e . après requirements

**Slide 10 — HomeButler Déploiement : FastAPI + Streamlit + Docker**
- POURQUOI : "Comment assembler tous les composants HomeButler dans un déploiement cohérent ?"
- Contenu : Architecture de déploiement
- Table (Composant | Port | Fichier | Dépendances) :
  - FastAPI API | 8000 | api/main.py + 4 routers | Agent ReAct + RAG
  - Streamlit | 8501 | homebutler/app.py | 4 pages UI
  - Gradio prototype | 7860 | gradio_prototype.py | Agent direct
  - Docker Compose | — | docker-compose.yml | api/Dockerfile + ui/Dockerfile
- Cibles de déploiement : Mac Intel (Python 3.13 + onnxruntime 1.23.2) / Mac ARM (Python 3.13+ ok) / VPS Linux x86_64 (Docker, Python 3.13+ ok)
- Callout : > 💡 Sur Mac Intel, Python 3.14 est incompatible avec onnxruntime — Microsoft a abandonné le support x86_64 sur macOS

🎓 **Ce que vous devez retenir — Chapitre 5**
| Concept | Pourquoi c'est important |
|---|---|
| 5 étapes notebook → prod | Chaque étape a ses pièges spécifiques |
| GGUF Q4_K_M | Meilleur format universel CPU/GPU pour Ollama |
| Ollama vs Jan.ai | Ollama = intégration LangChain, Jan.ai = démo GUI |
| Lifespan FastAPI | Agent initialisé une fois — pas à chaque requête |
| @st.cache_resource Streamlit | Évite le rechargement du modèle à chaque interaction |
| pip install -e . | Résout ModuleNotFoundError dans Streamlit |
| LangSmith = observabilité LLM | Tracer prompt + réponse + latence + coût |
| 5 risques sécurité | Prompt injection, exfiltration RAG, rate limiting, credentials |
| python-multipart >= 0.0.18 | Fix de compatibilité Gradio 5.x documenté |
| Mac Intel Python 3.13 | onnxruntime 1.26+ ARM-only — pin à 1.23.2 |

➡️ **Prochain chapitre** : Tout est déployé. Il est temps de répondre à la vraie question :
quand choisir RAG, quand choisir Fine Tuning, et quand combiner les deux ? RAFT apporte
la réponse en 2024.

---

## CHAPITRE 6 — Fine Tuning vs RAG (Jour 3)

**🎯 Objectif** : Maîtriser les critères de choix entre RAG, Fine Tuning et architecture hybride,
comprendre le papier RAFT (Zhang et al. 2024), calculer le coût total sur 12 mois, et valider
l'architecture finale de HomeButler AI.

---

**Slide 1 — Pourquoi cette question est stratégique en 2026**
- POURQUOI : "Pourquoi le mauvais choix entre RAG et Fine Tuning peut coûter 3 mois de retard ?"
- Contenu : Les conséquences réelles d'un mauvais choix
- Table (Choix erroné | Conséquence concrète | Coût estimé de correction) :
  - FT choisi pour données volatiles | Réentraînement toutes les semaines | $2k/mois GPU + 2 sem/mois ingénieur
  - RAG choisi pour besoin de ton de marque | Qualité médiocre, prompt engineering sans fin | 3 mois de patches
  - Aucun des deux (prompting seul) | Hallucinations en prod → incident client | Coût réputationnel
  - Hybride prématuré | Complexité × 3, maintenance lourde | 4 sem supplémentaires MVP
- Callout : > 💡 En 2026, la décision RAG vs FT vs hybride est devenue une compétence d'architecture à part entière

**Slide 2 — Comparaison approfondie : 8 critères de décision**
- POURQUOI : "Quels critères objectifs permettent de trancher sans hésitation ?"
- Contenu : Tableau de décision exhaustif
- Table (Critère | RAG | Fine Tuning | Hybride RAFT) :
  - Données changeantes fréquemment | ✓ | ✗ | ✓ |
  - Style / ton de marque | ✗ | ✓ | ✓ |
  - Citations / traçabilité nécessaires | ✓ | ✗ | ✓ |
  - Latence < 500ms critique | ✗ | ✓ | ~ |
  - Budget GPU limité | ✓ | ✗ | ~ |
  - < 500 exemples de training | ✓ | ✗ | ✗ |
  - Raisonnement métier spécialisé | ✗ | ✓ | ✓ |
  - Mise en prod < 1 semaine | ✓ | ✗ | ✗ |

**Slide 3 — Quand choisir le RAG**
- POURQUOI : "Dans quels scénarios le RAG est-il la solution dominante ?"
- Contenu : Les 5 cas où le RAG est clairement supérieur
- Table (Scénario | Pourquoi RAG gagne | Exemple concret) :
  - Données qui changent souvent | Réindexation rapide vs réentraînement coûteux | Notices produits mis à jour
  - Traçabilité requise | Le chunk source est retourné avec la réponse | Audit légal, conformité
  - Budget < $1 000 lancement | Pas de GPU, pas d'entraînement | Startup, POC
  - < 500 exemples disponibles | FT sur < 500 ex = overfitting quasi garanti | MVP en 1 semaine
  - Plusieurs domaines distincts | RAG peut indexer N corpus sans FT N fois | Multi-produits
- Stat : RAG atteint 89% d'accuracy sur QA ouvert — vs 60-70% sans retrieval

**Slide 4 — Quand choisir le Fine Tuning**
- POURQUOI : "Dans quels scénarios le Fine Tuning est-il irremplaçable ?"
- Contenu : Les 5 cas où le FT apporte une valeur unique
- Table (Scénario | Pourquoi FT gagne | Exemple concret) :
  - Ton / style de marque strict | Le contexte ne modifie pas le comportement général | Chatbot avec personnalité propriétaire
  - Latence < 500ms | Pas de retrieval, réponse directe | Interface temps réel
  - Confidentialité totale | Modèle local, aucune donnée sortante | Données patients, secrets industriels
  - Raisonnement métier très spécialisé | Logique métier non présente dans les données d'entraînement | Droit fiscal spécialisé
  - Format de sortie complexe strict | JSON structuré, code spécialisé | Générateur de contrats
- Stat : FT seul atteint 91% d'accuracy — légèrement supérieur à RAG sur raisonnement complexe

**Slide 5 — Architecture hybride : le meilleur des deux mondes**
- POURQUOI : "Pourquoi combiner RAG et Fine Tuning dans le même système ?"
- Contenu : Architecture hybride et cas d'usage
- Table (Couche | Rôle | Technologie HomeButler) :
  - Modèle de base fine-tuné | Ton, style, raisonnement spécialisé | LoRA sur 150 Q&A HomeButler
  - Retrieval (RAG) | Connaissance à jour, sources traçables | FAISS + ChromaDB
  - Prompt d'assemblage | Combine contexte récupéré + instruction | Template hwchase17/react
  - Observabilité | Tracer les deux couches | LangSmith ou Langfuse
- Résultat benchmark : hybride = 96% accuracy vs RAG 89% vs FT 91%
- Callout : > 💡 L'hybride est plus complexe à maintenir — il se justifie uniquement quand les deux couches apportent chacune une valeur irremplaçable

**Slide 6 — RAFT : Retrieval Augmented Fine Tuning (Zhang et al. 2024)**
- POURQUOI : "Pourquoi RAFT est-il une avancée par rapport au simple RAG ou au simple FT ?"
- Contenu : Le principe de RAFT
- Référence : Zhang et al., Mars 2024 — arxiv:2403.10131 (Gorilla project, Berkeley + Microsoft)
- Table (Aspect | RAG classique | Fine Tuning classique | RAFT) :
  - Contexte utilisé | Récupéré dynamiquement | Absent (mémoire paramétrique) | Entraîné sur oracle + distracteurs
  - Apprentissage du bruit | Non | Non | Oui (apprend à ignorer les distracteurs)
  - Généralisation hors domaine | Bonne | Limitée | Bonne (transfer learning)
  - Accuracy PubMed/HotpotQA | ~85% | ~82% | ~92%
- Intuition : Le modèle RAFT apprend à "extraire du contexte quand c'est utile, ignorer quand c'est du bruit"

**Slide 7 — Benchmarks comparatifs : les chiffres réels**
- POURQUOI : "Comment choisir objectivement entre les approches avec des données mesurées ?"
- Contenu : Benchmarks sur différents types de tâches
- Table (Type de tâche | RAG seul | FT seul | Hybride/RAFT) :
  - QA factuel ouvert | 89% | 79% | 94%
  - QA domaine spécialisé (médical) | 82% | 88% | 96%
  - Completion de code | 72% | 91% | 93%
  - QA multi-étapes (raisonnement) | 74% | 81% | 91%
  - Génération de style/ton | 65% | 94% | 95%
- ⚠️ **Piège** — Ces benchmarks mesurent des architectures optimisées : un RAG mal chunké ou un FT sur mauvaises données peut être bien en dessous de ces chiffres

**Slide 8 — Total Cost of Ownership sur 12 mois**
- POURQUOI : "Pourquoi le coût réel d'un système LLM s'évalue sur 12 mois, pas au lancement ?"
- Contenu : Décomposition des coûts récurrents et ponctuels
- Table (Poste de coût | RAG seul | Fine Tuning seul | Hybride) :
  - Setup initial | $500-1k (indexation) | $500-2k (entraînement) | $1.5k-3k |
  - Infra mensuelle | $50-200 (vectorstore + inférence) | $200-500 (GPU inférence) | $300-700 |
  - Mise à jour données | Réindexation (1-2h) | Réentraînement ($500-2k) | Réindexation + réentraînement trimestriel |
  - Total 12 mois estimé | $1k-3k | $3k-8k | $5k-12k |
- Callout : > 💡 Le RAG a le TCO le plus bas pour des données qui changent souvent. Le FT amortit son coût sur des données stables + fort volume de requêtes.

**Slide 9 — Arbre de décision : RAG, Fine Tuning ou Hybride ?**
- POURQUOI : "Comment décider en moins de 5 minutes dans un contexte projet réel ?"
- Contenu : Flux de décision structuré (format textuel car pas de code)
- Flux de décision :
  - Étape 1 — Vos données changent-elles plus d'une fois par mois ?
    - OUI → RAG (aller à l'étape 3)
    - NON → aller à l'étape 2
  - Étape 2 — Avez-vous plus de 500 exemples de qualité pour entraîner ?
    - NON → RAG
    - OUI → aller à l'étape 3
  - Étape 3 — Avez-vous un besoin fort de style/ton/raisonnement spécialisé ?
    - NON → RAG seul
    - OUI → aller à l'étape 4
  - Étape 4 — Avez-vous le budget GPU et le temps (> 2 semaines) pour le FT ?
    - NON → RAG + prompting avancé
    - OUI → Architecture hybride RAG + Fine Tuning
- ⚠️ **Piège** — Ne pas commencer par l'hybride : toujours valider RAG seul d'abord, puis mesurer le gap avant de fine-tuner

**Slide 10 — HomeButler Final : architecture hybride complète**
- POURQUOI : "Comment HomeButler AI combine RAG et Fine Tuning pour être une application de production ?"
- Contenu : Architecture finale des 3 jours
- Table (Couche | Composant | Rôle dans HomeButler) :
  - Embedding & RAG | FastEmbedEmbeddings + FAISS + ChromaDB + EnsembleRetriever | Répondre sur les notices, l'énergie, les producteurs |
  - Fine Tuning | LoRA sur 150 Q&A HomeButler (format Alpaca) | Adapter le ton conciergerie + format de réponse |
  - Orchestration | LangChain 0.3 + ReAct (hwchase17/react) | Décider quel outil appeler |
  - API | FastAPI + 4 routers + middleware sécurité | Exposer au monde |
  - UI | Streamlit 4 pages + Gradio prototype | Interface utilisateur |
  - Infra | Docker Compose + VPS Linux | Déploiement reproductible |
  - Observabilité | LangSmith (formation) / Langfuse (prod) | Tracer, débugger, optimiser |
- Callout : > 💡 En 3 jours, on a construit une application complète de 40 fichiers — chaque chapitre correspond à une couche de cette architecture

🎓 **Ce que vous devez retenir — Chapitre 6**
| Concept | Pourquoi c'est important |
|---|---|
| 8 critères de décision | RAG vs FT vs Hybride — tableau à garder sous la main |
| RAG = données volatiles + traçabilité | 89% accuracy, TCO $1k-3k/an |
| FT = style + raisonnement + latence | 91% accuracy, TCO $3k-8k/an |
| Hybride = meilleur des deux | 96% accuracy, TCO $5k-12k/an |
| RAFT (Zhang 2024) | Entraîner sur oracle + distracteurs = robustesse au bruit |
| TCO 12 mois | Coût réel = setup + infra mensuelle + mises à jour |
| Arbre de décision | 4 questions pour choisir en < 5 minutes |
| HomeButler = hybride | FastEmbed + FAISS (RAG) + LoRA (FT) + LangChain + FastAPI + Streamlit + Docker |
| Commencer par RAG | Valider d'abord, fine-tuner sur le gap mesuré |
| Pas d'hybride prématuré | Complexité × 3 — se justifie seulement sur valeur mesurée |

---

## Vérification post-exécution

1. Compter les sections `📝 Slide` dans le fichier → doit afficher **60**
2. Vérifier l'absence de backtick triple (` ``` `) dans le fichier → zéro tolérance
3. Vérifier la présence de 6 sections `🎓 Ce que vous devez retenir`
4. Vérifier les 6 sections `➡️ Prochain chapitre` (sauf le dernier chapitre)
5. Vérifier que chaque chapitre comporte exactement 10 slides numérotés 1-10
6. Coller le contenu du Chapitre 1 dans gamma.app → valider l'affichage
7. Vérifier que le projet HomeButler apparaît dans la slide 10 de chaque chapitre
8. Vérifier la cohérence des stats citées (mêmes chiffres dans les 6 chapitres si référencés plusieurs fois)
