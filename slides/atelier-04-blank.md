📝 Slide 1 : Atelier 04 — Fine-tuning LoRA/QLoRA (mission en un coup d'œil)

POURQUOI fine-tuner quand le RAG fonctionne déjà ?

Le RAG (AT02-03) résout le problème de CONNAISSANCE manquante (« cette info n'est pas dans le modèle »). Il NE RÉSOUT PAS le problème de STYLE/TON (« réponds toujours comme une conciergerie chaleureuse, format strict accueil + corps + signature »). Pour modifier le COMPORTEMENT du modèle, il faut toucher ses poids — c'est le fine-tuning. LoRA (Low-Rank Adaptation) le rend abordable : on n'entraîne que ~1 % des poids (matrices Q et V de l'attention) au lieu de tout.

| Bloc | Ce qu'il fait | Pourquoi c'est nécessaire |
|------|---------------|---------------------------|
| Dataset Q/R (150 paires en dur) | Format Alpaca `{instruction, input, output}` | Le dataset = la SUPERVISION du fine-tuning |
| `generate()` (À CODER) | Sérialise en JSONL + classifie par catégorie | JSONL = format standard HuggingFace ; catégorie = équilibrage |
| `paraphrase_question()` (À CODER) | Augmente 150 → 500 paires sans LLM | Plus de variantes = meilleure généralisation, sans coût LLM |
| Cellule 11 notebook (À CODER) | Charge Mistral-7B en QLoRA 4-bit | 14 GB → 4 GB de VRAM (tient sur T4 15 GB) |
| Cellule 13 (À CODER) | `LoraConfig` (r=8, alpha=16, target Q/V) | Définit QUELS poids et COMBIEN entraîner |
| Cellule 15 (À CODER) | `TrainingArguments` + `SFTTrainer` + MLFlow | Lance l'entraînement avec tracking |

> 💡 **Branche élève** : `git checkout student/04-finetuning`. Particularité : le notebook est édité via `scripts/blank_notebook.py` (nbformat), pas à la main.


📝 Slide 2 : État initial vs ce qu'on va construire

POURQUOI conserver les 150 paires Q/R en dur dans le code ?

Les 150 paires sont du contenu MÉTIER (chaudière, bail, énergie, marketplace) — pas du concept pédagogique. Les blanker te forcerait à inventer 150 paires, ce qui n'est ni faisable en 1h40 ni intéressant. On garde les paires et on blanke la LOGIQUE de transformation (classification, sérialisation, paraphrase, training).

| Fichier | État | Pourquoi |
|---------|------|----------|
| `homebutler/llm/`, `homebutler/rag/`, `api/` | ✅ Acquis AT01-03 | RAG, agent, prompts déjà OK |
| `scripts/generate_qa_dataset.py` → `QA_PAIRS` (data) | ✅ Conservé | Contenu métier, pas concept |
| `scripts/generate_qa_dataset.py` → `generate()` | 🛠️ **À CODER** | Concept : sérialisation Alpaca + classification |
| `scripts/augment_qa_dataset.py` → règles + suffixes | ✅ Conservé | Patterns linguistiques (lecture) |
| `scripts/augment_qa_dataset.py` → `paraphrase_question` | 🛠️ **À CODER** | Concept : data augmentation déterministe par règles + RNG seedé |
| `notebooks/03_finetuning_lora.ipynb` cellules 11/13/15 | 🛠️ **À CODER** | Concept : QLoRA, LoraConfig, SFTTrainer |
| `scripts/blank_notebook.py` | ✅ Fourni (script de blanking) | Reproductibilité de la branche |


📝 Slide 3 : Concept #1 — Charger Mistral-7B en QLoRA 4-bit

POURQUOI 4-bit et pas FP16 sur Colab T4 ?

T4 = 15 GB de VRAM. Mistral-7B en FP16 = 14 GB juste pour les poids (rien pour les activations ni les gradients) → OOM. En 4-bit (NF4) + double quantization, on tombe à ~4 GB → confortable, on peut ouvrir un batch de 4 sans crasher. Le coût : ~1-2 % de qualité en moins, négligeable.

**Cellule 11 à compléter** (extrait blank) :

```python
# TODO — Charger Mistral-7B-Instruct-v0.2 avec quantization 4-bit
# Tu auras besoin de :
#   1. BitsAndBytesConfig (avec 4 paramètres clés)
#   2. AutoTokenizer (en alignant pad_token sur eos_token)
#   3. AutoModelForCausalLM (avec quantization_config + device_map='auto')

raise NotImplementedError("Cellule 11 — voir indices ci-dessous")
```

**Indice léger** — La lib `bitsandbytes` (intégrée à `transformers`) expose `BitsAndBytesConfig`. Tu actives `load_in_4bit=True` puis tu choisis le type de quantization (3 options possibles : nf4, fp4, ou int4).

**Indice fort** — Configuration optimale pour T4 : `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type='nf4')`. ⚠️ Trois pièges connus :
- T4 ne supporte PAS `bfloat16` → utilise `float16` (sinon OOM ou crash).
- Mistral n'a pas de `pad_token` natif → `tokenizer.pad_token = tokenizer.eos_token`.
- Si tu actives le gradient checkpointing en cellule 13, mets `model.config.use_cache = False` **MAINTENANT** (en cellule 11) — sinon training cassé.

> 💡 **Analogie** : QLoRA 4-bit = compresser une encyclopédie HD en JPEG basse qualité. 4× plus léger, presque pas visible à l'œil nu (cas d'usage : tu LIS le contenu, pas un pixel à la fois).

