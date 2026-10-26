# Deploiement du kit d'onboarding IRO

Deux gestes a faire, le reste je m'en occupe.

## Geste 1 - Le RIB dans un secret Paperclip (toi, pas moi)

Sur l'agent IRO, onglet " Secrets & variables ", cree un secret :

- Nom : DFC_RIB
- Valeur : le bloc coordonnees bancaires, par exemple
    Titulaire : DualForce Capital Ltd
    IBAN : ...
    BIC : ...
    Banque : ...

Tu colles ta valeur toi-meme. Elle ne doit jamais apparaitre dans le chat, un depot ou un journal. Le modele T3 la lit depuis ce secret au moment de l'envoi.

Tant que DFC_RIB n'existe pas, l'IRO escalade au lieu d'envoyer l'email de versement (comportement voulu).

## Geste 2 - Pousser le kit sur GitHub

Copie le dossier dfc-onboarding a la racine du depot kinggis/dfc-skills (a cote des autres skills), puis :

    git add dfc-onboarding
    git commit -m "Ajout skill dfc-onboarding (procedure, modeles, pieces jointes)"
    git push

Passe le depot en public deux minutes si besoin, comme pour les autres skills.

## Ensuite (moi)

Quand c'est pousse, dis-le moi : j'importe dfc-onboarding par URL de sous-dossier, je l'active sur l'IRO, et je verifie qu'il se charge. L'IRO sera alors capable de derouler l'onboarding en autonomie, pack compris.

## Contenu du kit

- SKILL.md : la procedure qui fait foi, le regime d'autonomie, les 8 etapes, les 8 modeles d'emails, la checklist.
- assets/ : tes 9 documents DCA (Shareholder Letter, Information Memorandum, FAQs, Subscription Agreement, Risk Disclosure, Subscription Form, Investor Acknowledgement, Monthly Reporting Template, NAV Methodology).

A confirmer quand tu veux, non bloquant : montant et frequence de versement standard, et la source NAV validee.
