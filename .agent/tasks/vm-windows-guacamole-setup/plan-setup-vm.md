# Plan — Setup VM Windows (Guacamole) pour la formation RAFT

## Contexte

VM Windows 10 (10.0.26200.8246), user `PLB` (compte FORMATEUR), accessible via Apache Guacamole.
Ni Claude Code CLI, ni le projet `pre-training-rag` ne sont installés.
Objectif : setup complet + test GPU + validation de toutes les features LLM (Anthropic, Ollama, HuggingFace/Colab).

**Verdict GPU anticipé** : aucun GPU local n'est requis pour la formation.
- Anthropic → cloud API, zéro GPU
- HuggingFace fine-tuning → Google Colab GPU T4 (cloud gratuit)
- Ollama → CPU-only acceptable (~5-8 tok/s sur 7B), GPU accélérerait les démos live

---

## Étape 0 — Vérifier le script "Install-Formati..." sur le bureau

Sur le bureau Windows : double-cliquer sur `Install-Formati...`.
Si le script installe Python/Git automatiquement → vérifier ce qui est fait (`python --version`, `git --version` en CMD).
Si ça ne fait rien d'utile → continuer avec les étapes ci-dessous.

---

## Étape 1 — Ouvrir PowerShell en administrateur

Barre des tâches → clic droit sur l'icône **Terminal** (ou chercher "PowerShell" → clic droit → "Exécuter en tant qu'administrateur").

```powershell
# Vérifier la génération de la VM HyperV (Gen 1 ou Gen 2)
# Important pour savoir si WSL2 fonctionne
systeminfo | findstr /i "BIOS"
# Si "BIOS Mode: UEFI" → Gen 2 → WSL2 possible
# Si "BIOS Mode: Legacy" → Gen 1 → fallback Git Bash (voir Étape 2b)
```

---

## Étape 2a — Installer WSL2 + Ubuntu 22.04 (si VM Gen 2 / UEFI)

> **Important** : cette VM tourne sur HyperV. WSL2 nécessite la virtualisation imbriquée (nested virtualization).
> L'admin qui gère HyperV doit avoir activé `Set-VMProcessor -VMName <PLB-VM> -ExposeVirtualizationExtensions $true`.
> Si ce n'est pas fait → demander à l'admin ou utiliser le fallback Étape 2b.

```powershell
# Dans PowerShell admin — installe WSL2 + Ubuntu 22.04
wsl --install

# REDÉMARRER la VM après l'installation (obligatoire)
```

Après redémarrage, Ubuntu s'ouvre automatiquement → créer un user Unix :
- **Username** : `formateur`
- **Password** : au choix (simple, ex: `raft2026`)

```bash
# Dans Ubuntu WSL2 — mettre à jour et installer les outils
sudo apt update && sudo apt upgrade -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y git curl wget python3.13 python3.13-venv python3.13-dev build-essential
python3.13 --version   # attendu : Python 3.13.x
git --version
```

**Note réseau importante** : avec WSL2, les services (Streamlit, FastAPI…) ne sont PAS accessibles via `localhost` depuis Firefox Windows. Utiliser l'IP WSL2 :
```bash
hostname -I   # affiche ex : 172.31.234.45
# → accéder aux services via http://172.31.234.45:8501 depuis Firefox
```

---

## Étape 2b — Fallback : Python natif Windows + Git Bash (si WSL2 échoue)

```powershell
# Installer Git for Windows (inclut Git Bash)
winget install Git.Git

# Installer Python 3.13 (mode "current user", pas besoin d'admin)
# Télécharger depuis https://www.python.org/downloads/windows/
# → Cocher "Add Python to PATH" pendant l'install

# Vérification
python --version    # Python 3.13.x
git --version

# Toutes les commandes suivantes s'exécutent dans Git Bash
# Remplacer "source .venv/bin/activate" par ".venv/Scripts/activate"
```

---

## Étape 3 — Cloner le projet

```bash
# Dans Ubuntu WSL2 (ou Git Bash si fallback)
cd ~
git clone https://github.com/YoLoADR/pre-training-rag.git formation
cd formation
```

---

## Étape 4 — Créer le venv et installer les dépendances

