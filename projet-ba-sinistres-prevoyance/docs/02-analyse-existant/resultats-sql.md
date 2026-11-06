# Résultats SQL — analyse de l'existant

_Fichier généré par `scripts/analyser_existant.py` à partir de `sql/analyse_existant.sql`._

## A1 : volumétrie et issue des dossiers

| statut_final | nb_dossiers | pct |
|---|---|---|
| PAYE | 1430 | 71.5 |
| REJETE | 570 | 28.5 |

## A2 : délai de bout en bout décomposé par étape (dossiers payés, en jours calendaires)

| declaration | completude | instruction | paiement | total_declaration_paiement |
|---|---|---|---|---|
| 24.6 | 7.9 | 13.1 | 4.3 | 25.3 |

## A3 : dossiers incomplets à réception, par taille d'entreprise et canal

| taille_entreprise | canal | nb_dossiers | pct_incomplets |
|---|---|---|---|
| TPE | courrier | 556 | 45.3 |
| TPE | email | 339 | 41.6 |
| PME | courrier | 503 | 34.4 |
| PME | email | 324 | 26.5 |
| ETI | courrier | 155 | 25.8 |
| ETI | email | 123 | 18.7 |

## A4 : pièce manquante la plus fréquente

| piece | nb_dossiers | pct_des_incomplets | relances_moyennes |
|---|---|---|---|
| attestation_salaire | 346 | 48.4 | 1.53 |
| decompte_ijss | 213 | 29.8 | 1.66 |
| arret_travail | 93 | 13.0 | 1.54 |
| rib | 63 | 8.8 | 1.49 |

## A5 : motifs de rejet

| motif_rejet | nb_rejets | pct_des_rejets |
|---|---|---|
| franchise_non_atteinte | 469 | 82.3 |
| hors_delai | 72 | 12.6 |
| non_affilie | 29 | 5.1 |

## A6 : impact des pièces manquantes sur le délai et les appels

| dossier | nb_dossiers | jours_completude | appels_moyens |
|---|---|---|---|
| complet | 1285 | 2.8 | 1.04 |
| incomplet | 715 | 17.2 | 1.9 |

## A7 : erreurs de calcul détectées en audit (dossiers payés)

| dossiers_payes | erreurs | pct_erreurs | montant_total_verse |
|---|---|---|---|
| 1430 | 41 | 2.9 | 6538905.0 |

## A8 : répartition des durées d'arrêt (dimensionnement des règles)

| tranche | nb_dossiers | pct |
|---|---|---|
| 1. 30 jours ou moins (franchise) | 484 | 24.2 |
| 2. 31 à 90 jours | 1025 | 51.3 |
| 3. 91 à 180 jours | 150 | 7.5 |
| 4. plus de 180 jours (contrôle médical) | 341 | 17.1 |
