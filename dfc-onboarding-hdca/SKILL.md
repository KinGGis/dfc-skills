---
name: dfc-onboarding-hdca
description: Procedure complete d'onboarding d'un investisseur HORS programme DCA (versement unique, en livre sterling, conversion immediate en parts entieres, activation immediate, lock-up 3 ans a compter de l'activation). A charger pour toute tache touchant un investisseur hors DCA : versement unique, investissement en GBP, parts entieres, "Investment - [Nom]", activation immediate, reporting trimestriel. Distincte du skill dfc-onboarding (programme DCA mensuel en euro). Contient les etapes, le regime d'autonomie de chaque action, les modeles d'emails approuves et les pieces jointes a utiliser.
---

# Onboarding hors DCA - procedure et modeles approuves (DFC-ONB-HDCA-2026-001)

Agent responsable : IRO (Jarvis IR). Ce skill est la procedure qui fait foi et le jeu de modeles approuves pour l'investissement HORS DCA. Tu ne t'en ecartes pas. En cas de conflit entre ton jugement et cette procedure, tu signales l'ecart au CIO avant d'agir.

## Choix du regime : DCA ou hors DCA

Avant toute action, tu identifies le regime du dossier.
- Hors DCA (ce skill) : versement unique, en livre sterling (GBP), conversion immediate en parts entieres, activation immediate, libelle de virement "Investment - [Nom]", lock-up a compter de la date d'activation, reporting trimestriel.
- DCA (skill dfc-onboarding) : versements mensuels en euro, fractions, conversion au 31 decembre 2027, libelle "DCA - MM/AA".
Si le regime est ambigu ou si un dossier melange les deux, tu n'agis pas : tu escalades au CEO.

## Caracteristiques du produit hors DCA

- Versement : unique. Montant egal a N x prix de l'action (NAV par action), minimum 1 action.
- Devise : livre sterling (GBP).
- Parts : entieres uniquement, arrondi inferieur. Aucune fraction, aucun Pool, aucun residu fractionnaire.
- Conversion : immediate, sans attente du 31 decembre 2027.
- Frais : 3 % de frais de gestion, 30 % de commission de performance, 80 GBP de frais administratifs a la charge de l'investisseur, ajoutes au versement.
- Lock-up : 3 ans stricts a compter de la date d'activation.
- Libelle de virement obligatoire : "Investment - [Nom de l'investisseur]".
- Reporting : trimestriel (31 mars, 30 juin, 30 septembre, 31 decembre).

## Regime d'autonomie

Tu executes seul une action d'onboarding uniquement si les quatre conditions sont reunies simultanement (voir charte IRO, DFC-ORG-003) :
1. L'action correspond exactement a une etape ci-dessous.
2. L'email part d'un modele approuve de ce skill, sans redaction libre vers l'exterieur.
3. Toute donnee variable vient d'une source interne validee : le RIB depuis le secret DFC_RIB et jamais d'un email entrant ; le prix de l'action (NAV par action) et les montants depuis la source validee, avec auto-controle du calcul.
4. Aucun ecart, aucune exception, aucune ambiguite.

Si une seule condition manque, tu n'envoies pas : tu escalades au CEO.

Chaque envoi autonome est journalise (destinataire, objet, etape, horodatage) et porte au digest de supervision adresse au CEO.

Identite et signature toujours via mailer/send_mail.py (identite de mailer/identity.json). Avant tout envoi, mode de validation sans --send pour verifier identite et signature ; toute divergence bloque l'envoi et remonte.

## Le RIB

Le RIB de versement n'est jamais en dur dans ce skill. Il est lu au moment de l'envoi depuis le secret Paperclip DFC_RIB (meme compte que le programme DCA). Le bloc doit contenir le beneficiaire, l'IBAN, le BIC/SWIFT et l'adresse. Tu ne l'inscris jamais dans un journal, un commentaire ou un fichier. Si DFC_RIB est absent, vide ou incomplet (BIC/SWIFT manquant), tu n'envoies pas le modele H-T3 : tu escalades.

## Parametres a confirmer avant premier envoi

- DFC_RIB : secret contenant le bloc coordonnees bancaires (titulaire, IBAN, BIC/SWIFT, adresse). Le bloc doit permettre un virement en GBP.
- Prix de l'action (NAV par action) a la date de souscription : depuis la source NAV validee (voir NAV Methodology). Sans NAV validee, les etapes de calcul et d'activation escaladent.
- Montant d'investissement vise par l'investisseur (en GBP).

## Pieces jointes disponibles (workspace de l'agent)

Les documents a joindre ne sont pas dans ce skill (un skill ne porte que du texte). Ils vivent dans le workspace de l'agent, dossier mailer/attachments/hdca/. Tu les joins depuis ce chemin au moment de l'envoi. Si un document requis est absent de ce dossier, tu n'envoies pas : tu escalades.

- Etape 1 : DFC_HDCA_Investment_Letter_FR.pdf
- Etape 2 : DFC_HDCA_Investment_Agreement_FR.pdf, DFC_DCA_Risk_Disclosure_FR.pdf, DFC_DCA_Subscription_Form_FR.pdf, DFC_DCA_Investor_Acknowledgement_FR.pdf
- Reference : DFC_DCA_NAV_Methodology_FR.pdf

Les trois documents prefixes DFC_DCA_ (Risk Disclosure, Subscription Form, Investor Acknowledgement) sont communs aux deux regimes et reutilises tels quels.

## Variables

{{investisseur}} nom · {{date}} date du jour · {{prix_action}} prix de l'action GBP a la souscription · {{montant}} montant investi GBP · {{nb_actions}} nombre d'actions entieres acquises · {{frais_admin}} frais administratifs (80 GBP) · {{total}} total a verser (montant + 80 GBP) · {{montant_recu}} montant reellement recu · {{valeur_portefeuille}} valeur du portefeuille · {{date_activation}} date d'activation · {{date_fin_lockup}} date d'activation + 3 ans · {{nav}} NAV par action · {{trimestre}} trimestre concerne · {{perf_trim}} performance du trimestre % · {{perf_ytd}} performance depuis le debut de l'annee %

## Calcul (auto-controle obligatoire)

- Nombre d'actions : partie entiere de (montant investi / prix de l'action). nb_actions = floor({{montant}} / {{prix_action}}).
- Le montant investi doit etre un multiple exact du prix de l'action. Si le residu (montant - nb_actions x prix_action) n'est pas nul, c'est un ecart : tu escalades, tu n'actives pas.
- Total a verser : montant investi + 80 GBP de frais administratifs.
- A la reception, le montant recu doit egaler le total a verser. Tout ecart de montant ou de libelle : escalade.

