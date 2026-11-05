# Modélisation des processus (BPMN simplifié)

Les diagrammes ci-dessous suivent la logique BPMN : des couloirs par acteur, des tâches, des passerelles de décision et des événements de début et de fin. Ils sont rédigés en Mermaid pour être lisibles directement sur GitHub.

## Processus actuel (*as-is*)

```mermaid
flowchart LR
    subgraph Client
        A((Début)) --> B[Télécharger et remplir le formulaire]
        B --> C[Envoyer courrier + RIB + pièce d'identité]
    end
    subgraph Courrier
        C --> D[Numériser le courrier]
    end
    subgraph Gestionnaire
        D --> E{Dossier complet ?}
        E -- Non --> F[Relancer le client par courrier]
        F --> C
        E -- Oui --> G[Ressaisir la demande]
        G --> H{Montant élevé ?}
        H -- Non --> K[Déclencher le paiement]
    end
    subgraph Conformité
        H -- Oui --> I[Analyser le dossier reçu par e-mail]
        I --> K
    end
    K --> Z((Fin : paiement sous 12 jours en moyenne))
```

**Points de rupture** : courrier (délai), dossiers incomplets (18 %), ressaisie (erreurs), échanges par e-mail avec la Conformité (pas de traçabilité).

## Processus cible (*to-be*)

```mermaid
flowchart TD
    A((Début)) --> B[Client : consulter le contrat et simuler]
    B --> C{Saisie valide ?<br/>RG-03 RG-04 RG-05}
    C -- Non --> B
    C -- Oui --> D[Client : valider avec code SMS<br/>RG-11]
    D --> E{Contrat nanti ?<br/>RG-06}
    E -- Oui --> F[Conseiller : obtenir l'accord du créancier]
    E -- Non --> G{KYC à jour ?<br/>RG-02}
    G -- Non --> H[Client : fournir les justificatifs]
    G -- Oui --> I{Seuil LCB-FT ?<br/>RG-07}
    I -- Oui --> J[Conformité : analyser le dossier]
    I -- Non --> K{IBAN vérifié ?<br/>RG-08}
    K -- Non --> H
    K -- Oui --> L[Système : acceptation automatique]
    H --> M[Gestionnaire : contrôler les pièces]
    M --> L
    J --> N{Avis conformité}
    N -- Favorable --> L
    N -- Défavorable --> R((Fin : refus motivé))
    F --> L
    L --> P[Système : désinvestir les supports<br/>et payer sous 3 jours ouvrés - RG-10]
    P --> Z((Fin : rachat payé))
```

**Gains attendus** : plus de courrier ni de ressaisie, dossiers complets dès la saisie, Conformité intégrée au flux avec un motif tracé, paiement en 3 jours ouvrés pour les dossiers simples.
