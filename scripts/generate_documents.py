"""
Génère les 6 documents PDF fictifs du corpus HomeButler AI.
Chaque PDF est structuré avec des sections titrées pour que le chunking récursif
batte le chunking à taille fixe - effet pédagogique voulu.
"""

import os
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "documents")


class HomePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 5, "HomeButler AI - Document fictif à usage pédagogique", align="C")
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.cell(0, 5, f"Page {self.page_no()}", align="C")

    def title_section(self, text: str, level: int = 1):
        sizes = {1: 14, 2: 11, 3: 9}
        self.set_font("Helvetica", "B", sizes.get(level, 10))
        self.ln(4)
        self.multi_cell(0, 7, text)
        self.set_font("Helvetica", "", 9)
        self.ln(1)

    def body(self, text: str):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, text)
        self.ln(2)


def generate_bail():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("CONTRAT DE BAIL D'HABITATION", 1)
    pdf.body(
        "Conclu entre les soussignes :\n"
        "BAILLEUR : Monsieur Jean-Pierre MARTIN, domicilie au 12 rue des Lilas, 75011 Paris.\n"
        "LOCATAIRE : Madame Camille DUPONT, 32 ans, cadre superieur, domiciliee a l'adresse "
        "du logement loue a compter de la prise d'effet du present contrat."
    )

    pdf.title_section("ARTICLE 1 - DESIGNATION DU LOGEMENT", 2)
    pdf.body(
        "Le bailleur donne en location a la locataire le logement ci-apres designe :\n"
        "- Adresse : 28 avenue des Chenes, 92100 Boulogne-Billancourt\n"
        "- Type : Appartement F3, situe au 3eme etage (avec ascenseur)\n"
        "- Surface habitable : 68 m2 (loi Carrez : 66,4 m2)\n"
        "- Composition : salon/sejour 22 m2, 2 chambres (12 et 11 m2), cuisine equipee, "
        "salle de bain, WC independants, cave n°7, place de parking n°12 en sous-sol.\n"
        "- DPE : Classe D (consommation energetique : 230 kWh/m2/an)\n"
        "- GES : Classe E"
    )

    pdf.title_section("ARTICLE 2 - DUREE DU BAIL", 2)
    pdf.body(
        "Le present bail est consenti pour une duree de 3 ans, prenant effet le 1er mars 2024 "
        "et se terminant le 28 fevrier 2027, sous reserve du respect du preavis legal.\n\n"
        "Renouvellement : Le bail se renouvelle par tacite reconduction pour des periodes "
        "successives d'un an, sauf conge donne par l'une des parties dans les formes et "
        "delais prevus par la loi n°89-462 du 6 juillet 1989."
    )

    pdf.title_section("ARTICLE 3 - LOYER ET CHARGES", 2)
    pdf.body(
        "Loyer mensuel : 1 250 EUR (mille deux cent cinquante euros), payable d'avance "
        "le 1er de chaque mois.\n\n"
        "Charges locatives : 120 EUR/mois de provision sur charges, avec regularisation "
        "annuelle sur justificatifs. Les charges comprennent :\n"
        "- Entretien des parties communes et des espaces verts\n"
        "- Eau froide collective\n"
        "- Frais d'ascenseur (contrat de maintenance)\n"
        "- Taxe d'enlevement des ordures menageres (TEOM)\n"
        "- Frais de gardiennage (a hauteur de 75% du cout total)"
    )

    pdf.title_section("ARTICLE 4 - DEPOT DE GARANTIE", 2)
    pdf.body(
        "Un depot de garantie d'un montant de 2 500 EUR (deux mois de loyer hors charges) "
        "est verse le jour de la signature du present bail.\n"
        "Il sera restitue dans un delai maximum de 2 mois apres la remise des cles, "
        "deduction faite des sommes dues par la locataire au titre d'eventuelles "
        "degradations constatees lors de l'etat des lieux de sortie."
    )

    pdf.title_section("ARTICLE 5 - OBLIGATIONS DU LOCATAIRE", 2)
    pdf.body(
        "La locataire s'engage a :\n"
        "1. User du logement en bon pere de famille et conformement a sa destination d'habitation\n"
        "2. Payer le loyer et les charges aux termes convenus\n"
        "3. Souscrire une assurance multirisques habitation avant l'entree dans les lieux "
        "et en justifier chaque annee\n"
        "4. Entretenir les menus reparations locatives (article 7c de la loi de 1989) :\n"
        "   - Entretien annuel de la chaudiere individuelle\n"
        "   - Debouchage des canalisations (en cas d'usage anormal)\n"
        "   - Remplacement des joints, robinets de radiateurs, mecanismes de chasse d'eau\n"
        "   - Entretien des volets et persiennes\n"
        "   - Remplacement des ampoules\n"
        "5. Ne pas transformer le logement sans accord ecrit du bailleur\n"
        "6. Permettre l'acces au logement pour les travaux urgents et necessaires"
    )

    pdf.title_section("ARTICLE 6 - OBLIGATIONS DU BAILLEUR", 2)
    pdf.body(
        "Le bailleur s'engage a :\n"
        "1. Delivrer un logement en bon etat d'usage et de reparations\n"
        "2. Assurer la jouissance paisible du logement\n"
        "3. Prendre en charge les grosses reparations (article 606 du Code civil) :\n"
        "   - Remplacement de la chaudiere en cas de vetuste\n"
        "   - Etancheite de la toiture\n"
        "   - Remise en etat des canalisations collectives\n"
        "4. Remettre quittance de loyer sur demande"
    )

    pdf.title_section("ARTICLE 7 - CONGE", 2)
    pdf.body(
        "La locataire peut donner conge a tout moment, avec un preavis de 3 mois, "
        "reduit a 1 mois dans les cas suivants :\n"
        "- Zone tendue (la commune de Boulogne-Billancourt est classee en zone tendue)\n"
        "- Mutation professionnelle\n"
        "- Perte d'emploi ou nouvel emploi consecutif a une perte d'emploi\n"
        "- Etat de sante justifiant un changement de domicile\n"
        "- Attribution d'un logement social\n\n"
        "Le conge est donne par lettre recommandee avec AR ou par acte d'huissier."
    )

    pdf.title_section("ARTICLE 8 - TRAVAUX ET AMELIORATIONS", 2)
    pdf.body(
        "Tous travaux de transformation du logement sont interdits sans accord prealable "
        "ecrit du bailleur. Les ameliorations apportees par la locataire ne donnent lieu "
        "a aucune indemnite ni a aucune reprise en fin de bail, sauf accord contraire expres.\n\n"
        "Le bailleur peut exiger la remise en etat des lieux lors du depart, aux frais "
        "de la locataire, si des transformations ont ete effectuees sans autorisation."
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "bail_location.pdf")
    pdf.output(path)
    print(f"  OK {path}")


