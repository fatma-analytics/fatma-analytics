-- =============================================================
-- Schéma de démonstration : rachat partiel d'assurance vie
-- Compatible SQLite (et transposable PostgreSQL / Snowflake)
-- =============================================================

DROP TABLE IF EXISTS rachat_lignes;
DROP TABLE IF EXISTS rachats;
DROP TABLE IF EXISTS versements;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS supports;
DROP TABLE IF EXISTS contrats;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id_client       TEXT PRIMARY KEY,
    nom             TEXT NOT NULL,
    prenom          TEXT NOT NULL,
    date_maj_kyc    DATE NOT NULL,          -- dernière mise à jour de la connaissance client
    iban_verifie    TEXT NOT NULL           -- IBAN déjà contrôlé par la conformité
);

CREATE TABLE contrats (
    id_contrat        TEXT PRIMARY KEY,
    id_client         TEXT NOT NULL REFERENCES clients(id_client),
    produit           TEXT NOT NULL,
    date_souscription DATE NOT NULL,
    statut            TEXT NOT NULL CHECK (statut IN ('ACTIF', 'CLOS')),
    nanti             INTEGER NOT NULL DEFAULT 0 CHECK (nanti IN (0, 1))  -- contrat donné en garantie
);

CREATE TABLE supports (
    id_support  TEXT PRIMARY KEY,
    libelle     TEXT NOT NULL,
    type        TEXT NOT NULL CHECK (type IN ('EURO', 'UC'))  -- fonds en euros ou unité de compte
);

CREATE TABLE positions (
    id_contrat  TEXT NOT NULL REFERENCES contrats(id_contrat),
    id_support  TEXT NOT NULL REFERENCES supports(id_support),
    valeur      NUMERIC NOT NULL CHECK (valeur >= 0),
    PRIMARY KEY (id_contrat, id_support)
);

CREATE TABLE versements (
    id_versement  INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contrat    TEXT NOT NULL REFERENCES contrats(id_contrat),
    date_versement DATE NOT NULL,
    montant       NUMERIC NOT NULL CHECK (montant > 0)
);

CREATE TABLE rachats (
    id_rachat           INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contrat          TEXT NOT NULL REFERENCES contrats(id_contrat),
    date_demande        DATE NOT NULL,
    montant             NUMERIC NOT NULL,
    iban                TEXT NOT NULL,
    statut              TEXT NOT NULL CHECK (statut IN (
                            'ACCEPTEE_AUTO', 'EN_CONTROLE_LCBFT', 'EN_ATTENTE_PIECES',
                            'ORIENTEE_CONSEILLER', 'PAYEE', 'REFUSEE')),
    motif               TEXT,
    part_produits       NUMERIC NOT NULL DEFAULT 0,   -- quote-part de gains (base fiscale estimée)
    date_paiement_prevue DATE
);

CREATE TABLE rachat_lignes (
    id_rachat   INTEGER NOT NULL REFERENCES rachats(id_rachat),
    id_support  TEXT NOT NULL REFERENCES supports(id_support),
    montant     NUMERIC NOT NULL CHECK (montant > 0),
    PRIMARY KEY (id_rachat, id_support)
);
