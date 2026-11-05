-- =============================================================
-- Contrôles SQL de recette
-- Chaque requête de contrôle doit renvoyer 0 ligne.
-- Une ligne renvoyée = une anomalie à ouvrir dans Jira.
-- =============================================================

-- CTRL-01 (RG-07) : aucun rachat ≥ 50 000 € ne doit être accepté automatiquement
SELECT id_rachat, id_contrat, montant, statut
FROM rachats
WHERE statut = 'ACCEPTEE_AUTO'
  AND montant >= 50000;

-- CTRL-02 (RG-06) : aucun rachat accepté automatiquement sur un contrat nanti
SELECT r.id_rachat, r.id_contrat, r.statut
FROM rachats r
JOIN contrats c ON c.id_contrat = r.id_contrat
WHERE r.statut = 'ACCEPTEE_AUTO'
  AND c.nanti = 1;

-- CTRL-03 (RG-05) : la somme des lignes par support doit égaler le montant du rachat
SELECT r.id_rachat, r.montant, SUM(l.montant) AS total_lignes
FROM rachats r
JOIN rachat_lignes l ON l.id_rachat = r.id_rachat
GROUP BY r.id_rachat, r.montant
HAVING ROUND(SUM(l.montant), 2) <> ROUND(r.montant, 2);

-- CTRL-04 (RG-08) : aucun rachat accepté automatiquement vers un IBAN non vérifié
SELECT r.id_rachat, r.iban, cl.iban_verifie
FROM rachats r
JOIN contrats c  ON c.id_contrat = r.id_contrat
JOIN clients cl  ON cl.id_client = c.id_client
WHERE r.statut = 'ACCEPTEE_AUTO'
  AND r.iban <> cl.iban_verifie;

-- CTRL-05 (RG-04) : aucun contrat actif ne doit passer sous 1 500 € après un rachat accepté
SELECT p.id_contrat, SUM(p.valeur) AS encours
FROM positions p
JOIN contrats c ON c.id_contrat = p.id_contrat
WHERE c.statut = 'ACTIF'
  AND EXISTS (SELECT 1 FROM rachats r
              WHERE r.id_contrat = p.id_contrat AND r.statut = 'ACCEPTEE_AUTO')
GROUP BY p.id_contrat
HAVING SUM(p.valeur) < 1500;

-- CTRL-06 (RG-10) : date de paiement prévue au plus tard 2 mois après la demande
SELECT id_rachat, date_demande, date_paiement_prevue
FROM rachats
WHERE date_paiement_prevue > DATE(date_demande, '+2 months');

-- CTRL-07 (RG-02) : aucun rachat accepté automatiquement avec un KYC de plus de 36 mois
SELECT r.id_rachat, cl.id_client, cl.date_maj_kyc
FROM rachats r
JOIN contrats c ON c.id_contrat = r.id_contrat
JOIN clients cl ON cl.id_client = c.id_client
WHERE r.statut = 'ACCEPTEE_AUTO'
  AND cl.date_maj_kyc < DATE(r.date_demande, '-36 months');


-- =============================================================
-- Requêtes de pilotage (comités de suivi / support post-déploiement)
-- =============================================================

-- PIL-01 : répartition des demandes par statut (taux d'automatisation)
SELECT statut,
       COUNT(*) AS nb_demandes,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM rachats
GROUP BY statut
ORDER BY nb_demandes DESC;

-- PIL-02 : montant moyen et total racheté par mois
SELECT STRFTIME('%Y-%m', date_demande) AS mois,
       COUNT(*)                        AS nb_demandes,
       ROUND(AVG(montant), 0)          AS montant_moyen,
       ROUND(SUM(montant), 0)          AS montant_total
FROM rachats
GROUP BY mois
ORDER BY mois;

-- PIL-03 : file de travail des gestionnaires (dossiers non automatiques)
SELECT r.id_rachat, r.date_demande, r.id_contrat, r.montant, r.statut, r.motif
FROM rachats r
WHERE r.statut IN ('EN_CONTROLE_LCBFT', 'EN_ATTENTE_PIECES', 'ORIENTEE_CONSEILLER')
ORDER BY r.date_demande;
