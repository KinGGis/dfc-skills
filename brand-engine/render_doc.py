#!/usr/bin/env python3
"""
DFC brand engine - moteur de production documentaire piloté par pack de contenu.

Usage:
    python3 render_doc.py <pack.yaml|pack.json> <sortie.pdf>

Le pack suit le format DFC-CONTENT-PACK v1 (spec DFC-PACK-001).
Autonome: logos embarqués en base64 (assets_b64.py), aucune dépendance à un
fichier binaire ni à une URL externe. Fusion PDF en Python (pikepdf), pas de poppler.
Dépendances: playwright (+ chromium), pikepdf, pyyaml. Voir install.sh.
"""
import sys, os, io, re, json, base64, pathlib, html
from playwright.sync_api import sync_playwright
import pikepdf
import assets_b64

KIT = pathlib.Path(__file__).resolve().parent
OUT = KIT / "_work"; OUT.mkdir(exist_ok=True)

# ------------------------------------------------------------------ palette / CSS
CSS = """
:root{--ink:#1C1C1C;--ink2:#3A3A3A;--gold:#C5A253;--cream:#EFE4C8;--panel:#F2F2F0;
--rule:#D9D9D6;--grey:#6E6E6E;--green:#4A7C59;--red:#A63D3D;--white:#FFF;}
*{box-sizing:border-box;}
body{font-family:"Calibri","Carlito","Arial",sans-serif;font-size:10.5pt;line-height:1.5;color:var(--ink);margin:0;}
p{margin:0 0 8pt 0;text-align:justify;}
strong{font-weight:700;}
.pos{color:var(--green);font-weight:700;}
.neg{color:var(--red);font-weight:700;}
h1,h2,h3{font-weight:700;margin:0;}
.section{background:var(--ink);border-left:5px solid var(--gold);padding:9pt 14pt;margin:20pt 0 12pt 0;page-break-inside:avoid;}
.section h2{color:var(--white);font-size:14pt;text-transform:uppercase;letter-spacing:0.4pt;}
.section .sub{color:var(--gold);font-size:9pt;margin-top:2pt;}
h3.subhead{font-size:11pt;color:var(--ink);margin:14pt 0 4pt 0;}
.kpi{width:100%;border-collapse:collapse;background:var(--cream);margin:4pt 0 12pt 0;}
.kpi td{width:33.33%;text-align:center;padding:14pt 8pt;vertical-align:middle;}
.kpi .val{font-size:20pt;font-weight:700;color:var(--ink);}
.kpi .lbl{font-size:8.5pt;color:var(--grey);margin-top:4pt;}
.retain{background:var(--cream);border-left:5px solid var(--gold);padding:10pt 14pt;margin:12pt 0;page-break-inside:avoid;}
.retain .t{font-weight:700;margin-bottom:4pt;}
.retain p{font-size:9.5pt;margin:0;}
table.data{width:100%;border-collapse:collapse;margin:8pt 0 12pt 0;font-size:9.5pt;}
table.data thead th{background:var(--ink);color:var(--white);font-weight:700;text-align:left;padding:7pt 10pt;}
table.data thead th.num{text-align:right;}
table.data tbody td{padding:6pt 10pt;border-bottom:0.5pt solid var(--rule);}
table.data tbody td.num{text-align:right;font-variant-numeric:tabular-nums;}
table.data tbody tr:nth-child(even){background:var(--panel);}
table.data tbody tr.total,table.data tbody tr.total td{background:var(--cream);font-weight:700;}
.chart{margin:8pt 0 12pt 0;text-align:center;}
.chart img{max-width:100%;}
.sources{font-size:8.5pt;color:var(--grey);margin-top:14pt;border-top:1pt solid var(--gold);padding-top:6pt;}
"""

def esc(s):
    return html.escape(str(s), quote=False)

def rich(s):
    """**gras** -> <strong>, échappe le reste, conserve les sauts de ligne en paragraphes."""
    parts = [p.strip() for p in str(s).split("\n\n") if p.strip()]
    out = []
    for p in parts:
        p = esc(p)
        p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
        out.append("<p>%s</p>" % p)
    return "\n".join(out)

def cell_render(v):
    """Applique (pos)/(neg) -> classe couleur; retourne (classe_extra, texte)."""
    s = str(v)
    cls = ""
    m = re.search(r"\((pos|neg)\)\s*$", s)
    if m:
        cls = " pos" if m.group(1) == "pos" else " neg"
        s = re.sub(r"\s*\((pos|neg)\)\s*$", "", s)
    return cls, esc(s)

