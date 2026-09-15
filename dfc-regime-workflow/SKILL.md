---
name: dfc-regime-workflow
description: Orchestrer le workflow complet du playbook DFC de bout en bout, en enchaînant les rôles analyste, trader et portfolio manager et en faisant respecter les points de contrôle G0 à G7. Utiliser quand l'utilisateur demande un cycle complet — « lance la session du jour », « déroule le playbook sur X », « fais tourner le process complet », « prépare le comité d'investissement » — ou quand plusieurs rôles doivent intervenir séquentiellement sur un même sujet. Pour un travail relevant d'un seul rôle, utiliser directement le skill de ce rôle.
---

# Orchestrateur du workflow DFC

Enchaîne les trois rôles et fait respecter les gates. Charge
`_shared/HANDOFF_SCHEMAS.md` avant de démarrer.

## Règles d'orchestration — non négociables

1. **Un rôle à la fois, explicitement annoncé.** Ouvrir chaque
   segment par `[RÔLE : ANALYSTE]`, `[RÔLE : TRADER]`,
   `[RÔLE : PM]`. Ne jamais mélanger deux rôles dans un même bloc de
   raisonnement — c'est précisément ce que le playbook interdit.
2. **Aucun saut de gate.** Un `REJECTED` renvoie en amont, jamais en
   aval.
3. **Aucun artefact `PENDING` ne déclenche d'action aval.**
4. **Signature humaine requise** aux gates G3 et G4. L'orchestrateur
   s'arrête et attend confirmation explicite. Il ne s'auto-autorise
   pas au motif que l'utilisateur a lancé le workflow.
5. **Traçabilité** : chaque gate franchi produit une ligne de registre
   horodatée. Un gate sans trace équivaut à un gate non franchi.

## Séquence

```
G0  PM       Ouverture de session, budget de risque
 │           ↳ si session_open = false : STOP
Ph1 ANALYSTE Collecte
Ph2 ANALYSTE Scoring G/I/L
Ph3 ANALYSTE Probabilisation R1-R4
Ph4 ANALYSTE Policy Impact Matrix
Ph5 ANALYSTE + TRADER  Cross-check marché
G1  PM       Validation du régime  ──── REJECTED → retour Ph2
Ph6 ANALYSTE Scénarios (tail risk obligatoire)
Ph7 PM       Allocation cible + stress tests
Ph8 ANALYSTE Fiches de stock-picking + ranking
G2  PM       Validation de thèse   ──── REJECTED → retour Ph8
Ph9 TRADER   Setups, niveaux, taille implicite
             ↳ si verdict NO-GO : la thèse ne passe pas en G3
G3  PM       DÉCISION  ★ signature humaine
G4  PM       MANDAT    ★ signature humaine
Ph10 TRADER  Exécution
G5  PM       Contrôle post-exécution
Ph11 ANALYSTE + TRADER  Monitoring → ALERT
G6  PM       Revue de position
G7  PM       Clôture + post-mortem
```

## Points d'arrêt obligatoires

L'orchestrateur **s'arrête et rend la main** dans ces cas :

| Condition | Comportement |
|---|---|
| `session_open = false` | Stop. Aucune analyse exploitable, aucune exécution. |
| Somme des probabilités ≠ 100 % | Stop. Retour phase 3. |
| Scénario tail risk absent | Stop. Retour phase 6. |
| Fiche sans invalidation ou sans argumentaire adverse | Rejet G2. |
| Setup `NO-GO` | La thèse n'atteint pas G3. Ne pas contourner. |
| Gates G3 ou G4 | Stop. Attente de signature humaine. |
| Dépassement de limite détecté | Stop. Escalade PM immédiate. |
| `ALERT` de sévérité `CRITICAL` | Interrompt le cycle en cours. |
| Données insuffisantes | Stop et le dire. Ne jamais fabriquer une probabilité. |

## Modes d'exécution

- **Session complète** — G0 → G2, produit le matériel de comité.
  S'arrête avant G3.
- **Cycle idée** — part d'une thèse existante validée, va de Ph9 à G4.
- **Revue** — Ph11 → G6, traite les alertes sur positions ouvertes.
- **Post-mortem** — G7 seul, sur position clôturée.

Demander lequel si ce n'est pas évident, plutôt que de dérouler le
cycle entier par défaut.

## Sortie

Pour chaque cycle :
1. Les artefacts JSON de chaque étape (schémas partagés)
2. Une synthèse de comité en prose : régime, convictions, décisions
   proposées, risques, conditions de revue
3. Le **registre du cycle** : gates franchis, horodatage, statut,
   overlays signés, dérogations, points d'arrêt rencontrés

## Anti-pattern principal

Le risque de l'orchestration automatique est le **franchissement
silencieux** : enchaîner les phases en produisant une apparence de
rigueur alors que les contrôles n'ont pas réellement mordu.

Contre-mesure : à chaque gate, énoncer explicitement le critère de
passage et la donnée qui le satisfait. Si le critère n'est pas
satisfait, s'arrêter — même si le reste du cycle est prêt et que
l'utilisateur attend une conclusion. Un workflow qui ne bloque jamais
n'est pas un workflow de contrôle : c'est une mise en scène.
