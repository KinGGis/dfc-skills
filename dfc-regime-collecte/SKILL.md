---
name: dfc-regime-collecte
description: Methode DFC de collecte macro et marche publique, production de lecture de regime et labellisation des issues (T+1/T+3, Mahalanobis, abstention). A charger pour produire une lecture de regime, tenir la maturite de la calibration, ou labelliser une periode passee. Le cadre est fixe, la collecte est autonome sous source-discipline.
---

# Collecte et labellisation de regime DFC

Ce skill fixe la methode par laquelle l'Analyste DFC produit, chaque mois et de facon autonome, une lecture de regime pour les cinq zones suivies, et labellise apres coup le regime qui a reellement prevalu. Le cadre et la methode sont ici, deterministes. La collecte de la donnee publique est ton travail. On ne veut pas un automate qui remplit des cases: on veut un analyste qui va chercher la donnee, la qualifie, juge les cas limites, et anticipe. L'attribution finale reste deterministe, pour la reproductibilite.

Se combine avec dfc-regime-analyst (grille et scoring), dfc-parametres (seuils et poids, source unique), source-discipline (collecte), dfc-document-production (restitution a la charte).

## 1. Ce que tu produis

Lecture de regime (mensuelle et a la demande): pour chaque zone, les scores G/I/L, les probabilites de regime, le regime dominant, le drapeau de changement, l'evidence et les sources. Artefact de type REGIME_READ.

Label d'issue (T+1 puis T+3): pour un couple zone/periode passe, le regime qui a reellement prevalu, ou l'abstention. C'est ce qui alimente l'autocalibration.

## 2. Zones

Cinq zones calibrees: US, Zone euro (EZ), Japon (JP), Chine (CN), Emergents hors Chine (EMxCN). Le Monde n'est pas une zone calibree: c'est un derive, moyenne ponderee par capitalisation boursiere des cinq zones. Ne jamais injecter le Monde comme observation de calibration: c'est un agregat.

## 3. Ce que tu collectes, sous source-discipline

Fondamentaux, pour scorer G, I, L. G: PIB reel et momentum, production industrielle, emploi, PMI, ventes de detail. I: la mesure privilegiee par la banque centrale de la zone (deflateur PCE sous-jacent US, HICP sous-jacent EZ, CPI sous-jacent JP, CPI CN). Le choix de la mesure n'est pas neutre. L: taux directeur et trajectoire, taux reel 2 ans, spreads IG et HY, bilan de banque centrale, change effectif, conditions financieres.

Marche, six classes d'actifs pour la labellisation: actions, souverains, spreads de credit, or, dollar, commodities.

Regles: hierarchie des sources et verification des chiffres pivots (source-discipline). Source primaire d'abord. Dater la donnee, distinguer preliminaire/revise/definitif. Jamais de chiffre invente: declarer la limite.

## 4. Produire la lecture de regime

1. Scorer G, I, L sur -2 a +2, avec evidence chiffree et sourcee (grille dans dfc-regime-analyst).
2. Lire poids et seuil dans dfc-parametres (source unique). Au demarrage, provisoires non calibres: wG = wI = wL = 1,0 et tau = 1,0. Toute probabilite produite ainsi est presentee comme parametres provisoires, non calibres.
3. Par regime k (R1..R4): S_k = wG x G + wI x I + wL x L selon la signature du regime, puis P_k = exp(S_k / tau) sur la somme des exp(S_j / tau). Les quatre P somment a 1.
4. Regime dominant = plus forte probabilite.
5. Drapeau de changement: vs la lecture precedente de la meme zone. Si la plus grande variation absolue de P atteint le seuil (15 points), lever le drapeau et signaler une revue anticipee hors calendrier.
6. Consigner au format REGIME_READ (scores, probabilites, dominant, drapeau, evidence, sources). Tant que l'ingestion Supabase n'est pas en ligne, deposer comme artefact dans ce format, ingerable telle quelle plus tard.

## 5. Labelliser l'issue, apres coup

Le regime n'a de valeur que s'il discrimine les rendements. La verite terrain se definit par ce que le marche a reellement paye, pas par une remesure des fondamentaux avec la meme grille (circulaire).

1. z-score de chaque classe d'actifs sur la periode, normalise par sa volatilite de long terme.
2. Distance de Mahalanobis aux quatre signatures de reference. Mahalanobis, pas euclidienne, car les classes sont correlees.
3. Attribuer au plus proche. R2 vs R3: direction des actions. R1 vs R4: direction des spreads.

Abstention, imperative: si la distance aux deux regimes les plus proches differe de moins de 15 pour cent, soit (d2 - d1)/d1 < 0,15, la periode est indeterminee et exclue de la calibration.

Deux statuts: provisoire a T+1 (rendements seuls, tableau de bord, n'alimente pas la calibration); confirme a T+3 seulement si le label de rendements et le controle fondamental definitif concordent. Discordance = indetermine. Seuls les confirmes alimentent la calibration.

## 6. Signatures de reference

Necessaires a la labellisation. Sans historique detenu, initialiser une version theorique (directions attendues de la grille R1-R4), puis raffiner par collecte publique. Covariance calculee sur les rendements publics collectes. Tout raffinement est propose, jamais applique sans signature du PM.

## 7. Ce que tu ne fais jamais

Jamais engager de capital ni modifier les parametres. Tu proposes, l'humain signe (G3, G4). Ne consommer qu'un artefact PASSED. Jamais d'allocation presentee comme actee: propose, en attente de signature. Jamais de seuil ou poids code en dur: tout vient de dfc-parametres. Jamais de donnee manquante comblee par un chiffre invente.

## 8. Cadence

Lecture: mensuelle, plus a la demande sur evenement macro majeur (la recalibration des parametres, elle, reste calendaire). Label provisoire: le mois suivant. Label confirme: trois mois apres. Maturite de la calibration: tenue a jour a chaque lecture.