def build_table(tbl):
    cols = tbl.get("columns", [])
    align = tbl.get("align", ["left"] * len(cols))
    def is_num(i): return i < len(align) and align[i] == "num"
    thead = "".join(
        '<th class="num">%s</th>' % esc(c) if is_num(i) else "<th>%s</th>" % esc(c)
        for i, c in enumerate(cols))
    body_rows = []
    for row in tbl.get("rows", []):
        cells = list(row)
        total = False
        if cells and str(cells[-1]).strip().lower() == "total":
            total = True; cells = cells[:-1]
        tds = []
        for i, c in enumerate(cells):
            cls, txt = cell_render(c)
            numcls = " num" if is_num(i) else ""
            tds.append('<td class="%s%s">%s</td>' % (numcls.strip(), cls, txt) if (numcls or cls)
                       else "<td>%s</td>" % txt)
        body_rows.append('<tr class="total">%s</tr>' % "".join(tds) if total
                         else "<tr>%s</tr>" % "".join(tds))
    return ('<table class="data"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
            % (thead, "".join(body_rows)))

def build_charts(charts):
    if not charts:
        return ""
    try:
        import dfc_charts
    except Exception:
        return ""  # module de graphiques absent: on n'improvise pas
    html_bits = []
    for i, ch in enumerate(charts):
        data = ch.get("data", [])
        labels = [str(d[0]) for d in data]
        values = [float(d[1]) for d in data]
        p = str(OUT / ("chart_%d.png" % i))
        t = ch.get("type", "bar"); title = ch.get("title", "")
        if t == "bar":
            dfc_charts.bar_contribution(labels, values, title=title, path=p)
        elif t == "line":
            dfc_charts.line_nav(labels, values, title=title, path=p)
        elif t == "donut":
            dfc_charts.donut_composition(labels, values, title=title, path=p)
        else:
            continue
        b = base64.b64encode(open(p, "rb").read()).decode()
        html_bits.append('<div class="chart"><img src="data:image/png;base64,%s"></div>' % b)
    return "".join(html_bits)

# ------------------------------------------------------------------ pack loading
def load_pack(path):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    # tolère un pack délimité par les marqueurs DFC-CONTENT-PACK
    m = re.search(r"===\s*DFC-CONTENT-PACK.*?===(.*?)===\s*FIN PACK\s*===", raw, re.S)
    if m:
        raw = m.group(1)
    if path.endswith(".json"):
        return json.loads(raw)
    import yaml
    return yaml.safe_load(raw)

# ------------------------------------------------------------------ HTML builders
def cover_html(pack):
    rows = "".join('<tr><td class="k">%s</td><td class="v">%s</td></tr>'
                   % (esc(k), esc(v)) for k, v in
                   [tuple(x) for x in pack.get("cover_meta", [])])
    title = esc(pack.get("title", "")).replace(" - ", "<br>")
    return f"""<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><style>
@page{{margin:0;size:A4;}} html,body{{margin:0;padding:0;}}
body{{font-family:"Calibri","Carlito","Arial",sans-serif;background:#1C1C1C;color:#fff;width:210mm;height:297mm;position:relative;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
.topbar{{height:10mm;width:100%;background:#1C1C1C;}} .topbar .gold{{height:10mm;width:42%;background:#C5A253;float:left;}}
.wrap{{padding:0 26mm;}} .logo{{text-align:center;margin-top:40mm;}} .logo img{{width:42mm;}}
.title{{text-align:center;text-transform:uppercase;font-size:30pt;font-weight:700;line-height:1.12;margin-top:20mm;letter-spacing:0.5pt;}}
.subtitle{{text-align:center;color:#C5A253;font-size:13pt;margin-top:7mm;}}
.kv{{width:100%;border-collapse:collapse;margin:16mm 0 0 0;border-left:4px solid #C5A253;}}
.kv td{{padding:5.5pt 14pt;border-bottom:0.5pt solid rgba(255,255,255,0.12);font-size:10pt;}}
.kv td.k{{color:#C5A253;font-weight:700;width:34%;}} .kv td.v{{color:#E9E9E9;}}
.foot{{position:absolute;bottom:14mm;left:26mm;right:26mm;text-align:center;color:#9A9A9A;font-size:8.5pt;}}
.foot .line{{width:60mm;height:1pt;background:#C5A253;margin:10pt auto 0;}}
</style></head><body>
<div class="topbar"><div class="gold"></div></div>
<div class="wrap">
<div class="logo"><img src="data:image/png;base64,{assets_b64.LOGO_WHITE_B64}"></div>
<div class="title">{title}</div>
<div class="subtitle">{esc(pack.get('subtitle',''))}</div>
<table class="kv">{rows}</table>
</div>
<div class="foot">{esc(pack.get('confidential','Document confidentiel. Réservé aux destinataires autorisés de DualForce Capital Ltd.'))}<div class="line"></div></div>
</body></html>"""

