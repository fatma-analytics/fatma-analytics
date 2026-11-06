from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)

BASE = {
    "date_debut_arret": "2026-08-03", "date_fin_arret": "2026-10-02", "date_declaration": "2026-08-20",
    "date_affiliation": "2019-04-01", "salaire_brut_12_mois": 36500, "ijss_journaliere": 41.47,
    "pieces": ["arret_travail", "attestation_salaire", "decompte_ijss"], "date_traitement": "2026-11-06",
}


def test_api_dossier_accepte():
    r = client.post("/sinistres/evaluation", json=BASE)
    assert r.status_code == 200
    b = r.json()
    assert b["statut"] == "ACCEPTE" and float(b["montant"]) == 1039.43


def test_api_piece_manquante():
    r = client.post("/sinistres/evaluation", json={**BASE, "pieces": ["arret_travail"]})
    assert r.json()["statut"] == "EN_ATTENTE_PIECES"
    assert r.json()["pieces_manquantes"] == ["attestation_salaire", "decompte_ijss"]


def test_api_donnee_invalide():
    r = client.post("/sinistres/evaluation", json={**BASE, "salaire_brut_12_mois": -10})
    assert r.status_code == 422
