# Deploiement du skill d'onboarding hors DCA (HDCA)

Le parcours hors DCA est distinct du DCA : un skill dedie, dfc-onboarding-hdca, pour que l'IRO ne confonde jamais les deux regimes. Il classe chaque dossier entrant (DCA ou hors DCA) et applique le bon skill.

## Ce qui est deja fait (moi)

- Skill dfc-onboarding-hdca redige (7 etapes, regime d'autonomie, 7 modeles H-T1 a H-T7, checklist).
- Charte IRO (DFC-ORG-003) mise a jour en v2.1 avec le regime hors DCA.
- Doc de modeles (DFC-ONB-HDCA-TPL-2026-001) enregistre dans le projet.

## Geste 1 - Pousser le skill sur GitHub (toi)

Copie le dossier dfc-onboarding-hdca a la racine du depot kinggis/dfc-skills (a cote de dfc-onboarding), puis :

    git add dfc-onboarding-hdca
    git commit -m "Ajout skill dfc-onboarding-hdca (procedure, modeles hors DCA)"
    git push

Le depot doit etre public le temps de l'import, comme pour les autres skills.

## Geste 2 - Me fournir les 2 PDF specifiques HDCA

Deux documents n'existaient pas dans la suite DCA et sont a produire :
- DFC_HDCA_Investment_Letter_FR.pdf (adaptation de la Shareholder Letter)
- DFC_HDCA_Investment_Agreement_FR.pdf (adaptation du Subscription Agreement)

Les 3 documents communs (Risk Disclosure, Subscription Form, Investor Acknowledgement) et la NAV Methodology sont deja dans le workspace : je les copie moi-meme dans le dossier hors DCA.

## Ensuite (moi)

Quand le skill est pousse et les 2 PDF disponibles dans le workspace :
1. J'importe et j'active dfc-onboarding-hdca sur l'IRO.
2. Je cree mailer/attachments/hdca/, j'y copie les 3 docs communs et j'y place les 2 PDF HDCA.
3. Je complete l'AGENTS.md de l'IRO : classification DCA / hors DCA, chemin absolu des pieces jointes hors DCA.
4. Je lance une validation en lecture seule (sans envoi) d'un H-T1 fictif, comme pour le DCA.

Tant qu'un document requis manque, l'IRO escalade au lieu d'envoyer (fail-closed), donc rien ne part de travers entre-temps.

## Point a confirmer, non bloquant

DFC_RIB sert aussi au hors DCA (meme compte). Verifie juste que le bloc contient bien le BIC/SWIFT et permet un virement en GBP, car l'email H-T3 affiche une ligne SWIFT.
