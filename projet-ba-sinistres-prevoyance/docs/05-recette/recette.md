# Recette

## 1. Approche : des user stories exécutables

Les critères d'acceptation sont écrits en **Gherkin français** (Étant donné / Quand / Alors) dans [`features/`](../../features/), puis **exécutés automatiquement** contre le moteur de règles avec `pytest-bdd`.

Un même texte sert ainsi :
- de **spécification**, lue et validée par l'Actuariat et les gestionnaires ;
- de **cas de test**, rejoué à chaque modification ;
- de **documentation vivante** : si une règle change sans que le scénario suive, le test échoue.

```bash
pytest -v      # 13 scénarios métier + 3 tests d'API
```

## 2. Couverture des règles

| Règle | Scénario(s) | Résultat |
|---|---|---|
| RG-01 Affiliation | Salarié radié avant l'arrêt | ✅ |
| RG-02 Délai de déclaration | Déclaration au-delà de 90 jours | ✅ |
| RG-03 Pièces | Attestation de salaire manquante (+ test API) | ✅ |
| RG-04 Franchise | Arrêt de 12 jours ; arrêt de 30 jours (limite) ; nouvel arrêt pour une autre cause | ✅ |
| RG-05 Rechute | Rechute pour la même cause ; reprise de 60 jours (limite) | ✅ |
| RG-06 Calcul | Arrêt de 61 jours (31 jours × 33,53 €) | ✅ |
| RG-07 Écrêtement | Maintien employeur de 10 €/jour (26,53 €) | ✅ |
| RG-08 Durée maximale | 1 090 jours déjà indemnisés → 5 jours | ✅ |
| RG-09 Contrôle médical | Arrêt de 245 jours | ✅ |
| RG-10 Vigilance | Arrêt 15 jours après l'affiliation | ✅ |
| RG-11 Paiement | Paiement prévu le 20/11/2026 | ✅ |

**Valeurs limites** automatisées : arrêt de 30 jours exactement (franchise non dépassée) et reprise 60 jours exactement après l'arrêt précédent (rechute retenue).

## 3. Rejeu de l'historique (test de non-régression métier)

Les 2 000 dossiers de 2025 servent de référence. Pour les arrêts de 30 jours ou moins, le moteur doit conclure au rejet RG-04 comme la gestion manuelle (469 dossiers). Les écarts sont analysés un par un avec les gestionnaires : soit erreur manuelle, soit règle mal spécifiée.

## 4. Anomalies

| ID | Gravité | Description | Qualification | Statut |
|---|---|---|---|---|
| ANO-01 | Majeure | En cas de rechute, la franchise de 30 jours était appliquée une seconde fois. | Bug de développement : l'arrêt précédent n'était pas transmis au calcul | ✅ Corrigée — scénario « Rechute pour la même cause » |
| ANO-02 | Bloquante | La durée maximale ne tenait pas compte des jours déjà indemnisés avant la rechute : risque de paiement au-delà de 1 095 jours. | Oubli de spécification : RG-08 ne précisait pas « rechutes comprises » | ✅ Corrigée — SFD v1.1, scénario « Durée maximale » ajouté |
| ANO-03 | Mineure | Le message de rejet RG-04 ne rappelait pas la durée de la franchise. | Libellé | ✅ Corrigée |

## 5. Scénarios UAT

| ID | Utilisateur | Scénario | Critère |
|---|---|---|---|
| UAT-01 | RH de TPE | Déclarer un arrêt de 12 jours | Message d'information compris sans appeler le service client |
| UAT-02 | RH de PME | Déclarer un arrêt de 61 jours avec toutes les pièces | Montant et date de paiement affichés |
| UAT-03 | Gestionnaire | Traiter un dossier A_ETUDIER | Justification consultable, décision tracée |
| UAT-04 | Médecin-conseil | Recevoir un dossier de plus de 180 jours | Seul le médecin-conseil voit les éléments médicaux |
| UAT-05 | Actuariat | Vérifier 20 calculs tirés au hasard | 0 écart avec le calcul de référence |