**📚 Dépendances natives utilisées**

- `transformers.BitsAndBytesConfig(...)` — config de quantization (vient de la lib `bitsandbytes`). Paramètres :
  - `load_in_4bit: bool` — active le chargement en 4 bits. À combiner avec les 3 suivants.
  - `bnb_4bit_compute_dtype: torch.dtype` — type des CALCULS pendant le training. `torch.float16` sur T4 (T4 ne supporte PAS bfloat16) ; `torch.bfloat16` sur A100/H100.
  - `bnb_4bit_use_double_quant: bool` — `True` quantize aussi les constantes de quantization → gain ~0.4 bits/param.
  - `bnb_4bit_quant_type: "nf4" | "fp4"` — `"nf4"` (NormalFloat4) OPTIMAL pour LLM (distribution normale-like des poids).

- `transformers.AutoModelForCausalLM.from_pretrained(name, ...)` — charge un modèle causal. Paramètres clés :
  - `pretrained_model_name_or_path: str` — nom HuggingFace (`"mistralai/Mistral-7B-Instruct-v0.2"`) ou path local.
  - `quantization_config: BitsAndBytesConfig | None` — config bnb ci-dessus. Si `None`, charge en FP16/FP32.
  - `device_map: "auto" | "balanced" | dict` — répartition GPU. `"auto"` = HuggingFace décide.
  - `trust_remote_code: bool` — `True` autorise l'exécution de code Python custom embarqué dans le repo HF.
  - `torch_dtype: torch.dtype | "auto"` — type des poids non-quantizés.

- `transformers.AutoTokenizer.from_pretrained(name, trust_remote_code)` — charge le tokenizer. ⚠️ Mistral n'a pas de `pad_token` natif → après chargement : `tokenizer.pad_token = tokenizer.eos_token`.


📝 Slide 4 : Concept #2 — LoraConfig (r=8, alpha=16, target Q/V)

POURQUOI n'entraîner que les matrices Q et V de l'attention ?

Un transformer a beaucoup de matrices : Q (Query), K (Key), V (Value), O (Output) dans chaque tête d'attention, plus les feed-forward. L'article LoRA (Hu et al. 2021) a empiriquement montré que **Q et V sont les plus impactantes** : adapter uniquement ces 2 matrices capture ~95 % du gain de l'adaptation complète, avec 1/4 des paramètres entraînables. Sur Mistral-7B : ~4 M params entraînables au lieu de 7 G — gain ×1750.

