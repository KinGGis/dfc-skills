#!/usr/bin/env python3
# DFC brand kit — render engine (Playwright/Chromium): full CSS + running header/footer with page numbers.
import base64, pathlib, subprocess
from playwright.sync_api import sync_playwright

KIT = pathlib.Path(__file__).resolve().parent
OUT = KIT / "out"; OUT.mkdir(exist_ok=True)
def ensure_emblem():
    """Derive the monogram-only emblem (no wordmark) from the full dark logo if absent."""
    emb = KIT/"assets/dfc-emblem-dark.png"
    if emb.exists():
        return emb
    from PIL import Image
    import numpy as np
    im = Image.open(KIT/"assets/dfc-logo-dark.png").convert("RGBA")
    w, h = im.size
    top = im.crop((0, 0, w, int(h*0.63)))            # circle sits in the top ~63%
    a = np.array(top); rgb = a[:,:,:3].astype(int); al = a[:,:,3]
    ink = (rgb.sum(axis=2) < 720) & (al > 10)
    ys, xs = np.where(ink)
    if len(xs):
        p = 6
        box = (max(0,xs.min()-p), max(0,ys.min()-p),
               min(top.size[0],xs.max()+p), min(top.size[1],ys.max()+p))
        top = top.crop(box)
    top.save(emb)
    return emb

LOGO_DARK   = base64.b64encode((KIT/"assets/dfc-logo-dark.png").read_bytes()).decode()
EMBLEM_DARK = base64.b64encode(ensure_emblem().read_bytes()).decode()

# body.html and cover.html are produced by build.py (logos + content injected).
cover_url = (OUT/"cover.html").as_uri()
# strip CSS @page margins on body so Chromium uses the pdf() margins (room for header/footer)
body_html = (OUT/"body.html").read_text().replace("@page{size:A4;margin:0;}", "")
(OUT/"body_render.html").write_text(body_html)
body_url = (OUT/"body_render.html").as_uri()

HEADER = f'''<div style="width:100%;font-family:Calibri,Arial,sans-serif;-webkit-print-color-adjust:exact;">
  <div style="padding:0 18mm 6px 18mm;overflow:hidden;">
    <img src="data:image/png;base64,{EMBLEM_DARK}" style="height:26px;float:left;">
    <div style="float:right;text-align:right;">
      <div style="font-size:9px;font-weight:700;color:#1C1C1C;text-transform:uppercase;letter-spacing:.3px;">DualForce Capital</div>
      <div style="font-size:8px;color:#6E6E6E;margin-top:1px;">Arrêté de la valeur liquidative · Août 2026</div>
    </div>
  </div>
  <div style="height:8px;line-height:0;"><div style="display:inline-block;width:42%;height:8px;background:#C5A253;"></div><div style="display:inline-block;width:57%;height:8px;background:#1C1C1C;"></div></div>
</div>'''

FOOTER = '''<div style="width:100%;font-family:Calibri,Arial,sans-serif;font-size:8px;color:#6E6E6E;padding:0 18mm;-webkit-print-color-adjust:exact;">
  <div style="border-top:.5px solid #D9D9D6;padding-top:5px;overflow:hidden;">
    <span style="float:left;">DualForce Capital Ltd&nbsp;&nbsp;|&nbsp;&nbsp;Confidentiel&nbsp;&nbsp;|&nbsp;&nbsp;DFC-NAV-DCA-2026-001</span>
    <span style="float:right;font-weight:700;color:#1C1C1C;"><span class="pageNumber"></span></span>
  </div>
</div>'''

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(cover_url, wait_until="networkidle")
    pg.pdf(path=str(OUT/"cover.pdf"), width="210mm", height="297mm",
           margin={"top":"0","bottom":"0","left":"0","right":"0"},
           print_background=True, prefer_css_page_size=True)
    pg.goto(body_url, wait_until="networkidle")
    pg.pdf(path=str(OUT/"body.pdf"), format="A4", print_background=True,
           display_header_footer=True, header_template=HEADER, footer_template=FOOTER,
           margin={"top":"27mm","bottom":"20mm","left":"0","right":"0"})
    b.close()

subprocess.run(["pdfunite", str(OUT/"cover.pdf"), str(OUT/"body.pdf"), str(OUT/"DFC_sample_NAV.pdf")], check=True)
print("OK ->", OUT/"DFC_sample_NAV.pdf")