def generate_reglement_copropriete():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("REGLEMENT DE COPROPRIETE", 1)
    pdf.body(
        "Residence Les Chenes - 28 avenue des Chenes, 92100 Boulogne-Billancourt\n"
        "Immeuble construit en 1987 - 24 lots - Syndic : Cabinet IMMO CONSEIL"
    )

    pdf.title_section("TITRE I - DESCRIPTION ET DESTINATION DE L'IMMEUBLE", 2)
    pdf.body(
        "L'immeuble comprend 24 appartements repartis sur 6 etages, 24 caves, "
        "24 emplacements de parking en sous-sol, et les parties communes suivantes :\n"
        "- Hall d'entree avec interphone et badge magnetique\n"
        "- Ascenseur (marque OTIS, capacite 8 personnes)\n"
        "- Escaliers A et B\n"
        "- Local poubelles en rez-de-chaussee\n"
        "- Espace vert commun (300 m2) avec systeme d'arrosage automatique\n"
        "- Local velo securise (rez-de-chaussee, acces badge)"
    )

    pdf.title_section("TITRE II - CHARGES ET REPARTITION", 2)
    pdf.body(
        "Les charges generales (entretien, gardiennage, assurance immeuble) sont "
        "reparties selon les tantièmes de chaque lot.\n\n"
        "Repartition par type de lot :\n"
        "- Studios (lots 1-6) : 32/1000emes chacun\n"
        "- F2 (lots 7-14) : 41/1000emes chacun\n"
        "- F3 (lots 15-20, dont lot 18 = appartement de Mme DUPONT) : 52/1000emes\n"
        "- F4 (lots 21-24) : 61/1000emes"
    )

    pdf.title_section("TITRE III - REGLES DE VIE EN COPROPRIETE", 2)

    pdf.title_section("Article 1 - Bruit et tranquillite", 3)
    pdf.body(
        "Il est interdit de troubler la tranquillite des autres residents par des bruits "
        "excessifs (musique, television, travaux) :\n"
        "- En semaine : de 22h00 a 8h00\n"
        "- Le week-end et jours feries : de 22h00 a 9h00\n"
        "- Travaux bruyants : uniquement en semaine de 9h00 a 12h00 et de 14h00 a 18h00\n\n"
        "Les instruments de musique doivent etre joues avec sourdine apres 20h00."
    )

    pdf.title_section("Article 2 - Animaux", 3)
    pdf.body(
        "Les animaux de compagnie sont autorises dans les conditions suivantes :\n"
        "- Maximum 2 animaux par appartement\n"
        "- Les chiens doivent etre tenus en laisse dans les parties communes\n"
        "- Les dejections doivent etre ramassees immediatement\n"
        "- Les animaux ne doivent pas errer dans les parties communes"
    )

    pdf.title_section("Article 3 - Poubelles et dechets", 3)
    pdf.body(
        "Les ordures menageres doivent etre deposees dans les conteneurs prevus a cet effet, "
        "situes dans le local poubelles en rez-de-chaussee.\n\n"
        "Tri selectif obligatoire :\n"
        "- Conteneur jaune : emballages plastique, carton, metal\n"
        "- Conteneur vert : verre\n"
        "- Conteneur gris : ordures menageres\n\n"
        "Il est strictement interdit de deposer des encombrants dans le local poubelles "
        "sans accord prealable du syndic. La dechetterie municipale est situee "
        "au 45 rue du Moulin (ouverte du lundi au samedi de 8h a 18h)."
    )

    pdf.title_section("Article 4 - Stationnement", 3)
    pdf.body(
        "Le stationnement est autorise uniquement sur les emplacements attribues. "
        "Il est formellement interdit de stationner dans les alees de circulation "
        "et devant les locaux poubelles.\n\n"
        "Chaque proprietaire/locataire dispose de l'emplacement correspondant a son lot. "
        "Les vehicules en infraction pourront etre mis en fourriere apres mise en demeure."
    )

    pdf.title_section("TITRE IV - ENTRETIEN ET TRAVAUX", 2)
    pdf.body(
        "Tout travaux affectant les parties communes ou les elements porteurs de l'immeuble "
        "(murs porteurs, planchers, facade) doit faire l'objet d'une autorisation de l'assemblee "
        "generale a la majorite de l'article 25 de la loi du 10 juillet 1965.\n\n"
        "Les travaux de renovation interieurs dans les parties privatives doivent etre notifies "
        "au syndic au moins 15 jours avant leur debut. Le syndic peut imposer des plages "
        "horaires pour limiter les nuisances."
    )

    path = os.path.join(OUTPUT_DIR, "reglement_copropriete.pdf")
    pdf.output(path)
    print(f"  OK {path}")