**Cellule 13 à compléter** :

```python
# TODO — Préparer le modèle pour k-bit training, puis y appliquer LoRA
# Tu auras besoin de :
#   1. prepare_model_for_kbit_training(model)
#   2. Instancier LoraConfig (5 paramètres clés)
#   3. get_peft_model(model, lora_config)
#   4. Afficher model.print_trainable_parameters() pour vérifier ~0.05 % entraînables

raise NotImplementedError("Cellule 13 — voir indices ci-dessous")
```

**Indice léger** — La lib `peft` expose `LoraConfig`. Ses paramètres clés : `r`, `lora_alpha`, `target_modules`, `lora_dropout`, `task_type`. La règle de pouce empirique : `lora_alpha = 2 × r`.

**Indice fort** — Pour adapter le STYLE/TON sur 150 paires : `r=8` (capacité moyenne), `lora_alpha=16` (ratio 2 standard), `target_modules=['q_proj', 'v_proj']` (Q et V uniquement, suffit à 95 % du gain), `lora_dropout=0.05`, `bias='none'`, `task_type='CAUSAL_LM'`. Pour un domaine technique nouveau (juridique, médical), monte à `r=16` ou `32`.

| r | Params entraînables | Cas d'usage |
|---|--------------------|--------------|
| r=4  | ~1.7 M | Petite adaptation style/ton |
| r=8  | ~3.4 M | **Standard** — style + format de réponse |
| r=16 | ~6.8 M | Domaine technique nouveau (juridique, médical) |
| r=64 | ~27 M  | Quasi full FT, dépasse souvent l'utile |

> 💡 **Analogie** : LoRA = des **post-its sur les pages clés** d'un livre de 7 000 pages. Le livre reste figé. À l'usage, on lit le livre + les post-its. Les post-its pèsent <50 MB et s'écrivent en 15 min ; réécrire le livre prendrait des semaines et 14 GB.

**📚 Dépendances natives utilisées**

- `peft.prepare_model_for_kbit_training(model)` — prépare un modèle quantizé pour le training : active le gradient checkpointing (recalcul des activations en backward → économise VRAM contre temps), désactive `model.config.use_cache`, gèle les poids quantizés.

- `peft.LoraConfig(...)` — configuration de l'adaptation LoRA. Paramètres :
  - `r: int` — RANG des matrices A (in×r) et B (r×out) qui remplacent l'update ΔW. Plus `r` est grand, plus on a de capacité ; plus on entraîne de params. r=8 sweet spot adaptation style/ton.
  - `lora_alpha: int` — facteur d'échelle des updates LoRA. Forward : `output = W @ x + (alpha/r) × B @ A @ x`. Règle de pouce : `alpha = 2 × r`.
  - `target_modules: list[str] | str` — modules à adapter. Pour attention : `["q_proj", "v_proj"]` (Q+V suffit à 95 % du gain). Pour adaptation complète : `"all-linear"`.
  - `lora_dropout: float` — dropout sur les updates LoRA (régularisation). 0.05 typique.
  - `bias: "none" | "all" | "lora_only"` — `"none"` = on ne touche pas aux biais (économie params).
  - `task_type: "CAUSAL_LM" | "SEQ_CLS" | "SEQ_2_SEQ_LM"` — détermine quelle classe PEFT instancier.
  - `modules_to_save: list[str] | None` — modules ENTIÈREMENT entraînés (pas LoRA-isés). Utile pour réajuster `lm_head` ou `embed_tokens`.

- `peft.get_peft_model(model, lora_config) → PeftModel` — applique LoRA : gèle les poids originaux et ajoute A/B entraînables. Le modèle retourné s'utilise comme un transformer normal mais seuls A/B sont mis à jour pendant le `.backward()`.


📝 Slide 5 : Concept #3 — TrainingArguments + SFTTrainer + MLFlow

POURQUOI SFTTrainer plutôt que `Trainer` brut ?