```bash
python3.13 -m venv .venv
source .venv/bin/activate          # WSL2/Linux
# .venv/Scripts/activate           # Git Bash Windows

pip install --upgrade pip
pip install -r requirements.txt
pip install -e .    # OBLIGATOIRE : installe le package homebutler (sinon Streamlit plante)

# Vérification rapide des imports critiques
python -c "
import langchain; print('LangChain:', langchain.__version__)
import chromadb; print('ChromaDB:', chromadb.__version__)
import fastembed; print('FastEmbed OK')
import fitz; print('PyMuPDF OK')
import fastapi; print('FastAPI:', fastapi.__version__)
import streamlit; print('Streamlit:', streamlit.__version__)
print('=== Tous les imports OK ===')
"
```

---

## Étape 5 — Configurer le fichier .env

```bash
cp .env.example .env
nano .env   # ou "notepad .env" dans Git Bash
```

### Variables OBLIGATOIRES (sans elles, l'app ne démarre pas) :

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...          # ← OBLIGATOIRE : clé du formateur
ANTHROPIC_MODEL=claude-sonnet-4-6
```

### Variables OPTIONNELLES (valeurs par défaut suffisent pour démarrer) :

```env
# Ollama (si LLM_PROVIDER=ollama)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b-instruct      # modèle recommandé 2025 (voir Étape 6)

# Observabilité — désactivé par défaut, activer sur J2/J3
TRACING_PROVIDER=langfuse
LANGCHAIN_TRACING_V2=false
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=pk-lf-...         # clés Langfuse du formateur
LANGFUSE_SECRET_KEY=sk-lf-...

# Chemins (auto-créés par les scripts)
CHROMA_PATH=./data/chroma_db
FAISS_PATH=./data/faiss_index
API_KEY=homebutler-dev-key
API_URL=http://localhost:8000
```

---

## Étape 6 — Installer Ollama (natif Windows) et télécharger les modèles

> Installer **côté Windows natif** (pas WSL2) pour la détection GPU.
> Télécharger l'installeur depuis : https://ollama.com/download/windows → lancer l'installation.
> Ollama tourne en tâche de fond sur le port 11434.

```powershell
# Dans PowerShell Windows (pas WSL2)
ollama --version   # attendu : 0.x.x

# Modèle principal recommandé 2025 (meilleur français + ratio perf/qualité)
ollama pull qwen2.5:7b-instruct     # ~4.7 Go

# Modèle backup léger pour démo rapide (3.8B, ~1.5x plus rapide)
ollama pull phi4-mini               # ~2.8 Go

# Modèle du projet pour compatibilité exercices (garder pour les TPs)
ollama pull mistral:7b-instruct     # ~4.1 Go

# Total : ~11 Go — prévoir 20 Go libres sur le disque
```

### Test de performance et détection GPU :

```powershell
# Test démo live (mesure la vitesse)
ollama run qwen2.5:7b-instruct "Explique le RAG en 3 phrases simples en français"

# Vérifier si GPU ou CPU est utilisé
ollama ps
# Résultat attendu :
# NAME                        ID      SIZE  PROCESSOR  UNTIL
# qwen2.5:7b-instruct:latest  ...     4.7GB 100% CPU   ...
# → Si "100% CPU" : CPU only (~5-8 tok/s) — suffisant pour la formation
# → Si "100% GPU" : GPU disponible (~30-50 tok/s)

# Vérification visuelle GPU : Task Manager → onglet "GPU" → moteur "Compute"
```

### Tableau comparatif des modèles Ollama pour cette VM :

| Modèle | Taille | Vitesse CPU | Français | Usage recommandé |
|---|---|---|---|---|
| `qwen2.5:7b-instruct` | 4.7 Go | ~6-9 tok/s | Excellent | **Principal — J1, J2, J3** |
| `phi4-mini` | 2.8 Go | ~12-18 tok/s | Bon | **Backup — démo rapide** |
| `mistral:7b-instruct` | 4.1 Go | ~5-8 tok/s | Bon | Exercices TPs (projet utilise ce nom) |

> **Note GPU** : Cette VM HyperV n'a probablement pas de GPU passthrough.
> Ollama en CPU-only est **suffisant** — Anthropic API est le provider principal en formation.
> Fine-tuning HuggingFace → toujours sur Google Colab (GPU T4 cloud gratuit).

---

## Étape 7 — Valider la clé Anthropic AVANT d'indexer

> Ne pas sauter cette étape — évite de découvrir une clé invalide après 30 min d'indexation.

```bash
# Dans WSL2 (ou Git Bash), venv activé
python -c "
from homebutler.llm.provider import get_llm
llm = get_llm(temperature=0.1, max_tokens=50)
resp = llm.invoke('Réponds juste: OK')
print(f'✓ Anthropic API OK — réponse : {resp.content[:80]}')
" || echo "✗ Erreur API — vérifier ANTHROPIC_API_KEY dans .env"
```

---

## Étape 8 — Pré-charger le modèle d'embeddings et générer les données

```bash
# Modèle d'embeddings ONNX (~100 Mo) — pour la vectorisation RAG (≠ LLM Ollama)
# Télécharge "paraphrase-multilingual-MiniLM-L12-v2" dans ~/.cache/fastembed/
python scripts/preload_models.py

