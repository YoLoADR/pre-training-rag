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

## 6. Guide de débogage — VM Windows (Guacamole)

> Section formateur. Historique des problèmes rencontrés lors du setup de la VM Guacamole (Windows 10, HyperV, mai 2026) et leurs solutions validées.

### 6.1 Contexte de la VM Windows Guacamole

| Paramètre | Valeur |
|---|---|
| OS | Windows 10 (10.0.26200.8246) |
| Type VM | HyperV (virtualisation imbriquée non activée) |
| Accès | Apache Guacamole (navigateur → RDP) |
| User | PLB (FORMATEUR) |
| Python installé | 3.13.13 (natif Windows, pas WSL2) |
| Chemin projet | `C:\Formation_RAFT\pre-training-rag` |
| Script d'install | `Install-FormationRAFT.ps1` (bureau Windows) |

### 6.2 Problèmes rencontrés et solutions

#### P1 — `git clone` non exécuté malgré le script d'installation

**Symptôme** : `C:\Formation_RAFT` existe mais `pre-training-rag` est absent.

**Cause** : Le script `Install-FormationRAFT.ps1` installe Git via winget puis clone immédiatement. La fonction `Refresh-Path` du script ne met pas toujours à jour le PATH dans la session PowerShell courante — `git.exe` est introuvable au moment du clone.

**Solution** : Ouvrir un **nouveau** terminal PowerShell (git dans le PATH) et cloner manuellement :
```powershell
git clone https://github.com/YoLoADR/pre-training-rag.git C:\Formation_RAFT\pre-training-rag
```

**Fix script** : Ajouter après l'install de Git un redémarrage du shell ou un `$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine')` explicite.

---

#### P2 — `slowapi>=0.5.7` introuvable lors du `pip install -r requirements.txt`

**Symptôme** :
```
ERROR: Could not find a version that satisfies the requirement slowapi>=0.5.7
(from versions: 0.1.0, 0.1.1, ..., 0.1.9)
```

**Cause** : Erreur de version dans `requirements.txt` — la version max de slowapi est `0.1.9`, pas `0.5.7`.

**Solution** : Déjà corrigé dans le repo (`slowapi>=0.1.0`). Si un élève a une ancienne copie :
```powershell
git pull  # récupère le fix
pip install -r requirements.txt
```

---

#### P3 — `chroma-hnswlib` ne compile pas (Visual C++ manquant)

**Symptôme** :
```
error: Microsoft Visual C++ 14.0 or greater is required.
Failed building wheel for chroma-hnswlib
```

**Cause** : `chromadb==0.5.23` dépend de `chroma-hnswlib`, une extension C++. Il n'existe pas de wheel pré-compilé pour Python 3.13 Windows (max supporté = Python 3.12). Upgrade vers chromadb 1.x impossible car incompatible avec `langchain-community==0.3.14`.

**Solution retenue (Python 3.13, pas de downgrade)** : installer Visual C++ Build Tools (une seule fois par machine) :
```powershell
# Dans PowerShell admin — durée ~20-40 min (téléchargement ~4 Go)
winget install Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
# Redémarrer la VM, puis relancer pip install -r requirements.txt
```

**Fix script** : Ajouter cette commande dans `Install-FormationRAFT.ps1` avant la section `pip install`.

**Solution alternative (si connexion lente)** : utiliser Python 3.12 (`py -3.12 -m venv .venv`) — `chroma-hnswlib` a un wheel cp312 pré-compilé, zéro compilation nécessaire.

---

#### P4 — Commandes Python multilignes dans PowerShell via Guacamole

**Symptôme** :
```
IndentationError: unexpected indent
```

**Cause** : Guacamole coupe les longues lignes. PowerShell interprète la suite comme une deuxième ligne Python indentée.

**Solution** : Écrire le script dans un fichier `.py` via `Set-Content` + `Add-Content` (une commande courte par ligne) :
```powershell
Set-Content script.py "ligne 1"
Add-Content script.py "ligne 2"
Add-Content script.py "ligne 3"
python script.py
```

---

#### P5 — Modèle Ollama `homebutler` introuvable (404)

**Symptôme** :
```json
{"detail": "Erreur agent : Ollama call failed with status code 404. Maybe your model is not found and you should pull the model with `ollama pull homebutler`."}
```

**Cause** : `OLLAMA_MODEL=homebutler` dans `.env` référence un modèle custom Ollama qui n'est pas encore créé sur la machine. Ce modèle est défini par le `Modelfile` du projet (ajouté en mai 2026).

**Solution** :
```powershell
cd C:\Formation_RAFT\pre-training-rag
git pull  # récupère le Modelfile
ollama create homebutler -f Modelfile  # quelques secondes, pas de re-téléchargement
```

**Fix script** : Ajouter `ollama create homebutler -f Modelfile` dans `Install-FormationRAFT.ps1` après le `git clone`.

---

#### P6 — Avertissements non-bloquants à connaître

Ces messages apparaissent systématiquement — ils sont **inoffensifs** et peuvent être ignorés :

| Message | Source | Impact |
|---|---|---|
| `UserWarning: The model ... now uses mean pooling instead of CLS` | fastembed | Aucun — changement interne fastembed |
| `UserWarning: huggingface_hub cache-system uses symlinks... machine does not support them` | HuggingFace | Aucun — cache fonctionne sans symlinks, occupe plus de disque |
| `Failed to send telemetry event ClientStartEvent: capture() takes 1 positional argument` | chromadb | Aucun — bug telemetry chromadb, pas d'impact fonctionnel |
| `LangChainDeprecationWarning: Please see the migration guide` | LangChain | Aucun — API dépréciée mais fonctionnelle en 0.3.x |
| `LangSmithMissingAPIKeyWarning` | LangSmith | Aucun — normal si `LANGCHAIN_TRACING_V2=false` |
| `UserWarning: The 'tuples' format for chatbot messages is deprecated` | Gradio | Aucun — dépreciation Gradio, à corriger en v6 |

---

### 6.3 Ordre de démarrage des services (Windows natif)

```powershell
# Chaque service dans un onglet PowerShell séparé (bouton + dans Windows Terminal)