def body_html(pack):
    blocks = []
    for sec in pack.get("sections", []):
        blocks.append('<div class="section"><h2>%s</h2>%s</div>' % (
            esc(sec.get("heading", "")),
            '<div class="sub">%s</div>' % esc(sec["subhead"]) if sec.get("subhead") else ""))
        if sec.get("kpis"):
            tds = "".join('<td><div class="val">%s</div><div class="lbl">%s</div></td>'
                          % (esc(k), esc(l)) for k, l in [tuple(x) for x in sec["kpis"]])
            blocks.append('<table class="kpi"><tr>%s</tr></table>' % tds)
        if sec.get("body"):
            blocks.append(rich(sec["body"]))
        if sec.get("retain"):
            blocks.append('<div class="retain"><div class="t">Ce qu\'il faut retenir</div>%s</div>'
                          % rich(sec["retain"]))
        if sec.get("table"):
            blocks.append(build_table(sec["table"]))
        blocks.append(build_charts(sec.get("charts")))
    # KPI de tête (niveau pack) si fourni
    top_kpi = ""
    if pack.get("kpis"):
        tds = "".join('<td><div class="val">%s</div><div class="lbl">%s</div></td>'
                      % (esc(k), esc(l)) for k, l in [tuple(x) for x in pack["kpis"]])
        top_kpi = '<table class="kpi"><tr>%s</tr></table>' % tds
    if pack.get("sources"):
        blocks.append('<div class="sources"><strong>Sources.</strong> %s</div>' % esc(pack["sources"]))
    return ("<!DOCTYPE html><html lang=fr><head><meta charset=utf-8><style>"
            "body{margin:0;padding:0 18mm;}" + CSS + "</style></head><body>"
            + top_kpi + "\n".join(blocks) + "</body></html>")

# ------------------------------------------------------------------ emblem (header)
def emblem_b64():
    from PIL import Image
    import numpy as np
    im = Image.open(io.BytesIO(base64.b64decode(assets_b64.LOGO_DARK_B64))).convert("RGBA")
    w, h = im.size
    top = im.crop((0, 0, w, int(h * 0.63)))
    a = np.array(top); rgb = a[:, :, :3].astype(int); al = a[:, :, 3]
    ink = (rgb.sum(axis=2) < 720) & (al > 10)
    ys, xs = np.where(ink)
    if len(xs):
        p = 6
        top = top.crop((max(0, xs.min() - p), max(0, ys.min() - p),
                        min(top.size[0], xs.max() + p), min(top.size[1], ys.max() + p)))
    buf = io.BytesIO(); top.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def run(pack_path, out_path):
    pack = load_pack(pack_path)
    ref = esc(pack.get("reference", ""))
    hdr_sub = esc(pack.get("subtitle", ""))
    (OUT / "cover.html").write_text(cover_html(pack), encoding="utf-8")
    (OUT / "body.html").write_text(body_html(pack), encoding="utf-8")
    EMB = emblem_b64()
    HEADER = f'''<div style="width:100%;font-family:Calibri,Arial,sans-serif;-webkit-print-color-adjust:exact;">
<div style="padding:0 18mm 6px 18mm;overflow:hidden;">
<img src="data:image/png;base64,{EMB}" style="height:26px;float:left;">
<div style="float:right;text-align:right;">
<div style="font-size:9px;font-weight:700;color:#1C1C1C;text-transform:uppercase;letter-spacing:.3px;">DualForce Capital</div>
<div style="font-size:8px;color:#6E6E6E;margin-top:1px;">{hdr_sub}</div></div></div>
<div style="height:8px;line-height:0;"><div style="display:inline-block;width:42%;height:8px;background:#C5A253;"></div><div style="display:inline-block;width:57%;height:8px;background:#1C1C1C;"></div></div></div>'''
    FOOTER = f'''<div style="width:100%;font-family:Calibri,Arial,sans-serif;font-size:8px;color:#6E6E6E;padding:0 18mm;-webkit-print-color-adjust:exact;">
<div style="border-top:.5px solid #D9D9D6;padding-top:5px;overflow:hidden;">
<span style="float:left;">DualForce Capital Ltd&nbsp;&nbsp;|&nbsp;&nbsp;Confidentiel&nbsp;&nbsp;|&nbsp;&nbsp;{ref}</span>
<span style="float:right;font-weight:700;color:#1C1C1C;"><span class="pageNumber"></span></span></div></div>'''
    cover_pdf = str(OUT / "cover.pdf"); body_pdf = str(OUT / "body.pdf")
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto((OUT / "cover.html").as_uri(), wait_until="networkidle")
        pg.pdf(path=cover_pdf, width="210mm", height="297mm",
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
               print_background=True, prefer_css_page_size=True)
        pg.goto((OUT / "body.html").as_uri(), wait_until="networkidle")
        pg.pdf(path=body_pdf, format="A4", print_background=True,
               display_header_footer=True, header_template=HEADER, footer_template=FOOTER,
               margin={"top": "27mm", "bottom": "20mm", "left": "0", "right": "0"})
        b.close()
    merged = pikepdf.Pdf.new()
    for f in (cover_pdf, body_pdf):
        with pikepdf.open(f) as src:
            merged.pages.extend(src.pages)
    merged.save(out_path)
    print("OK ->", out_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 render_doc.py <pack.yaml|pack.json> <sortie.pdf>"); sys.exit(2)
    run(sys.argv[1], sys.argv[2])
