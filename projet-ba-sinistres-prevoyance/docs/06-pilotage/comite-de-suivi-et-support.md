# Comité de suivi et support post-déploiement

## Comité de suivi n°2 — 23/10/2026

**Participants** : Direction Prévoyance (sponsor), PO, Actuariat, médecin-conseil, DSI, BA (animation)

| Axe | Météo | Commentaire |
|---|---|---|
| Périmètre | 🟢 | US-01, US-02, US-04 et US-05 livrées |
| Planning | 🟡 | ANO-02 (durée maximale) a mobilisé 2 jours ; UAT maintenue au 16/11 |
| Qualité | 🟢 | Scénarios Gherkin des sprints 1 et 2 au vert, rejeu de l'historique en cours |
| Données de santé | 🟢 | Habilitations médecin-conseil validées par le DPO |

| Sprint | Engagé (pts) | Livré (pts) | User stories |
|---|---|---|---|
| Sprint 1 | 8 | 8 | US-01, US-02 |
| Sprint 2 | 13 | 13 | US-04, US-05 |
| Sprint 3 (en cours) | 11 | — | US-03, US-06, US-07 |

**Fait marquant** : ANO-02 venait d'une règle ambiguë (« 1 095 jours » sans préciser « rechutes comprises »). L'écart a été trouvé grâce au scénario Gherkin écrit avec l'Actuariat. Le risque évité est un paiement au-delà de la garantie.

**Décisions**
| # | Décision | Décideur |
|---|---|---|
| D1 | Les paramètres de garantie sont stockés par contrat, pas en dur | Sponsor, DSI |
| D2 | Pilote avec 50 entreprises clientes en décembre avant généralisation | Sponsor |

**Risques**
| Risque | Action | Porteur |
|---|---|---|
| Faible adoption du portail par les TPE | Accompagnement téléphonique pendant le pilote, guide en une page | Service client |
| Charge du médecin-conseil (17 % d'arrêts longs) | Planification des expertises dès J + 150 | Médecin-conseil |

---

## Accompagnement et support

**Accompagnement**
| Population | Action |
|---|---|
| RH des entreprises clientes | Guide en une page « Déclarer un arrêt en 5 minutes », webinaire de 30 min |
| Gestionnaires | Atelier sur les nouvelles files de travail et les statuts |
| Service client | Fiche réflexe : franchise, pièces, rechute, délais de paiement |

**Hypercare (6 semaines)**
| Indicateur | Cible | Requête de suivi |
|---|---|---|
| Délai déclaration → paiement | ≤ 12 jours | A2 de `sql/analyse_existant.sql`, appliquée aux nouveaux dossiers |
| Dossiers incomplets | ≤ 15 % | A3 / A4 |
| Rejets pour franchise | − 80 % | A5 |
| Écarts de calcul en audit | 0 | A7 |

**Évolutions identifiées** : récupération automatique des IJSS (flux CPAM), pré-remplissage du salaire via la DSN, notification SMS au salarié.
