# language: fr
Fonctionnalité: Éligibilité et orientation des dossiers
  En tant que responsable de la gestion des sinistres
  Je veux que chaque dossier soit orienté automatiquement vers la bonne file
  Afin que seuls les dossiers simples soient payés sans intervention

  Contexte:
    Étant donné un salarié affilié depuis le "01/04/2019" avec un salaire brut annuel de 36500 €
    Et des indemnités journalières de la Sécurité sociale de 41,47 € par jour

  Scénario: US-01 — Arrêt plus court que la franchise
    Étant donné un arrêt de travail du "05/10/2026" au "16/10/2026" déclaré le "06/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "REJETE"
    Et la règle "RG-04" est appliquée

  Scénario: US-01 — Salarié radié avant le début de l'arrêt
    Étant donné un salarié radié le "30/06/2026"
    Et un arrêt de travail du "15/07/2026" au "30/09/2026" déclaré le "20/07/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "REJETE"
    Et la règle "RG-01" est appliquée

  Scénario: US-02 — Attestation de salaire manquante
    Étant donné un arrêt de travail du "01/09/2026" au "31/10/2026" déclaré le "05/09/2026"
    Et toutes les pièces sauf "attestation_salaire"
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "EN_ATTENTE_PIECES"
    Et la pièce manquante signalée est "attestation_salaire"

  Scénario: US-06 — Déclaration au-delà de 90 jours
    Étant donné un arrêt de travail du "01/06/2026" au "30/09/2026" déclaré le "05/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "A_ETUDIER"
    Et la règle "RG-02" est appliquée

  Scénario: US-06 — Arrêt débutant peu après l'affiliation
    Étant donné un salarié affilié depuis le "20/09/2026" avec un salaire brut annuel de 36500 €
    Et un arrêt de travail du "05/10/2026" au "30/11/2026" déclaré le "08/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "CONTROLE_GESTIONNAIRE"
    Et la règle "RG-10" est appliquée

  Scénario: US-06 — Arrêt long soumis à contrôle médical
    Étant donné un arrêt de travail du "01/03/2026" au "31/10/2026" déclaré le "10/03/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "EN_CONTROLE_MEDICAL"
    Et la règle "RG-09" est appliquée

  Scénario: US-01 — Valeur limite : arrêt de 30 jours exactement
    Étant donné un arrêt de travail du "01/10/2026" au "30/10/2026" déclaré le "02/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "REJETE"
    Et la règle "RG-04" est appliquée