def generate_notice_chaudiere():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("NOTICE D'UTILISATION ET D'ENTRETIEN", 1)
    pdf.title_section("CHAUDIERE A CONDENSATION VIESSMANN VITODENS 100-W", 1)
    pdf.body("Modele : B1HF - Puissance : 26 kW - Gaz naturel")

    pdf.title_section("1. DESCRIPTION DE L'APPAREIL", 2)
    pdf.body(
        "Votre chaudiere Viessmann Vitodens 100-W est une chaudiere a condensation gaz "
        "a haut rendement (jusqu'a 109% PCI). Elle assure :\n"
        "- Le chauffage central de votre logement (radiateurs)\n"
        "- La production d'eau chaude sanitaire (en mode instantane)\n\n"
        "Composants principaux :\n"
        "- Echangeur inox a condensation\n"
        "- Bruleur modulant MatriX (20-100% de puissance)\n"
        "- Circulateur integre\n"
        "- Vase d'expansion pre-rempli 8 litres\n"
        "- Soupape de securite 3 bars\n"
        "- Interface de commande Vitotronic 100"
    )

    pdf.title_section("2. REGLAGES ET TEMPERATURES RECOMMANDES", 2)
    pdf.body(
        "TEMPERATURES DE CONFORT RECOMMANDEES :\n\n"
        "Mode jour (7h-22h) :\n"
        "- Temperature ambiante cible : 19-21 degres C (recommandation ADEME)\n"
        "- Temperature de depart chaudiere : 55-65 degres C\n\n"
        "Mode nuit / absence (22h-7h) :\n"
        "- Temperature ambiante cible : 16-17 degres C\n"
        "- Temperature de depart chaudiere : 40-45 degres C\n"
        "  (IMPORTANT : ne jamais descendre sous 15 degres C pour eviter le gel)\n\n"
        "Mode vacances (absence prolongee) :\n"
        "- Regler le thermostat de securite anti-gel a 12 degres C\n"
        "- Ne PAS eteindre completement la chaudiere en hiver\n\n"
        "EAU CHAUDE SANITAIRE :\n"
        "- Temperature de production : 60 degres C (minimum legal anti-legionelles)\n"
        "- Pour economiser l'energie, programmer le ballon si vous avez un cumulus"
    )

    pdf.title_section("3. PROGRAMMATION HORAIRE", 2)
    pdf.body(
        "L'interface Vitotronic 100 permet de programmer des plages de chauffage.\n\n"
        "Acces a la programmation :\n"
        "1. Appuyer sur le bouton MENU (icone maison)\n"
        "2. Naviguer avec les fleches jusqu'a 'Chauffage > Plages horaires'\n"
        "3. Selectionner le jour ou la plage (Lun-Ven, Sam-Dim, ou chaque jour)\n"
        "4. Definir jusqu'a 3 plages par jour (heure debut / heure fin)\n"
        "5. Valider avec OK\n\n"
        "Exemple de programmation optimale :\n"
        "- 6h30-9h00 : mode confort (21 degres C)\n"
        "- 9h00-17h00 : mode reduit (16 degres C) si absence\n"
        "- 17h00-22h30 : mode confort (21 degres C)\n"
        "- 22h30-6h30 : mode nuit (16 degres C)"
    )

    pdf.title_section("4. ENTRETIEN ANNUEL OBLIGATOIRE", 2)
    pdf.body(
        "ATTENTION : L'entretien annuel de la chaudiere est OBLIGATOIRE (decret du 9 juin 2009). "
        "Il doit etre realise par un professionnel qualifie RGE.\n\n"
        "Operations effectuees lors de la revision annuelle :\n"
        "1. Nettoyage du bruleur et de l'echangeur\n"
        "2. Controle de la combustion (CO2, CO, rendement)\n"
        "3. Verification de l'etancheite du circuit gaz\n"
        "4. Controle de la pression du circuit hydraulique (doit etre entre 1 et 2 bars a froid)\n"
        "5. Purgeavec des radiateurs si necessaire\n"
        "6. Verification du vase d'expansion\n"
        "7. Mise a jour du carnet d'entretien\n\n"
        "Periode recommandee : septembre-octobre (avant la saison de chauffe)"
    )

    pdf.title_section("5. CODES D'ERREUR ET DEPANNAGE", 2)
    pdf.body(
        "VOYANT ROUGE FIXE - Blocage de la chaudiere :\n"
        "- F0 : Surchauffe (temperature > 110 degres C) - verifier la pression du circuit\n"
        "- F1 : Defaut ionisation - nettoyer l'electrode ou appeler technicien\n"
        "- F4 : Pression insuffisante - regonfler le circuit (voir section 6)\n"
        "- F9 : Defaut ventilateur - appeler le service apres-vente\n\n"
        "VOYANT ORANGE CLIGNOTANT - Avertissement :\n"
        "- A1 : Maintenance due (plus d'un an depuis la derniere revision)\n"
        "- A3 : Temperature exterieure trop basse (risque de gel)\n\n"
        "PROCEDURE DE RESET apres un blocage :\n"
        "1. Attendre 3 minutes\n"
        "2. Appuyer sur le bouton RESET (triangle orange) pendant 3 secondes\n"
        "3. Si le blocage se repete plus de 3 fois, appeler un technicien"
    )

    pdf.title_section("6. PROCEDURE DE REMPRESSURISATION DU CIRCUIT", 2)
    pdf.body(
        "Si la pression du manometre est inferieure a 1 bar (zone rouge) :\n\n"
        "1. Localiser le robinet de remplissage (tuyau flexible sous la chaudiere)\n"
        "2. Placer un recipient sous le purgeur automatique\n"
        "3. Ouvrir lentement le robinet de remplissage\n"
        "4. Surveiller le manometre : s'arreter entre 1,5 et 2 bars\n"
        "5. Fermer le robinet de remplissage\n"
        "6. Si la pression rechute frequemment : contacter un plombier-chauffagiste\n"
        "   (peut indiquer une fuite ou un vase d'expansion defaillant)\n\n"
        "IMPORTANT : Ne jamais laisser la pression depasser 3 bars "
        "(la soupape de securite se declencherait)."
    )

    path = os.path.join(OUTPUT_DIR, "notice_chaudiere.pdf")
    pdf.output(path)
    print(f"  OK {path}")


