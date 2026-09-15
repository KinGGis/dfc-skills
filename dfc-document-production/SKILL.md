---
name: dfc-document-production
description: Produire tout livrable DFC destiné à être lu (rapport de régime, note, arrêté de NAV, briefing macro, comité, deck) strictement à la charte graphique DualForce Capital. À charger dès qu'un rôle DFC doit RESTITUER un livrable formaté, pas seulement le raisonner. Déclenche sur « produis le rapport », « mets à la charte », « génère le PDF/Word/PPT », « le briefing », « le comité ». Ne jamais fabriquer un thème générique: le rendu passe toujours par le moteur de charte fourni ici.
---

# Production documentaire DFC

Ce skill garantit qu'un livrable DFC sort toujours à la charte de la maison, et jamais avec un thème générique inventé par le modèle. Il fournit la charte, le moteur de rendu et la structure obligatoire de chaque type de document.

Règle absolue: tu ne rends jamais un document DFC avec un habillage improvisé (couleurs teal, barres rouges, wordmark sans logo, etc.). Tout rendu passe par le moteur de ce skill. Si le moteur ne peut pas tourner, tu livres le contenu structuré (pack de contenu) et tu le dis, tu n'improvises pas une charte.

## 1. Charte DFC (valeurs canoniques)

Couleurs: anthracite #1C1C1C (fond sombre), gris foncé #3A3A3A (bandeaux de section), or antique mat #C5A253 (accent signature), crème #EFE4C8 (bande KPI, encadrés, lignes de total), blanc cassé #F2F2F0 (panneaux, lignes alternées), gris clair #D9D9D6 (filets), gris moyen #6E6E6E (sous-titres), vert #4A7C59 (chiffres positifs), rouge #A63D3D (chiffres négatifs).

Police: Calibri (repli Carlito puis Arial). Titres en capitales, gras. Format 16:9 pour les decks, A4 pour les documents.

Logo: version blanche (assets/dfc-logo-white.png) sur fonds sombres, version noire (assets/dfc-logo-dark.png) sur fonds clairs, monogramme seul (assets/dfc-emblem-dark.png) pour les en-têtes de pages internes.

Interdits: pas de tiret cadratin dans les textes rédigés; pas de couleur hors palette; pas de logo en simple texte.

## 2. Grammaire de mise en page

Cover: fond anthracite plein, barre or en haut à gauche, logo blanc centré, titre capitales, sous-titre or, tableau clé/valeur à liseré or, mention de confidentialité en pied. Pages internes: en-tête = monogramme à gauche + nom du document à droite, AU-DESSUS d'une double bande or/noir; pied = filet gris, « DualForce Capital Ltd | Confidentiel | référence » à gauche, numéro de page à droite. Bandeau de section: bloc sombre, liseré or à gauche, titre capitales blanches, sous-titre or. Bande KPI: fond crème, trois chiffres centrés. Encadré « à retenir »: fond crème, liseré or. Tableaux: en-tête sombre texte blanc, lignes alternées blanc cassé, totaux crème gras, chiffres positifs verts, négatifs rouges.

## 3. Moteur de rendu (fichiers de ce skill)

- PDF (rendu le plus fidèle, moteur phare): `render.py` (Chromium/Playwright) rend une cover pleine page puis les pages internes avec en-tête et pied courants, et fusionne (pdfunite). Le contenu et les métadonnées sont injectés par `build.py` dans les gabarits `templates/`.
- Word éditable: `docx_build.js` (docx-js).
- PowerPoint éditable: `pptx_build.js` (pptxgenjs).
- Graphiques à la palette: `dfc_charts.py` (matplotlib) — barres, courbe, donut.
- Feuille de style commune: `dfc-brand.css`. Logos: `assets/`.

Dépendances: Chromium (Playwright), Node avec docx-js et pptxgenjs, python avec Pillow et matplotlib, poppler (pdftoppm, pdfunite), LibreOffice (soffice) pour convertir docx/pptx en PDF de contrôle. Vérifier leur présence avant de rendre; installer ce qui manque quand le réseau le permet. Si une dépendance manque et ne s'installe pas, livrer le pack de contenu et le signaler, sans improviser d'habillage.

Contrôle qualité obligatoire: après tout rendu, convertir en images et les regarder (cover plus une page interne au minimum). Vérifier logo, palette, en-tête au-dessus de la bande, tableaux, chiffres verts/rouges, absence de débordement. Ne remettre un document qu'après cette vérification visuelle.

## 4. Du contenu au document: le pack de contenu

Le contenu arrive au format DFC-CONTENT-PACK v1 (voir spec DFC-PACK-001): type de document, référence, titre, sous-titre, classification, métadonnées de couverture, exactement trois KPI, sections (titre, sous-titre, corps, encadré optionnel, tableau optionnel avec suffixes pos/neg/total), graphiques optionnels, sources. Remplir les gabarits avec ce pack, puis rendre. Ne jamais mettre en forme à la main hors moteur.

## 5. Structure obligatoire par type de document

Rapport de régime / comité (playbook §11), dans cet ordre: Executive Summary (régime dominant, changements, convictions, risques), Dashboard macro (G/I/L par zone), Probabilités (R1/R2/R3/R4 et variations), Policy/news overlay, Scénarios (central, upside, downside, tail risk), Cross-asset, Allocation (proposée, sous réserve de signature PM humaine), Stock-picking (top longs, top shorts, watchlist), AT/liquidité (setups), Risk (concentrations, corrélations, stress, liquidité), Monitoring (indicateurs et conditions de révision), Registre de décision. Chaque bloc porte le rôle producteur. Aucune allocation ni décision présentée comme actée: « proposé, en attente de signature ».

Arrêté de NAV: cover + synthèse (3 KPI: prix de l'action, variation, NAV nette) + composition poche par poche + méthodologie + traitement des souscriptions + taux de change + confidentialité. Devise explicite, virgule décimale.

## 6. Référence et confidentialité

Référence document: `DFC-[type]-[géographie/programme]-[année]-[séquence]-[suffixe]`. Bandeau de confidentialité systématique (INTERNE DFC, revue CEO, diffusion externe interdite pour les documents internes). La diffusion externe reste sous gate de communication: un document interne ne se diffuse pas sans validation humaine explicite.

## 7. Discipline

Un livrable DFC se reconnaît au premier coup d'oeil: anthracite et or, monogramme, structure institutionnelle. Si le rendu ne ressemble pas à la base documentaire DFC, il est faux, quel que soit le fond. La forme fait partie de la crédibilité du fonds.
