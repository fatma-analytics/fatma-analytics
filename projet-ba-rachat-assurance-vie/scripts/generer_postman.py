"""Génère la collection Postman (format v2.1) à partir des cas de recette API."""
import json
from pathlib import Path

CAS = [
    # (id, titre, méthode, chemin, client, otp, corps, statut HTTP attendu, statut métier attendu)
    ("CT-01", "Simulation 5 000 € au prorata", "POST", "/rachats/simulation", "C001", False,
     {"id_contrat": "CT-1001", "montant": 5000}, 200, "ACCEPTEE_AUTO"),
    ("CT-02", "Demande acceptée automatiquement", "POST", "/rachats", "C001", True,
     {"id_contrat": "CT-1001", "montant": 5000}, 201, "ACCEPTEE_AUTO"),
    ("CT-06", "Montant < 500 € (RG-03)", "POST", "/rachats", "C001", True,
     {"id_contrat": "CT-1001", "montant": 400}, 422, None),
    ("CT-07", "Encours résiduel < 1 500 € (RG-04)", "POST", "/rachats", "C001", True,
     {"id_contrat": "CT-1001", "montant": 39000}, 422, None),
    ("CT-11", "Seuil LCB-FT montant (RG-07)", "POST", "/rachats", "C002", True,
     {"id_contrat": "CT-1002", "montant": 60000}, 201, "EN_CONTROLE_LCBFT"),
    ("CT-12", "Seuil LCB-FT fréquence (RG-07)", "POST", "/rachats", "C005", True,
     {"id_contrat": "CT-1005", "montant": 1000}, 201, "EN_CONTROLE_LCBFT"),
    ("CT-13", "Contrat nanti (RG-06)", "POST", "/rachats", "C003", True,
     {"id_contrat": "CT-1003", "montant": 2000}, 201, "ORIENTEE_CONSEILLER"),
    ("CT-14", "KYC périmé (RG-02)", "POST", "/rachats", "C004", True,
     {"id_contrat": "CT-1004", "montant": 2000}, 201, "EN_ATTENTE_PIECES"),
    ("CT-15", "Nouvel IBAN (RG-08)", "POST", "/rachats", "C001", True,
     {"id_contrat": "CT-1001", "montant": 2000, "iban": "FR7612345000000000000000185"}, 201, "EN_ATTENTE_PIECES"),
    ("CT-17", "Sans authentification forte (RG-11)", "POST", "/rachats", "C001", False,
     {"id_contrat": "CT-1001", "montant": 1000}, 401, None),
    ("CT-18", "Contrat d'un autre client", "POST", "/rachats", "C001", True,
     {"id_contrat": "CT-1002", "montant": 1000}, 403, None),
]


def item(cas):
    cid, titre, methode, chemin, client, otp, corps, http, statut = cas
    headers = [{"key": "X-Client-Id", "value": client}, {"key": "Content-Type", "value": "application/json"}]
    if otp:
        headers.append({"key": "X-OTP-Valide", "value": "true"})
    tests = [f'pm.test("{cid} — code HTTP {http}", () => pm.response.to.have.status({http}));']
    if statut:
        tests.append(f'pm.test("{cid} — statut {statut}", () => '
                     f'pm.expect(pm.response.json().statut).to.eql("{statut}"));')
    return {
        "name": f"{cid} — {titre}",
        "request": {
            "method": methode,
            "header": headers,
            "body": {"mode": "raw", "raw": json.dumps(corps, ensure_ascii=False, indent=2)},
            "url": {"raw": "{{base_url}}" + chemin, "host": ["{{base_url}}"], "path": chemin.strip("/").split("/")},
        },
        "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": tests}}],
    }


collection = {
    "info": {
        "name": "Rachat partiel assurance vie — Recette API",
        "description": "Cas de recette API (voir docs/05-recette/cahier-de-recette.md). "
                       "Relancer l'API entre deux exécutions pour repartir du jeu de données initial.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "variable": [{"key": "base_url", "value": "http://127.0.0.1:8000"}],
    "item": [
        {"name": "Consultation", "item": [{
            "name": "Consulter le contrat CT-1001",
            "request": {"method": "GET", "header": [{"key": "X-Client-Id", "value": "C001"}],
                        "url": {"raw": "{{base_url}}/contrats/CT-1001", "host": ["{{base_url}}"],
                                "path": ["contrats", "CT-1001"]}},
            "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": [
                'pm.test("Code 200", () => pm.response.to.have.status(200));',
                'pm.test("Valeur de rachat 40 000 €", () => pm.expect(Number(pm.response.json().valeur_rachat)).to.eql(40000));']}}],
        }]},
        {"name": "Cas de recette", "item": [item(c) for c in CAS]},
    ],
}

out = Path(__file__).resolve().parent.parent / "postman" / "rachat-assurance-vie.postman_collection.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(collection, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Collection écrite : {out}")