# Générer les données fictives du projet fil rouge HomeButler
python scripts/generate_documents.py    # 6 PDFs notices logement
python scripts/generate_energy_data.py  # CSV 365 jours consommation
python scripts/generate_producers.py    # 30 producteurs locaux JSON
python scripts/generate_qa_dataset.py   # 150 paires Q/A JSONL

# Vérification
ls data/documents/    # doit afficher les PDFs
ls data/             # doit afficher energy_data.csv, producers.json, qa_dataset.jsonl
```

---

## Étape 9 — Indexer les documents RAG (FAISS + ChromaDB)

```bash
# Durée estimée : 3-5 min selon la machine
python -c "
from homebutler.rag.ingestion import ingest_all_documents
from homebutler.rag.vectorstore import build_faiss_index, build_chroma_db

docs = ingest_all_documents()
if not docs:
    raise ValueError('Aucun document trouvé — relancer les scripts generate_*.py')
print(f'✓ {len(docs)} chunks chargés depuis les PDFs')

faiss_store = build_faiss_index(docs, force_rebuild=True)
print('✓ Index FAISS créé (data/faiss_index/)')

chroma_store = build_chroma_db(docs, force_rebuild=True)
print('✓ Index ChromaDB créé (data/chroma_db/)')

# Test retrieval rapide
results = faiss_store.similarity_search('température chaudière nuit', k=2)
if results:
    print(f'✓ Test retrieval OK : {results[0].metadata.get(\"source\", \"?\")} trouvé')
print('=== Indexation terminée ===')
"
```

---

## Étape 10 — Lancer les 3 services

Ouvrir **3 onglets distincts** dans le terminal (bouton `+` dans Windows Terminal) :

```bash
# Terminal 1 — API FastAPI
source ~/formation/.venv/bin/activate && cd ~/formation
uvicorn api.main:app --reload --port 8000 --host 0.0.0.0

# Terminal 2 — UI Streamlit
source ~/formation/.venv/bin/activate && cd ~/formation
streamlit run ui/app.py --server.port 8501 --server.address 0.0.0.0

# Terminal 3 — Prototype Gradio
source ~/formation/.venv/bin/activate && cd ~/formation
python ui/gradio_prototype.py
```

### Accès depuis Firefox dans Guacamole :

> **Important WSL2** : utiliser l'IP WSL2 (pas `localhost`) depuis Firefox Windows.
> Récupérer l'IP : `hostname -I` dans WSL2 → ex : `172.31.234.45`

| Service | URL d'accès | Description |
|---|---|---|
| FastAPI docs | `http://172.31.234.45:8000/docs` | Interface Swagger — tester les endpoints |
| Streamlit UI | `http://172.31.234.45:8501` | App HomeButler complète |
| Gradio | `http://172.31.234.45:7860` | Prototype démo rapide |
| Jupyter | `http://172.31.234.45:8888` | Notebooks pédagogiques |

> Si Python natif Windows (fallback) : remplacer par `http://localhost:PORT`

---

## Étape 11 — Lancer Jupyter pour les notebooks

```bash
# Terminal 4 — Jupyter
source ~/formation/.venv/bin/activate && cd ~/formation
jupyter notebook --no-browser --port=8888 --ip=0.0.0.0 2>&1 | tee jupyter.log

# Copier le token depuis les logs (ex: ?token=abc123...)
# → Accéder à http://172.31.234.45:8888/?token=abc123...
```

### Notebooks disponibles :

| Notebook | Environnement | GPU | Description |
|---|---|---|---|
| `01_llm_baseline.ipynb` | Local (WSL2) | ✗ | Tester Anthropic + Ollama sans RAG |
| `02_ingestion_vectorisation.ipynb` | Local (WSL2) | ✗ | Pipeline RAG complet, FAISS vs ChromaDB |
| `03_finetuning_lora.ipynb` | **Colab OBLIGATOIRE** | ✓ T4 | Fine-tuning QLoRA — ne pas exécuter localement |

