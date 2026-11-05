# Comité de suivi n°3 — fin du sprint 3

**Date** : 30/10/2026 · **Animation** : Business Analyst
**Participants** : Directrice Épargne (sponsor), PO, Conformité, Risques opérationnels, responsable DSI, Scrum Master

---

## 1. Météo du projet

| Axe | Météo | Commentaire |
|---|---|---|
| Périmètre | 🟢 | US-07 (orientation conformité) livrée et démontrée |
| Planning | 🟡 | 2 anomalies bloquantes corrigées en fin de sprint, recette UAT maintenue au 16/11 |
| Qualité | 🟢 | 18 cas de recette des sprints 1 à 3 automatisés et au vert, 7 contrôles SQL à 0 anomalie |
| Budget | 🟢 | Conforme |
| Conformité | 🟢 | Règles RG-02, RG-06 et RG-07 validées en démo par la Conformité |

## 2. Avancement

| Sprint | Engagé (pts) | Livré (pts) | User stories |
|---|---|---|---|
| Sprint 1 | 7 | 7 | US-01, US-02 |
| Sprint 2 | 11 | 11 | US-03, US-04, US-05 |
| Sprint 3 | 8 | 8 | US-07 |
| Sprint 4 (en cours) | 10 | — | US-06, US-08, US-09 |

**Vélocité moyenne** : 8,7 points par sprint. Reste à faire : 10 points, couvert par le sprint 4.

## 3. Recette

| Indicateur | Valeur |
|---|---|
| Cas de test exécutés (sprints 1 à 3) | 18 / 18 |
| Cas OK | 18 |
| Anomalies ouvertes depuis le début | 3 (2 bloquantes, 1 majeure) |
| Anomalies corrigées et retestées | 3 |
| Anomalies ouvertes à date | 0 |

**Fait marquant** : l'anomalie **ANO-03** (3e rachat sur 12 mois accepté automatiquement) venait d'un **oubli dans la SFD**, pas d'un bug de développement. La règle de fréquence avait été évoquée en atelier 2 mais pas reportée dans la v1.1. La SFD est passée en v1.2 et un cas de test dédié a été ajouté (CT-12).
→ **Action d'amélioration** : relecture croisée systématique entre compte rendu d'atelier et SFD avant chaque validation.

## 4. Risques et points d'attention

| Risque | Évolution | Action | Porteur |
|---|---|---|---|
| Charge des gestionnaires sur les dossiers non automatiques | ↗ | Estimation : 25 % de dossiers non automatiques au lancement. Renfort de 2 gestionnaires le premier mois | Gestion |
| Délai de traitement Conformité non défini | → | Engagement de 5 jours ouvrés à formaliser | Conformité |
| Disponibilité des utilisateurs pour l'UAT | → | 4 gestionnaires et 2 analystes Conformité réservés du 16 au 27/11 | PO |

## 5. Décisions

| # | Décision | Décideur |
|---|---|---|
| D1 | Délai de réponse Conformité affiché au client : 5 jours ouvrés | Sponsor, Conformité |
| D2 | Le motif LCB-FT n'est jamais affiché au client (suite à ANO-02) | Conformité |
| D3 | Mise en production maintenue le 30/11 sous réserve d'un PV de recette sans réserve bloquante | Sponsor |

## 6. Actions

| Action | Porteur | Échéance |
|---|---|---|
| Préparer les jeux de données UAT par persona | BA | 13/11 |
| Rédiger le guide utilisateur gestionnaire | BA | 20/11 |
| Formaliser l'engagement de délai Conformité | Conformité | 06/11 |
| Préparer le script du service client | BA + service client | 25/11 |

**Prochain comité** : 13/11/2026, fin du sprint 4.
