# DFC — Suite de skills « Market Regime Playbook »

Implémentation opérationnelle du playbook v2.0. Quatre skills couvrant
les trois rôles et l'orchestration.

## Contenu

```
dfc-skills/
├── README.md                          ← ce fichier
├── _shared/
│   └── HANDOFF_SCHEMAS.md             ← contrat de données entre rôles
├── dfc-regime-analyst/SKILL.md        ← phases 1-8, gates G1-G2
├── dfc-execution-trader/SKILL.md      ← phases 9-11, exécution
├── dfc-portfolio-manager/SKILL.md     ← gates G0-G7, décision
└── dfc-regime-workflow/SKILL.md       ← orchestrateur bout en bout
```

## Installation

Copier chaque dossier dans le répertoire des skills utilisateur :

```bash
cp -r dfc-regime-analyst dfc-execution-trader \
      dfc-portfolio-manager dfc-regime-workflow _shared \
      /mnt/skills/user/
```

`_shared/` doit être accessible depuis les trois skills de rôle : ils y
référencent les schémas de handoff.

## Usage

**Un seul rôle** — invoquer directement le skill concerné.
« Analyse le régime européen » → `dfc-regime-analyst`.
« Où entrer sur RACE et avec quel stop » → `dfc-execution-trader`.
« Quelle taille et faut-il y aller » → `dfc-portfolio-manager`.

**Cycle complet** — `dfc-regime-workflow`, qui enchaîne les rôles et
fait respecter les gates.

## Principe de conception

Les trois skills sont **volontairement bridés** dans leur autorité :

| Rôle | Peut | Ne peut pas |
|---|---|---|
| Analyste | Lire, scorer, probabiliser, proposer des thèses | Dimensionner, allouer, exécuter, s'auto-accorder un overlay |
| Trader | Timing, niveaux, taille implicite, exécution dans le mandat | Décider du sens ou de l'opportunité, sortir des bornes |
| PM | Instruire et rédiger toute décision, contrôler le risque | Signer à la place de l'humain, engager du capital réel seul |

Cette asymétrie est le cœur du dispositif. Un skill qui peut tout faire
reproduit exactement le problème que le playbook v2.0 corrige :
l'absence de séparation entre l'acte d'analyser, l'acte d'exécuter et
l'acte de décider.

## Frontière agent / humain

Le skill PM prépare des décisions **prêtes à signer** mais ne signe
pas. Les gates G3 (décision) et G4 (mandat) exigent une confirmation
humaine explicite, par ordre, à chaque fois — une autorisation générale
en début de session ne vaut pas signature.

Raison : le playbook (§12.2) signale déjà que la fonction Risk est
portée par celui qui engage le capital, faute de séparation des tâches
à l'échelle actuelle du fonds. Donner à un agent l'autonomie
d'engagement supprimerait le dernier point de contrôle humain — ce qui
serait difficilement défendable en due diligence investisseur.

## Usage recommandé : le contradicteur

Le contrôle compensatoire le plus utile en mode mono-opérateur est
l'**argumentaire adverse obligatoire** (playbook §19). C'est le cas
d'usage où un agent apporte le plus de valeur immédiate : faire tenir
le rôle d'analyste contradicteur sur les thèses à forte conviction,
avant décision — un rôle qu'une équipe réduite ne peut structurellement
pas tenir contre elle-même.

## Points ouverts à trancher

1. **Seuils chiffrés.** Les skills référencent « le seuil DFC » de
   reward/risk, la taille minimale de pertinence et le seuil de
   changement de régime sans les chiffrer. À figer dans une annexe
   avant tout usage agentique — un seuil non défini est un seuil non
   contrôlé.
2. **Calibration de τ et des poids wG/wI/wL.** Le playbook impose une
   calibration historique. Elle n'existe pas encore : sans elle, la
   probabilisation reste une pondération d'opinion présentée comme un
   modèle.
3. **Support du registre.** Le dispositif repose entièrement sur la
   traçabilité. Décider du support (Notion, base, fichiers versionnés)
   avant de dérouler le workflow en production.
