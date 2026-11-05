# Spécifications fonctionnelles détaillées (SFD)

| | |
|---|---|
| **Projet** | DIGI-RACHAT — Rachat partiel d'assurance vie en ligne |
| **Version** | 1.2 (règle RG-07 complétée après le sprint 2, voir ANO-03) |
| **Validation** | PO Épargne, Conformité, Risques, Fiscalité |

---

## 1. Objet

Ce document décrit **ce que** le système doit faire pour permettre à un client de demander un rachat partiel en ligne : écrans, données, règles de gestion, statuts et messages. Il sert de référence aux équipes de développement et de test.

## 2. Acteurs

| Acteur | Description |
|---|---|
| Client | Souscripteur connecté à son espace client |
| Gestionnaire | Back-office, traite les dossiers en attente de pièces |
| Analyste Conformité | Traite les dossiers en contrôle LCB-FT |
| Conseiller | Traite les contrats nantis avec le créancier |

## 3. Écrans

### E1 — Mes contrats
| Donnée | Source | Règle |
|---|---|---|
| Nom du produit, n° de contrat | SI Contrats | — |
| Valeur de rachat | Somme des positions | — |
| Montant maximum de rachat partiel | Valeur − 1 500 € | RG-04 |
| Bouton « Faire un rachat partiel » | — | Masqué si contrat non actif (RG-01) |

### E2 — Simulation
| Champ | Type | Obligatoire | Règle |
|---|---|---|---|
| Montant brut | Décimal, 2 décimales | Oui | RG-03, RG-04 |
| Mode de répartition | Prorata / Choix des supports | Oui (prorata par défaut) | RG-05 |

**Affichage du résultat** : répartition par support, encours restant, part de capital, part de gains (estimation), statut prévisionnel.

### E3 — Supports et IBAN
| Champ | Règle |
|---|---|
| Montant par support (mode avancé) | RG-05 |
| IBAN de versement | Pré-rempli avec l'IBAN vérifié ; modifiable (RG-08) |

### E4 — Récapitulatif et validation
Récapitulatif complet, case « J'ai pris connaissance de l'information fiscale », saisie du code SMS (RG-11).

### E5 — Confirmation et suivi
| Statut | Message affiché au client |
|---|---|
| ACCEPTEE_AUTO | « Votre demande est acceptée. Paiement prévu le {date}. » |
| EN_ATTENTE_PIECES | « Votre demande est enregistrée. Pour la finaliser : {motif}. » |
| EN_CONTROLE_LCBFT | « Votre demande est en cours d'étude. Nous revenons vers vous sous 5 jours ouvrés. » |
| ORIENTEE_CONSEILLER | « Votre conseiller va vous contacter pour finaliser votre demande. » |

> Le motif LCB-FT n'est **jamais** affiché au client (obligation de confidentialité). Il est visible uniquement dans la file de travail interne.

## 4. Règles de gestion

Les règles sont appliquées **dans cet ordre**. Les contrôles de saisie (RG-01, RG-03 à RG-05) bloquent la demande. Les règles d'orientation (RG-06, RG-02, RG-07, RG-08) déterminent le statut : la première qui s'applique l'emporte.