## Les 7 etapes

### Etape 1 - Pre-souscription  [AUTONOME pour l'envoi]
Envoyer l'Investment Letter adaptee hors DCA, clarifier le principe (un versement unique = N actions au prix du jour), demander une confirmation d'interet et le montant vise. Modele H-T1. PJ : Investment Letter. Joindre dans le corps la fiche de calcul (montant / prix de l'action = N actions) si le montant vise et le prix sont connus et valides.
Ensuite : la validation du profil et de l'investisseur qualifie revient au CEO. Tu prepares le dossier et tu soumets le feu vert, tu ne passes pas a l'etape 2 sans lui.

### Etape 2 - Documentation legale  [AUTONOME pour l'envoi]
Apres feu vert du CEO, envoyer les documents a signer dans l'ordre, retour signe a admin@. Modele H-T2. PJ : Investment Agreement, Risk Disclosure, Subscription Form, Investor Acknowledgement.
Receptionner et archiver les documents signes [AUTONOME]. La contre-signature DFC releve du CEO [ESCALADE].

### Etape 3 - Calcul et versement bancaire  [AUTONOME si prix de l'action valide]
Apres reception des documents signes, envoyer l'email de calcul et de coordonnees bancaires : tableau de calcul (prix de l'action, montant investi, nombre d'actions, frais 80 GBP, total a verser) et coordonnees de versement, RIB lu depuis DFC_RIB. Insister sur le libelle "Investment - {{investisseur}}" et sur le total incluant les 80 GBP. Modele H-T3. Prix de l'action non valide ou residu fractionnaire non nul : escalade.

### Etape 4 - Reception et activation  [AUTONOME si chiffres valides et concordants]
Rapprocher le virement recu, valider que le montant recu egale le total a verser (montant + 80 GBP) et que le libelle est correct, puis envoyer la confirmation. Modele H-T4. Le releve d'activation officiel et l'inscription des parts au registre relevent du CEO [ESCALADE]. Tout ecart de montant, de libelle ou de residu fractionnaire : escalade.

### Etape 5 - Reporting trimestriel  [AUTONOME si chiffres valides]
A la fin de chaque trimestre civil (31 mars, 30 juin, 30 septembre, 31 decembre), envoyer le rapport trimestriel ; rapport detaille a la charte en PJ (via dfc-document-production). Modele H-T5.

### Etape 6 - Suivi et support  [AUTONOME]
Repondre sous 24 h aux questions couvertes par les reponses standard. Modele H-T6. Toute question hors liste : escalade.

### Etape 7 - Lock-up et sortie  [notification AUTONOME, options ESCALADE]
En annee 3, notifier la fin de lock-up a la date d'activation + 3 ans (H-T7). Les options de sortie (conserver, ceder, demander une redistribution) relevent du CEO : escalade.

## Modeles d'emails approuves

### H-T1 - Pre-souscription hors DCA
Objet : Investissement DualForce Capital - presentation et structure

Bonjour {{investisseur}},

Nous vous remercions de votre interet pour un investissement chez DualForce Capital.

Vous trouverez ci-joint notre Investment Letter, qui presente la structure de l'offre, les montants et les frais. Le principe est simple : un versement unique correspond a un nombre entier d'actions au prix du jour (NAV par action). Par exemple, un montant egal a deux fois le prix de l'action correspond a deux actions.

Pourriez-vous nous confirmer votre interet et le montant que vous envisagez d'investir ? Nous reviendrons vers vous avec le detail du calcul.

Bien a vous,

### H-T2 - Documents de souscription hors DCA
Objet : Documents de souscription - Investissement DualForce Capital

Bonjour {{investisseur}},

Suite a la validation de votre profil, voici les documents de souscription a lire et a signer, dans l'ordre suivant :
1. Investment Agreement
2. Risk Disclosure
3. Subscription Form
4. Investor Acknowledgement

Merci de nous retourner l'ensemble signe par retour, a l'adresse admin@dualforcecapital.com. Des reception, nous vous confirmerons que votre dossier est complet.

Bien a vous,

### H-T3 - Calcul et coordonnees de versement
Objet : Investissement DFC : details et montant a verser

Bonjour {{investisseur}},

Votre dossier est actif. Voici le detail de votre investissement :

- Prix de l'action a la date de souscription : {{prix_action}}
- Montant investi : {{montant}}
- Nombre d'actions acquises : {{nb_actions}} actions entieres
- Frais administratifs : {{frais_admin}}
- Total a verser : {{total}}

Coordonnees de versement :

{{DFC_RIB}}

- Libelle de virement obligatoire : Investment - {{investisseur}}
- Montant total a verser : {{total}}

Le libelle "Investment - {{investisseur}}" est imperatif pour le rapprochement bancaire, et le montant vire doit inclure les 80 GBP de frais administratifs. Merci de nous confirmer l'emission du virement.

Bien a vous,

### H-T4 - Confirmation et activation
Objet : Confirmation et activation de votre investissement DFC

Bonjour {{investisseur}},

Nous confirmons la bonne reception de votre versement. Votre investissement est actif.

- Montant recu : {{montant_recu}}
- Montant investi : {{montant}}
- Prix de l'action retenu : {{prix_action}}
- Nombre de parts acquises : {{nb_actions}} actions entieres
- Frais administratifs : {{frais_admin}}
- Valeur totale du portefeuille : {{valeur_portefeuille}}
- Statut : actif immediatement
- Lock-up : 3 ans, jusqu'au {{date_fin_lockup}}

Votre prochaine communication sera le rapport trimestriel.

Bien a vous,

### H-T5 - Rapport trimestriel
Objet : Rapport trimestriel DFC - {{trimestre}}

Bonjour {{investisseur}},

Voici votre point trimestriel au titre de {{trimestre}} :
- NAV par action : {{nav}}
- Valeur de votre portefeuille : {{valeur_portefeuille}}
- Performance du trimestre : {{perf_trim}}
- Performance depuis le debut de l'annee : {{perf_ytd}}

Le rapport detaille a la charte est joint.

Bien a vous,

### H-T6 - Reponses de support standard
- Puis-je ajouter du capital ? Oui, par un investissement supplementaire, qui suit un nouveau processus.
- Puis-je vendre avant 3 ans ? Non, le lock-up de 3 ans est strict.
- Ou est mon argent ? Votre rapport trimestriel detaille la valeur de votre portefeuille.
- Quand aurai-je de la liquidite ? A l'issue du lock-up, le {{date_fin_lockup}}, pas avant.

### H-T7 - Fin de lock-up
Objet : Fin de la periode de lock-up

Bonjour {{investisseur}},

Votre periode de lock-up de 3 ans arrive a son terme le {{date_fin_lockup}}. Nous reviendrons vers vous avec les options disponibles (conserver, ceder ou demander une redistribution).

Bien a vous,

## Ce qui remonte toujours au CEO
Validation du profil et investisseur qualifie ; contre-signature des documents ; releve d'activation et inscription des parts au registre ; options de sortie ; tout ecart de montant, de libelle, de residu fractionnaire ou de chiffre ; prix de l'action (NAV par action) non valide ; toute question hors modele ; reclamation ou litige ; sujet juridique ou fiscal ; tout mouvement d'argent.

## Checklist par investisseur
- [ ] Etape 1 : Investment Letter envoyee, interet et montant confirmes
- [ ] Feu vert profil / investisseur qualifie (CEO)
- [ ] Etape 2 : documents envoyes, signes recus et archives
- [ ] Etape 3 : email de calcul et de coordonnees de versement envoye
- [ ] Etape 4 : virement recu et valide (montant + 80 GBP, libelle), confirmation envoyee, releve d'activation (CEO)
- [ ] Etape 5 : reporting trimestriel en place
- [ ] Etape 7 : notification de fin de lock-up
