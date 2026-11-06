# Note de cadrage — Sinistres arrêt de travail en prévoyance collective

| | |
|---|---|
| **Projet** | DIGI-AT — Déclaration et indemnisation des arrêts de travail |
| **Sponsor (MOA)** | Direction Prévoyance collective — « Prévoyance Démo » (assureur fictif) |
| **Rédaction** | Fatma Hammami, Business Analyst AMOA |
| **Méthode** | Scrum, sprints de 2 semaines |

## 1. Contexte

En prévoyance collective, l'entreprise souscrit un contrat qui complète les indemnités journalières de la Sécurité sociale (IJSS) de ses salariés en arrêt de travail. Aujourd'hui, l'employeur déclare l'arrêt par courrier ou par e-mail, puis le gestionnaire **ressaisit** le dossier et **calcule l'indemnité à la main**.

L'[analyse des données 2025](../02-analyse-existant/analyse.md) montre : **25 jours** entre la déclaration et le paiement, **36 %** de dossiers incomplets, **82 %** de rejets évitables et **2,9 %** d'erreurs de calcul.

## 2. Objectifs

| Objectif | Indicateur | Cible |
|---|---|---|
| Accélérer l'indemnisation | Délai déclaration → paiement | ≤ 12 jours |
| Fiabiliser les dossiers | Dossiers incomplets à réception | ≤ 15 % |
| Éviter les déclarations inutiles | Rejets pour franchise non atteinte | − 80 % |
| Supprimer les erreurs | Erreurs de calcul en audit | 0 |
| Réduire les appels | Appels par dossier | − 40 % |

## 3. Périmètre

**Dans le périmètre** : déclaration en ligne par l'employeur, contrôle d'éligibilité, dépôt et contrôle des pièces, calcul automatique de l'indemnité complémentaire, orientation des dossiers, suivi en ligne.

**Hors périmètre** : invalidité et décès, paiement des IJSS (Sécurité sociale), échanges automatisés avec la CPAM et la DSN (étape suivante).

## 4. Parties prenantes

| Acteur | Rôle |
|---|---|
| Direction Prévoyance collective | Sponsor, MOA, arbitrages |
| Product Owner | Porte le backlog |
| Gestionnaires sinistres | Utilisateurs internes, traitent les dossiers orientés |
| Médecin-conseil | Expertise des arrêts longs |
| Conformité / lutte contre la fraude | Règles de vigilance |
| Actuariat | Valide les paramètres de garantie |
| Entreprises clientes (RH) | Déclarent les arrêts, fournissent l'attestation de salaire |
| DSI | MOE : portail employeur, moteur de calcul, API |
| DPO | Données de santé : minimisation, habilitations |

## 5. Contraintes

- **Données de santé** : le motif médical de l'arrêt n'est jamais collecté ; accès restreint au médecin-conseil (RGPD).
- **Contrat** : les paramètres (franchise, taux, plafond, durée maximale) varient selon les contrats. Ils doivent être **paramétrables**.
- **Calendrier** : mise en production avant le renouvellement des contrats collectifs au 1er janvier.

## 6. Gouvernance

| Instance | Fréquence | Animation |
|---|---|---|
| Daily | Quotidien | Scrum Master |
| Affinage du backlog | Hebdomadaire | BA |
| Revue de sprint | Toutes les 2 semaines | PO / BA |
| **Comité de suivi** | Toutes les 2 semaines | **BA** |
