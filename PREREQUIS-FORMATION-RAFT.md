# Prérequis — Formation RAG et Fine Tuning d'un LLM (RAFT)
**Référence PLB : RAFT — v2026-0512 — Durée : 3 jours**

---

## Table des matières

1. [Public cible et prérequis pédagogiques](#1-public-cible-et-prérequis-pédagogiques)
2. [Comptes et accès à créer AVANT la formation](#2-comptes-et-accès-à-créer-avant-la-formation)
3. [Installation — poste participant](#3-installation--poste-participant)
4. [Vérification de l'environnement](#4-vérification-de-lenvironnement)
5. [Fiche technique pour le service informatique — VM de backup](#5-fiche-technique-pour-le-service-informatique--vm-de-backup)

---

## 1. Public cible et prérequis pédagogiques

### Profil visé

Data scientists, ingénieurs ML/IA, développeurs Python, architectes logiciels, chefs de projet techniques travaillant sur des projets d'IA générative.

### Prérequis obligatoires

| Domaine | Niveau attendu |
|---|---|
| **Python** | Maîtrise solide — fonctions, classes, gestion d'environnements virtuels, pip |
| **Machine Learning** | Connaissance des concepts (entraînement, évaluation, métriques, overfitting) |
| **Bibliothèques Python** | Expérience pratique avec **Pandas** et idéalement **Transformers** ou **PyTorch** |
| **API REST** | Savoir consommer une API HTTP (requêtes GET/POST, JSON) |
| **Terminal / ligne de commande** | Aisance de base (navigation, exécution de scripts, activation de venv) |

### Prérequis appréciés (non bloquants)

- Notions de NLP (tokenisation, embeddings, attention)
- Utilisation de Jupyter Notebook
- Bases de Docker

---

## 2. Comptes et accès à créer AVANT la formation

Ces comptes sont **gratuits** à créer. Prévoir 20 à 30 minutes pour les créer et noter les clés API.

### 2.1 Anthropic (Claude API) — OBLIGATOIRE pour J1 et J2

> Utilisé pour le provider LLM principal du projet fil rouge HomeButler en développement local.

1. Créer un compte sur [console.anthropic.com](https://console.anthropic.com)
2. Générer une clé API : **Paramètres → Clés API → Créer une clé**
3. Créditer le compte (recommandé : 50 à 100 USD suffisent pour les 3 jours)
4. Noter la clé : `sk-ant-api03-...`

### 2.2 LangSmith — OBLIGATOIRE pour J2 et J3

> Plateforme d'observabilité LLM utilisée pour tracer les agents ReAct et analyser les traces.

1. Créer un compte sur [smith.langchain.com](https://smith.langchain.com)
2. Créer un projet `homebutler-raft`
3. Générer une clé API : **Paramètres → Clés API**
4. Noter la clé : `lsv2_pt_...`

### 2.3 Google Account (Colab) — OBLIGATOIRE pour J2 fine-tuning

> Les TP de fine-tuning LoRA/QLoRA se font sur Google Colab (GPU T4 gratuit) car un GPU local n'est pas requis.

- Un compte Google suffit : [colab.research.google.com](https://colab.research.google.com)
- Vérifier l'accès à un runtime **GPU T4** (gratuit, en-tête → Runtime → Changer le type → T4 GPU)

### 2.4 HuggingFace (optionnel mais recommandé)

> Accès aux modèles open-source (Mistral-7B-Instruct) pour les TP de fine-tuning.

1. Créer un compte sur [huggingface.co](https://huggingface.co)
2. Accepter les conditions d'utilisation de `mistralai/Mistral-7B-Instruct-v0.2`
3. Générer un token lecture : **Paramètres → Access Tokens**

---

## 3. Installation — poste participant

### 3.1 Configuration matérielle minimale

| Composant | Minimum | Recommandé |
|---|---|---|
| RAM | 8 Go | 16 Go |
| Stockage libre | 10 Go | 15 Go |
| CPU | 4 cœurs | 6+ cœurs |
| GPU | Non requis | Non requis (fine-tuning sur Colab) |
| Connexion Internet | Oui | Haut débit (téléchargement modèles ~100 Mo) |

> **Important** : aucun GPU local n'est nécessaire. Tous les TP de fine-tuning LoRA/QLoRA utilisent Google Colab avec un GPU T4 cloud gratuit.

### 3.2 Systèmes d'exploitation supportés

| OS | Architecture | Python cible | Notes |
|---|---|---|---|
| **macOS** | Intel (x86_64) | **3.13.x UNIQUEMENT** | Python 3.14 est incompatible (onnxruntime 1.23.2 requis, non disponible pour Mac Intel > 1.23) |
| **macOS** | ARM (M1/M2/M3/M4) | 3.13.x ou 3.14.x | Les deux fonctionnent |
| **Windows 10/11** | x86_64 | 3.13.x | WSL2 fortement recommandé |
| **Linux** | x86_64 | 3.13.x ou 3.14.x | Environnement optimal |

### 3.3 Version Python — installation

#### macOS (Homebrew)

```bash
brew install python@3.13
python3.13 --version   # doit afficher Python 3.13.x
```

#### macOS (pyenv — recommandé pour gérer plusieurs versions)

```bash
brew install pyenv
pyenv install 3.13.5
pyenv global 3.13.5
python --version
```

#### Linux (Ubuntu 22.04+)

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update && sudo apt install python3.13 python3.13-venv python3.13-dev
python3.13 --version
```

#### Windows (WSL2 recommandé)

1. Installer WSL2 avec Ubuntu 22.04 : `wsl --install`
2. Puis suivre les instructions Linux ci-dessus

> **Conda n'est pas utilisé dans cette formation.** Le projet utilise exclusivement `venv` standard Python.

### 3.4 Outils système à installer

| Outil | Commande de vérification | Installation |
|---|---|---|
| **Git** | `git --version` | [git-scm.com](https://git-scm.com) |
| **Docker** + Docker Compose | `docker --version && docker compose version` | [docker.com/get-docker](https://www.docker.com/get-docker) |
| **Ollama** | `ollama --version` | [ollama.com](https://ollama.com) |
| **curl** | `curl --version` | Préinstallé sur macOS/Linux |

#### Télécharger le modèle Ollama

Après installation d'Ollama, télécharger le modèle de base (environ 4 Go) :

```bash
ollama pull mistral:7b-instruct
```

> Ce téléchargement peut être long selon la connexion. À faire impérativement **avant** la formation.

### 3.5 Cloner le projet et installer les dépendances

```bash
# 1. Cloner le dépôt
git clone https://github.com/YoLoADR/pre-training-rag.git
cd pre-training-rag

# 2. Créer l'environnement virtuel avec Python 3.13
python3.13 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

# 3. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 4. Installer le package homebutler en mode éditable (obligatoire)
pip install -e .

# 5. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et renseigner :
#   ANTHROPIC_API_KEY=sk-ant-api03-...
#   LANGCHAIN_API_KEY=lsv2_pt_...
#   LANGCHAIN_TRACING_V2=true
```

### 3.6 Dépendances Python clés (extrait de `requirements.txt`)

> Le fichier `requirements.txt` complet est dans le dépôt. Voici les bibliothèques principales pour information.

| Bibliothèque | Version | Rôle |
|---|---|---|
| `langchain` | 0.3.14 | Framework agents et pipelines LLM |
| `langchain-anthropic` | 0.3.0 | Connecteur Claude API |
| `langchain-community` | 0.3.14 | Intégrations tierces (FAISS, ChromaDB…) |
| `anthropic` | 0.40.0 | SDK Anthropic (Claude) |
| `fastapi` | 0.115.6 | API REST du projet fil rouge |
| `uvicorn[standard]` | 0.32.1 | Serveur ASGI |
| `streamlit` | 1.41.1 | Interface web multipage |
| `gradio` | 5.9.1 | Interface prototype |
| `faiss-cpu` | 1.13.2 | Base vectorielle en mémoire (FAISS) |
| `chromadb` | 0.5.23 | Base vectorielle persistante |
| `fastembed` | ≥ 0.8.0 | Embeddings ONNX (sans PyTorch) |
| `onnxruntime` | **1.23.2** | Runtime ONNX — **version fixe obligatoire sur Mac Intel** |
| `pymupdf` | 1.25.1 | Extraction PDF (s'importe `import fitz`) |
| `pydantic` | ≥ 2.7.4 | Validation de données |
| `langsmith` | 0.2.3 | Observabilité LangChain |
| `jupyter` | 1.1.1 | Notebooks pédagogiques |
| `plotly` | 5.24.1 | Visualisation (énergie, marketplace) |
| `slowapi` | dernière | Rate limiting API |

> **Note fastembed / PyTorch** : ce projet utilise `fastembed` (basé sur ONNX Runtime) à la place de `sentence-transformers` pour éviter la dépendance à PyTorch. Aucune installation PyTorch locale n'est nécessaire — PyTorch est uniquement utilisé sur Google Colab pour le fine-tuning.

---

## 4. Vérification de l'environnement

Lancer ce script de vérification **avant la formation** pour s'assurer que tout fonctionne :

```bash
cd pre-training-rag
source .venv/bin/activate

# Vérification Python
python --version                    # Python 3.13.x

# Vérification imports critiques
python -c "
import langchain; print('LangChain:', langchain.__version__)
import chromadb; print('ChromaDB:', chromadb.__version__)
import fastembed; print('FastEmbed OK')
import fitz; print('PyMuPDF (fitz) OK')
import fastapi; print('FastAPI:', fastapi.__version__)
import streamlit; print('Streamlit:', streamlit.__version__)
print('Tous les imports OK')
"

# Vérification Ollama
ollama list                         # doit afficher mistral:7b-instruct

# Vérification Docker
docker compose version
```

Sortie attendue (sans erreur) :

```
LangChain: 0.3.14
ChromaDB: 0.5.23
FastEmbed OK
PyMuPDF (fitz) OK
FastAPI: 0.115.6
Streamlit: 1.41.1
Tous les imports OK
```

---

## 5. Fiche technique pour le service informatique — VM de backup

> Cette section est destinée au service technique du centre de formation pour la création de VMs de secours en cas de problème sur le poste d'un participant.

### 5.1 Spécifications VM recommandées

| Paramètre | Valeur recommandée |
|---|---|
| **OS** | Ubuntu 22.04 LTS (x86_64) |
| **vCPU** | 4 cores minimum, 6 recommandés |
| **RAM** | 8 Go minimum, **16 Go recommandés** |
| **Stockage** | **20 Go SSD minimum** (OS + Python env + modèles + données) |
| **GPU** | Non requis |
| **Accès réseau** | Internet requis (appels API Anthropic, téléchargement modèles) |
| **Ports à ouvrir** | 8000 (FastAPI), 8501 (Streamlit), 7860 (Gradio), 11434 (Ollama), 8888 (Jupyter) |

### 5.2 Stack logicielle à préinstaller

#### Système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
    git curl wget build-essential \
    python3.13 python3.13-venv python3.13-dev \
    docker.io docker-compose-plugin \
    libssl-dev libffi-dev
```

#### Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral:7b-instruct     # ~4 Go — à faire lors du provisioning
```

#### Projet et dépendances Python

```bash
git clone https://github.com/YoLoADR/pre-training-rag.git /home/stagiaire/formation
cd /home/stagiaire/formation

python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

#### Pré-chargement du modèle d'embeddings

```bash
source .venv/bin/activate
python scripts/preload_models.py    # télécharge ~100 Mo dans ~/.cache/fastembed/
```

#### Génération des données fictives du projet fil rouge

```bash
source .venv/bin/activate
python scripts/generate_documents.py    # 6 PDFs notices logement
python scripts/generate_energy_data.py  # CSV 365 jours consommation
python scripts/generate_producers.py   # 30 producteurs locaux JSON
python scripts/generate_qa_dataset.py  # 150 paires Q/A JSONL
```

#### Indexation RAG (FAISS + ChromaDB)

```bash
source .venv/bin/activate
python -c "
from homebutler.rag.ingestion import ingest_all_documents
from homebutler.rag.vectorstore import build_faiss_index, build_chroma_db
docs = ingest_all_documents()
print(f'{len(docs)} chunks indexés')
build_faiss_index(docs, force_rebuild=True)
build_chroma_db(docs, force_rebuild=True)
print('Index FAISS et ChromaDB créés')
"
```

### 5.3 Variables d'environnement à préparer

Créer le fichier `.env` à la racine du projet. Les clés Anthropic et LangSmith seront fournies par le formateur le jour J ou distribuées aux participants :

```env
# Fichier /home/stagiaire/formation/.env

LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=CLEF_A_RENSEIGNER
ANTHROPIC_MODEL=claude-sonnet-4-6

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=mistral:7b-instruct

LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=CLEF_A_RENSEIGNER

CHROMA_PATH=./data/chroma_db
FAISS_PATH=./data/faiss_index
OPEN_METEO_CACHE_TTL=3600
```

### 5.4 Commandes de démarrage des services

Les participants lanceront ces commandes dans 3 terminaux séparés :

```bash
# Terminal 1 — API FastAPI
source .venv/bin/activate && uvicorn api.main:app --reload --port 8000

# Terminal 2 — Interface Streamlit
source .venv/bin/activate && streamlit run ui/app.py --server.port 8501

# Terminal 3 — Prototype Gradio
source .venv/bin/activate && python ui/gradio_prototype.py
```

URLs d'accès :
- FastAPI docs : `http://localhost:8000/docs`
- Streamlit UI : `http://localhost:8501`
- Gradio : `http://localhost:7860`
- Jupyter : `http://localhost:8888` (lancer avec `jupyter notebook`)

### 5.5 Points d'attention critiques

| Point | Détail |
|---|---|
| **Python 3.14 interdit sur Linux Intel** | Utiliser Python 3.13 par défaut. `onnxruntime==1.23.2` est pinnée dans `requirements.txt` pour compatibilité x86_64 |
| **`pip install -e .`** | Étape obligatoire après `pip install -r requirements.txt`. Sans cette étape, Streamlit ne trouve pas le package `homebutler` |
| **`pymupdf` s'importe `fitz`** | Installé via `pip install pymupdf`, mais dans le code `import fitz`. Comportement normal, à signaler si un participant est surpris |
| **FAISS `allow_dangerous_deserialization`** | Hardcodé dans `homebutler/rag/vectorstore.py`. Comportement attendu par LangChain 0.3.x |
| **Modèle embeddings ~100 Mo** | Le premier lancement de `preload_models.py` télécharge le modèle ONNX dans `~/.cache/fastembed/`. À faire lors du provisioning VM, pas le jour J |
| **Modèle Ollama ~4 Go** | `mistral:7b-instruct` via `ollama pull`. À télécharger lors du provisioning VM |
| **GPU Colab** | Pour les TP de fine-tuning (J2), les participants utilisent Google Colab avec GPU T4 cloud. Aucun GPU VM requis |
| **Ports réseau** | S'assurer que les ports 8000, 8501, 7860, 11434, 8888 sont accessibles depuis les postes participants si la VM est distante |

### 5.6 Estimation de l'espace disque

| Composant | Taille approximative |
|---|---|
| Ubuntu 22.04 base | ~3 Go |
| Python 3.13 + pip packages | ~3 Go |
| Modèle fastembed (ONNX) | ~100 Mo |
| Modèle Ollama mistral:7b-instruct | ~4 Go |
| Données projet (PDFs, CSV, JSON, index FAISS/ChromaDB) | ~200 Mo |
| **Total** | **~10-11 Go** |

Prévoir **20 Go** pour laisser de la marge (logs, notebooks, exports).

---

*Document produit pour la formation RAFT — PLB ref. RAFT v2026-0512*
*Formateur : Yohann Ravino — Mise à jour : mai 2026*