def generate_notice_vmc():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("NOTICE D'ENTRETIEN - VMC DOUBLE FLUX", 1)
    pdf.title_section("ZEHNDER COMFOAIR Q 350 TR", 1)
    pdf.body("Installation : Appartement F3 - 68 m2")

    pdf.title_section("1. PRESENTATION ET FONCTIONNEMENT", 2)
    pdf.body(
        "La VMC double flux renouvelle l'air de votre logement en recyclant la chaleur "
        "de l'air extrait pour prechauffer l'air insuffle. Rendement de recuperation : "
        "jusqu'a 93%.\n\n"
        "Flux d'air :\n"
        "- INSUFFLATION (air neuf) : depuis l'exterieur -> echangeur -> chambres et sejour\n"
        "- EXTRACTION (air vicie) : cuisine, salle de bain, WC -> echangeur -> exterieur\n\n"
        "L'echangeur recupere jusqu'a 93% de la chaleur de l'air extrait."
    )

    pdf.title_section("2. REGLAGES DES DEBITS D'AIR", 2)
    pdf.body(
        "Trois modes de fonctionnement :\n\n"
        "MODE 0 - Arret (deconseille sauf absence prolongee en ete) :\n"
        "Aucun renouvellement d'air. Risque de condensation et moisissures.\n\n"
        "MODE 1 - Vitesse reduite (absence, nuit) :\n"
        "- Debit total : 100 m3/h\n"
        "- Cuisine : 30 m3/h / Salle de bain : 25 m3/h / WC : 15 m3/h\n"
        "- Chambres : 15 m3/h chacune\n\n"
        "MODE 2 - Vitesse normale (presence) :\n"
        "- Debit total : 175 m3/h\n"
        "- Recommande en permanence de jour\n\n"
        "MODE 3 - Boost cuisine (pendant et apres la cuisson) :\n"
        "- Debit total : 350 m3/h\n"
        "- Activation : bouton boost sur la telecommande ou manuellement\n"
        "- Duree automatique : 30 minutes puis retour mode 2"
    )

    pdf.title_section("3. ENTRETIEN DES FILTRES - OPERATIONS PAR L'OCCUPANT", 2)
    pdf.body(
        "FILTRE G4 (bouche d'insufflation) - CHAQUE 3 MOIS :\n"
        "1. Eteindre la VMC (bouton ON/OFF)\n"
        "2. Ouvrir le caisson VMC (trappe dans le placard technique)\n"
        "3. Extraire le filtre G4 (filtre blanc, 350x250 mm)\n"
        "4. Nettoyer a l'aspirateur ou rincer a l'eau tiede\n"
        "5. Laisser secher completement avant reinstallation\n"
        "6. Reinstaller et fermer le caisson\n\n"
        "FILTRE F7 (haute filtration, filtration des PM2.5) - TOUS LES 6 MOIS :\n"
        "Ce filtre ne se nettoie pas - il doit etre remplace.\n"
        "Reference : Zehnder ComfoFond-L Q 350 F7\n"
        "Prix indicatif : 25-35 EUR la paire (disponible en ligne)\n\n"
        "NETTOYAGE DE L'ECHANGEUR - ANNUEL (technicien recommande) :\n"
        "Verifier l'absence de depots sur les plaques de l'echangeur enthalpique."
    )

    pdf.title_section("4. SIGNALISATION ET ALARMES", 2)
    pdf.body(
        "LED VERTE : fonctionnement normal\n"
        "LED ORANGE : entretien des filtres necessaire (delai < 30 jours)\n"
        "LED ROUGE : filtre colmate - remplacement urgent\n"
        "BIPER : anomalie - consulter l'afficheur pour le code erreur\n\n"
        "Codes erreur courants :\n"
        "E01 : Sonde temperature exterieure defaillante\n"
        "E03 : Debit insuffisant (filtre colmate ou grille obtruee)\n"
        "E07 : Moteur ventilateur hors plage - appeler technicien"
    )

    path = os.path.join(OUTPUT_DIR, "notice_vmc.pdf")
    pdf.output(path)
    print(f"  OK {path}")


