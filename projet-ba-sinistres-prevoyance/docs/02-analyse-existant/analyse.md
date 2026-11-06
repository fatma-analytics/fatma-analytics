# Analyse de l'existant — ce que disent les données

Avant les ateliers, la BA a analysé **2 000 sinistres arrêt de travail traités en 2025** pour objectiver les irritants. Les chiffres viennent des requêtes de [`sql/analyse_existant.sql`](../../sql/analyse_existant.sql). Les résultats bruts sont dans [`resultats-sql.md`](resultats-sql.md).

> Données **fictives**, générées par [`scripts/generer_historique.py`](../../scripts/generer_historique.py) (graine fixe, donc reproductibles).

---

## Constat 1 — Il faut 25 jours entre la déclaration et le paiement

| Étape (dossiers payés) | Durée moyenne |
|---|---|
| Début de l'arrêt → déclaration | 24,6 jours |
| Déclaration → dossier complet | **7,9 jours** |
| Dossier complet → décision (ressaisie, calcul manuel) | **13,1 jours** |
| Décision → paiement | 4,3 jours |
| **Déclaration → paiement** | **25,3 jours** |

**Lecture** : plus de la moitié du délai (13,1 jours) est de l'**instruction manuelle**. C'est le premier levier d'automatisation.

## Constat 2 — Plus d'un dossier sur trois arrive incomplet

- **715 dossiers sur 2 000 (36 %)** sont incomplets à réception.
- Taux le plus élevé : **TPE par courrier, 45 %**. Le plus faible : ETI par e-mail, 19 %.
- La pièce qui manque le plus est **l'attestation de salaire (48 % des cas)**. Elle est fournie par l'**employeur**, pas par le salarié.
- Un dossier incomplet met **17,2 jours** à être complété (contre 2,8 jours), et génère **1,9 appel** au service client (contre 1,0).

**Lecture** : le problème vient surtout de l'employeur, en particulier des petites entreprises. → Besoin d'un **dépôt en ligne côté employeur** avec contrôle des pièces au moment de la saisie.

## Constat 3 — 82 % des rejets auraient pu être évités

| Motif de rejet | Nb | Part des rejets |
|---|---|---|
| Franchise non atteinte (arrêt ≤ 30 jours) | 469 | **82 %** |
| Déclaration hors délai | 72 | 13 % |
| Salarié non affilié | 29 | 5 % |

**Lecture** : 469 dossiers, soit 23 % du volume total, ont été déclarés, instruits puis rejetés alors que l'arrêt ne dépassait pas la franchise. → Besoin d'un **contrôle d'éligibilité dès la déclaration**, qui informe avant l'envoi des pièces.

## Constat 4 — Le calcul manuel produit des erreurs

- **41 erreurs de calcul** détectées en audit sur 1 430 dossiers payés (**2,9 %**), pour 6,5 M€ versés.

**Lecture** : un calcul automatique et testé (franchise, rechute, écrêtement, durée maximale) supprime ce risque opérationnel.

## Constat 5 — Les arrêts longs pèsent lourd

- **17 %** des arrêts dépassent 180 jours. Ils exigent une expertise médicale, déclenchée aujourd'hui « au fil de l'eau ».

**Lecture** : le déclenchement du contrôle médical doit être **automatique et tracé**.

---

## Du constat au besoin

| Constat | Besoin | User story |
|---|---|---|
| 82 % des rejets = franchise | Vérifier l'éligibilité avant la déclaration | US-01 |
| 36 % de dossiers incomplets, attestation employeur en tête | Dépôt employeur en ligne, contrôle des pièces à la saisie | US-02, US-03 |
| 13,1 jours d'instruction, 2,9 % d'erreurs | Calcul automatique de l'indemnité | US-04, US-05 |
| Arrêts longs, hors délai, vigilance | Orientation automatique vers la bonne file | US-06 |
| 1,9 appel par dossier incomplet | Suivi en ligne pour le salarié et l'employeur | US-07 |

## Gains estimés (hypothèses présentées au comité de cadrage)

| Levier | Hypothèse | Effet estimé sur 2 000 dossiers/an |
|---|---|---|
| Contrôle d'éligibilité | 80 % des arrêts sous la franchise ne sont plus déclarés | ≈ 375 dossiers évités |
| Contrôle des pièces à la saisie | Les dossiers incomplets passent de 36 % à 15 % | ≈ 420 dossiers incomplets en moins |
| Calcul automatique | Instruction de 13,1 à 2 jours pour les dossiers simples | Délai déclaration → paiement ≈ 12 jours |
| Calcul testé | Erreurs de 2,9 % à ~0 % | ≈ 40 erreurs évitées |
