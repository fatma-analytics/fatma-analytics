# Accompagnement des utilisateurs et support post-déploiement

## 1. Plan d'accompagnement

| Population | Action | Format | Quand |
|---|---|---|---|
| Gestionnaires back-office | Formation à la file de travail et aux statuts | Atelier de 1 h 30 + guide | Semaine avant la mise en production |
| Analystes Conformité | Traitement des dossiers EN_CONTROLE_LCBFT | Atelier de 1 h | Semaine avant la mise en production |
| Conseillers | Contrats nantis, réponse aux clients | Vidéo de 10 min + fiche réflexe | Jour de la mise en production |
| Service client | Script d'appel, lecture du suivi | Fiche réflexe + FAQ | Jour de la mise en production |
| Clients | Bannière dans l'espace client, aide en ligne | FAQ | Jour de la mise en production |

## 2. Guide utilisateur — gestionnaire

**Ouvrir la file de travail** : les dossiers sont triés du plus ancien au plus récent. Chaque ligne affiche le contrat, le montant, le statut et le motif.

| Statut | Motif | Que faire ? |
|---|---|---|
| EN_ATTENTE_PIECES | Nouvel IBAN | Vérifier que le RIB est au nom du souscripteur. Si conforme : valider (le dossier passe en ACCEPTEE_AUTO). Sinon : refuser avec motif. |
| EN_ATTENTE_PIECES | Mise à jour KYC | Vérifier la pièce d'identité et le justificatif de domicile, mettre à jour la date KYC, puis valider. |
| EN_CONTROLE_LCBFT | Montant ou fréquence | **Ne pas traiter** : dossier réservé à la Conformité. |
| ORIENTEE_CONSEILLER | Contrat nanti | Transmis au conseiller, qui recueille l'accord écrit du créancier. |

**Rappel** : le motif LCB-FT ne doit jamais être communiqué au client.

## 3. Fiche réflexe — service client

| Le client dit… | Statut visible | Réponse |
|---|---|---|
| « Je n'ai pas reçu mon argent » | ACCEPTEE_AUTO | Indiquer la date de paiement prévue (3 jours ouvrés). Au-delà, escalader au back-office. |
| « On me demande des pièces » | EN_ATTENTE_PIECES | Lire le motif et indiquer les pièces à déposer dans l'espace client. |
| « Ma demande est en cours d'étude » | EN_CONTROLE_LCBFT | « Votre demande est en cours d'étude, réponse sous 5 jours ouvrés. » **Ne pas évoquer de contrôle.** |
| « Je ne peux pas retirer plus » | — | Expliquer l'encours minimum de 1 500 €. Pour un rachat total, orienter vers le formulaire dédié. |

## 4. Support post-déploiement (hypercare, 30 jours)

**Organisation**
- Point quotidien de 15 min pendant 2 semaines (BA, PO, DSI, back-office), puis hebdomadaire.
- Anomalies de production tracées dans Jira avec l'étiquette `hypercare`.
- La BA qualifie chaque retour : anomalie, demande d'évolution ou besoin de formation.

**Indicateurs suivis** (requêtes `PIL-01` à `PIL-03` de [`sql/controles_recette.sql`](../../sql/controles_recette.sql))

| Indicateur | Cible | Seuil d'alerte |
|---|---|---|
| Taux d'acceptation automatique | ≥ 70 % | < 60 % |
| Dossiers en file de plus de 5 jours | 0 | > 10 |
| Contrôles CTRL-01 à CTRL-07 | 0 ligne | ≥ 1 ligne → incident bloquant |
| Taux d'abandon entre simulation et validation | < 40 % | > 55 % |

**Backlog d'évolutions identifiées** : rachat total en ligne, rachats programmés, dépôt de pièces directement depuis le suivi, notification par SMS du changement de statut.
