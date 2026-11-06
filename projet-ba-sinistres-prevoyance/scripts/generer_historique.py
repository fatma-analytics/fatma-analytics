"""
Génère un historique FICTIF de 2 000 sinistres arrêt de travail traités en 2025
selon le processus actuel (courrier / e-mail, ressaisie manuelle).

Les distributions sont choisies pour refléter des irritants plausibles ;
elles servent à illustrer la démarche d'analyse de l'existant, pas à décrire
un assureur réel.

Usage : python scripts/generer_historique.py
Sortie : data/sinistres_2025.csv
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
N = 2000
OUT = Path(__file__).resolve().parent.parent / "data" / "sinistres_2025.csv"

PIECES = ["attestation_salaire", "decompte_ijss", "arret_travail", "rib"]
POIDS_PIECES = [0.52, 0.28, 0.12, 0.08]       # l'attestation employeur manque le plus souvent
TAILLES = ["TPE", "PME", "ETI"]


def jours_ouvres(d: date, n: int) -> date:
    while n > 0:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


rows = []
for i in range(1, N + 1):
    taille = random.choices(TAILLES, [0.45, 0.40, 0.15])[0]
    canal = random.choices(["courrier", "email"], [0.62, 0.38])[0]
    debut = date(2025, 1, 1) + timedelta(days=random.randint(0, 330))
    # Durée d'arrêt : beaucoup d'arrêts courts déclarés inutilement (< franchise de 30 jours)
    duree = int(random.choices(
        [random.randint(3, 30), random.randint(31, 90), random.randint(91, 365)],
        [0.24, 0.52, 0.24])[0])
    delai_decl = int(min(200, random.expovariate(1 / 22))) + 2
    if random.random() < 0.04:
        delai_decl = random.randint(95, 180)               # déclarations hors délai
    declaration = debut + timedelta(days=delai_decl)

    # Dossier incomplet à réception : plus fréquent en TPE et par courrier
    p_incomplet = {"TPE": 0.44, "PME": 0.30, "ETI": 0.18}[taille] + (0.05 if canal == "courrier" else -0.04)
    incomplet = random.random() < p_incomplet
    piece = random.choices(PIECES, POIDS_PIECES)[0] if incomplet else ""
    relances = random.choices([1, 2, 3], [0.55, 0.32, 0.13])[0] if incomplet else 0
    attente_pieces = sum(random.randint(6, 12) for _ in range(relances))
    acheminement = random.randint(3, 6) if canal == "courrier" else random.randint(0, 1)
    complet = declaration + timedelta(days=acheminement + attente_pieces)

    # Décision
    if delai_decl > 90 and random.random() < 0.7:
        statut, motif = "REJETE", "hors_delai"
    elif duree <= 30:
        statut, motif = "REJETE", "franchise_non_atteinte"
    elif random.random() < 0.015:
        statut, motif = "REJETE", "non_affilie"
    else:
        statut, motif = "PAYE", ""

    traitement = random.randint(5, 14)                     # ressaisie + calcul manuel (jours ouvrés)
    decision = jours_ouvres(complet, traitement)
    paiement = jours_ouvres(decision, random.randint(2, 4)) if statut == "PAYE" else None

    sjr = round(random.uniform(55, 190), 2)               # salaire journalier de référence brut
    ijss = round(min(41.47, sjr * 0.5), 2)
    ij = round(max(0, 0.75 * sjr - ijss), 2)
    jours_indem = max(0, duree - 30) if statut == "PAYE" else 0
    montant = round(jours_indem * ij, 2)
    erreur = 1 if statut == "PAYE" and random.random() < 0.038 else 0   # détectée en audit a posteriori
    controle_medical = 1 if duree > 180 else 0

    rows.append({
        "id_sinistre": f"S25-{i:05d}",
        "taille_entreprise": taille,
        "canal": canal,
        "date_debut_arret": debut.isoformat(),
        "duree_arret_jours": duree,
        "date_declaration": declaration.isoformat(),
        "piece_manquante_initiale": piece,
        "nb_relances": relances,
        "date_dossier_complet": complet.isoformat(),
        "date_decision": decision.isoformat(),
        "date_paiement": paiement.isoformat() if paiement else "",
        "statut_final": statut,
        "motif_rejet": motif,
        "montant_verse": montant,
        "erreur_calcul_audit": erreur,
        "controle_medical": controle_medical,
        "appels_service_client": random.choices([0, 1, 2, 3], [0.38, 0.33, 0.19, 0.10])[0] + (1 if incomplet else 0),
    })

OUT.parent.mkdir(exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} sinistres écrits dans {OUT}")
