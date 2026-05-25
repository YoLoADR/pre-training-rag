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

Les 150 paires sont du contenu MÉTIER (chaudière, bail, énergie, marketplace) — pas du concept pédagogique. Les blanker forcerait l'élève à inventer 150 paires, ce qui n'est ni faisable en 1h40 ni intéressant. On garde les paires et on blanke la LOGIQUE de transformation (classification, sérialisation, paraphrase, training).

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

**Évolution à apporter** (cellule 11 du notebook) :

```python
# AVANT (blank) : NotImplementedError + commentaires d'indices
# APRÈS (corrigé) :

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = 'mistralai/Mistral-7B-Instruct-v0.2'

# AVANTAGE QLoRA 4-bit : on stocke chaque poids sur 4 bits (16 valeurs possibles)
# au lieu de 16 bits. Compression 4×. La double_quant compresse même les
# CONSTANTES de quantization → gain supplémentaire ~0.4 bits/param.
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,                       # quantize les poids en 4 bits
    bnb_4bit_compute_dtype=torch.float16,    # calculs en FP16 (T4 = pas de BF16)
    bnb_4bit_use_double_quant=True,          # économise ~0.4 bits/param
    bnb_4bit_quant_type='nf4',               # NormalFloat4 — optimal pour les LLM
    #  ↑ nf4 > fp4 : la distribution des poids des LLM est NORMALE-like, donc
    #    un quantiseur calibré sur cette distribution (NF) préserve mieux
    #    la qualité que le quantiseur "uniforme" (FP).
)

# Tokenizer : Mistral n'a pas de pad_token natif → on alias eos_token.
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'right'      # évite des warnings de SFTTrainer

# Chargement modèle. `device_map='auto'` répartit automatiquement entre les
# GPU disponibles (sur T4 unique, ça revient à "tout sur cuda:0").
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=bnb_config,
    device_map='auto',
    trust_remote_code=True,
)
model.config.use_cache = False
#  ↑ CRITIQUE : `use_cache` (KV cache) est INCOMPATIBLE avec le gradient
#    checkpointing (qu'on active à la cellule suivante pour économiser la
#    VRAM pendant le training). À laisser à True UNIQUEMENT pour l'inférence.
```

> 💡 **Analogie** : QLoRA 4-bit = compresser une encyclopédie HD en JPEG basse qualité. 4× plus léger, presque pas visible à l'œil nu (cas d'usage : tu LIS le contenu, pas un pixel à la fois).


📝 Slide 4 : Concept #2 — LoraConfig (r=8, alpha=16, target Q/V)

POURQUOI n'entraîner que les matrices Q et V de l'attention ?

Un transformer a beaucoup de matrices : Q (Query), K (Key), V (Value), O (Output) dans chaque tête d'attention, plus les feed-forward. L'article LoRA (Hu et al. 2021) a empiriquement montré que **Q et V sont les plus impactantes** : adapter uniquement ces 2 matrices capture ~95 % du gain de l'adaptation complète, avec 1/4 des paramètres entraînables. Sur Mistral-7B : ~4 M params entraînables au lieu de 7 G — gain ×1750.

**Évolution à apporter** (cellule 13) :

```python
# AVANT (blank) : NotImplementedError
# APRÈS (corrigé) :

from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Active le gradient checkpointing : on recalcule les activations en backward
# plutôt que de les stocker. Économise la VRAM en échange d'un peu de temps.
model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=8,
    #  ↑ RANG des matrices A (in × r) et B (r × out). Plus r est grand,
    #    plus on a de capacité d'adaptation MAIS plus on entraîne de params.
    #    r=8 = sweet spot pour adapter le STYLE/TON. Pour adapter un nouveau
    #    DOMAINE technique, on monterait à r=16 ou 32.

    lora_alpha=16,
    #  ↑ FACTEUR D'ÉCHELLE des mises à jour LoRA. Règle de pouce : alpha = 2 × r.
    #    Pendant le forward : output = W @ x + (alpha/r) × B @ A @ x
    #    Avec alpha=16, r=8 → ratio 2. C'est la valeur par défaut de la lib peft.

    target_modules=['q_proj', 'v_proj'],
    #  ↑ ON CIBLE UNIQUEMENT Q et V (Query et Value de l'attention multi-tête).
    #    Empiriquement (LoRA paper §7.1) : cible Q+V → 95 % du gain de cibler
    #    Q+K+V+O, avec 50 % moins de params. Trade-off optimal.

    lora_dropout=0.05,                # régularisation légère
    bias='none',                      # on ne touche pas aux biais (économie params)
    task_type='CAUSAL_LM',            # génération autoregressive (vs SEQ_CLS)
)

# Applique LoRA : remplace `model` par sa version PEFT.
# Tous les poids originaux sont GELÉS, seules les matrices A/B sont entraînables.
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → "trainable params: 3,407,872 || all params: 7,245,344,768 || trainable: 0.0470 %"
#    ↑ 0.047 % des params à entraîner !
```