`SFTTrainer` (de la lib TRL) est un wrapper spécialisé pour le **Supervised Fine-Tuning** sur des datasets text-only. Il gère automatiquement la tokenization avec le bon template (Mistral, Llama, etc.), le packing des séquences, le mask de loss sur les tokens de prompt. Avec `Trainer` brut, il faudrait écrire 50 lignes de glue code.

**Cellule 15 à compléter** :

```python
# TODO — Configurer TrainingArguments + lancer SFTTrainer dans mlflow.start_run()
# Tu auras besoin de :
#   1. TrainingArguments (8-10 hyperparamètres clés)
#   2. mlflow.start_run() + log_params + log_metrics
#   3. SFTTrainer(model, train_dataset, eval_dataset, peft_config, tokenizer, args)
#   4. trainer.train() puis trainer.save_model()

raise NotImplementedError("Cellule 15 — voir indices ci-dessous")
```

**Indice léger** — Pour LoRA sur 150 paires, le batch effectif (`batch_size × gradient_accumulation_steps`) doit être ≥ 16 pour un gradient stable. `learning_rate` LoRA est ~10-100× plus élevé qu'un full FT (`2e-4` typique). 3 epochs suffisent — au-delà tu overfit.

**Indice fort** — Hyperparamètres recommandés T4 : `num_train_epochs=3`, `per_device_train_batch_size=4`, `gradient_accumulation_steps=4` (batch effectif = 16), `learning_rate=2e-4`, `warmup_steps=50`, `fp16=True`, `optim='paged_adamw_32bit'` (économise ~3 GB VRAM), `lr_scheduler_type='cosine'`, `eval_strategy='steps', eval_steps=50`, `load_best_model_at_end=True`. ⚠️ Si `loss=NaN` au 1er step → divise `learning_rate` par 2.

> 💡 **Critère de succès** : loss train ≤ 1.5 après 3 epochs ; adapter < 50 MB sur disque ; ROUGE-L sur 10 questions test > ROUGE-L du modèle base.

**📚 Dépendances natives utilisées**

