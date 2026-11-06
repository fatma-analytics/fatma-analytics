# language: fr
Fonctionnalité: Calcul de l'indemnité complémentaire d'arrêt de travail
  En tant que gestionnaire prévoyance
  Je veux que l'indemnité soit calculée automatiquement selon le contrat
  Afin de supprimer les erreurs de calcul manuel (2,9 % des dossiers payés en 2025)

  Contexte:
    Étant donné un salarié affilié depuis le "01/04/2019" avec un salaire brut annuel de 36500 €
    Et des indemnités journalières de la Sécurité sociale de 41,47 € par jour

  Scénario: US-04 — Arrêt de 61 jours indemnisé après la franchise
    Étant donné un arrêt de travail du "03/08/2026" au "02/10/2026" déclaré le "20/08/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "ACCEPTE"
    Et l'indemnité journalière complémentaire est de 33,53 €
    Et 31 jours sont indemnisés pour un montant de 1039,43 €
    Et le paiement est prévu le "20/11/2026"

  Scénario: US-04 — Écrêtement quand l'employeur maintient une partie du salaire
    Étant donné un maintien de salaire par l'employeur de 10 € par jour
    Et un arrêt de travail du "01/09/2026" au "15/10/2026" déclaré le "10/09/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "ACCEPTE"
    Et l'indemnité est écrêtée
    Et l'indemnité journalière complémentaire est de 26,53 €
    Et 15 jours sont indemnisés pour un montant de 397,95 €

  Scénario: US-05 — Rechute pour la même cause : pas de nouvelle franchise
    Étant donné un arrêt précédent pour la même cause terminé le "31/08/2026" avec 50 jours d'arrêt dont 20 jours indemnisés
    Et un arrêt de travail du "10/10/2026" au "29/10/2026" déclaré le "12/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "ACCEPTE"
    Et aucune franchise n'est appliquée
    Et 20 jours sont indemnisés pour un montant de 670,60 €

  Scénario: US-05 — Nouvel arrêt pour une autre cause : la franchise s'applique
    Étant donné un arrêt précédent pour une autre cause terminé le "31/08/2026" avec 50 jours d'arrêt dont 20 jours indemnisés
    Et un arrêt de travail du "10/10/2026" au "29/10/2026" déclaré le "12/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "REJETE"
    Et la règle "RG-04" est appliquée

  Scénario: US-05 — Durée maximale d'indemnisation atteinte en cours d'arrêt
    Étant donné un arrêt précédent pour la même cause terminé le "30/09/2026" avec 1120 jours d'arrêt dont 1090 jours indemnisés
    Et un arrêt de travail du "10/10/2026" au "29/10/2026" déclaré le "12/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors la règle "RG-08" est appliquée
    Et 5 jours sont indemnisés pour un montant de 167,65 €

  Scénario: US-05 — Valeur limite : rechute 60 jours exactement après la reprise
    Étant donné un arrêt précédent pour la même cause terminé le "11/08/2026" avec 50 jours d'arrêt dont 20 jours indemnisés
    Et un arrêt de travail du "10/10/2026" au "29/10/2026" déclaré le "12/10/2026"
    Et toutes les pièces obligatoires
    Quand le dossier est évalué le "06/11/2026"
    Alors le dossier est "ACCEPTE"
    Et aucune franchise n'est appliquée