def generate_notice_lave_linge():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("NOTICE D'UTILISATION - LAVE-LINGE", 1)
    pdf.title_section("BOSCH SERIE 6 WAU28P90FF", 1)
    pdf.body("Capacite : 9 kg - Essorage max : 1400 tr/min - Classe energetique : A")

    pdf.title_section("1. PROGRAMMES ET TEMPERATURES", 2)
    pdf.body(
        "COTON (programmes 1-4) :\n"
        "- Coton 90 degres C : linge tres sale, blanc. Duree : 3h15\n"
        "- Coton 60 degres C : linge de couleur sale. Duree : 2h45\n"
        "- Coton 40 degres C : linge peu sale. Duree : 2h10\n"
        "- Coton Eco 40-60 : programme economique, duree : 3h55 mais -50% energie\n\n"
        "SYNTHETIQUES (programmes 5-7) :\n"
        "- Synthetiques 40 degres C : chemises, polos. Duree : 1h30\n"
        "- Synthetiques 30 degres C : vetements delicats. Duree : 1h05\n\n"
        "PROGRAMMES SPECIAUX :\n"
        "- Laine / Delicats 30 degres C : tricots, pulls\n"
        "- Sport : tenues de sport, microfibres\n"
        "- Rinçage + Essorage\n"
        "- Vidange seule\n"
        "- Rapide 15 min (linge peu charge, peu sale)"
    )

    pdf.title_section("2. PRODUITS LESSIVIELS RECOMMANDES", 2)
    pdf.body(
        "- Lessive poudre ou liquide : maximum 100 ml par lavage en bac principal\n"
        "- Assouplissant : bac 'fleur' (maximum 80 ml - ne pas depasser le repere MAX)\n"
        "- Produit anti-calcaire : 1 fois par mois dans le bac principal\n\n"
        "ATTENTION : Ne pas utiliser de savon de Marseille en copeaux "
        "(peut obstruer le filtre de vidange). Eviter le surdosage qui favorise les moisissures."
    )

    pdf.title_section("3. ENTRETIEN ET PREVENTION DES PANNES", 2)
    pdf.body(
        "NETTOYAGE DU FILTRE DE VIDANGE - MENSUEL :\n"
        "1. Placer un chiffon absorbant sous la trappe en bas a droite du lave-linge\n"
        "2. Ouvrir la trappe\n"
        "3. Debrancher le bouchon de vidange d'urgence (tuyau noir) et vider l'eau\n"
        "4. Devisser le filtre (dans le sens anti-horaire)\n"
        "5. Nettoyer le filtre sous l'eau, retirer les corps etrangers (pieces, fibres)\n"
        "6. Revisser le filtre et fermer la trappe\n\n"
        "NETTOYAGE DU BAC A LESSIVE - MENSUEL :\n"
        "Retirer le bac (tirer vers soi jusqu'au bout), rincer a l'eau chaude.\n\n"
        "PROGRAMME TAMBOUR PROPRE - TOUS LES 30 CYCLES :\n"
        "Sans linge, sans lessive, a 60 degres C. La machine vous le signale automatiquement.\n\n"
        "DETARTRAGE - TOUS LES 6 MOIS (eau calcaire) :\n"
        "Utiliser un detartrant pour lave-linge (ex: Calgon) selon les instructions du produit."
    )

    pdf.title_section("4. CODES D'ERREUR ET SOLUTIONS", 2)
    pdf.body(
        "E17 / F17 : Probleme d'alimentation en eau\n"
        "-> Verifier que le robinet d'arrivee d'eau est ouvert\n"
        "-> Verifier que le tuyau d'alimentation n'est pas coudé\n\n"
        "E18 / F18 : Probleme de vidange\n"
        "-> Verifier que le filtre de vidange n'est pas obstrue\n"
        "-> Verifier que le tuyau de vidange n'est pas plie\n\n"
        "E23 : Fuite detectee par le systeme AquaStop\n"
        "-> Eteindre la machine et couper l'arrivee d'eau\n"
        "-> Appeler un technicien - ne pas redemarrer\n\n"
        "Bruit anormal (grince, vibre excessivement) :\n"
        "-> Verifier que la machine est parfaitement horizontale (regler les pieds)\n"
        "-> Verifier l'absence de corps etranger dans le tambour\n"
        "-> Reduire la charge si le programme est trop charge"
    )

    path = os.path.join(OUTPUT_DIR, "notice_lave_linge.pdf")
    pdf.output(path)
    print(f"  OK {path}")