> **Notebook 03** : ouvrir sur https://colab.research.google.com — GPU T4 requis.
> Modèles HuggingFace compatibles pour ce TP (sur Colab) :
> - `Qwen/Qwen2.5-7B-Instruct` — recommandé 2025 (meilleur français)
> - `mistralai/Mistral-7B-Instruct-v0.3` — modèle historique du projet

---

## Étape 12 — Tests end-to-end

```bash
# Test complet de l'agent (API doit être lancée — Étape 10 Terminal 1)

# Test 1 : RAG retrieval
curl -X POST http://localhost:8000/rag/retrieve \
  -H "Content-Type: application/json" \
  -H "X-API-Key: homebutler-dev-key" \
  -d '{"query": "température chaudière nuit", "k": 3}' | python3 -m json.tool

# Test 2 : Chat avec agent ReAct
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: homebutler-dev-key" \
  -d '{"message": "Quelle est la température recommandée pour la chaudière la nuit ?"}' \
  | python3 -m json.tool

# Test 3 : Consommation énergie
curl -X GET http://localhost:8000/consumption \
  -H "X-API-Key: homebutler-dev-key" | python3 -m json.tool

# Test 4 : Switcher sur Ollama (remplacer dans .env : LLM_PROVIDER=ollama + restart API)
# Permet de valider que Ollama répond correctement
```

---

## Étape 13 — Installer Claude Code CLI

```powershell
# Dans PowerShell Windows (Git doit être installé — Étape 2b ou via winget)
irm https://claude.ai/install.ps1 | iex

# Relancer le terminal, puis :
claude --version

# Lancer Claude Code dans le dossier du projet (dans Git Bash ou WSL2)
cd ~/formation
claude
```

---

## Étape 14 — Script de vérification globale

```bash
source ~/formation/.venv/bin/activate && cd ~/formation

echo "=== Vérification Python ==="
python --version

echo "=== Vérification imports ==="
python -c "
import langchain; print('LangChain:', langchain.__version__)
import chromadb; print('ChromaDB:', chromadb.__version__)
import fastembed; print('FastEmbed OK')
import fitz; print('PyMuPDF OK')
import fastapi; print('FastAPI:', fastapi.__version__)
import streamlit; print('Streamlit:', streamlit.__version__)
print('Tous les imports OK')
"

echo "=== Vérification Ollama ==="
ollama list   # doit afficher les 3 modèles

echo "=== Vérification données ==="
ls data/documents/ | wc -l   # doit afficher 6
ls data/faiss_index/ && echo "FAISS OK"
ls data/chroma_db/ && echo "ChromaDB OK"
```

---

## Résumé verdict GPU

| Scénario | Résultat attendu | Action |
|---|---|---|
| Ollama `ollama ps` → `100% GPU` | GPU disponible (~30-50 tok/s) | Formation premium — démos ultra-fluides |
| Ollama `ollama ps` → `100% CPU` | CPU only (~5-8 tok/s) | **Suffisant** — utiliser phi4-mini pour démos live |
| Fine-tuning HuggingFace | **Toujours sur Google Colab** | GPU VM non requis, jamais |
| Anthropic API | Cloud, zéro GPU | Toujours rapide quelle que soit la VM |

**Conclusion** : même sans GPU, la VM couvre 100% des exercices de la formation.
Seules les démos Ollama live sur gros modèle seront légèrement lentes — utiliser `phi4-mini` dans ce cas.

---

## Fichiers critiques

| Fichier | Rôle |
|---|---|
| `requirements.txt` | Toutes les dépendances pip |
| `.env.example` → `.env` | Variables d'environnement — ANTHROPIC_API_KEY obligatoire |
| `scripts/preload_models.py` | Télécharge le modèle ONNX fastembed (~100 Mo) |
| `homebutler/config.py` | Chargement + validation des variables .env |
| `homebutler/llm/provider.py` | Abstraction Anthropic / Ollama |
| `api/main.py` | Point d'entrée FastAPI (port 8000) |
| `ui/app.py` | Point d'entrée Streamlit (port 8501) |
| `notebooks/03_finetuning_lora.ipynb` | **Colab seulement** — GPU T4 requis |
