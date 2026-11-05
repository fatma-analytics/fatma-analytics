"""
API de démonstration — Rachat partiel d'assurance vie en ligne.

Implémente les règles de gestion de la SFD (docs/03-specifications/sfd.md).
Chaque contrôle porte l'identifiant de sa règle (RG-xx) pour assurer la
traçabilité exigence -> code -> test.

Lancer :  uvicorn api.app:app --reload
Docs   :  http://127.0.0.1:8000/docs
"""
from __future__ import annotations

import os
import sqlite3
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------
# Paramètres métier (validés en atelier n°2 — voir compte rendu)
# ---------------------------------------------------------------
MONTANT_MIN = Decimal("500")              # RG-03
ENCOURS_RESIDUEL_MIN = Decimal("1500")    # RG-04
SEUIL_LCBFT_MONTANT = Decimal("50000")    # RG-07
SEUIL_LCBFT_NB_RACHATS = 3                # RG-07 (sur 12 mois glissants, demande incluse)
KYC_VALIDITE_MOIS = 36                    # RG-02
DELAI_PAIEMENT_JOURS_OUVRES = 3           # RG-10 (objectif interne, max légal 2 mois)


# ---------------------------------------------------------------
# Base de données
# ---------------------------------------------------------------
def init_db(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript((ROOT / "sql" / "seed.sql").read_text(encoding="utf-8"))
    conn.commit()
    return conn


app = FastAPI(
    title="Rachat partiel assurance vie — API démo",
    version="1.0.0",
    description="Projet portfolio Business Analyst / AMOA. Données fictives.",
)
app.state.db = init_db(os.getenv("RACHAT_DB", ":memory:"))
app.state.date_reference = date.fromisoformat(os.getenv("DATE_REFERENCE", "2026-11-05"))


def get_db(request: Request) -> sqlite3.Connection:
    return request.app.state.db


def today(request: Request) -> date:
    return request.app.state.date_reference


# ---------------------------------------------------------------
# Modèles
# ---------------------------------------------------------------
class LigneRepartition(BaseModel):
    id_support: str
    montant: Decimal = Field(gt=0)


class DemandeRachat(BaseModel):
    id_contrat: str
    montant: Decimal = Field(gt=0, description="Montant brut demandé en euros")
    iban: Optional[str] = Field(None, description="IBAN de versement (défaut : IBAN vérifié)")
    repartition: Optional[list[LigneRepartition]] = Field(
        None, description="Répartition par support ; absente = prorata (RG-05)"
    )


# ---------------------------------------------------------------
# Outils
# ---------------------------------------------------------------
def d2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def erreur(status: int, regle: str, message: str):
    raise HTTPException(status_code=status, detail={"regle": regle, "message": message})


def ajouter_mois(d: date, mois: int) -> date:
    m = d.month - 1 + mois
    y, m = d.year + m // 12, m % 12 + 1
    jours = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30,
             31, 31, 30, 31, 30, 31][m - 1]
    return date(y, m, min(d.day, jours))


def ajouter_jours_ouvres(d: date, n: int) -> date:
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def charger_contrat(db, id_contrat: str, id_client: str):
    contrat = db.execute("SELECT * FROM contrats WHERE id_contrat = ?", (id_contrat,)).fetchone()
    if contrat is None:
        erreur(404, "RG-01", "Contrat introuvable.")
    if contrat["id_client"] != id_client:
        erreur(403, "RG-01", "Ce contrat n'appartient pas au client connecté.")
    if contrat["statut"] != "ACTIF":
        erreur(422, "RG-01", "Le contrat n'est pas actif.")
    positions = db.execute(
        "SELECT p.id_support, s.libelle, s.type, p.valeur FROM positions p "
        "JOIN supports s USING (id_support) WHERE p.id_contrat = ? AND p.valeur > 0 "
        "ORDER BY p.id_support",
        (id_contrat,),
    ).fetchall()
    return contrat, positions


def valeur_totale(positions) -> Decimal:
    return sum((Decimal(str(p["valeur"])) for p in positions), Decimal("0"))


