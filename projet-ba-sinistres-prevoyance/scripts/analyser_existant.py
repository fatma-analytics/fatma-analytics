"""
Charge data/sinistres_2025.csv dans SQLite, exécute sql/analyse_existant.sql
et écrit les résultats dans docs/02-analyse-existant/resultats-sql.md.

Usage : python scripts/analyser_existant.py
"""
import csv
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
db = sqlite3.connect(":memory:")

with (ROOT / "data" / "sinistres_2025.csv").open(encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
cols = list(rows[0])
db.execute(f"CREATE TABLE sinistres ({', '.join(cols)})")
db.executemany(f"INSERT INTO sinistres VALUES ({', '.join('?' * len(cols))})",
               [[r[c] for c in cols] for r in rows])
for c in ["duree_arret_jours", "nb_relances", "erreur_calcul_audit", "controle_medical", "appels_service_client"]:
    db.execute(f"UPDATE sinistres SET {c} = CAST({c} AS INTEGER)")
db.execute("UPDATE sinistres SET montant_verse = CAST(montant_verse AS REAL)")

sql = (ROOT / "sql" / "analyse_existant.sql").read_text(encoding="utf-8")
out = ["# Résultats SQL — analyse de l'existant", "",
       "_Fichier généré par `scripts/analyser_existant.py` à partir de `sql/analyse_existant.sql`._", ""]
for bloc in [b for b in sql.split(";") if "SELECT" in b]:
    titre = [l for l in bloc.splitlines() if re.match(r"-- A\d", l.strip())][0].strip("- ").strip()
    cur = db.execute(bloc)
    head = [d[0] for d in cur.description]
    out += [f"## {titre}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in cur.fetchall()]
    out.append("")

dest = ROOT / "docs" / "02-analyse-existant" / "resultats-sql.md"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
