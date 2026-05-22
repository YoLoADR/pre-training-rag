# Insights — Setup VM Windows Guacamole

> Mis à jour itérativement au fil de l'exécution du setup.
> Chaque entrée : date · catégorie · finding.

---

## Architecture & Contraintes découvertes

### WSL2 dans HyperV — Point bloquant potentiel
- **Finding** : WSL2 nécessite la nested virtualization activée sur la VM HyperV côté hôte.
  La commande admin hôte est : `Set-VMProcessor -VMName <PLB-VM> -ExposeVirtualizationExtensions $true`
- **Impact** : si non activée, `wsl --install` échoue avec l'erreur `0x80370095`
- **Workaround validé** : Python 3.13 natif Windows + Git Bash (Étape 2b du plan) — fonctionnel mais sans shell Linux

### Réseau WSL2 → Windows — Point subtil
- **Finding** : avec WSL2 en mode NAT (défaut sur Windows 10), les services sur `127.0.0.1` dans WSL2 ne sont PAS accessibles depuis Firefox Windows via `localhost`
- **Solution** : utiliser l'IP WSL2 → `hostname -I` dans WSL2 → ex: `172.31.x.x`
- **Note** : le mode "mirrored" (résout le problème) est Windows 11 uniquement — non applicable ici

### `pip install -e .` — Obligatoire non évident
- **Finding** : sans cette étape, `streamlit run ui/app.py` plante avec `ModuleNotFoundError: homebutler`
  car le package n'est pas enregistré dans le venv comme module importable
- **Action** : à ne jamais omettre, toujours après `pip install -r requirements.txt`

---

## Modèles Ollama — Sélection 2025

### Pourquoi qwen2.5:7b-instruct plutôt que mistral:7b-instruct
- **Finding** : Qwen 2.5 7B outperform Mistral 7B sur les benchmarks 2025 (MMLU, français, reasoning)
  tout en ayant un footprint similaire (~4.7 Go vs 4.1 Go)
- **Vitesse CPU estimée** : 6-9 tok/s vs 5-8 tok/s pour Mistral — légèrement plus rapide
- **Décision** : `qwen2.5:7b-instruct` comme modèle Ollama principal pour la formation

### phi4-mini — Backup idéal pour démos rapides
- **Finding** : 3.8B paramètres, ~2.8 Go, 12-18 tok/s en CPU-only
  Meilleur pour les moments où la fluidité de la démo prime sur la profondeur
- **Usage** : démos live J3 si la connexion est lente ou la VM charge

### mistral:7b-instruct — Garder pour compatibilité exercices
- Le `.env.example` du projet référence `OLLAMA_MODEL=homebutler` (Modelfile custom)
  mais `mistral:7b-instruct` est le modèle de base utilisé dans les TPs
- À conserver pour que les exercices fonctionnent sans modification

---

## GPU — Verdict anticipé

| Test | Attendu sur cette VM | Raison |
|---|---|---|
| `ollama ps` → PROCESSOR | `100% CPU` | VM HyperV sans GPU passthrough probable |
| Vitesse génération | ~5-9 tok/s | CPU-only sur modèle 7B |
| Fine-tuning HuggingFace | N/A local | Colab uniquement — GPU T4 cloud |
| Anthropic API | ~30-80 tok/s | Cloud — indépendant du GPU local |

**Conclusion anticipée** : GPU non requis pour la formation. La VM est suffisante.

> À mettre à jour avec les résultats réels après `ollama ps` (Phase 4.6).

---

## Variables .env — Classification réelle

| Variable | Statut | Valeur par défaut | Note |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | **OBLIGATOIRE** | Aucune | Exception levée si manquante avec `LLM_PROVIDER=anthropic` |
| `LLM_PROVIDER` | Optionnel | `anthropic` | Switch entre providers |
| `ANTHROPIC_MODEL` | Optionnel | `claude-sonnet-4-6` | Valeur correcte par défaut |
| `OLLAMA_MODEL` | Optionnel | `homebutler` | Mettre `qwen2.5:7b-instruct` pour J3 |
| `LANGCHAIN_TRACING_V2` | Optionnel | `false` | Activer pour J2/J3 observabilité |
| `LANGFUSE_*` | Optionnel | — | Ignoré si tracing désactivé |
| `CHROMA_PATH` | Optionnel | `./data/chroma_db` | Auto-créé par indexation |
| `FAISS_PATH` | Optionnel | `./data/faiss_index` | Auto-créé par indexation |

---

## Notebooks — Contraintes importantes

### Notebook 03 → Colab OBLIGATOIRE
- `03_finetuning_lora.ipynb` utilise `bitsandbytes` avec quantization 4-bit
- Requiert GPU T4 (16 Go VRAM) — impossible en CPU-only local
- Sur une VM sans GPU, l'exécution locale plante à la section chargement modèle
- **Action formateur** : toujours ouvrir via https://colab.research.google.com

### Notebooks 01 & 02 → Local sans GPU
- `01_llm_baseline.ipynb` : teste Anthropic + Ollama, aucun GPU requis
- `02_ingestion_vectorisation.ipynb` : pipeline RAG complet, FastEmbed ONNX (pas PyTorch)
- Les deux fonctionnent dans WSL2 Jupyter sur cette VM

---

## Résultats réels

