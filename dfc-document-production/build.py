#!/usr/bin/env python3
# DFC brand kit — build a branded PDF from HTML templates (wkhtmltopdf engine).
import base64, subprocess, sys, os, pathlib

KIT = pathlib.Path(__file__).resolve().parent
T   = KIT / "templates"
OUT = KIT / "out"
OUT.mkdir(exist_ok=True)

def b64(p): return base64.b64encode((KIT / p).read_bytes()).decode()
LOGO_WHITE = b64("assets/dfc-logo-white.png")
LOGO_DARK  = b64("assets/dfc-logo-dark.png")
CSS = (KIT / "dfc-brand.css").read_text()

def fill(name, repl):
    s = (T / name).read_text()
    for k, v in repl.items():
        s = s.replace("__%s__" % k, v)
    return s

# --- sample content (mini NAV note, faithful to the reference) ---
COVER_ROWS = "".join(
    '<tr><td class="k">%s</td><td class="v">%s</td></tr>' % kv for kv in [
    ("Émetteur", "DualForce Capital Ltd, société de droit britannique"),
    ("Objet", "Arrêté mensuel de la valeur liquidative et du prix de souscription"),
    ("Date d'arrêté", "31 août 2026"),
    ("Périmètre", "Portefeuille opérationnel, hors poche dédiée"),
    ("Devise de référence", "Livre sterling (GBP)"),
    ("Destinataires", "Souscripteurs du programme et actionnaires autorisés"),
    ("Classification", "Confidentiel"),
    ("Référence", "DFC-NAV-DCA-2026-001"),
    ("Date d'émission", "4 septembre 2026"),
])

cover = fill("cover.html", {
    "LOGO_WHITE": LOGO_WHITE,
    "TITLE": "Note d'arrêté<br>de la valeur liquidative",
    "SUBTITLE": "Programme d'investissement progressif · Août 2026",
    "COVER_ROWS": COVER_ROWS,
    "CONFIDENTIAL": "Document confidentiel. Réservé aux souscripteurs et actionnaires autorisés de DualForce Capital Ltd.",
})
header = fill("header.html", {
    "LOGO_DARK": LOGO_DARK,
    "HEADER_RIGHT1": "DualForce Capital",
    "HEADER_RIGHT2": "Arrêté de la valeur liquidative · Août 2026",
})
footer = fill("footer.html", {
    "FOOTER_LEFT": "DualForce Capital Ltd&nbsp;&nbsp;|&nbsp;&nbsp;Confidentiel&nbsp;&nbsp;|&nbsp;&nbsp;DFC-NAV-DCA-2026-001",
})
body = fill("report-body.html", {"CSS": CSS})

(OUT / "cover.html").write_text(cover)
(OUT / "header.html").write_text(header)
(OUT / "footer.html").write_text(footer)
(OUT / "body.html").write_text(body)

def run(cmd):
    print("+", " ".join(cmd)); subprocess.run(cmd, check=True)

# 1) full-bleed cover, margins 0
run(["wkhtmltopdf","--enable-local-file-access","--background","--print-media-type",
     "-T","0","-B","0","-L","0","-R","0",
     str(OUT/"cover.html"), str(OUT/"cover.pdf")])

# 2) inner pages with running header/footer
run(["wkhtmltopdf","--enable-local-file-access","--background","--print-media-type",
     "-T","26mm","-B","18mm","-L","0","-R","0",
     "--header-html", str(OUT/"header.html"), "--header-spacing","4",
     "--footer-html", str(OUT/"footer.html"), "--footer-spacing","4",
     str(OUT/"body.html"), str(OUT/"body.pdf")])

# 3) merge
run(["pdfunite", str(OUT/"cover.pdf"), str(OUT/"body.pdf"), str(OUT/"DFC_sample_NAV.pdf")])
print("OK ->", OUT/"DFC_sample_NAV.pdf")