# Onglet 1 — FastAPI
cd C:\Formation_RAFT\pre-training-rag
.\.venv\Scripts\Activate.ps1
uvicorn api.main:app --reload --port 8000

# Onglet 2 — Streamlit
cd C:\Formation_RAFT\pre-training-rag
.\.venv\Scripts\Activate.ps1
streamlit run ui/app.py

# Onglet 3 — Gradio
cd C:\Formation_RAFT\pre-training-rag
.\.venv\Scripts\Activate.ps1
python ui/gradio_prototype.py

# Onglet 4 — Jupyter (notebooks)
cd C:\Formation_RAFT\pre-training-rag
.\.venv\Scripts\Activate.ps1
jupyter notebook --port=8888
```

URLs d'accès (Windows natif — pas WSL2) :

| Service | URL |
|---|---|
| FastAPI Swagger | `http://localhost:8000/docs` |
| Streamlit UI | `http://localhost:8501` |
| Gradio | `http://localhost:7860` |
| Jupyter | `http://localhost:8888` |

---

### 6.4 Comparaison Anthropic vs Ollama (observée en conditions réelles)

| Critère | Anthropic (claude-sonnet-4-6) | Ollama homebutler (mistral:7b-instruct CPU) |
|---|---|---|
| Latence (VM sans GPU) | ~2 secondes | ~2-5 minutes |
| Qualité RAG | Excellente — retrouve les bons documents, répond précisément | Dégradée — peut confondre les outils (ex: météo au lieu de RAG) |
| Suivi format ReAct | Très fiable | Fragile sur petits modèles |
| Usage recommandé | J1, J2 (exercices) | J3 (démonstration impact modèle) |

> **Message pédagogique J3** : cette différence de qualité illustre directement l'intérêt du fine-tuning RAFT — adapter un modèle local à un domaine précis pour réduire l'écart avec les modèles cloud.

---

### 6.5 Améliorations à apporter au script `Install-FormationRAFT.ps1`

À intégrer lors de la prochaine révision du script (sur le partage `\\192.168.10.251\Install\COURS\RAFT\RAVINO`) :

```powershell
# 1. Avant la section pip install — ajouter les VS Build Tools
winget install Microsoft.VisualStudio.2022.BuildTools --silent `
  --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"

# 2. Après git clone — créer le modèle Ollama homebutler
Push-Location $ProjectPath
& ollama create homebutler -f Modelfile
Pop-Location

# 3. Forcer le rafraîchissement du PATH après winget Git
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
            [System.Environment]::GetEnvironmentVariable('Path','User')
```

---

*Section ajoutée : mai 2026 — Session de validation VM Guacamole Windows*
*Document produit pour la formation RAFT — PLB ref. RAFT v2026-0512*
*Formateur : Yohann Ravino — Mise à jour : mai 2026*
