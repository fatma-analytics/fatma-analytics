# Stratégie de recette

## 1. Objectif

Vérifier que la solution respecte les spécifications (**recette fonctionnelle**) puis qu'elle répond au besoin réel des utilisateurs (**UAT**), sans régression sur le traitement papier existant.

## 2. Niveaux de test

| Niveau | Qui | Quoi | Outil |
|---|---|---|---|
| Tests unitaires | Développeurs | Fonctions de calcul | pytest |
| **Recette fonctionnelle API** | **BA** | Chaque règle RG-xx, codes retour, statuts | **Postman**, pytest |
| **Contrôles de données** | **BA** | Cohérence en base après exécution | **SQL** |
| Recette des parcours | BA + testeur | Écrans E1 à E5 | Navigateur, cahier de recette |
| **UAT** | Gestionnaires, Conformité, panel de clients internes | Scénarios métier de bout en bout | Cahier UAT, Jira |
| Non-régression | Testeur | Traitement des rachats papier | Campagne existante |

## 3. Approche

- **Une règle = au moins un cas nominal et un cas d'erreur.** Les valeurs limites sont testées explicitement : 500 €, 38 500 € (encours restant exactement 1 500 €), 3e rachat.
- **Personas** : un jeu de données par situation métier, défini dans `sql/seed.sql`.

| Persona | Contrat | Situation testée |
|---|---|---|
| Claire | CT-1001 | Cas nominal, limites, répartition, IBAN |
| Karim | CT-1002 | Seuil LCB-FT en montant |
| Sophie | CT-1003 | Contrat nanti |
| Lucas | CT-1004 | KYC périmé |
| Emma | CT-1005 | Seuil LCB-FT en fréquence |

- **Date de référence figée** au 05/11/2026 pour rendre les calculs de délai reproductibles.
- **Traçabilité** : chaque cas renvoie à une user story et une règle (voir la matrice dans la SFD §6).

## 4. Gestion des anomalies

| Gravité | Définition | Délai de correction |
|---|---|---|
| Bloquante | Risque financier ou réglementaire, ou parcours impossible | Avant la fin du sprint |
| Majeure | Règle mal appliquée sans risque financier | Sprint suivant |
| Mineure | Libellé, ergonomie | Selon priorisation du PO |

Cycle d'une anomalie dans Jira : **Ouverte → En analyse → En correction → À retester → Fermée**. La BA qualifie l'anomalie : est-ce un bug de développement, un oubli de spécification ou une évolution ?

## 5. Critères d'entrée et de sortie

**Entrée en UAT** : 100 % des cas de recette fonctionnelle exécutés, aucune anomalie bloquante ouverte.
**Sortie (PV de recette)** : 100 % des cas UAT exécutés, 0 anomalie bloquante, 0 anomalie majeure sans contournement validé, 7 contrôles SQL à 0 ligne.
