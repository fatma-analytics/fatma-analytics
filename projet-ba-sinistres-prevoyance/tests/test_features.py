"""
User stories exécutables : les scénarios Gherkin de features/*.feature
sont joués contre le moteur de règles (documentation vivante).

Lancer : pytest -v
"""
from datetime import date, datetime
from decimal import Decimal

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from moteur.regles import PIECES_OBLIGATOIRES, ArretPrecedent, Declaration, evaluer

scenarios("../features")


def dt(s: str) -> date:
    return datetime.strptime(s, "%d/%m/%Y").date()


def eur(s: str) -> Decimal:
    return Decimal(s.replace(",", ".").replace(" ", ""))


@pytest.fixture
def ctx():
    return {"pieces": set(), "maintien": Decimal("0"), "radiation": None, "precedent": None}


@given(parsers.parse('un salarié affilié depuis le "{d}" avec un salaire brut annuel de {s} €'))
def affilie(ctx, d, s):
    ctx["affiliation"], ctx["salaire"] = dt(d), eur(s)


@given(parsers.parse('un salarié radié le "{d}"'))
def radie(ctx, d):
    ctx["radiation"] = dt(d)


@given(parsers.parse("des indemnités journalières de la Sécurité sociale de {x} € par jour"))
def ijss(ctx, x):
    ctx["ijss"] = eur(x)


@given(parsers.parse("un maintien de salaire par l'employeur de {x} € par jour"))
def maintien(ctx, x):
    ctx["maintien"] = eur(x)


@given(parsers.parse('un arrêt de travail du "{d1}" au "{d2}" déclaré le "{d3}"'))
def arret(ctx, d1, d2, d3):
    ctx["debut"], ctx["fin"], ctx["declaration"] = dt(d1), dt(d2), dt(d3)


@given("toutes les pièces obligatoires")
def toutes_pieces(ctx):
    ctx["pieces"] = set(PIECES_OBLIGATOIRES)


@given(parsers.parse('toutes les pièces sauf "{p}"'))
def pieces_sauf(ctx, p):
    ctx["pieces"] = set(PIECES_OBLIGATOIRES) - {p}


@given(parsers.re(r'un arrêt précédent pour (?P<cause>la même cause|une autre cause) terminé le "(?P<d>[^"]+)" '
                  r"avec (?P<a>\d+) jours d'arrêt dont (?P<i>\d+) jours indemnisés"))
def precedent(ctx, cause, d, a, i):
    ctx["precedent"] = ArretPrecedent(dt(d), cause == "la même cause", int(a), int(i))


@when(parsers.parse('le dossier est évalué le "{d}"'))
def evaluation(ctx, d):
    ctx["decision"] = evaluer(Declaration(
        date_debut_arret=ctx["debut"], date_fin_arret=ctx["fin"], date_declaration=ctx["declaration"],
        date_affiliation=ctx["affiliation"], date_radiation=ctx["radiation"],
        salaire_brut_12_mois=ctx["salaire"], ijss_journaliere=ctx["ijss"],
        maintien_employeur_journalier=ctx["maintien"], pieces=ctx["pieces"],
        arret_precedent=ctx["precedent"]), dt(d))


@then(parsers.parse('le dossier est "{statut}"'))
def statut(ctx, statut):
    assert ctx["decision"].statut == statut


@then(parsers.parse('la règle "{rg}" est appliquée'))
def regle(ctx, rg):
    assert rg in ctx["decision"].regles


@then(parsers.parse("l'indemnité journalière complémentaire est de {x} €"))
def ij(ctx, x):
    assert ctx["decision"].ij_complementaire == eur(x)


@then(parsers.parse("{n:d} jours sont indemnisés pour un montant de {x} €"))
def montant(ctx, n, x):
    assert ctx["decision"].jours_indemnisables == n
    assert ctx["decision"].montant == eur(x)


@then(parsers.parse('le paiement est prévu le "{d}"'))
def paiement(ctx, d):
    assert ctx["decision"].date_paiement_prevue == dt(d)


@then(parsers.parse('la pièce manquante signalée est "{p}"'))
def piece(ctx, p):
    assert ctx["decision"].pieces_manquantes == [p]


@then("aucune franchise n'est appliquée")
def sans_franchise(ctx):
    assert ctx["decision"].rechute and ctx["decision"].jours_franchise == 0


@then("l'indemnité est écrêtée")
def ecretee(ctx):
    assert ctx["decision"].ecretement
