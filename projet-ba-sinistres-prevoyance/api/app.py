"""
API d'évaluation d'un sinistre arrêt de travail (démonstration).

Lancer : uvicorn api.app:app --reload  ->  http://127.0.0.1:8000/docs
"""
from datetime import date
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from moteur.regles import ArretPrecedent, Declaration, evaluer

app = FastAPI(title="Sinistres prévoyance — API démo", version="1.0.0",
              description="Projet portfolio Business Analyst / AMOA. Données fictives.")


class ArretPrecedentIn(BaseModel):
    date_fin: date
    meme_cause: bool
    jours_arret_cumules: int = Field(ge=0)
    jours_indemnises_cumules: int = Field(ge=0)


class DeclarationIn(BaseModel):
    date_debut_arret: date
    date_fin_arret: date
    date_declaration: date
    date_affiliation: date
    date_radiation: Optional[date] = None
    salaire_brut_12_mois: Decimal = Field(gt=0)
    ijss_journaliere: Decimal = Field(ge=0)
    maintien_employeur_journalier: Decimal = Field(default=Decimal("0"), ge=0)
    pieces: list[str] = []
    arret_precedent: Optional[ArretPrecedentIn] = None
    date_traitement: date = Field(default_factory=date.today)


@app.post("/sinistres/evaluation")
def evaluation(d: DeclarationIn):
    ap = ArretPrecedent(**d.arret_precedent.model_dump()) if d.arret_precedent else None
    dec = evaluer(Declaration(
        date_debut_arret=d.date_debut_arret, date_fin_arret=d.date_fin_arret,
        date_declaration=d.date_declaration, date_affiliation=d.date_affiliation,
        date_radiation=d.date_radiation, salaire_brut_12_mois=d.salaire_brut_12_mois,
        ijss_journaliere=d.ijss_journaliere, maintien_employeur_journalier=d.maintien_employeur_journalier,
        pieces=set(d.pieces), arret_precedent=ap), d.date_traitement)
    return dec.__dict__
