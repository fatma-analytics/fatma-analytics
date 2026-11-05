# Expression de besoins

Synthèse des besoins issus des ateliers, priorisés avec le Product Owner selon la méthode **MoSCoW**.

| ID | Besoin | Acteur | Irritant traité | Priorité |
|---|---|---|---|---|
| BE-01 | Connaître la valeur de rachat et le montant maximum que je peux retirer | Client | I3 | Must |
| BE-02 | Simuler un rachat et voir la répartition, l'encours restant et la part de gains | Client | I3 | Must |
| BE-03 | Faire ma demande en ligne sans courrier | Client | I1, I2 | Must |
| BE-04 | Choisir les supports sur lesquels je rachète | Client | I2 | Should |
| BE-05 | Être payé vite quand mon dossier est simple | Client | — | Must |
| BE-06 | Suivre l'avancement de ma demande | Client | I4 | Must |
| BE-07 | Bloquer l'automatisme quand un contrôle conformité est requis | Conformité | I5 | Must |
| BE-08 | Ne jamais payer sur un IBAN non vérifié sans contrôle | Risques | — | Must |
| BE-09 | Recevoir dans une file de travail les dossiers non automatiques, avec leur motif | Gestionnaire | I5 | Must |
| BE-10 | Disposer d'indicateurs de pilotage (taux d'automatisation, délais) | Direction | — | Should |
| BE-11 | Reprendre une simulation abandonnée | Client | — | Could |
| BE-12 | Programmer des rachats réguliers | Client | — | Won't (v1) |

**Exigences non fonctionnelles**

| ID | Exigence |
|---|---|
| ENF-01 | Authentification forte (code à usage unique) avant validation |
| ENF-02 | Piste d'audit : chaque demande conserve montant, répartition, IBAN, statut, motif et date |
| ENF-03 | Données personnelles minimisées et conservées selon la politique RGPD |
| ENF-04 | Temps de réponse de la simulation < 2 secondes |
| ENF-05 | Seuils métier paramétrables sans nouvelle livraison |