def capital_net(db, id_contrat: str) -> Decimal:
    """Versements - part de capital déjà rachetée (base du calcul RG-09)."""
    v = db.execute("SELECT COALESCE(SUM(montant),0) FROM versements WHERE id_contrat=?",
                   (id_contrat,)).fetchone()[0]
    r = db.execute(
        "SELECT COALESCE(SUM(montant - part_produits),0) FROM rachats "
        "WHERE id_contrat=? AND statut IN ('ACCEPTEE_AUTO','PAYEE')", (id_contrat,)
    ).fetchone()[0]
    return Decimal(str(v)) - Decimal(str(r))


def calculer_repartition(positions, montant: Decimal, demandee):
    """RG-05 : prorata par défaut, sinon répartition choisie et contrôlée."""
    valeurs = {p["id_support"]: Decimal(str(p["valeur"])) for p in positions}
    if demandee:
        lignes = {}
        for l in demandee:
            if l.id_support not in valeurs:
                erreur(422, "RG-05", f"Support {l.id_support} absent du contrat.")
            if l.montant > valeurs[l.id_support]:
                erreur(422, "RG-05", f"Montant supérieur à la valeur du support {l.id_support}.")
            lignes[l.id_support] = d2(l.montant)
        if sum(lignes.values()) != d2(montant):
            erreur(422, "RG-05", "La somme de la répartition doit être égale au montant demandé.")
        return lignes
    total = sum(valeurs.values())
    lignes, cumul = {}, Decimal("0")
    ids = list(valeurs)
    for i, s in enumerate(ids):
        part = d2(montant - cumul) if i == len(ids) - 1 else d2(montant * valeurs[s] / total)
        lignes[s] = part
        cumul += part
    return {s: m for s, m in lignes.items() if m > 0}


def evaluer(db, ref: date, id_client: str, demande: DemandeRachat):
    """Applique les règles dans l'ordre de la SFD (§4) et renvoie la décision."""
    contrat, positions = charger_contrat(db, demande.id_contrat, id_client)       # RG-01
    client = db.execute("SELECT * FROM clients WHERE id_client=?", (id_client,)).fetchone()
    montant = d2(demande.montant)
    total = valeur_totale(positions)

    # Contrôles bloquants (saisie)
    if montant < MONTANT_MIN:                                                      # RG-03
        erreur(422, "RG-03", f"Le montant minimum d'un rachat partiel est de {MONTANT_MIN} €.")
    if total - montant < ENCOURS_RESIDUEL_MIN:                                     # RG-04
        erreur(422, "RG-04",
               f"L'encours restant doit être d'au moins {ENCOURS_RESIDUEL_MIN} €. "
               f"Montant maximum possible : {d2(total - ENCOURS_RESIDUEL_MIN)} €.")
    lignes = calculer_repartition(positions, montant, demande.repartition)        # RG-05

    # RG-09 : quote-part de produits (gains) incluse dans le rachat
    gains = max(Decimal("0"), total - capital_net(db, demande.id_contrat))
    part_produits = d2(montant * gains / total) if total else Decimal("0")

    # Orientation du dossier
    iban = (demande.iban or client["iban_verifie"]).replace(" ", "").upper()
    depuis = ajouter_mois(ref, -12).isoformat()
    nb_rachats_12m = db.execute(
        "SELECT COUNT(*) FROM rachats WHERE id_contrat=? AND date_demande > ? AND statut <> 'REFUSEE'",
        (demande.id_contrat, depuis),
    ).fetchone()[0] + 1
    kyc_limite = ajouter_mois(date.fromisoformat(client["date_maj_kyc"]), KYC_VALIDITE_MOIS)

    if contrat["nanti"]:                                                           # RG-06
        statut, motif = "ORIENTEE_CONSEILLER", "Contrat nanti : accord du créancier nanti requis."
    elif ref > kyc_limite:                                                         # RG-02
        statut, motif = "EN_ATTENTE_PIECES", "Mise à jour KYC requise (justificatifs d'identité et de domicile)."
    elif montant >= SEUIL_LCBFT_MONTANT or nb_rachats_12m >= SEUIL_LCBFT_NB_RACHATS:  # RG-07
        statut, motif = "EN_CONTROLE_LCBFT", (
            f"Contrôle conformité : montant ≥ {SEUIL_LCBFT_MONTANT} €"
            if montant >= SEUIL_LCBFT_MONTANT else
            f"Contrôle conformité : {nb_rachats_12m} rachats sur 12 mois glissants")
    elif iban != client["iban_verifie"]:                                           # RG-08
        statut, motif = "EN_ATTENTE_PIECES", "Nouvel IBAN : RIB au nom du souscripteur à fournir."
    else:
        statut, motif = "ACCEPTEE_AUTO", None

    paiement = ajouter_jours_ouvres(ref, DELAI_PAIEMENT_JOURS_OUVRES) if statut == "ACCEPTEE_AUTO" else None  # RG-10
    return {
        "id_contrat": demande.id_contrat,
        "montant": montant,
        "repartition": [{"id_support": s, "montant": m} for s, m in lignes.items()],
        "valeur_rachat_avant": d2(total),
        "encours_residuel": d2(total - montant),
        "part_produits": part_produits,
        "part_capital": d2(montant - part_produits),
        "iban": iban,
        "statut": statut,
        "motif": motif,
        "date_paiement_prevue": paiement,
        "date_paiement_max_legale": ajouter_mois(ref, 2),                         # RG-10
    }


