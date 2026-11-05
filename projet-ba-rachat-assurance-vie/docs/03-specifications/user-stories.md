# User stories et critères d'acceptation

Epic **EP-01 — Rachat partiel en ligne**. Les critères sont rédigés au format Gherkin (Étant donné / Quand / Alors) pour être directement testables. Le backlog importable dans Jira est disponible dans [`jira/backlog-import.csv`](../../jira/backlog-import.csv).

---

### US-01 — Consulter ma valeur de rachat · *Must* · 2 pts
**En tant que** client, **je veux** voir la valeur de rachat de mon contrat et le montant maximum que je peux retirer, **afin de** savoir ce qui est possible avant de commencer.

- **Étant donné** Claire, contrat CT-1001 valorisé 40 000 €, **quand** elle ouvre son contrat, **alors** elle voit une valeur de rachat de 40 000 € et un montant maximum de 38 500 €.
- **Étant donné** un contrat qui n'appartient pas au client connecté, **quand** il tente de l'ouvrir, **alors** l'accès est refusé.

### US-02 — Simuler un rachat partiel · *Must* · 5 pts
**En tant que** client, **je veux** simuler un rachat, **afin de** connaître la répartition, l'encours restant et la part de gains avant de m'engager.

- **Étant donné** Claire, **quand** elle simule 5 000 €, **alors** la répartition affichée est de 3 125 € sur le fonds en euros et 1 875 € sur l'UC Actions, la part de gains de 1 250 € et l'encours restant de 35 000 €.
- **Étant donné** un montant de 400 €, **quand** elle simule, **alors** le message « Le montant minimum d'un rachat partiel est de 500 € » s'affiche.
- **Étant donné** un montant de 39 000 €, **quand** elle simule, **alors** un message indique que le montant maximum possible est de 38 500 €.

### US-03 — Choisir les supports désinvestis · *Should* · 3 pts
**En tant que** client, **je veux** choisir sur quels supports je rachète, **afin de** préserver mes unités de compte si je le souhaite.

- **Étant donné** Claire, **quand** elle affecte 2 000 € au fonds en euros pour un rachat de 2 000 €, **alors** seul le fonds en euros est désinvesti.
- **Étant donné** une répartition dont la somme diffère du montant, **quand** elle valide, **alors** un message demande que la somme soit égale au montant.
- **Étant donné** 16 000 € demandés sur l'UC Actions valorisée 15 000 €, **quand** elle valide, **alors** la demande est bloquée.

### US-04 — Choisir l'IBAN de versement · *Must* · 3 pts
**En tant que** client, **je veux** recevoir les fonds sur le compte de mon choix, **afin de** les utiliser où j'en ai besoin.

- **Étant donné** l'IBAN vérifié pré-rempli, **quand** Claire valide, **alors** la demande peut être acceptée automatiquement.
- **Étant donné** un nouvel IBAN, **quand** elle valide, **alors** la demande passe EN_ATTENTE_PIECES avec le motif « RIB au nom du souscripteur à fournir ».

### US-05 — Valider ma demande · *Must* · 5 pts
**En tant que** client, **je veux** valider ma demande en ligne avec un code SMS, **afin d'**être payé rapidement et en sécurité.

- **Étant donné** un dossier simple et un code SMS valide, **quand** Claire valide 5 000 € le jeudi 05/11/2026, **alors** le statut est ACCEPTEE_AUTO, le paiement est prévu le 10/11/2026 et la valeur du contrat passe à 35 000 €.
- **Étant donné** l'absence de code SMS valide, **quand** elle valide, **alors** la demande est refusée et rien n'est enregistré.

### US-06 — Suivre ma demande · *Must* · 2 pts
**En tant que** client, **je veux** voir le statut de ma demande, **afin de** ne pas avoir à appeler le service client.

- **Étant donné** une demande enregistrée, **quand** Claire ouvre le suivi, **alors** elle voit le statut, le montant, la répartition et la date de paiement prévue.

### US-07 — Orienter automatiquement les dossiers sensibles · *Must* · 8 pts
**En tant qu'**analyste Conformité, **je veux** que les dossiers à risque ne soient jamais acceptés automatiquement, **afin de** respecter nos obligations LCB-FT et nos engagements envers les créanciers.

- **Étant donné** Karim, **quand** il demande 60 000 €, **alors** le statut est EN_CONTROLE_LCBFT et aucun support n'est désinvesti.
- **Étant donné** Emma, qui a déjà fait 2 rachats sur 12 mois, **quand** elle en demande un 3e, **alors** le statut est EN_CONTROLE_LCBFT.
- **Étant donné** Sophie, dont le contrat est nanti, **quand** elle fait une demande, **alors** le statut est ORIENTEE_CONSEILLER.
- **Étant donné** Lucas, dont le KYC date de janvier 2022, **quand** il fait une demande, **alors** le statut est EN_ATTENTE_PIECES avec un motif de mise à jour KYC.

### US-08 — File de travail des gestionnaires · *Must* · 5 pts
**En tant que** gestionnaire, **je veux** une file des dossiers non automatiques avec leur motif, triée par ancienneté, **afin de** traiter les plus anciens en premier.

- **Étant donné** des dossiers aux statuts EN_ATTENTE_PIECES, EN_CONTROLE_LCBFT ou ORIENTEE_CONSEILLER, **quand** j'ouvre la file, **alors** je vois chaque dossier avec son motif, du plus ancien au plus récent.

### US-09 — Indicateurs de pilotage · *Should* · 3 pts
**En tant que** directrice Épargne, **je veux** suivre le taux d'automatisation et les montants rachetés par mois, **afin de** mesurer l'atteinte des objectifs du projet.

- **Étant donné** les demandes du mois, **quand** j'ouvre le tableau de bord, **alors** je vois la répartition par statut en nombre et en pourcentage.

---

**Definition of Ready** : critères d'acceptation rédigés, règles référencées, données de test identifiées, maquette validée si écran.
**Definition of Done** : développée, tests automatisés au vert, recette fonctionnelle OK, documentation Confluence à jour, démontrée en revue de sprint.
