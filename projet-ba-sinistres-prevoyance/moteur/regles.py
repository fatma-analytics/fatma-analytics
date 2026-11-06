"""
Moteur de règles — sinistres arrêt de travail (prévoyance collective).

Traduction directe des règles RG-01 à RG-11 de la SFD
(docs/04-specifications/sfd.md). Les paramètres sont illustratifs
(contrat fictif « Prévoyance Démo »).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

# Paramètres du contrat (validés en atelier 2)
DELAI_DECLARATION_JOURS = 90        # RG-02
PIECES_OBLIGATOIRES = ("arret_travail", "attestation_salaire", "decompte_ijss")  # RG-03
FRANCHISE_JOURS = 30                # RG-04
DELAI_RECHUTE_JOURS = 60            # RG-05
TAUX_GARANTIE = Decimal("0.75")     # RG-06 : 75 % du salaire brut de référence
TAUX_NET = Decimal("0.78")          # RG-07 : salaire net de référence = 78 % du brut
DUREE_MAX_JOURS = 1095              # RG-08
SEUIL_CONTROLE_MEDICAL = 180        # RG-09
CARENCE_AFFILIATION_JOURS = 30      # RG-10
DELAI_PAIEMENT_JOURS_OUVRES = 10    # RG-11


@dataclass
class ArretPrecedent:
    date_fin: date
    meme_cause: bool
    jours_arret_cumules: int        # durée totale des arrêts précédents liés
    jours_indemnises_cumules: int


@dataclass
class Declaration:
    date_debut_arret: date
    date_fin_arret: date
    date_declaration: date
    date_affiliation: date
    salaire_brut_12_mois: Decimal
    ijss_journaliere: Decimal
    pieces: set[str] = field(default_factory=set)
    date_radiation: Optional[date] = None
    maintien_employeur_journalier: Decimal = Decimal("0")
    arret_precedent: Optional[ArretPrecedent] = None


@dataclass
class Decision:
    statut: str
    regles: list[str]
    motif: Optional[str] = None
    pieces_manquantes: list[str] = field(default_factory=list)
    rechute: bool = False
    jours_arret: int = 0
    jours_franchise: int = 0
    jours_indemnisables: int = 0
    sjr_brut: Decimal = Decimal("0")
    ij_complementaire: Decimal = Decimal("0")
    ecretement: bool = False
    montant: Decimal = Decimal("0")
    date_paiement_prevue: Optional[date] = None


def d2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def jours_ouvres(d: date, n: int) -> date:
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def calculer_ij(dec: Declaration) -> tuple[Decimal, Decimal, bool]:
    """RG-06 et RG-07 : indemnité journalière complémentaire, écrêtée au net."""
    sjr = d2(dec.salaire_brut_12_mois / Decimal(365))
    ij = max(Decimal("0"), d2(TAUX_GARANTIE * sjr - dec.ijss_journaliere))
    plafond = d2(TAUX_NET * sjr - dec.ijss_journaliere - dec.maintien_employeur_journalier)
    if ij > plafond:
        return sjr, max(Decimal("0"), plafond), True
    return sjr, ij, False


def evaluer(dec: Declaration, date_traitement: date) -> Decision:
    regles: list[str] = []
    jours_arret = (dec.date_fin_arret - dec.date_debut_arret).days + 1

    # RG-01 : affiliation à la date de début de l'arrêt
    affilie = dec.date_affiliation <= dec.date_debut_arret and (
        dec.date_radiation is None or dec.date_radiation >= dec.date_debut_arret)
    if not affilie:
        return Decision("REJETE", ["RG-01"], "Salarié non affilié à la date de début de l'arrêt.",
                        jours_arret=jours_arret)

    # RG-05 : rechute (même cause, reprise de moins de 60 jours) -> pas de nouvelle franchise
    ap = dec.arret_precedent
    rechute = bool(ap and ap.meme_cause
                   and (dec.date_debut_arret - ap.date_fin).days <= DELAI_RECHUTE_JOURS)
    if rechute:
        regles.append("RG-05")
    franchise = 0 if rechute else FRANCHISE_JOURS
    deja_indemnises = ap.jours_indemnises_cumules if rechute else 0
    arret_cumule = jours_arret + (ap.jours_arret_cumules if rechute else 0)

    # RG-04 : franchise non atteinte
    if jours_arret <= franchise:
        return Decision("REJETE", regles + ["RG-04"],
                        f"Arrêt de {jours_arret} jours : la franchise de {FRANCHISE_JOURS} jours n'est pas dépassée.",
                        jours_arret=jours_arret, jours_franchise=franchise)

    # RG-06 / RG-07 / RG-08 : calcul
    sjr, ij, ecrete = calculer_ij(dec)
    regles += ["RG-06"] + (["RG-07"] if ecrete else [])
    indemnisables = jours_arret - franchise
    if deja_indemnises + indemnisables > DUREE_MAX_JOURS:
        indemnisables = max(0, DUREE_MAX_JOURS - deja_indemnises)
        regles.append("RG-08")
    montant = d2(ij * indemnisables)
    base = dict(rechute=rechute, jours_arret=jours_arret, jours_franchise=franchise,
                jours_indemnisables=indemnisables, sjr_brut=sjr, ij_complementaire=ij,
                ecretement=ecrete, montant=montant)

    # Orientation (la première règle qui s'applique l'emporte)
    manquantes = [p for p in PIECES_OBLIGATOIRES if p not in dec.pieces]
    if manquantes:                                                                      # RG-03
        return Decision("EN_ATTENTE_PIECES", regles + ["RG-03"], "Pièces obligatoires manquantes.",
                        pieces_manquantes=manquantes, **base)
    if (dec.date_declaration - dec.date_debut_arret).days > DELAI_DECLARATION_JOURS:   # RG-02
        return Decision("A_ETUDIER", regles + ["RG-02"],
                        f"Déclaration au-delà de {DELAI_DECLARATION_JOURS} jours : justification à examiner.", **base)
    if (dec.date_debut_arret - dec.date_affiliation).days < CARENCE_AFFILIATION_JOURS:  # RG-10
        return Decision("CONTROLE_GESTIONNAIRE", regles + ["RG-10"],
                        "Arrêt débutant moins de 30 jours après l'affiliation : contrôle de vigilance.", **base)
    if arret_cumule > SEUIL_CONTROLE_MEDICAL:                                           # RG-09
        return Decision("EN_CONTROLE_MEDICAL", regles + ["RG-09"],
                        f"Arrêt cumulé de {arret_cumule} jours : expertise médicale requise.", **base)
    if indemnisables == 0:                                                              # RG-08
        return Decision("REJETE", regles, "Durée maximale d'indemnisation atteinte.", **base)

    return Decision("ACCEPTE", regles + ["RG-11"], None,
                    date_paiement_prevue=jours_ouvres(date_traitement, DELAI_PAIEMENT_JOURS_OUVRES), **base)
