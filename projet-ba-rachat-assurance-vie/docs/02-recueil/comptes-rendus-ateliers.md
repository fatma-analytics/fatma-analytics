# Comptes rendus des ateliers de recueil des besoins

> Ateliers animés par la Business Analyst. Chaque compte rendu est diffusé sous 24 h sur Confluence et validé par les participants.

---

## Atelier 1 — Processus actuel et irritants

**Date** : 09/09/2026 · **Durée** : 2 h
**Participants** : PO Épargne digitale, 2 gestionnaires back-office, responsable service client, BA

**Objectif** : comprendre le processus actuel (*as-is*) et lister les irritants.

**Ce qu'on a appris**
1. Le client télécharge un formulaire, l'imprime, le signe et l'envoie par courrier avec RIB et pièce d'identité.
2. Le courrier est numérisé, puis le gestionnaire ressaisit la demande dans l'outil de gestion.
3. Le gestionnaire vérifie : contrat actif, contrat non nanti, montant possible, IBAN au nom du client.
4. Au-delà d'un certain montant, il transmet le dossier à la Conformité par e-mail.
5. Le paiement est déclenché manuellement.

**Irritants**
| # | Irritant | Source |
|---|---|---|
| I1 | 18 % de dossiers incomplets → relance courrier, + 7 jours | Gestion |
| I2 | Ressaisie manuelle et erreurs de répartition entre supports | Gestion |
| I3 | Le client ne sait pas combien il peut retirer | Service client |
| I4 | Aucune visibilité sur l'avancement → appels répétés | Service client |
| I5 | Transmission à la Conformité par e-mail, sans traçabilité | Gestion |

**Décisions**
- Le parcours en ligne doit afficher le **montant maximum** autorisé avant toute saisie (réponse à I3).
- Un **statut de suivi** visible par le client est un incontournable (réponse à I4).

**Actions**
| Action | Porteur | Échéance |
|---|---|---|
| Fournir les règles de gestion actuelles (procédure interne) | Gestion | 11/09 |
| Extraire les volumes de rachats sur 12 mois | BA (SQL) | 12/09 |

---

## Atelier 2 — Règles de gestion et conformité

**Date** : 15/09/2026 · **Durée** : 2 h 30
**Participants** : PO, Conformité LCB-FT, Risques opérationnels, Fiscalité, gestionnaire senior, BA

**Analyse préalable (BA)** : extraction SQL de 12 mois de rachats papier.
- 85 % des rachats sont inférieurs à 10 000 €.
- 2 % sont supérieurs ou égaux à 50 000 €.
- Moins de 1 % des contrats font plus de 2 rachats par an.

**Règles validées**
| Règle | Décision | Validée par |
|---|---|---|
| Montant minimum | 500 € | PO, Gestion |
| Encours minimum après rachat | 1 500 € (en dessous : rachat total, hors périmètre) | PO, Gestion |
| Contrat nanti | Pas d'acceptation automatique : orientation conseiller | Risques |
| Connaissance client (KYC) | Mise à jour datant de moins de 36 mois, sinon justificatifs demandés | Conformité |
| Seuil LCB-FT montant | Contrôle manuel à partir de 50 000 € | Conformité |
| Seuil LCB-FT fréquence | Contrôle manuel à partir du 3e rachat sur 12 mois glissants | Conformité |
| IBAN | Seul l'IBAN déjà vérifié permet l'automatisme ; un nouvel IBAN → RIB à fournir | Conformité, Risques |
| Fiscalité | Afficher une **estimation** de la part de gains, sans calcul d'impôt | Fiscalité |

**Point de désaccord et arbitrage**
- Le PO souhaitait un seuil LCB-FT à 100 000 € pour maximiser l'automatisation.
- La Conformité a refusé : au-dessus de 50 000 €, l'analyse de l'origine et de la destination des fonds est obligatoire selon la procédure interne.
- **Arbitrage du sponsor** : seuil à 50 000 €, paramétrable. L'impact reste limité : environ 2 % des volumes.

**Actions**
| Action | Porteur | Échéance |
|---|---|---|
| Rédiger les règles RG-01 à RG-11 dans la SFD | BA | 19/09 |
| Valider les libellés fiscaux | Fiscalité | 22/09 |

---

## Atelier 3 — Parcours client et maquettes

**Date** : 18/09/2026 · **Durée** : 2 h
**Participants** : PO, UX designer, développeur front, service client, BA

**Parcours retenu** (5 écrans) : Mes contrats → Simulation → Choix des supports et de l'IBAN → Récapitulatif et validation (code SMS) → Confirmation et suivi.

**Décisions**
- Répartition **au prorata par défaut**, avec un mode avancé pour choisir les supports.
- Les messages d'erreur indiquent toujours **la valeur autorisée** (par exemple : « montant maximum possible : 38 500 € »).
- L'écran de confirmation affiche la **date de paiement prévue** quand le dossier est accepté automatiquement, sinon le motif et la prochaine étape.

**Point d'attention (économie comportementale)**
- Sur l'écran de simulation, on affiche la part de gains et l'encours restant **avant** la validation. Cela réduit l'effet de surprise fiscale et le regret après coup.
- On évite tout bouton par défaut sur « montant maximum » : l'**effet d'ancrage** pousserait à retirer plus que nécessaire.
