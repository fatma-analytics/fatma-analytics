# Cahier de recette

Date de référence : **05/11/2026**. Les 19 cas ci-dessous sont **automatisés** dans [`tests/test_recette.py`](../../tests/test_recette.py). Les cas API sont aussi rejouables dans Postman ([`postman/`](../../postman/)).

## Cas de recette fonctionnelle

| ID | US | Règle | Persona | Étapes | Résultat attendu | Statut |
|---|---|---|---|---|---|---|
| CT-01 | US-02 | RG-05, RG-09 | Claire | Simuler 5 000 € au prorata | Euros 3 125 € / UC 1 875 € ; gains 1 250 € ; encours 35 000 € | ✅ OK |
| CT-02 | US-05 | RG-10 | Claire | Demander 5 000 € avec code SMS | 201, ACCEPTEE_AUTO, paiement 10/11/2026, limite 05/01/2027 | ✅ OK |
| CT-03 | US-01 | RG-10 | Claire | Après CT-02, consulter le contrat | Valeur de rachat 35 000 € | ✅ OK |
| CT-04 | US-03 | RG-05 | Claire | 2 000 € uniquement sur le fonds en euros | Une seule ligne : EURO-01 2 000 € | ✅ OK |
| CT-05 | US-06 | — | Claire | Consulter une demande créée | 200, statut ACCEPTEE_AUTO | ✅ OK |
| CT-06 | US-02 | RG-03 | Claire | Demander 400 € | 422, RG-03 | ✅ OK |
| CT-07 | US-02 | RG-04 | Claire | Demander 39 000 € | 422, RG-04, message « 38500.00 » | ✅ OK |
| CT-08 | US-02 | RG-04 | Claire | Demander 38 500 € (limite) | 201, encours restant 1 500 € | ✅ OK |
| CT-09 | US-03 | RG-05 | Claire | 3 000 € demandés, 2 000 € répartis | 422, RG-05 | ✅ OK |
| CT-10 | US-03 | RG-05 | Claire | 16 000 € sur l'UC Actions (15 000 €) | 422, RG-05 | ✅ OK |
| CT-11 | US-07 | RG-07 | Karim | Demander 60 000 € | EN_CONTROLE_LCBFT, pas de date de paiement | ✅ OK |
| CT-12 | US-07 | RG-07 | Emma | 3e rachat sur 12 mois (1 000 €) | EN_CONTROLE_LCBFT | ✅ OK |
| CT-13 | US-07 | RG-06 | Sophie | Demander 2 000 € | ORIENTEE_CONSEILLER | ✅ OK |
| CT-14 | US-07 | RG-02 | Lucas | Demander 2 000 € | EN_ATTENTE_PIECES, motif KYC | ✅ OK |
| CT-15 | US-04 | RG-08 | Claire | 2 000 € vers un nouvel IBAN | EN_ATTENTE_PIECES, motif IBAN | ✅ OK |
| CT-16 | US-07 | RG-10 | Karim | Après CT-11, consulter le contrat | Valeur inchangée : 120 000 € | ✅ OK |
| CT-17 | US-05 | RG-11 | Claire | Demander sans code SMS | 401, RG-11 | ✅ OK |
| CT-18 | US-05 | RG-01 | Claire | Demander sur le contrat de Karim | 403 | ✅ OK |
| CT-19 | US-01 | RG-01 | Claire | Consulter CT-9999 | 404 | ✅ OK |

## Contrôles de données SQL

À exécuter après chaque campagne : [`sql/controles_recette.sql`](../../sql/controles_recette.sql). **Résultat attendu : 0 ligne pour chaque contrôle.**

| ID | Règle | Ce qu'on vérifie | Résultat |
|---|---|---|---|
| CTRL-01 | RG-07 | Aucun rachat ≥ 50 000 € accepté automatiquement | 0 ✅ |
| CTRL-02 | RG-06 | Aucun contrat nanti accepté automatiquement | 0 ✅ |
| CTRL-03 | RG-05 | Somme des lignes = montant du rachat | 0 ✅ |
| CTRL-04 | RG-08 | Aucun paiement automatique vers un IBAN non vérifié | 0 ✅ |
| CTRL-05 | RG-04 | Aucun contrat sous 1 500 € après rachat | 0 ✅ |
| CTRL-06 | RG-10 | Paiement prévu au plus tard à J + 2 mois | 0 ✅ |
| CTRL-07 | RG-02 | Aucune acceptation automatique avec un KYC périmé | 0 ✅ |

## Scénarios UAT (utilisateurs métier)

| ID | Utilisateur | Scénario de bout en bout | Critère de validation |
|---|---|---|---|
| UAT-01 | Client interne | Simuler, ajuster le montant, valider, suivre | Parcours réalisé sans aide en moins de 5 min |
| UAT-02 | Gestionnaire | Traiter un dossier « nouvel IBAN » depuis la file de travail | Dossier passé en ACCEPTEE_AUTO après contrôle du RIB |
| UAT-03 | Analyste Conformité | Traiter un dossier de 60 000 € | Motif visible en interne, invisible côté client |
| UAT-04 | Conseiller | Traiter un contrat nanti | Accord du créancier tracé dans le dossier |
| UAT-05 | Service client | Répondre à « où en est mon rachat ? » | Réponse donnée à partir du suivi, sans escalade |
