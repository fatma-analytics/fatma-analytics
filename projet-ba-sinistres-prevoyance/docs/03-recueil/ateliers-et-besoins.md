# Ateliers et expression de besoins

## Atelier 1 — Restitution de l'analyse de données · 14/09/2026

**Participants** : Direction Prévoyance, PO, 2 gestionnaires, service client, BA

La BA présente les 5 constats de l'[analyse de l'existant](../02-analyse-existant/analyse.md).

**Réactions et apports du métier**
- Les gestionnaires confirment que l'attestation de salaire est « le point noir » : les TPE n'ont souvent pas de service RH.
- Le service client signale que beaucoup d'employeurs **ne connaissent pas la franchise** et déclarent tous les arrêts « par précaution ».
- La Direction valide la priorité : **éviter les dossiers inutiles avant d'automatiser le calcul**.

**Décision** : le contrôle d'éligibilité (US-01) est prioritaire et sera livré dès le sprint 1.

## Atelier 2 — Règles de garantie et de gestion · 17/09/2026

**Participants** : PO, Actuariat, médecin-conseil, Conformité, gestionnaire senior, BA

| Règle | Décision | Validée par |
|---|---|---|
| Franchise | 30 jours continus | Actuariat |
| Rechute | Même cause, reprise de moins de 60 jours : pas de nouvelle franchise, durées cumulées | Actuariat, médecin-conseil |
| Garantie | 75 % du salaire brut de référence, sous déduction des IJSS | Actuariat |
| Plafond | IJSS + maintien employeur + complément ≤ 100 % du salaire net de référence | Actuariat |
| Durée maximale | 1 095 jours d'indemnisation | Actuariat |
| Contrôle médical | Au-delà de 180 jours d'arrêt cumulés | Médecin-conseil |
| Délai de déclaration | 90 jours ; au-delà, examen par un gestionnaire (pas de rejet automatique) | Gestion |
| Vigilance | Arrêt débutant moins de 30 jours après l'affiliation → contrôle | Conformité |

**Point de discussion** : l'Actuariat voulait **rejeter automatiquement** les déclarations hors délai. La BA a montré, données à l'appui, qu'un quart des dossiers hors délai de 2025 (28 sur 112) avaient finalement été payés après justification (hospitalisation, erreur de l'employeur). **Arbitrage** : orientation vers un gestionnaire (statut A_ETUDIER) plutôt qu'un rejet.

**Point d'attention écrêtement** : un cas réel a été rejoué en atelier (salaire de 36 500 €, maintien employeur de 10 €/jour). L'Actuariat confirme que le complément passe de 33,53 € à 26,53 €. Ce cas devient un scénario de test.

## Atelier 3 — Parcours employeur · 22/09/2026

**Participants** : PO, UX designer, 3 RH d'entreprises clientes (1 TPE, 1 PME, 1 ETI), BA

**Retours des RH**
- « Je ne sais jamais quelles pièces envoyer. » → liste des pièces affichée **avant** la déclaration.
- « L'attestation de salaire, je la remplis à la main. » → formulaire en ligne pré-rempli, généré au moment de la déclaration.
- « Je veux savoir si c'est payé pour prévenir mon salarié. » → suivi en ligne.

**Choix de conception (économie comportementale)**
- Le contrôle d'éligibilité affiche un message clair (« Cet arrêt ne dépasse pas la franchise de 30 jours : aucune indemnité ne sera versée ») plutôt qu'un blocage. L'employeur garde la main et comprend pourquoi.
- Une **liste de pièces avec cases à cocher** et une barre de progression réduisent l'oubli et la procrastination.

---

## Expression de besoins (MoSCoW)

| ID | Besoin | Acteur | Priorité | User story |
|---|---|---|---|---|
| BE-01 | Savoir avant de déclarer si l'arrêt peut être indemnisé | Employeur | Must | US-01 |
| BE-02 | Être alerté des pièces manquantes dès la saisie | Employeur | Must | US-02 |
| BE-03 | Remplir l'attestation de salaire en ligne | Employeur | Should | US-03 |
| BE-04 | Calcul automatique et exact de l'indemnité | Gestionnaire | Must | US-04 |
| BE-05 | Gestion automatique des rechutes et de la durée maximale | Gestionnaire | Must | US-05 |
| BE-06 | Orientation automatique des dossiers à examiner | Gestionnaire, médecin-conseil, Conformité | Must | US-06 |
| BE-07 | Suivre l'avancement et la date de paiement | Employeur, salarié | Should | US-07 |
| BE-08 | Échanges automatiques avec la DSN et la CPAM | DSI | Won't (v1) | — |