# ---------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/contrats/{id_contrat}")
def consulter_contrat(id_contrat: str, x_client_id: str = Header(...), db=Depends(get_db)):
    contrat, positions = charger_contrat(db, id_contrat, x_client_id)
    total = valeur_totale(positions)
    return {
        "id_contrat": contrat["id_contrat"],
        "produit": contrat["produit"],
        "nanti": bool(contrat["nanti"]),
        "valeur_rachat": d2(total),
        "montant_max_rachat_partiel": d2(max(Decimal("0"), total - ENCOURS_RESIDUEL_MIN)),
        "supports": [dict(p) for p in positions],
    }


@app.post("/rachats/simulation")
def simuler(demande: DemandeRachat, request: Request, x_client_id: str = Header(...), db=Depends(get_db)):
    """US-02 : simulation sans engagement, sans authentification forte."""
    return evaluer(db, today(request), x_client_id, demande)


@app.post("/rachats", status_code=201)
def demander(
    demande: DemandeRachat,
    request: Request,
    x_client_id: str = Header(...),
    x_otp_valide: Optional[str] = Header(None),
    db=Depends(get_db),
):
    """US-05 : enregistrement de la demande après authentification forte (RG-11)."""
    if x_otp_valide != "true":
        erreur(401, "RG-11", "Authentification forte requise pour valider la demande.")
    ref = today(request)
    r = evaluer(db, ref, x_client_id, demande)
    cur = db.execute(
        "INSERT INTO rachats (id_contrat, date_demande, montant, iban, statut, motif, part_produits, date_paiement_prevue) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (r["id_contrat"], ref.isoformat(), float(r["montant"]), r["iban"], r["statut"], r["motif"],
         float(r["part_produits"]), r["date_paiement_prevue"].isoformat() if r["date_paiement_prevue"] else None),
    )
    id_rachat = cur.lastrowid
    for l in r["repartition"]:
        db.execute("INSERT INTO rachat_lignes VALUES (?,?,?)", (id_rachat, l["id_support"], float(l["montant"])))
        if r["statut"] == "ACCEPTEE_AUTO":   # désinvestissement immédiat des supports
            db.execute("UPDATE positions SET valeur = valeur - ? WHERE id_contrat=? AND id_support=?",
                       (float(l["montant"]), r["id_contrat"], l["id_support"]))
    db.commit()
    return {"id_rachat": id_rachat, **r}


@app.get("/rachats/{id_rachat}")
def suivre(id_rachat: int, x_client_id: str = Header(...), db=Depends(get_db)):
    """US-06 : suivi de la demande."""
    row = db.execute(
        "SELECT r.*, c.id_client FROM rachats r JOIN contrats c USING (id_contrat) WHERE id_rachat=?",
        (id_rachat,),
    ).fetchone()
    if row is None:
        erreur(404, "RG-01", "Demande introuvable.")
    if row["id_client"] != x_client_id:
        erreur(403, "RG-01", "Cette demande n'appartient pas au client connecté.")
    lignes = db.execute("SELECT id_support, montant FROM rachat_lignes WHERE id_rachat=?", (id_rachat,)).fetchall()
    out = {k: row[k] for k in row.keys() if k != "id_client"}
    out["repartition"] = [dict(l) for l in lignes]
    return out