### Phase 0 — Pré-vérification (2026-05-22)
```
Script "Install-Formati..." : Install-FormationRAFT.ps1 — script PowerShell complet (idempotent)
python --version            : Python 3.13.13 ✅
claude --version            : non reconnu ❌ (à installer)
Architecture retenue        : Python NATIF Windows (pas WSL2)
Chemin projet               : C:\Formation_RAFT\pre-training-rag
```

### Ce que le script Install-FormationRAFT.ps1 fait automatiquement
```
1. Installe Git for Windows (winget)
2. Installe Python 3.13.13 depuis partage réseau \\192.168.10.251\Install\COURS\RAFT\RAVINO
3. Installe Docker Desktop depuis le partage
4. Installe Ollama depuis le partage (OllamaSetup.exe)
5. Pull mistral:7b-instruct (~4 Go)
6. Clone https://github.com/YoLoADR/pre-training-rag.git → C:\Formation_RAFT\pre-training-rag
7. Crée venv .venv avec Python 3.13
8. pip install -r requirements.txt + pip install -e .
9. Crée .env (avec placeholders ANTHROPIC_API_KEY et LANGCHAIN_API_KEY)
10. python scripts/preload_models.py (fastembed ~100 Mo)
```

### Implication architecture — Réseau
```
Installation native Windows (pas WSL2)
→ Services accessibles via http://localhost:PORT depuis Firefox Windows
→ Pas besoin de hostname -I / IP WSL2
→ Commande activation venv : C:\Formation_RAFT\pre-training-rag\.venv\Scripts\Activate.ps1
```

### Modèle Ollama du script vs plan révisé
```
Script installe : mistral:7b-instruct
Plan révisé recommande : qwen2.5:7b-instruct (principal) + phi4-mini (backup)
→ Action : après vérif mistral OK, pull qwen2.5 + phi4-mini en plus
→ Mettre à jour OLLAMA_MODEL dans .env selon le jour de formation
```

### Phase 1 — Vérification stack (2026-05-22)
```
git version  : 2.54.0.windows.1 ✅
ollama       : 0.24.0 ✅
ollama list  : mistral:7b-instruct (4.4 GB, modifié il y a 41h) ✅
projet clone : ❌ C:\Formation_RAFT existe mais pre-training-rag absent
               → cause probable : git pas dans PATH au moment du script
venv         : ❌ absent (dépend du clone)
.env         : ❌ absent (dépend du clone)
```

### Python 3.12 requis sur Windows (pas 3.13) — Finding critique
- **Cause racine** : `chroma-hnswlib==0.7.6` (dépendance de `chromadb 0.5.23`) n'a PAS de wheel Windows pour Python 3.13 (cp313). Max supporté = cp312.
- **chromadb 1.5.x** : incompatible avec `langchain-community==0.3.14` (constraint `<0.7.0` hardcodée dans langchain)
- **Seule solution sans compilation** : utiliser **Python 3.12** — `chroma-hnswlib 0.7.6` a un wheel `cp312-win_amd64` pré-compilé ✅
- **Fix immédiat** : `winget install Python.Python.3.12` → supprimer `.venv` → recréer avec `py -3.12 -m venv .venv`
- **Fix install script** : remplacer `python-3.13.13-amd64.exe` par `python-3.12.x-amd64.exe` dans `Install-FormationRAFT.ps1` ET sur le partage réseau `\\192.168.10.251\Install\COURS\RAFT\RAVINO`
- **À signaler formateur** : documentation du projet dit "Python 3.13" mais Windows nécessite 3.12 à cause de chroma-hnswlib. Mac Intel et Linux 3.13 restent valides.

### chroma-hnswlib — Visual C++ Build Tools manquants (bloquant)
- **Erreur** : `Failed building wheel for chroma-hnswlib` → `Microsoft Visual C++ 14.0 or greater is required`
- **Cause** : `chromadb==0.5.23` dépend de `chroma-hnswlib` qui est une extension C++ compilée à la volée.
  Le script d'install (Install-FormationRAFT.ps1) installe Docker Desktop mais pas les VS Build Tools.
- **Fix** : installer Microsoft C++ Build Tools via winget (~3-4 Go, 10-20 min) puis relancer pip install
  ```powershell
  winget install Microsoft.VisualStudio.2022.BuildTools --silent --override "--wait --quiet --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
  ```
- **Après install** : fermer et rouvrir PowerShell, réactiver le venv, relancer `pip install -r requirements.txt`
- **À signaler au formateur** : ajouter Visual C++ Build Tools dans le script Install-FormationRAFT.ps1 (avant pip install)

### Pourquoi le clone a échoué dans le script
Le script installe Git via winget PUIS clone immédiatement.
Winget n'actualise pas le PATH de la session PowerShell en cours.
`Refresh-Path` (fonction interne du script) tente de le faire mais parfois insuffisant.
→ Le `git clone` s'est exécuté avant que `git.exe` soit trouvable.
→ Solution : relancer le clone manuellement dans un nouveau terminal (git dans le PATH maintenant).

### Phase 4 — Ollama GPU verdict
```
ollama ps PROCESSOR : [À remplir → 100% CPU ou 100% GPU]
Vitesse tok/s qwen2.5:7b : [À remplir]
Vitesse tok/s phi4-mini : [À remplir]
```

### Phase 9 — Tests end-to-end
```
/rag/retrieve → chunks trouvés : [À remplir]
/chat Anthropic → latence : [À remplir]
/chat Ollama → latence : [À remplir]
Streamlit UI → fonctionnel : [À remplir]
Gradio → fonctionnel : [À remplir]
```