- `transformers.TrainingArguments(...)` — config d'entraînement HuggingFace. Paramètres clés :
  - `output_dir: str` — où sauver checkpoints + tokenizer + adapter.
  - `num_train_epochs: float` — nombre d'epochs. 3 pour LoRA sur petit dataset.
  - `per_device_train_batch_size: int` — batch par GPU. 4 sur T4 pour 7B QLoRA.
  - `gradient_accumulation_steps: int` — accumule N forwards avant un backward. Batch effectif = `batch_size × gradient_accumulation × num_devices`.
  - `learning_rate: float` — LR initial. `2e-4` standard LoRA (10-100× plus haut qu'un full FT).
  - `warmup_steps: int` — montée linéaire du LR sur N steps avant le scheduler. 50 typique.
  - `fp16: bool` / `bf16: bool` — calculs en demi-précision. T4 → `fp16=True` ; A100+ → `bf16=True`.
  - `optim: "adamw_torch" | "paged_adamw_32bit" | …` — `paged_adamw_32bit` économise ~3 GB VRAM en swappant les états AdamW (m, v) CPU↔GPU.
  - `lr_scheduler_type: "linear" | "cosine" | "constant"` — `"cosine"` recommandé.
  - `eval_strategy: "no" | "steps" | "epoch"` + `eval_steps: int` — fréquence des évaluations.
  - `save_steps: int` + `save_total_limit: int` — fréquence des checkpoints + nombre max conservés.
  - `load_best_model_at_end: bool` — restore le checkpoint avec la val_loss min à la fin.
  - `report_to: "none" | "tensorboard" | "wandb" | "mlflow"` — destination des logs auto.

- `trl.SFTTrainer(...)` — wrapper spécialisé Supervised Fine-Tuning. Paramètres :
  - `model: PreTrainedModel` — le modèle PEFT-LoRA.
  - `train_dataset` / `eval_dataset: Dataset` — datasets HuggingFace.
  - `peft_config: LoraConfig | None` — re-passé pour générer un adapter propre à la fin.
  - `dataset_text_field: str` — nom du champ texte dans le dataset (ex. `"text"`).
  - `max_seq_length: int` — longueur max après tokenization. Tronque les exemples plus longs.
  - `tokenizer: PreTrainedTokenizer` — le tokenizer associé.
  - `args: TrainingArguments` — la config ci-dessus.

- `mlflow.set_tracking_uri(uri)` + `mlflow.set_experiment(name)` — initialisent le store local Colab (ex. `'file:///content/mlruns'`).
- `mlflow.start_run(run_name)` — context manager pour un run.
- `mlflow.log_params(dict)` + `mlflow.log_metrics(dict)` — tracking des hyperparams et métriques.


📝 Slide 6 : Pipeline complet — du dataset au modèle FT déployable

POURQUOI vue d'ensemble ?

```
QA_PAIRS (150 en dur dans .py)
   │
   ▼  generate() — À CODER : sérialise + classifie
data/qa_dataset/concierge_qa.jsonl          # format Alpaca
   │
   ▼  paraphrase_question() x N — À CODER : data augmentation
data/qa_dataset/augmented_concierge_qa.jsonl  # ~500 paires
   │
   ▼  Notebook cellule 11 — À CODER : Mistral-7B + QLoRA 4-bit
model + tokenizer chargés en ~4 GB VRAM
   │
   ▼  Cellule 13 — À CODER : LoraConfig r=8 sur q_proj/v_proj
model peft → 0.047 % params entraînables
   │
   ▼  Cellule 15 — À CODER : SFTTrainer 3 epochs
adapter LoRA sauvegardé (~50 MB)
   │
   ▼  Cellules 18-19 (déjà fournies) — éval base vs FT
ROUGE-L FT > ROUGE-L base sur 10 questions test
   │
   ▼  Cellules 23-25 (déjà fournies) — merge + GGUF + Ollama
modèle déployable en local via Ollama
```


📝 Slide 7 : Récap — démarrer sur la branche `student/04-finetuning`

POURQUOI 2 environnements (local Mac + Colab) ?

Les **scripts dataset** (generate_qa, augment_qa) tournent en local — pas besoin de GPU. Le **notebook training** tourne sur Colab T4 (gratuit, 4-6h/jour) — impossible en local sans GPU Nvidia 12 GB+.

```bash
# 1. Local : préparer le dataset
git checkout student/04-finetuning
source .venv/bin/activate
python scripts/generate_qa_dataset.py     # À CODER `generate()` d'abord
python scripts/augment_qa_dataset.py      # À CODER `paraphrase_question()` d'abord
# Vérification :
wc -l data/qa_dataset/concierge_qa.jsonl              # ≥ 150
wc -l data/qa_dataset/augmented_concierge_qa.jsonl    # ≥ 500

# 2. Colab : ouvrir le notebook
# https://colab.research.google.com → File → Upload notebook → 03_finetuning_lora.ipynb
# Runtime → Change runtime type → GPU T4
# Run all cells (15-20 min de training à la cellule 15)

# 3. Validation locale
python ateliers/atelier-04-finetuning/checkpoints/check_1.py
#    → 3 termes lexique + verbalisation pourquoi q_proj+v_proj

# 4. En dernier recours
git diff student/04-finetuning atelier/04-finetuning -- notebooks/03_finetuning_lora.ipynb
git diff student/04-finetuning atelier/04-finetuning -- scripts/generate_qa_dataset.py
git diff student/04-finetuning atelier/04-finetuning -- scripts/augment_qa_dataset.py
```

⚠️ **Limite T4 Colab gratuit** : ~4-6h/jour. Si tu épuises ton quota, tu peux soit attendre 24 h, soit acheter Colab Pro (~10 €/mois), soit louer un VPS GPU (Lambda, RunPod ~0.5 €/h).

> 💡 **Tip** : sur le notebook, fais d'abord tourner les cellules 1-10 (chargement + dataset), puis pose-toi la question avant chaque cellule pivot (11, 13, 15) : « qu'est-ce que je m'attends à voir affiché ? » — puis lance et compare.
