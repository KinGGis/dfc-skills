---
name: dfc-onboarding
description: Procedure complete d'onboarding d'un investisseur au programme DCA de DualForce Capital, de la pre-souscription a la sortie de lock-up. A charger pour toute tache touchant l'integration ou le suivi d'un investisseur DCA (envoi du pack, documents legaux, coordonnees de versement, confirmation de versement, reporting mensuel, support, rappels de conversion, lock-up). Contient les etapes, le regime d'autonomie de chaque action, les modeles d'emails approuves et les pieces jointes a utiliser.
---

# Onboarding DCA - procedure et modeles approuves (DFC-ONB-DCA-2026-001)

Agent responsable : IRO (Jarvis IR). Ce skill est la procedure qui fait foi et le jeu de modeles approuves. Tu ne t'en ecartes pas. En cas de conflit entre ton jugement et cette procedure, tu signales l'ecart au CIO avant d'agir.

## Regime d'autonomie

Tu executes seul une action d'onboarding uniquement si les quatre conditions sont reunies simultanement (voir charte IRO, DFC-ORG-003) :
1. L'action correspond exactement a une etape ci-dessous.
2. L'email part d'un modele approuve de ce skill, sans redaction libre vers l'exterieur.
3. Toute donnee variable vient d'une source interne validee : le RIB depuis le secret DFC_RIB et jamais d'un email entrant ; les chiffres (NAV, fractions) depuis la source validee, avec auto-controle du calcul.
4. Aucun ecart, aucune exception, aucune ambiguite.

Si une seule condition manque, tu n'envoies pas : tu escalades au CEO.

Chaque envoi autonome est journalise (destinataire, objet, etape, horodatage) et porte au digest de supervision adresse au CEO.

Identite et signature toujours via mailer/send_mail.py (identite de mailer/identity.json). Avant tout envoi, mode de validation sans --send pour verifier identite et signature ; toute divergence bloque l'envoi et remonte.

## Le RIB

Le RIB de versement n'est jamais en dur dans ce skill. Il est lu au moment de l'envoi depuis le secret Paperclip DFC_RIB. Tu ne l'inscris jamais dans un journal, un commentaire ou un fichier. Si DFC_RIB est absent ou vide, tu n'envoies pas le modele T3 : tu escalades.

## Parametres a confirmer avant premier envoi

- DFC_RIB : secret contenant le bloc coordonnees bancaires (titulaire, IBAN, BIC, banque).
- Parametres de versement de l'investisseur : montant et frequence (jour du mois).
- Source NAV validee et jour d'arrete (voir piece jointe NAV Methodology).

## Pieces jointes disponibles (workspace de l'agent)

Les documents a joindre ne sont pas dans ce skill (un skill ne porte que du texte). Ils vivent dans le workspace de l'agent, dossier mailer/attachments/onboarding/. Tu les joins depuis ce chemin au moment de l'envoi. Si un document requis est absent de ce dossier, tu n'envoies pas : tu escalades.

- Etape 1 : DFC_DCA_Shareholder_Letter_FR.pdf, DFC_DCA_Information_Memorandum_FR.pdf, DFC_DCA_FAQs_FR.pdf
- Etape 2 : DFC_DCA_Subscription_Agreement_FR.pdf, DFC_DCA_Risk_Disclosure_FR.pdf, DFC_DCA_Subscription_Form_FR.pdf, DFC_DCA_Investor_Acknowledgement_FR.pdf
- Reference : DFC_DCA_Monthly_Reporting_Template_FR.pdf, DFC_DCA_NAV_Methodology_FR.pdf

## Variables

{{investisseur}} nom · {{date}} date du jour · {{mois}} mois concerne · {{libelle}} libelle DCA - MM/AA · {{montant}} montant devise explicite · {{frequence}} frequence et jour · {{nav}} NAV par part · {{fractions}} fractions acquises X,XXXX · {{fractions_cumul}} total cumule · {{valeur_portefeuille}} valeur · {{rendement}} rendement estime %

## Les 8 etapes

### Etape 1 - Pre-souscription  [AUTONOME]
Envoyer le pack standard en pieces jointes, demander confirmation de reception, repondre aux questions couvertes par la FAQ. Modele T1. PJ : Shareholder Letter, Information Memorandum, FAQs.
Ensuite : la validation " investisseur qualifie " revient au CEO. Tu prepares le dossier et tu soumets le feu vert, tu ne passes pas a l'etape 2 sans lui.

### Etape 2 - Documentation legale  [AUTONOME pour l'envoi]
Apres feu vert du CEO, envoyer les documents a signer dans l'ordre, retour signe a admin@. Modele T2. PJ : Subscription Agreement, Risk Disclosure, Subscription Form, Investor Acknowledgement.
Receptionner et archiver les documents signes [AUTONOME]. La contre-signature DFC releve du CEO [ESCALADE].

### Etape 3 - Details bancaires  [AUTONOME]
Envoyer l'email de bienvenue avec les coordonnees de versement, RIB lu depuis DFC_RIB. Insister sur le libelle {{libelle}}. Modele T3.

### Etape 4 - Premier versement  [AUTONOME si chiffres valides]
Rapprocher le versement recu (montant et libelle), calculer les fractions (versement / NAV par part), mettre a jour le suivi, confirmer. Modele T4. Tout ecart de montant ou de libelle, ou NAV non validee : escalade.

### Etape 5 - Reporting mensuel  [AUTONOME si chiffres valides]
Au dernier jour ouvre du mois, envoyer le point mensuel ; rapport detaille a la charte en PJ (via dfc-document-production). Modele T5.

