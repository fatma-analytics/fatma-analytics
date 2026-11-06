-- =============================================================
-- Analyse de l'existant : sinistres arrêt de travail 2025
-- Table : sinistres (chargée depuis data/sinistres_2025.csv)
-- Exécution : python scripts/analyser_existant.py
-- =============================================================

-- A1 : volumétrie et issue des dossiers
SELECT statut_final,
       COUNT(*) AS nb_dossiers,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM sinistres
GROUP BY statut_final
ORDER BY nb_dossiers DESC;

-- A2 : délai de bout en bout décomposé par étape (dossiers payés, en jours calendaires)
SELECT ROUND(AVG(JULIANDAY(date_declaration)     - JULIANDAY(date_debut_arret)), 1)    AS declaration,
       ROUND(AVG(JULIANDAY(date_dossier_complet) - JULIANDAY(date_declaration)), 1)    AS completude,
       ROUND(AVG(JULIANDAY(date_decision)        - JULIANDAY(date_dossier_complet)), 1) AS instruction,
       ROUND(AVG(JULIANDAY(date_paiement)        - JULIANDAY(date_decision)), 1)       AS paiement,
       ROUND(AVG(JULIANDAY(date_paiement)        - JULIANDAY(date_declaration)), 1)    AS total_declaration_paiement
FROM sinistres
WHERE statut_final = 'PAYE';

-- A3 : dossiers incomplets à réception, par taille d'entreprise et canal
SELECT taille_entreprise,
       canal,
       COUNT(*) AS nb_dossiers,
       ROUND(100.0 * SUM(piece_manquante_initiale <> '') / COUNT(*), 1) AS pct_incomplets
FROM sinistres
GROUP BY taille_entreprise, canal
ORDER BY pct_incomplets DESC;

-- A4 : pièce manquante la plus fréquente
SELECT piece_manquante_initiale AS piece,
       COUNT(*) AS nb_dossiers,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_des_incomplets,
       ROUND(AVG(nb_relances), 2) AS relances_moyennes
FROM sinistres
WHERE piece_manquante_initiale <> ''
GROUP BY piece_manquante_initiale
ORDER BY nb_dossiers DESC;

-- A5 : motifs de rejet
SELECT motif_rejet,
       COUNT(*) AS nb_rejets,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_des_rejets
FROM sinistres
WHERE statut_final = 'REJETE'
GROUP BY motif_rejet
ORDER BY nb_rejets DESC;

-- A6 : impact des pièces manquantes sur le délai et les appels
SELECT CASE WHEN piece_manquante_initiale = '' THEN 'complet' ELSE 'incomplet' END AS dossier,
       COUNT(*) AS nb_dossiers,
       ROUND(AVG(JULIANDAY(date_dossier_complet) - JULIANDAY(date_declaration)), 1) AS jours_completude,
       ROUND(AVG(appels_service_client), 2) AS appels_moyens
FROM sinistres
GROUP BY dossier;

-- A7 : erreurs de calcul détectées en audit (dossiers payés)
SELECT COUNT(*) AS dossiers_payes,
       SUM(erreur_calcul_audit) AS erreurs,
       ROUND(100.0 * SUM(erreur_calcul_audit) / COUNT(*), 1) AS pct_erreurs,
       ROUND(SUM(montant_verse), 0) AS montant_total_verse
FROM sinistres
WHERE statut_final = 'PAYE';

-- A8 : répartition des durées d'arrêt (dimensionnement des règles)
SELECT CASE WHEN duree_arret_jours <= 30  THEN '1. 30 jours ou moins (franchise)'
            WHEN duree_arret_jours <= 90  THEN '2. 31 à 90 jours'
            WHEN duree_arret_jours <= 180 THEN '3. 91 à 180 jours'
            ELSE '4. plus de 180 jours (contrôle médical)' END AS tranche,
       COUNT(*) AS nb_dossiers,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM sinistres
GROUP BY tranche
ORDER BY tranche;
