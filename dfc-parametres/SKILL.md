---
name: dfc-parametres
description: Parametres et seuils canoniques DFC (reward/risk, taille minimale, seuil de changement de regime, poids et temperature du modele). Source unique. A charger des qu'un calcul de regime, un seuil de decision ou un dimensionnement de position est en jeu.
---

# Parametres et seuils DFC

Source unique des seuils de decision et des parametres du modele de regime. Utilise toujours ces valeurs, n'en invente jamais d'autres. Revision uniquement sur calendrier methodologique, signee par le CEO, jamais apres un mauvais appel (playbook H3). Un seuil non defini est un seuil non controle.

## Seuils de decision (figes)

- Reward/risk minimal: 3:1. En dessous, le setup est NO-GO et n'est pas presente.
- Taille minimale de pertinence: 2% de la NAV. En dessous, ecarter le trade; ne jamais elargir le stop pour faire entrer une taille.
- Seuil de changement de regime: 15 points de probabilite. Une variation de 15 points ou plus sur la probabilite d'un regime, entre deux lectures d'une meme zone, declenche une revue anticipee hors calendrier.

## Modele de probabilisation (provisoire, NON calibre)

Forme: S_k = wG x G + wI x I + wL x L, puis P_k = exp(S_k / tau) / somme des exp(S_j / tau).
Valeurs de depart: wG = 1,0, wI = 1,0, wL = 1,0, tau = 1,0.
Ces valeurs sont provisoires et non calibrees: DFC demarre a plat et fait du forward-tuning, aucun historique n'est detenu au depart. Toute probabilite produite avec ces parametres est presentee explicitement comme "parametres provisoires, non calibres". Elles seront recalibrees par la boucle d'autocalibration (spec DFC-REG-001), sur calendrier, avec signature du CEO.

## Limites dures de session G0 (a fixer par le CEO)

Levier maximal, exposition brute maximale, exposition nette maximale, concentration maximale par position, drawdown stop: non encore fixes. Tant qu'ils ne le sont pas, ne pas ouvrir de session G0 comme si le budget de risque etait complet, et le signaler.

## Gouvernance

Toute valeur de ce document prime sur toute estimation. Toute revision de seuil ou de parametre est consignee au registre, datee et signee.
