---
name: dfc-document-production
description: Produire tout livrable DFC destine a etre lu (rapport de regime, note, arrete de NAV, briefing, comite) strictement a la charte DualForce Capital, via le service de rendu DFC. A charger des qu'un role DFC doit RESTITUER un livrable formate. Ne jamais fabriquer un theme generique; le rendu passe toujours par le service.
---

# Production documentaire DFC

Ce skill garantit qu'un livrable DFC sort toujours a la charte de la maison, jamais avec un theme generique. Tu ne fabriques jamais un habillage improvise (couleurs teal, barres rouges, wordmark sans logo). Tu ne dessines pas la charte toi-meme: tu produis un pack de contenu et tu appelles le service de rendu DFC, qui renvoie le PDF a la charte.

Regle absolue: si le service est injoignable, tu livres le pack de contenu structure et tu le signales; tu n'improvises jamais une charte.

## 1. Charte (valeurs canoniques, pour reference)

Couleurs: anthracite #1C1C1C (fond sombre), gris fonce #3A3A3A (bandeaux), or antique mat #C5A253 (accent), creme #EFE4C8 (bande KPI, encadres, totaux), blanc casse #F2F2F0 (panneaux, lignes alternees), gris clair #D9D9D6 (filets), gris moyen #6E6E6E (sous-titres), vert #4A7C59 (positifs), rouge #A63D3D (negatifs). Police Calibri. A4 pour les documents. Jamais de tiret cadratin, jamais de couleur hors palette. Le service applique cette charte; tu n'as pas a la reproduire.

## 2. Le pack de contenu (ce que TU produis)

Format DFC-CONTENT-PACK v1 (spec DFC-PACK-001), en YAML ou JSON:
doc_type, reference, title, subtitle, classification, cover_meta (lignes cle/valeur), kpis (exactement trois, au niveau du pack ou d'une section), sections (heading, subhead, body avec **gras** pour les chiffres cles, retain optionnel, table optionnel), charts optionnels, sources.
Conventions de tableau: suffixe (pos) = vert, (neg) = rouge; mot-cle total en fin de ligne = ligne de total; align par colonne left ou num. Devise explicite, virgule decimale, chiffres pivots sources.

## 3. Appeler le service de rendu

Le moteur de charte est un service HTTP sur le VPS. Son URL et son jeton sont fournis par les secrets de l'agent: DFC_RENDER_URL et DFC_RENDER_TOKEN. Tu envoies le pack, tu recois le PDF.

Ecris ton pack dans un fichier (par exemple pack.yaml), puis:

    curl -sS -X POST "$DFC_RENDER_URL" \
      -H "Authorization: Bearer $DFC_RENDER_TOKEN" \
      -H "Content-Type: application/x-yaml" \
      --data-binary @pack.yaml \
      -o sortie.pdf -w "%{http_code}"

Un code 200 et un fichier sortie.pdf non vide = rendu reussi. Livre alors le fichier PDF directement (joins-le a ta reponse ou a la tache), pas seulement son chemin.

Si le code n'est pas 200, ou si DFC_RENDER_URL / DFC_RENDER_TOKEN sont absents, ou si le PDF est vide: n'improvise pas. Rends le pack de contenu YAML que tu as ecrit, colle le code et le message d'erreur exacts, et signale que le service de rendu est injoignable.

## 4. Structure obligatoire par type

Rapport de regime ou comite (playbook section 11), dans cet ordre: Executive Summary, Dashboard macro (G/I/L par zone), Probabilites R1/R2/R3/R4, Policy overlay, Scenarios, Cross-asset, Allocation (proposee, sous reserve de signature PM), Stock-picking, AT/liquidite, Risk, Monitoring, Registre de decision. Chaque bloc porte le role producteur. Aucune allocation actee: proposee, en attente de signature.
Arrete de NAV: cover, synthese (trois KPI), composition poche par poche, methodologie, souscriptions, change, confidentialite.

## 5. Reference et confidentialite

Reference: DFC-[type]-[geographie]-[annee]-[sequence]. Bandeau de confidentialite systematique. La diffusion externe reste sous gate de communication: un document interne ne se diffuse pas sans validation humaine explicite.

## 6. Discipline

Un livrable DFC se reconnait au premier coup d'oeil: anthracite et or, monogramme, structure institutionnelle. La forme fait partie de la credibilite du fonds. Si tu ne peux pas produire a la charte via le service, tu livres le fond (le pack) et tu le dis; tu ne livres jamais un faux habillage.
