"""
Recette automatisée — chaque test correspond à un cas du cahier de recette
(docs/05-recette/cahier-de-recette.md). Date de référence : 2026-11-05.

Lancer : pytest -v
"""
import pytest
from fastapi.testclient import TestClient

from api.app import app, init_db

OTP = {"X-OTP-Valide": "true"}


@pytest.fixture(autouse=True)
def base_propre():
    app.state.db = init_db()
    yield


@pytest.fixture
def api():
    return TestClient(app)


def h(client_id, otp=True):
    return {"X-Client-Id": client_id, **(OTP if otp else {})}


# ---------- Cas nominaux ----------------------------------------------------

def test_CT01_simulation_prorata_et_fiscalite(api):
    """US-02 / RG-05 / RG-09 : simulation de 5 000 € au prorata."""
    r = api.post("/rachats/simulation", json={"id_contrat": "CT-1001", "montant": 5000}, headers=h("C001", otp=False))
    assert r.status_code == 200
    b = r.json()
    assert {l["id_support"]: float(l["montant"]) for l in b["repartition"]} == {"EURO-01": 3125.0, "UC-ACT": 1875.0}
    assert float(b["part_produits"]) == 1250.0      # gains 10 000 / valeur 40 000 = 25 %
    assert float(b["encours_residuel"]) == 35000.0
    assert b["statut"] == "ACCEPTEE_AUTO"


def test_CT02_demande_acceptee_automatiquement(api):
    """US-05 / RG-10 : acceptation auto, paiement prévu à J+3 ouvrés."""
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 5000}, headers=h("C001"))
    assert r.status_code == 201
    b = r.json()
    assert b["statut"] == "ACCEPTEE_AUTO"
    assert b["date_paiement_prevue"] == "2026-11-10"
    assert b["date_paiement_max_legale"] == "2027-01-05"


def test_CT03_desinvestissement_des_supports(api):
    """Après acceptation, la valeur de rachat du contrat diminue du montant racheté."""
    api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 5000}, headers=h("C001"))
    c = api.get("/contrats/CT-1001", headers=h("C001")).json()
    assert float(c["valeur_rachat"]) == 35000.0


def test_CT04_repartition_choisie(api):
    """RG-05 : le client choisit de racheter uniquement sur le fonds en euros."""
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 2000,
                                   "repartition": [{"id_support": "EURO-01", "montant": 2000}]}, headers=h("C001"))
    assert r.status_code == 201
    assert [(l["id_support"], float(l["montant"])) for l in r.json()["repartition"]] == [("EURO-01", 2000.0)]


def test_CT05_suivi_de_la_demande(api):
    """US-06 : le client retrouve sa demande et son statut."""
    id_r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 1000}, headers=h("C001")).json()["id_rachat"]
    r = api.get(f"/rachats/{id_r}", headers=h("C001"))
    assert r.status_code == 200 and r.json()["statut"] == "ACCEPTEE_AUTO"


# ---------- Cas limites -----------------------------------------------------

def test_CT06_montant_inferieur_au_minimum(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 400}, headers=h("C001"))
    assert r.status_code == 422 and r.json()["detail"]["regle"] == "RG-03"


def test_CT07_encours_residuel_insuffisant(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 39000}, headers=h("C001"))
    assert r.status_code == 422 and r.json()["detail"]["regle"] == "RG-04"
    assert "38500.00" in r.json()["detail"]["message"]


def test_CT08_montant_maximum_exact(api):
    """Valeur limite : 40 000 - 1 500 = 38 500 € est autorisé."""
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 38500}, headers=h("C001"))
    assert r.status_code == 201 and float(r.json()["encours_residuel"]) == 1500.0


def test_CT09_repartition_incoherente(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 3000,
                                   "repartition": [{"id_support": "EURO-01", "montant": 2000}]}, headers=h("C001"))
    assert r.status_code == 422 and r.json()["detail"]["regle"] == "RG-05"


def test_CT10_support_insuffisant(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 16000,
                                   "repartition": [{"id_support": "UC-ACT", "montant": 16000}]}, headers=h("C001"))
    assert r.status_code == 422 and r.json()["detail"]["regle"] == "RG-05"


# ---------- Orientation du dossier (conformité / risques) -------------------

def test_CT11_seuil_lcbft_montant(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1002", "montant": 60000}, headers=h("C002"))
    assert r.json()["statut"] == "EN_CONTROLE_LCBFT"
    assert r.json()["date_paiement_prevue"] is None


def test_CT12_seuil_lcbft_frequence(api):
    """Emma : 2 rachats sur 12 mois, le 3e déclenche le contrôle."""
    r = api.post("/rachats", json={"id_contrat": "CT-1005", "montant": 1000}, headers=h("C005"))
    assert r.json()["statut"] == "EN_CONTROLE_LCBFT"


def test_CT13_contrat_nanti(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1003", "montant": 2000}, headers=h("C003"))
    assert r.json()["statut"] == "ORIENTEE_CONSEILLER"


def test_CT14_kyc_perime(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1004", "montant": 2000}, headers=h("C004"))
    assert r.json()["statut"] == "EN_ATTENTE_PIECES" and "KYC" in r.json()["motif"]


def test_CT15_nouvel_iban(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 2000,
                                   "iban": "FR76 1234 5000 0000 0000 0000 185"}, headers=h("C001"))
    assert r.json()["statut"] == "EN_ATTENTE_PIECES" and "IBAN" in r.json()["motif"]


def test_CT16_pas_de_desinvestissement_si_non_accepte(api):
    api.post("/rachats", json={"id_contrat": "CT-1002", "montant": 60000}, headers=h("C002"))
    assert float(api.get("/contrats/CT-1002", headers=h("C002")).json()["valeur_rachat"]) == 120000.0


# ---------- Sécurité --------------------------------------------------------

def test_CT17_authentification_forte_obligatoire(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1001", "montant": 1000}, headers=h("C001", otp=False))
    assert r.status_code == 401 and r.json()["detail"]["regle"] == "RG-11"


def test_CT18_contrat_d_un_autre_client(api):
    r = api.post("/rachats", json={"id_contrat": "CT-1002", "montant": 1000}, headers=h("C001"))
    assert r.status_code == 403


def test_CT19_contrat_inexistant(api):
    r = api.get("/contrats/CT-9999", headers=h("C001"))
    assert r.status_code == 404