def generate_dpe():
    pdf = HomePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.title_section("DIAGNOSTIC DE PERFORMANCE ENERGETIQUE (DPE)", 1)
    pdf.body(
        "Bien diagnostique : 28 avenue des Chenes, Appart 3eme etage, 92100 Boulogne-Billancourt\n"
        "Surface habitable : 68 m2\n"
        "Diagnostiqueur : Cabinet ENERGETIQUE CONSEIL - N° ADEME : 0592-DIAG-2024\n"
        "Date du diagnostic : 15 janvier 2024\n"
        "Validite : 10 ans (jusqu'au 15 janvier 2034)"
    )

    pdf.title_section("1. ETIQUETTE ENERGETIQUE", 2)
    pdf.body(
        "CLASSE ENERGETIQUE : D\n"
        "Consommation : 230 kWh/m2/an (seuil classe D : 180-250 kWh/m2/an)\n"
        "Consommation totale logement : 15 640 kWh/an\n"
        "Cout energetique annuel estime : 1 300-1 760 EUR/an\n\n"
        "ETIQUETTE CLIMAT (GES) : E\n"
        "Emissions : 52 kg CO2eq/m2/an"
    )

    pdf.title_section("2. DESCRIPTION DES SYSTEMES ENERGETIQUES", 2)
    pdf.body(
        "CHAUFFAGE :\n"
        "- Systeme : Chaudiere gaz individuelle a condensation (Viessmann Vitodens 100-W, 26 kW)\n"
        "- Annee installation : 2019\n"
        "- Rendement : 97% PCI\n"
        "- Emetteurs : radiateurs acier (7 radiateurs, double panneau)\n\n"
        "EAU CHAUDE SANITAIRE :\n"
        "- Production par la chaudiere (fonction combi instantane)\n\n"
        "VENTILATION :\n"
        "- VMC double flux (Zehnder ComfoAir Q 350) - Rendement 93%\n\n"
        "ISOLATION :\n"
        "- Murs : isolation interieure 8 cm laine de verre (annee 1987)\n"
        "- Toiture : non applicable (appartement intermediaire)\n"
        "- Planchers bas : non applicable\n"
        "- Fenetres : double vitrage 4/16/4 (annee 2010)"
    )

    pdf.title_section("3. RECOMMANDATIONS D'AMELIORATION", 2)
    pdf.body(
        "Pour passer de la classe D a la classe C (< 180 kWh/m2/an) :\n\n"
        "TRAVAUX PRIORITAIRES (gain estime : 35-40%) :\n"
        "1. Remplacement des fenetres par triple vitrage (4/16/4/16/4)\n"
        "   Gain estime : -15% sur la facture de chauffage\n"
        "   Cout : 4 000 - 6 000 EUR (aide MaPrimeRenov possible)\n\n"
        "2. Isolation des ponts thermiques (menuiseries, coffres de volets)\n"
        "   Gain estime : -10%\n"
        "   Cout : 1 500 - 2 500 EUR\n\n"
        "OPTIMISATION DES USAGES (sans travaux) :\n"
        "1. Regler le thermostat a 19 degres C le jour (obligation legale), 16 degres C la nuit\n"
        "   Gain estime : -15% sur la facture de chauffage\n"
        "2. Purger les radiateurs chaque annee avant la saison de chauffe\n"
        "3. Installer des robinets thermostatiques sur les radiateurs\n"
        "   Cout : 200-400 EUR / Gain : -10%\n"
        "4. Ne pas obstruer les bouches de ventilation\n\n"
        "AIDES FINANCIERES DISPONIBLES (2024) :\n"
        "- MaPrimeRenov : selon revenus, jusqu'a 70% du montant des travaux\n"
        "- Eco-pret a taux zero : jusqu'a 50 000 EUR sans interet\n"
        "- CEE (Certificats d'Economie d'Energie) : selon les travaux\n"
        "- TVA reduite a 5,5% pour les travaux de renovation energetique"
    )

    pdf.title_section("4. ESTIMATION DE LA CONSOMMATION PAR USAGE", 2)
    pdf.body(
        "Repartition de la consommation annuelle (15 640 kWh/an) :\n"
        "- Chauffage : 9 800 kWh (63%)\n"
        "- Eau chaude sanitaire : 3 200 kWh (20%)\n"
        "- Auxiliaires (VMC, circulateur) : 640 kWh (4%)\n"
        "- Eclairage et prises (hors DPE) : 2 000 kWh (13%) - indicatif\n\n"
        "Note : ces valeurs sont calculees en conditions standard "
        "(methode 3CL-DPE 2021, arrete du 31 mars 2021). "
        "La consommation reelle peut varier selon les habitudes de vie."
    )

    path = os.path.join(OUTPUT_DIR, "dpe.pdf")
    pdf.output(path)
    print(f"  OK {path}")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Generation des documents PDF...")
    generate_bail()
    generate_reglement_copropriete()
    generate_notice_chaudiere()
    generate_notice_vmc()
    generate_notice_lave_linge()
    generate_dpe()
    print(f"\n6 documents generes dans {OUTPUT_DIR}/")
