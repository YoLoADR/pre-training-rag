# Context — Setup VM Windows (Guacamole) pour la formation RAFT

## Objectif

Configurer complètement une VM Windows 10 (10.0.26200.8246) accessible via Apache Guacamole
pour la formation RAFT (RAG & Fine-Tuning LLM — 3 jours).

La VM (user `PLB`, rôle FORMATEUR, guacamole.plb.fr) arrive vierge :
ni Claude Code CLI, ni le projet `pre-training-rag` ne sont installés.

## Périmètre

Installer, configurer et valider l'ensemble de la stack :

1. **Environnement Python** — WSL2 + Ubuntu 22.04 (ou Python natif Windows en fallback), Python 3.13, venv
2. **Projet fil rouge** — clone GitHub + `pip install -r requirements.txt` + `pip install -e .`
3. **LLM providers** :
   - Anthropic API (Claude) — provider principal J1/J2
   - Ollama (local CPU-only) — provider J3 + démos live
   - HuggingFace — fine-tuning QLoRA sur Google Colab (notebook 03, GPU T4)
4. **Services** — FastAPI (8000), Streamlit (8501), Gradio (7860), Jupyter (8888)
5. **Observabilité** — Langfuse (optionnel, J2/J3)
6. **Claude Code CLI** — installation Windows native

## Contraintes

- VM HyperV : nécessite nested virtualization pour WSL2 → vérifier BIOS UEFI
- Réseau WSL2 : services accessibles via IP WSL2 (`hostname -I`), pas `localhost`
- Disque : ~20 Go libres requis (Python env 3 Go + modèles Ollama ~11 Go + données ~200 Mo)
- RAM : 8-16 Go (suffisant sans GPU)
- **Aucun GPU requis** — fine-tuning toujours sur Colab, Anthropic API en cloud

## Modèles Ollama retenus

| Modèle | Taille | Rôle |
|---|---|---|
| `qwen2.5:7b-instruct` | 4.7 Go | Principal — meilleur français 2025 |
| `phi4-mini` | 2.8 Go | Backup — démo rapide CPU |
| `mistral:7b-instruct` | 4.1 Go | Compatibilité exercices TPs |

## Modèles HuggingFace (Colab uniquement)

- `Qwen/Qwen2.5-7B-Instruct` — recommandé 2025
- `mistralai/Mistral-7B-Instruct-v0.3` — modèle historique du projet

## Réf. plan détaillé

`.agent/tasks/vm-windows-guacamole-setup/plan-setup-vm.md`

## Sources

- Prérequis formation : `PREREQUIS-FORMATION-RAFT.md`
- Credentials Guacamole : `stage142 / UyMdU85wDd259y` (accès FORMATEUR)
- Repo GitHub : `https://github.com/YoLoADR/pre-training-rag`
