"""
Génère le catalogue JSON de 30 producteurs/artisans locaux autour de Boulogne-Billancourt.
Coordonnées GPS réalistes dans la région Île-de-France (rayon ~30 km).
"""

import json
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "marketplace")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "producers.json")

# Centre de référence : 28 avenue des Chênes, Boulogne-Billancourt
CENTER_LAT = 48.835
CENTER_LON = 2.240

PRODUCERS = [
    # ── Légumes & Fruits ──────────────────────────────────────────────────────
    {
        "id": 1, "nom": "Ferme du Moulin Vert", "type": "légumes",
        "produits": ["carottes", "pommes de terre", "courgettes", "haricots verts", "tomates"],
        "latitude": 48.791, "longitude": 2.168, "distance_km": 8.2,
        "livraison": True, "min_commande_eur": 20, "phone": "06 12 34 56 78",
        "horaires": "Mar-Sam 8h-19h", "description": "Maraîcher bio depuis 1995, certification AB",
    },
    {
        "id": 2, "nom": "Les Jardins de Versailles", "type": "légumes",
        "produits": ["salade", "épinards", "radis", "betteraves", "fenouil", "chou-fleur"],
        "latitude": 48.804, "longitude": 2.131, "distance_km": 12.5,
        "livraison": True, "min_commande_eur": 15, "phone": "01 39 50 12 34",
        "horaires": "Mer-Dim 9h-18h", "description": "Exploitation familiale, légumes de saison",
    },
    {
        "id": 3, "nom": "Potager de la Butte", "type": "légumes",
        "produits": ["pommes de terre ratte", "oignons", "poireaux", "navets", "persil"],
        "latitude": 48.862, "longitude": 2.205, "distance_km": 4.8,
        "livraison": False, "min_commande_eur": 0, "phone": "06 87 65 43 21",
        "horaires": "Sam 8h-13h (marché)", "description": "Vente au marché de Boulogne uniquement",
    },
    {
        "id": 4, "nom": "Ferme des Coteaux", "type": "fruits",
        "produits": ["pommes", "poires", "cerises", "prunes", "fraises", "framboises"],
        "latitude": 48.856, "longitude": 2.170, "distance_km": 6.1,
        "livraison": True, "min_commande_eur": 25, "phone": "06 11 22 33 44",
        "horaires": "Lun-Sam 9h-20h", "description": "Verger de 3 hectares, cueillette possible",
    },
    {
        "id": 5, "nom": "Verger de l'Ouest Parisien", "type": "fruits",
        "produits": ["pommes golden", "pommes braeburn", "poires williams", "coings"],
        "latitude": 48.817, "longitude": 2.099, "distance_km": 17.3,
        "livraison": True, "min_commande_eur": 30, "phone": "01 30 45 67 89",
        "horaires": "Mar-Sam 10h-18h", "description": "30 variétés de pommes et poires anciennes",
    },
    {
        "id": 6, "nom": "Maraîchage Bio des Bords de Seine", "type": "légumes",
        "produits": ["courges", "potimarrons", "butternut", "concombres", "aubergines"],
        "latitude": 48.870, "longitude": 2.190, "distance_km": 5.9,
        "livraison": True, "min_commande_eur": 18, "phone": "06 55 44 33 22",
        "horaires": "Jeu-Dim 9h-19h", "description": "Spécialiste cucurbitacées et légumes d'été",
    },
    {
        "id": 7, "nom": "Les Serres de Clamart", "type": "légumes",
        "produits": ["tomates cerises", "tomates cœur de bœuf", "basilic", "persil", "ciboulette"],
        "latitude": 48.793, "longitude": 2.261, "distance_km": 4.4,
        "livraison": True, "min_commande_eur": 12, "phone": "06 77 88 99 00",
        "horaires": "Tous les jours 8h-20h", "description": "Production sous serre toute l'année",
    },
    {
        "id": 8, "nom": "Champignons de Paris Authentiques", "type": "légumes",
        "produits": ["champignons de Paris", "girolles", "pleurotes", "shiitake"],
        "latitude": 48.828, "longitude": 2.281, "distance_km": 3.2,
        "livraison": True, "min_commande_eur": 10, "phone": "06 33 44 55 66",
        "horaires": "Lun-Ven 9h-18h", "description": "Champignonnière en caves naturelles",
    },
    # ── Pain & Boulangerie ────────────────────────────────────────────────────
    {
        "id": 9, "nom": "Boulangerie Artisanale du Moulin", "type": "pain",
        "produits": ["pain de campagne", "baguette tradition", "pain au levain", "pain aux céréales"],
        "latitude": 48.837, "longitude": 2.237, "distance_km": 0.8,
        "livraison": True, "min_commande_eur": 8, "phone": "01 46 03 78 90",
        "horaires": "Mar-Dim 7h-13h30 et 15h30-19h30", "description": "Boulangerie artisanale, farine bio",
    },
    {
        "id": 10, "nom": "Le Four à Bois de Sèvres", "type": "pain",
        "produits": ["pain de seigle", "pain complet", "pain aux noix", "focaccia"],
        "latitude": 48.824, "longitude": 2.224, "distance_km": 2.8,
        "livraison": False, "min_commande_eur": 0, "phone": "01 45 34 56 78",
        "horaires": "Mer-Lun 7h-19h30", "description": "Cuisson au feu de bois, pains de tradition",
    },
    {
        "id": 11, "nom": "Maison Lecomte — Pains Spéciaux", "type": "pain",
        "produits": ["pain au pavot", "pain à l'épeautre", "pain sans gluten", "brioche"],
        "latitude": 48.848, "longitude": 2.215, "distance_km": 3.5,
        "livraison": True, "min_commande_eur": 15, "phone": "06 98 76 54 32",
        "horaires": "Lun-Sam 7h30-20h", "description": "Pains spéciaux et produits sans allergènes",
    },
    {
        "id": 12, "nom": "Boulangerie Bio des Champs", "type": "pain",
        "produits": ["pain au levain naturel", "pain kamut", "pain chanvre", "pain à l'ail"],
        "latitude": 48.797, "longitude": 2.204, "distance_km": 6.8,
        "livraison": True, "min_commande_eur": 20, "phone": "01 46 42 11 22",
        "horaires": "Jeu-Mar 8h-13h", "description": "100% bio, levain naturel exclusivement",
    },
    # ── Fromage & Lait ────────────────────────────────────────────────────────
    {
        "id": 13, "nom": "Fromagerie de la Vallée de Chevreuse", "type": "fromage",
        "produits": ["chèvre frais", "camembert fermier", "brie artisanal", "comté 18 mois"],
        "latitude": 48.732, "longitude": 2.176, "distance_km": 19.8,
        "livraison": True, "min_commande_eur": 30, "phone": "01 30 52 89 00",
        "horaires": "Mer-Dim 9h-18h", "description": "Fromages de chèvre et vache, affinage maison",
    },
    {
        "id": 14, "nom": "La Chèvrerie du Perray", "type": "fromage",
        "produits": ["crottin de chèvre", "fromage blanc", "tomme de chèvre", "faisselle"],
        "latitude": 48.706, "longitude": 2.059, "distance_km": 28.4,
        "livraison": False, "min_commande_eur": 0, "phone": "06 12 98 76 54",
        "horaires": "Sam-Dim 10h-17h", "description": "Chèvrerie visitale, vente directe à la ferme",
    },
    {
        "id": 15, "nom": "Ferme Laitière des Yvelines", "type": "fromage",
        "produits": ["lait cru", "yaourts nature", "beurre fermier", "fromage blanc"],
        "latitude": 48.774, "longitude": 2.060, "distance_km": 26.1,
        "livraison": True, "min_commande_eur": 25, "phone": "01 30 57 34 56",
        "horaires": "Lun-Sam 9h-12h et 15h-19h", "description": "Vaches jersiaises, lait A2",
    },
    {
        "id": 16, "nom": "Affineur des Hauts-de-Seine", "type": "fromage",
        "produits": ["époisses", "munster", "roquefort artisanal", "beaufort"],
        "latitude": 48.867, "longitude": 2.260, "distance_km": 4.9,
        "livraison": True, "min_commande_eur": 35, "phone": "01 47 62 11 22",
        "horaires": "Mar-Dim 10h-19h30", "description": "Sélection de fromages affinés, cave propre",
    },
    # ── Viande ───────────────────────────────────────────────────────────────
    {
        "id": 17, "nom": "Boucherie-Élevage des Berges", "type": "viande",
        "produits": ["bœuf charolais", "agneau d'Ile-de-France", "veau fermier", "porc plein air"],
        "latitude": 48.791, "longitude": 2.157, "distance_km": 9.6,
        "livraison": True, "min_commande_eur": 50, "phone": "01 39 65 43 21",
        "horaires": "Mar-Sam 8h-13h et 15h-19h", "description": "Élevage propre, abattage local",
    },
    {
        "id": 18, "nom": "Volailles de Plein Air du Hurepoix", "type": "viande",
        "produits": ["poulet fermier", "pintade", "canard", "lapin", "oeufs fermiers"],
        "latitude": 48.748, "longitude": 2.184, "distance_km": 14.7,
        "livraison": True, "min_commande_eur": 30, "phone": "06 45 67 89 01",
        "horaires": "Mer et Sam 8h-13h", "description": "Volailles Label Rouge, plein air certifié",
    },
    {
        "id": 19, "nom": "Charcuterie Artisanale Dupuis", "type": "viande",
        "produits": ["jambon blanc", "saucisson sec", "pâté de campagne", "boudin noir"],
        "latitude": 48.852, "longitude": 2.201, "distance_km": 5.3,
        "livraison": False, "min_commande_eur": 0, "phone": "01 46 03 98 76",
        "horaires": "Mar-Sam 8h-19h30", "description": "Charcutier artisan, recettes traditionnelles",
    },
    {
        "id": 20, "nom": "Mouton de l'Île-de-France", "type": "viande",
        "produits": ["gigot d'agneau", "côtelettes", "épaule", "merguez maison"],
        "latitude": 48.824, "longitude": 2.155, "distance_km": 8.9,
        "livraison": True, "min_commande_eur": 45, "phone": "06 78 90 12 34",
        "horaires": "Jeu-Dim 9h-18h", "description": "Race Île-de-France, agneau de plein air",
    },
    # ── Artisans ──────────────────────────────────────────────────────────────
    {
        "id": 21, "nom": "Plomberie & Chauffage MARTIN", "type": "artisan-plombier",
        "produits": ["depannage chaudière", "installation radiateurs", "remplacement robinetterie", "debouchage"],
        "latitude": 48.834, "longitude": 2.250, "distance_km": 1.2,
        "livraison": False, "min_commande_eur": 80, "phone": "06 11 22 33 44",
        "horaires": "Lun-Ven 8h-18h, urgences 24h/24", "description": "Qualibat RGE, devis gratuit",
    },
    {
        "id": 22, "nom": "Électricité Générale BERNARD", "type": "artisan-electricien",
        "produits": ["tableau électrique", "prises et interrupteurs", "éclairage LED", "VMC"],
        "latitude": 48.841, "longitude": 2.232, "distance_km": 0.9,
        "livraison": False, "min_commande_eur": 100, "phone": "06 55 44 33 22",
        "horaires": "Lun-Sam 8h-19h", "description": "Qualifelec, interventions garanties 1 an",
    },
    {
        "id": 23, "nom": "Jardinerie & Entretien VERT NATURE", "type": "artisan-jardinage",
        "produits": ["taille haies", "tonte gazon", "élagage", "création jardin", "potager"],
        "latitude": 48.820, "longitude": 2.270, "distance_km": 2.8,
        "livraison": False, "min_commande_eur": 60, "phone": "06 99 88 77 66",
        "horaires": "Lun-Sam 8h-18h", "description": "Entretien jardins privés, devis sur place",
    },
    {
        "id": 24, "nom": "Peinture & Décoration LEBRUN", "type": "artisan-peintre",
        "produits": ["peinture intérieure", "papier peint", "ravalement", "enduit"],
        "latitude": 48.827, "longitude": 2.248, "distance_km": 2.1,
        "livraison": False, "min_commande_eur": 200, "phone": "06 44 55 66 77",
        "horaires": "Lun-Ven 8h-18h", "description": "Peintre qualifié, assurance décennale",
    },
    {
        "id": 25, "nom": "Serrurerie SÉCURIMAX", "type": "artisan-serrurier",
        "produits": ["changement serrure", "ouverture porte", "blindage", "fermeture sécurisée"],
        "latitude": 48.839, "longitude": 2.242, "distance_km": 0.5,
        "livraison": False, "min_commande_eur": 90, "phone": "06 00 11 22 33",
        "horaires": "Urgences 24h/24 - 7j/7", "description": "Intervention en moins de 30 min",
    },
    {
        "id": 26, "nom": "Menuiserie BOISART", "type": "artisan-menuisier",
        "produits": ["pose fenêtres", "portes intérieures", "parquet", "placards sur mesure"],
        "latitude": 48.814, "longitude": 2.222, "distance_km": 4.2,
        "livraison": False, "min_commande_eur": 300, "phone": "01 46 03 12 34",
        "horaires": "Lun-Ven 8h-17h", "description": "Menuisier ébéniste, travail sur mesure",
    },
    # ── Épicerie fine / autres ────────────────────────────────────────────────
    {
        "id": 27, "nom": "Miellerie de la Forêt de Meudon", "type": "épicerie",
        "produits": ["miel d'acacia", "miel de fleurs", "miel de châtaignier", "propolis", "cire"],
        "latitude": 48.808, "longitude": 2.225, "distance_km": 4.1,
        "livraison": True, "min_commande_eur": 12, "phone": "06 78 12 34 56",
        "horaires": "Sam 10h-18h ou sur RDV", "description": "Apiculteur local, 40 ruches en forêt",
    },
    {
        "id": 28, "nom": "Cave à Vins du Val de Marne", "type": "épicerie",
        "produits": ["vins de Loire", "vins de Bourgogne", "cidre artisanal", "bière locale"],
        "latitude": 48.801, "longitude": 2.291, "distance_km": 6.5,
        "livraison": True, "min_commande_eur": 30, "phone": "01 46 76 54 32",
        "horaires": "Lun-Sam 10h-20h", "description": "Vignerons indépendants, conseils personnalisés",
    },
    {
        "id": 29, "nom": "Confitures & Compotes de Marlène", "type": "épicerie",
        "produits": ["confiture fraise", "confiture abricot", "compote pomme", "gelée de coing"],
        "latitude": 48.857, "longitude": 2.261, "distance_km": 4.7,
        "livraison": True, "min_commande_eur": 15, "phone": "06 56 78 90 12",
        "horaires": "Mer-Dim 10h-18h", "description": "Production artisanale, recettes de grand-mère",
    },
    {
        "id": 30, "nom": "Épicerie Solidaire du Quartier", "type": "épicerie",
        "produits": ["paniers légumes du marché", "lait local", "produits secs bio", "conserves"],
        "latitude": 48.836, "longitude": 2.238, "distance_km": 0.3,
        "livraison": True, "min_commande_eur": 10, "phone": "01 46 03 45 67",
        "horaires": "Lun-Sam 9h-20h", "description": "Circuit court, producteurs locaux sélectionnés",
    },
]


def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(PRODUCERS, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {OUTPUT_FILE}")
    print(f"     {len(PRODUCERS)} producteurs/artisans générés")
    types = {}
    for p in PRODUCERS:
        types[p["type"]] = types.get(p["type"], 0) + 1
    for t, n in sorted(types.items()):
        print(f"     - {t}: {n}")


if __name__ == "__main__":
    print("Génération du catalogue producteurs locaux...")
    generate()
