#!/usr/bin/env python3
"""DFC brand kit - modele de graphiques (matplotlib) a la palette DFC.
Rendu PNG haute resolution, fond transparent, pour s'integrer aux documents brandes.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

INK="#1C1C1C"; INK2="#3A3A3A"; GOLD="#C5A253"; CREAM="#EFE4C8"
RULE="#D9D9D6"; GREY="#6E6E6E"; GREEN="#4A7C59"; RED="#A63D3D"
CATEGORICAL = [GOLD, INK2, GREY, GREEN, "#8A6D3B", "#B9B9B4"]

def dfc_style():
    base=None
    for fam in ["Calibri","Carlito"]:
        try:
            font_manager.findfont(fam, fallback_to_default=False); base=fam; break
        except Exception: base=None
    plt.rcParams.update({
        "font.family": [base] if base else ["DejaVu Sans"],
        "font.size": 11, "text.color": INK,
        "axes.edgecolor": RULE, "axes.labelcolor": INK, "axes.titlecolor": INK,
        "axes.titlesize": 13, "axes.titleweight": "bold",
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": GREY, "ytick.color": GREY,
        "grid.color": RULE, "grid.linewidth": 0.6,
        "figure.facecolor": "none", "axes.facecolor": "none",
    })

def _finish(ax, title=None):
    if title: ax.set_title(title, pad=12, loc="left")
    ax.yaxis.grid(True); ax.set_axisbelow(True)

def bar_contribution(labels, values, title="Contribution par poche (£)", path="chart_bar.png"):
    dfc_style(); fig, ax = plt.subplots(figsize=(7,3.6), dpi=200)
    colors = [GREEN if v>=0 else RED for v in values]
    b = ax.bar(labels, values, color=colors, width=0.62)
    for rect,v in zip(b,values):
        ax.annotate(f"{v:+.2f}".replace(".",","), (rect.get_x()+rect.get_width()/2, v),
                    ha="center", va="bottom" if v>=0 else "top", fontsize=9, color=INK, weight="bold")
    ax.axhline(0, color=INK2, lw=0.8)
    _finish(ax, title); plt.xticks(rotation=0, fontsize=9); fig.tight_layout()
    fig.savefig(path, transparent=True, bbox_inches="tight"); plt.close(fig); return path

def line_nav(x, y, title="Évolution de la NAV opérationnelle (£)", path="chart_line.png"):
    dfc_style(); fig, ax = plt.subplots(figsize=(7,3.6), dpi=200)
    ax.plot(x, y, color=GOLD, lw=2.4, marker="o", mfc=GOLD, mec="white", ms=6)
    ax.fill_between(x, y, min(y)*0.98, color=GOLD, alpha=0.10)
    _finish(ax, title); fig.tight_layout()
    fig.savefig(path, transparent=True, bbox_inches="tight"); plt.close(fig); return path

def donut_composition(labels, values, title="Composition de l'actif", path="chart_donut.png"):
    dfc_style(); fig, ax = plt.subplots(figsize=(5,3.8), dpi=200)
    w,_,at = ax.pie(values, colors=CATEGORICAL[:len(values)], startangle=90,
                    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=1.5),
                    autopct=lambda p: f"{p:.0f}%", pctdistance=0.79,
                    textprops=dict(color=INK, fontsize=9, weight="bold"))
    ax.legend(w, labels, loc="center left", bbox_to_anchor=(0.98,0.5), frameon=False, fontsize=9)
    ax.set_title(title, loc="left", pad=12, fontsize=13, weight="bold"); ax.axis("equal")
    fig.savefig(path, transparent=True, bbox_inches="tight"); plt.close(fig); return path