### Etape 6 - Suivi et support  [AUTONOME]
Repondre sous 24 h aux questions couvertes par les reponses standard. Modele T6. Toute question hors liste : escalade.

### Etape 7 - Conversion  [rappels AUTONOMES, releve ESCALADE]
Au 30 juin 2027, rappel (T7). Au 1er novembre 2027, pre-notification et affectation des residus au Pool (T7b). Le releve de conversion du 31 decembre 2027 releve du CEO (signature) : escalade.

### Etape 8 - Lock-up et sortie  [notification AUTONOME, options ESCALADE]
Notifier la fin de lock-up (T8). Les options de sortie (conserver, ceder, redistribuer) relevent du CEO : escalade.

## Modeles d'emails approuves

### T1 - Pack de pre-souscription
Objet : Programme DCA DualForce Capital - documents de presentation

Bonjour {{investisseur}},

Nous vous remercions de votre interet pour le programme DCA de DualForce Capital.

Vous trouverez ci-joint la Shareholder Letter, l'Information Memorandum et notre FAQ. Ces documents presentent l'opportunite, son fonctionnement et son cadre.

Nous restons a votre disposition pour toute question preliminaire. Pouvez-vous nous confirmer la bonne reception de ces documents ?

Bien a vous,

### T2 - Documents de souscription
Objet : Documents de souscription - Programme DCA

Bonjour {{investisseur}},

Suite a la validation de votre profil, voici les documents de souscription a lire et a signer, dans l'ordre suivant :
1. Subscription Agreement
2. Risk Disclosure
3. Subscription Form
4. Investor Acknowledgement

Comptez environ 45 a 60 minutes de lecture. Merci de nous retourner l'ensemble signe par retour, a l'adresse admin@dualforcecapital.com.

Bien a vous,

### T3 - Bienvenue et coordonnees de versement
Objet : Bienvenue au programme DCA - coordonnees de versement

Bonjour {{investisseur}},

Bienvenue au programme DCA. Vos documents signes nous sont bien parvenus.

Pour votre premier versement, voici les coordonnees :

{{DFC_RIB}}

- Libelle de virement obligatoire : {{libelle}}
- Montant : {{montant}}
- Frequence : {{frequence}}

Le libelle {{libelle}} est imperatif : c'est lui qui rattache chaque versement a votre dossier et au bon mois. Merci de le reporter exactement.

Bien a vous,

### T4 - Confirmation de versement
Objet : Confirmation de votre versement - {{libelle}}

Bonjour {{investisseur}},

Nous confirmons la reception de votre versement de {{montant}} au titre de {{mois}}.
- NAV par part retenue : {{nav}}
- Fractions acquises : {{fractions}}
- Total de fractions cumulees : {{fractions_cumul}}

Bien a vous,

### T5 - Rapport mensuel
Objet : Rapport mensuel DCA - {{mois}}

Bonjour {{investisseur}},

Voici votre point mensuel au titre de {{mois}} :
- NAV par part : {{nav}}
- Fractions acquises au cours du mois : {{fractions}}
- Total de fractions cumulees : {{fractions_cumul}}
- Valeur de votre portefeuille : {{valeur_portefeuille}}
- Rendement estime : {{rendement}}

Le rapport detaille a la charte est joint.

Bien a vous,

### T6 - Reponses de support standard
- Puis-je augmenter ou diminuer mon versement ? Oui, en nous le notifiant 5 jours a l'avance.
- Puis-je sauter un mois ? Contactez-nous, nous regardons votre situation.
- Ou est mon argent ? Votre rapport mensuel et votre suivi detaillent vos fractions et la valeur de votre portefeuille.
- Quand serai-je eligible au dividende ? Apres la conversion du 31 decembre 2027.

### T7 - Rappel de conversion
Objet : Conversion de vos fractions dans 6 mois

Bonjour {{investisseur}},

Nous vous rappelons que la conversion de vos fractions en parts entieres interviendra le 31 decembre 2027. Nous reviendrons vers vous avant cette echeance avec le detail.

Bien a vous,

### T7b - Pre-notification de conversion
Objet : Conversion du 31 decembre 2027 - pre-notification

Bonjour {{investisseur}},

En vue de la conversion du 31 decembre 2027, nous vous informons que le residu de fractions (au-dela de la partie entiere) sera affecte au Pool, conformement au programme. Le releve definitif vous sera adresse apres conversion.

Bien a vous,

### T8 - Fin de lock-up
Objet : Fin de la periode de lock-up

Bonjour {{investisseur}},

Votre periode de lock-up de 3 ans arrive a son terme. Nous reviendrons vers vous avec les options disponibles.

Bien a vous,

## Ce qui remonte toujours au CEO
Validation investisseur qualifie ; contre-signature des documents ; releve de conversion ; options de sortie ; tout ecart de montant, libelle ou chiffre ; toute question hors modele ; reclamation ou litige ; sujet juridique ou fiscal ; tout mouvement d'argent.

## Checklist par investisseur
- [ ] Etape 1 : pack envoye, reception confirmee
- [ ] Feu vert investisseur qualifie (CEO)
- [ ] Etape 2 : documents envoyes, signes recus et archives
- [ ] Etape 3 : coordonnees de versement envoyees
- [ ] Etape 4 : premier versement rapproche, fractions calculees, confirmation envoyee
- [ ] Etape 5 : reporting mensuel en place
- [ ] Etape 7 : rappels de conversion
- [ ] Etape 8 : notification de fin de lock-up
