# Grille de décision — RAG vs Fine-Tuning vs Hybride

> Source : Slide 2 + Slide 9 Chapitre 6, complétée par retour terrain projet HomeButler.

## Arbre de décision (4 questions)

```
Q1 — Les informations changent-elles souvent (> 1 fois/mois) ?
       ├─ OUI  →  RAG (facile à mettre à jour, pas de re-training)
       └─ NON  →  passer à Q2

Q2 — Le ton / style de réponse est-il critique pour l'usage ?
       ├─ OUI  →  Fine-Tuning  (ou Hybride si Q1 = OUI partiel)
       └─ NON  →  RAG seul suffit

Q3 — Avez-vous un budget GPU disponible (Colab gratuit OU H100 cloud) ?
       ├─ OUI  →  Hybride (FT + RAG) — meilleure qualité globale
       └─ NON  →  RAG seul (aucun GPU requis pour l'inférence Anthropic)

Q4 — Disposez-vous de > 500 paires Q/R annotées de qualité ?
       ├─ OUI  →  Fine-Tuning viable
       └─ NON  →  Prompt engineering + RAG (FT sous-performera)
```

## 8 critères détaillés

| #   | Critère                          | RAG seul              | FT seul                | Hybride            |
|-----|----------------------------------|-----------------------|------------------------|--------------------|
| 1   | Fraîcheur des données            | ✓ instantané          | ✗ figé au training     | ✓ via RAG          |
| 2   | Ton / style                      | dépend du LLM         | ✓ adapté précis        | ✓ adapté précis    |
| 3   | Coût initial (one-shot)          | faible                | moyen-élevé            | élevé              |
| 4   | Coût récurrent (run prod)        | tokens API            | inférence locale       | tokens + inference |
| 5   | Latence par requête              | +100 ms (retriever)   | équivalent             | +100 ms            |
| 6   | Précision factuelle              | dépend du recall      | hallucine si gap       | ✓ très bonne       |
| 7   | Effort maintenance               | mettre à jour PDFs    | re-training périodique | les deux           |
| 8   | Privacy (modèle local)           | ✓ via Ollama          | ✓ self-hosted          | ✓                  |

## Exemples métier — recommandations

### 1. Assistant interne RH (FAQ, congés, politique)

- **Q1** : non (mais MAJ trimestrielle) → continuer
- **Q2** : oui (ton corporate sur-mesure) → **FT** ou Hybride
- **Q3** : sans GPU → **RAG seul** avec prompt système soigné
- **Q4** : 1000+ tickets historiques → FT viable

**Recommandation** : Hybride si budget Colab, sinon **RAG + system prompt
finement engineered**.

### 2. Support technique produit (manuels, error codes, schémas)

- **Q1** : oui (firmwares évoluent) → **RAG obligatoire**
- **Q2** : moyen (technique mais standard) → pas critique
- **Q3** : N/A
- **Q4** : pas dataset Q/R → pas de FT

**Recommandation** : **RAG seul avec EnsembleRetriever** (FAISS pour les
manuels + ChromaDB filtré par modèle/version).

### 3. Analyse contrats juridiques (extraction clauses, recherche jurisprudence)

- **Q1** : non (lois stables) → continuer
- **Q2** : oui (vocabulaire juridique précis attendu) → FT
- **Q3** : oui (legaltech a budget GPU) → Hybride
- **Q4** : 5k contrats annotés → FT excellent

**Recommandation** : **Hybride — RAFT** (FT du modèle + RAG sur le corpus
réel) pour combiner précision lexicale + recherche sur précédents.

## TCO 12 mois (Slide 8 Chapitre 6)

> Estimation indicative pour ~10k requêtes/mois.

| Approche                | Setup (€) | Run/an (€)            | Total an 1 (€) |
|-------------------------|-----------|-----------------------|----------------|
| RAG seul (Claude API)   | 500       | 1 200 (tokens)        | **1 700**      |
| Fine-Tuning seul        | 3 000     | 600 (Ollama selfhosted)| **3 600**     |
| Hybride                 | 3 500     | 1 800                 | **5 300**      |

- **Setup** = annotation Q/R + temps ingénieur + GPU Colab pro éventuel
- **Run** = tokens API + serveur Ollama (VPS ~50 €/mois GPU partagé)
- **Hybride payant** seulement si gain qualité justifié vs coût (cas critique :
  santé, juridique, support payant haut de gamme).

## Conclusion fil rouge HomeButler

Pour un MVP : **RAG seul** suffit largement (Recall@5 ≈ 87 % sur les questions
logement). Le **Fine-Tuning** apporte sa valeur sur le **ton conciergerie
chaleureux** qui est un différenciateur produit — donc Hybride si on vise
une offre premium, RAG seul pour démarrer.
