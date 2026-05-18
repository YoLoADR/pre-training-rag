"""
Pré-télécharge le modèle d'embeddings depuis HuggingFace Hub (~470 Mo).
À lancer une seule fois avant la formation, idéalement avec une bonne connexion.
"""

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def main():
    print(f"Téléchargement du modèle d'embeddings : {MODEL_NAME}")
    print("(~470 Mo — opération unique, mise en cache dans ~/.cache/huggingface/)")
    model = SentenceTransformer(MODEL_NAME)

    # Test rapide
    test_phrases = [
        "Comment fonctionne ma chaudière ?",
        "Quelle est la température recommandée la nuit ?",
    ]
    embeddings = model.encode(test_phrases)
    print(f"\n✓ Modèle prêt — dimension des embeddings : {embeddings.shape[1]}")
    print(f"  Test encodage : {len(test_phrases)} phrases → {embeddings.shape}")
    print("\nLe modèle est maintenant en cache — les prochains chargements seront instantanés.")


if __name__ == "__main__":
    main()
