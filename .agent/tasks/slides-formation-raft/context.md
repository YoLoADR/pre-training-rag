# Context — Slides Formation RAFT

## Objectif

Produire un fichier `/Users/yohannravino/Factory/pre-training-rag/slides-formation-raft.md`
contenant les supports de formation complets pour la formation PLB "RAG et Fine Tuning d'un LLM"
(réf. RAFT, 3 jours, niveau intermédiaire).

## Format de sortie

- **1 fichier `.md` unique** utilisé comme source pour gamma.app
- **60 slides** : 10 slides × 6 chapitres
- **Langue** : français intégral
- **Pas de blocs de code** (Gamma gère mal les ``` — remplacer par tableaux / pseudo-flux textuels)
- Format validé par les exemples : `examples-supports/slides-inspiration-1.md` et `slides-inspiration-2.md`

## Structure de la formation (programme PLB RAFT)

| Jour | Chapitre | Titre |
|------|----------|-------|
| 1 | 1 | Introduction aux LLM et concepts RAG |
| 1 | 2 | Création d'un RAG simple avec Python |
| 2 | 3 | Intégration dans un pipeline RAG |
| 2 | 4 | Fine-tuning avec HuggingFace |
| 3 | 5 | Déploiement, bonnes pratiques, optimisation et supervision |
| 3 | 6 | Fine Tuning vs RAG |

## Format gamma.app (règles de structure)

- Titre chapitre : `Chapitre X : [Titre] — Jour Y` (plain text)
- Objectif : `🎯 Objectif du chapitre` + paragraphe
- Slide : `📝 Slide N : [Titre]`
- Ouverture : `POURQUOI [question] ?`
- Tables : markdown `|col|col|`
- Callout positif : `> 💡 [texte]`
- Avertissement : `⚠️ **Titre** — description`
- Recap : `🎓 Ce que vous devez retenir` + table `| Concept | Pourquoi c'est important |`
- Transition : `➡️ Prochain chapitre` + teaser
- Séparateur `---` entre chapitres

## Projet fil rouge HomeButler AI

Conciergerie IA HomeButler — progression au fil des chapitres :
- Chap 1 : Vision du projet (architecture cible)
- Chap 2 : Indexation des 6 PDFs → FAISS + ChromaDB
- Chap 3 : Pipeline LangChain + 4 outils ReAct
- Chap 4 : Dataset 150 Q&A → fine-tuning LoRA
- Chap 5 : FastAPI + Streamlit + Docker Compose
- Chap 6 : Architecture finale hybride RAG + FT

Stack HomeButler : LangChain 0.3.14, FastEmbedEmbeddings (paraphrase-multilingual-MiniLM,
384 dim), FAISS + ChromaDB, Python 3.13.5 (Intel Mac), FastAPI 0.115.6, Streamlit, Docker Compose.

## Sources

- Programme formation : `formation-RAFT.pdf`
- Format référence : `examples-supports/slides-inspiration-1.md`, `slides-inspiration-2.md`
- Projet fil rouge : `.agent/tasks/homebutler-ai-build/` (context, plan, insights)
- Plan détaillé : `.agent/tasks/slides-formation-raft/plan-detaille.md`
