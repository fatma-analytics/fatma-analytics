-- =============================================================
-- Jeu de données de recette (personas fictifs)
-- Date de référence de la recette : 2026-11-05
-- =============================================================

INSERT INTO supports (id_support, libelle, type) VALUES
    ('EURO-01', 'Fonds en euros Sécurité',      'EURO'),
    ('UC-ACT',  'UC Actions Europe',            'UC'),
    ('UC-OBL',  'UC Obligations Monde',         'UC');

-- P1 Claire  : cas nominal
-- P2 Karim   : gros encours -> seuil LCB-FT
-- P3 Sophie  : contrat nanti -> orientation conseiller
-- P4 Lucas   : KYC périmé (> 36 mois)
-- P5 Emma    : 2 rachats sur 12 mois -> le 3e déclenche LCB-FT
INSERT INTO clients (id_client, nom, prenom, date_maj_kyc, iban_verifie) VALUES
    ('C001', 'Martin', 'Claire', '2025-06-12', 'FR7630006000011234567890189'),
    ('C002', 'Benali', 'Karim',  '2025-02-03', 'FR7610107001011234567890129'),
    ('C003', 'Durand', 'Sophie', '2024-09-20', 'FR7620041010050500013M02606'),
    ('C004', 'Petit',  'Lucas',  '2022-01-15', 'FR7612739000304567891234567'),
    ('C005', 'Leroy',  'Emma',   '2026-01-08', 'FR7630004000031234567890143');

INSERT INTO contrats (id_contrat, id_client, produit, date_souscription, statut, nanti) VALUES
    ('CT-1001', 'C001', 'Assur''Vie Démo Multisupport', '2016-03-01', 'ACTIF', 0),
    ('CT-1002', 'C002', 'Assur''Vie Démo Multisupport', '2012-05-14', 'ACTIF', 0),
    ('CT-1003', 'C003', 'Assur''Vie Démo Multisupport', '2019-11-02', 'ACTIF', 1),
    ('CT-1004', 'C004', 'Assur''Vie Démo Multisupport', '2018-07-23', 'ACTIF', 0),
    ('CT-1005', 'C005', 'Assur''Vie Démo Multisupport', '2020-02-10', 'ACTIF', 0);

INSERT INTO positions (id_contrat, id_support, valeur) VALUES
    ('CT-1001', 'EURO-01', 25000), ('CT-1001', 'UC-ACT', 15000),
    ('CT-1002', 'EURO-01', 80000), ('CT-1002', 'UC-ACT', 30000), ('CT-1002', 'UC-OBL', 10000),
    ('CT-1003', 'EURO-01', 18000),
    ('CT-1004', 'EURO-01', 12000), ('CT-1004', 'UC-OBL', 3000),
    ('CT-1005', 'EURO-01', 20000), ('CT-1005', 'UC-ACT', 6000);

INSERT INTO versements (id_contrat, date_versement, montant) VALUES
    ('CT-1001', '2016-03-01', 20000), ('CT-1001', '2020-01-15', 10000),
    ('CT-1002', '2012-05-14', 100000),
    ('CT-1003', '2019-11-02', 16000),
    ('CT-1004', '2018-07-23', 14000),
    ('CT-1005', '2020-02-10', 28000);

-- Historique : Emma a déjà fait 2 rachats sur les 12 derniers mois
INSERT INTO rachats (id_contrat, date_demande, montant, iban, statut, motif, part_produits, date_paiement_prevue) VALUES
    ('CT-1005', '2026-02-10', 1000, 'FR7630004000031234567890143', 'PAYEE', NULL, 0, '2026-02-13'),
    ('CT-1005', '2026-07-01', 1000, 'FR7630004000031234567890143', 'PAYEE', NULL, 0, '2026-07-06');
INSERT INTO rachat_lignes (id_rachat, id_support, montant) VALUES
    (1, 'EURO-01', 1000), (2, 'EURO-01', 1000);
