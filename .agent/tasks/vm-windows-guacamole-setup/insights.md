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

## Résultats réels (à compléter pendant le setup)

### Phase 0 — Pré-vérification
```
Script "Install-Formati..." : [À remplir]
python --version : [À remplir]
git --version : [À remplir]
BIOS Mode (UEFI/Legacy) : [À remplir]
```

### Phase 1 — Environnement
```
WSL2 installé : [À remplir]
Ubuntu version : [À remplir]
Python3.13 version : [À remplir]
IP WSL2 (hostname -I) : [À remplir]
```

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