| r | Params entraînables | Cas d'usage |
|---|--------------------|--------------|
| r=4  | ~1.7 M | Petite adaptation style/ton |
| r=8  | ~3.4 M | **Standard** — style + format de réponse |
| r=16 | ~6.8 M | Domaine technique nouveau (juridique, médical) |
| r=64 | ~27 M  | Quasi full FT, dépasse souvent l'utile |

> 💡 **Analogie** : LoRA = des **post-its sur les pages clés** d'un livre de 7 000 pages. Le livre reste figé. À l'usage, on lit le livre + les post-its. Les post-its pèsent <50 MB et s'écrivent en 15 min ; réécrire le livre prendrait des semaines et 14 GB.


📝 Slide 5 : Concept #3 — TrainingArguments + SFTTrainer + MLFlow

POURQUOI SFTTrainer plutôt que `Trainer` brut ?

`SFTTrainer` (de la lib TRL) est un wrapper spécialisé pour le **Supervised Fine-Tuning** sur des datasets text-only. Il gère automatiquement la tokenization avec le bon template (Mistral, Llama, etc.), le packing des séquences, le mask de loss sur les tokens de prompt. Avec `Trainer` brut, il faudrait écrire 50 lignes de glue code.

**Évolution à apporter** (cellule 15) :

```python
# AVANT : NotImplementedError
# APRÈS :

import mlflow
from trl import SFTTrainer
from transformers import TrainingArguments

mlflow.set_tracking_uri('file:///content/mlruns')
mlflow.set_experiment('homebutler-finetuning')

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    #  ↑ 3 epochs : règle de pouce LoRA. Au-delà on risque l'overfit
    #    (val_loss remonte alors que train_loss continue à baisser).

    per_device_train_batch_size=4,             # 4 exemples par forward sur T4
    gradient_accumulation_steps=4,             # accumule 4 forward avant 1 backward
    #  ↑ COMBINÉ : batch effectif = 4 × 4 = 16. C'est la TAILLE QUI COMPTE pour la
    #    stabilité du gradient. Astuce VRAM : 16 d'un coup = OOM, mais 4 accumulés
    #    4 fois = OK.

    warmup_steps=50,                           # rampe douce du LR au début
    learning_rate=2e-4,
    #  ↑ LoRA tolère un LR PLUS ÉLEVÉ que le full FT (qui demande 1e-5 à 5e-5).
    #    2e-4 = standard LoRA. Si loss=NaN au 1er step → diviser par 2.

    fp16=True,                                 # calculs en FP16 (T4-friendly)
    logging_steps=25,
    eval_strategy='steps', eval_steps=50,
    save_steps=100, save_total_limit=2,        # garde 2 derniers checkpoints
    load_best_model_at_end=True,               # restore le meilleur (val_loss min)
    report_to='none',                          # on gère MLFlow à la main
    optim='paged_adamw_32bit',
    #  ↑ Optimiseur PAGINÉ : les états d'AdamW (m, v) sont swappés CPU↔GPU à
    #    la demande. Économise ~3 GB VRAM vs adamw_32bit normal. Critique sur T4.
    lr_scheduler_type='cosine',                # décroissance cosinus du LR
)

with mlflow.start_run(run_name='mistral-homebutler-qlora') as run:
    mlflow.log_params({
        'model': MODEL_NAME, 'lora_r': 8, 'lora_alpha': 16,
        'target_modules': 'q_proj,v_proj', 'epochs': 3,
        'batch_size': 4, 'gradient_accumulation': 4,
        'learning_rate': 2e-4, 'quantization': '4-bit NF4',
    })

    trainer = SFTTrainer(
        model=model, train_dataset=train_dataset, eval_dataset=eval_dataset,
        peft_config=lora_config,
        dataset_text_field='text',             # nom du champ texte dans le dataset
        max_seq_length=512,                    # tronque les ex trop longs (mémoire)
        tokenizer=tokenizer, args=training_args,
    )
    train_result = trainer.train()
    #  ↑ Sur T4, 150 paires × 3 epochs ≈ 15-20 minutes. Loss attendue : ≤ 1.5.

    mlflow.log_metrics({'final_train_loss': train_result.training_loss, ...})
    trainer.save_model(OUTPUT_DIR)   # sauve les adapters (~50 MB) — pas le modèle complet !
```

> 💡 **Critère de succès** : loss train ≤ 1.5 après 3 epochs ; adapter < 50 MB sur disque ; ROUGE-L sur 10 questions test > ROUGE-L du modèle base.


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