| ID | Règle | Type | Résultat si non respectée |
|---|---|---|---|
| **RG-01** | Le contrat existe, est **actif** et appartient au client connecté. | Bloquante | 404 / 403 / 422 |
| **RG-03** | Le montant demandé est **≥ 500 €**. | Bloquante | 422 — « Le montant minimum d'un rachat partiel est de 500 €. » |
| **RG-04** | L'encours restant après rachat est **≥ 1 500 €**. | Bloquante | 422 — message avec le montant maximum possible |
| **RG-05** | Répartition **au prorata** des supports par défaut. En mode avancé : chaque support appartient au contrat, chaque montant ≤ valeur du support, et la somme = montant demandé. Au prorata, l'écart d'arrondi est porté par le dernier support. | Bloquante | 422 |
| **RG-06** | Si le contrat est **nanti** → statut ORIENTEE_CONSEILLER. | Orientation | — |
| **RG-02** | Si la dernière mise à jour KYC date de **plus de 36 mois** → statut EN_ATTENTE_PIECES (justificatifs d'identité et de domicile). | Orientation | — |
| **RG-07** | Si montant **≥ 50 000 €** OU si la demande est le **3e rachat ou plus sur 12 mois glissants** (rachats refusés exclus) → statut EN_CONTROLE_LCBFT. | Orientation | — |
| **RG-08** | Si l'IBAN saisi diffère de l'IBAN vérifié → statut EN_ATTENTE_PIECES (RIB au nom du souscripteur). | Orientation | — |
| **RG-09** | Part de gains = montant × (valeur de rachat − capital net) / valeur de rachat, avec capital net = versements − part de capital des rachats déjà acceptés ou payés. Plancher à 0. | Calcul | — |
| **RG-10** | Si ACCEPTEE_AUTO : paiement prévu à **J + 3 jours ouvrés** et désinvestissement immédiat des supports. Dans tous les cas, date limite légale affichée = J + 2 mois. | Calcul | — |
| **RG-11** | La validation exige une **authentification forte** (code SMS valide). La simulation n'en exige pas. | Bloquante | 401 |

> Les seuils (500 €, 1 500 €, 50 000 €, 3 rachats, 36 mois, 3 jours) sont des **paramètres** (ENF-05), validés en atelier 2.

### Exemple de calcul (persona Claire, contrat CT-1001)

| Élément | Valeur |
|---|---|
| Positions | Fonds en euros 25 000 € + UC Actions 15 000 € = **40 000 €** |
| Versements | 30 000 € → gains = 10 000 € (25 %) |
| Rachat demandé | 5 000 € |
| Répartition au prorata | Fonds en euros 3 125 € (62,5 %) · UC Actions 1 875 € (37,5 %) |
| Part de gains (RG-09) | 5 000 × 25 % = **1 250 €** · part de capital = 3 750 € |
| Encours restant | 35 000 € |
| Montant maximum possible | 40 000 − 1 500 = **38 500 €** |
| Demande du jeudi 05/11/2026 | Paiement prévu le **mardi 10/11/2026** (J + 3 ouvrés) · limite légale 05/01/2027 |

## 5. Contrat d'interface (API)

| Méthode | Ressource | Usage | Codes retour |
|---|---|---|---|
| GET | `/contrats/{id}` | Écran E1 | 200, 403, 404 |
| POST | `/rachats/simulation` | Écran E2 | 200, 403, 404, 422 |
| POST | `/rachats` | Écran E4 (en-tête `X-OTP-Valide`) | 201, 401, 403, 404, 422 |
| GET | `/rachats/{id}` | Écran E5 / suivi | 200, 403, 404 |

Le client est identifié par l'en-tête `X-Client-Id`, simplification de démonstration du jeton de session. Les erreurs renvoient `{"detail": {"regle": "RG-xx", "message": "..."}}`.

**Exemple de requête**
```json
POST /rachats
{
  "id_contrat": "CT-1001",
  "montant": 5000,
  "repartition": [{"id_support": "EURO-01", "montant": 5000}]
}
```

## 6. Matrice de traçabilité

| Besoin | User story | Règles | Cas de test |
|---|---|---|---|
| BE-01 | US-01 | RG-01, RG-04 | CT-03, CT-19 |
| BE-02 | US-02 | RG-03, RG-04, RG-05, RG-09 | CT-01, CT-06, CT-07, CT-08 |
| BE-03 | US-05 | RG-11 | CT-02, CT-17, CT-18 |
| BE-04 | US-03 | RG-05 | CT-04, CT-09, CT-10 |
| BE-05 | US-05 | RG-10 | CT-02, CT-03 |
| BE-06 | US-06 | — | CT-05 |
| BE-07 | US-07 | RG-02, RG-06, RG-07 | CT-11, CT-12, CT-13, CT-14, CT-16 |
| BE-08 | US-04 | RG-08 | CT-15 |
| BE-09 | US-08 | — | PIL-03 (SQL) |
| BE-10 | US-09 | — | PIL-01, PIL-02 (SQL) |
