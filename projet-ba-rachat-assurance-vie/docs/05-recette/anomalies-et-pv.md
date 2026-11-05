# Suivi des anomalies et PV de recette

## Registre des anomalies

| ID | Gravité | Cas | Description | Qualification | Statut |
|---|---|---|---|---|---|
| ANO-01 | Majeure | CT-01 (variante sur 3 supports) | Pour 3 000 € au prorata sur 3 supports, la somme des lignes vaut 2 999,99 €. | Bug de développement : arrondi de chaque ligne sans report de l'écart | ✅ Fermée — l'écart d'arrondi est porté par le dernier support (RG-05 précisée) |
| ANO-02 | Bloquante | Recette écran E5 | Le motif « Contrôle conformité : montant ≥ 50 000 € » s'affiche sur l'écran de confirmation du client. | Oubli de spécification : affichage du motif non précisé par statut | ✅ Fermée — message générique côté client (SFD §3 E5), décision D2 |
| ANO-03 | Bloquante | CT-12 | Un 3e rachat sur 12 mois est accepté automatiquement. | Oubli de spécification : règle de fréquence évoquée en atelier 2 mais absente de la SFD v1.1 | ✅ Fermée — SFD v1.2, RG-07 complétée, CT-12 ajouté |

### Exemple de fiche d'anomalie (format Jira)

> **ANO-03 — Seuil de fréquence LCB-FT non appliqué**
> **Environnement** : recette, build 0.3.2 · **Gravité** : Bloquante · **Composant** : API Rachats
> **Prérequis** : persona Emma (CT-1005), 2 rachats payés le 10/02/2026 et le 01/07/2026
> **Étapes** : 1. Se connecter en tant qu'Emma · 2. Demander 1 000 € · 3. Valider avec le code SMS
> **Résultat obtenu** : statut ACCEPTEE_AUTO, paiement prévu le 10/11/2026
> **Résultat attendu** : statut EN_CONTROLE_LCBFT (3e rachat sur 12 mois glissants)
> **Analyse BA** : la règle a été validée en atelier 2 (compte rendu du 15/09) mais n'a pas été reportée dans la SFD v1.1. Il ne s'agit pas d'une erreur de développement. → Mise à jour de la SFD, nouvelle user story technique, information du comité de suivi.

## Bilan de la recette fonctionnelle (au 05/11/2026)

| Indicateur | Valeur |
|---|---|
| Cas de recette fonctionnelle | 19 / 19 OK |
| Contrôles SQL | 7 / 7 à 0 ligne |
| Scénarios UAT | 5 planifiés du 16 au 27/11 |
| Anomalies détectées | 3 (2 bloquantes, 1 majeure) |
| Anomalies ouvertes | 0 |
| Part des anomalies venant de la spécification | 2 sur 3 → action d'amélioration (relecture croisée atelier / SFD) |

---

## Modèle de PV de recette (à signer en fin d'UAT)

**Projet** : DIGI-RACHAT — Rachat partiel d'assurance vie en ligne · **Version** : 1.0.0
**Campagne** : du 16/11/2026 au 27/11/2026

La recette fonctionnelle et les tests d'acceptation utilisateurs ont été réalisés selon la stratégie de recette. Critères de sortie à atteindre : 100 % des cas exécutés, aucune anomalie bloquante ou majeure ouverte, contrôles de données conformes.

**Décision** : ☐ Recette prononcée sans réserve · ☐ Avec réserves (lister) · ☐ Refusée

| Rôle | Nom | Décision |
|---|---|---|
| Sponsor — Direction Épargne | (signature) | |
| Product Owner | (signature) | |
| Conformité LCB-FT | (signature) | |
| Risques opérationnels | (signature) | |
| Business Analyst | Fatma Hammami | |
