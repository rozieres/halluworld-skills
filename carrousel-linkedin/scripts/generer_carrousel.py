#!/usr/bin/env python3
"""
Génère un carrousel LinkedIn (PDF + une image PNG par slide) à partir de deux
fichiers JSON : la charte graphique (charte.json) et les textes validés.

Usage : python generer_carrousel.py <charte.json> <textes.json> <dossier_de_sortie>
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch
from matplotlib.textpath import TextPath

FIG_W, FIG_H = 7.2, 9  # 1080 x 1350 px à 150 dpi, le format portrait de LinkedIn
DPI = 150
SKILL_DIR = Path(__file__).resolve().parent.parent

LIMITES = {"titre": 70, "label": 30, "contexte": 250, "phrase_choc": 120}


def charger_polices(charte):
    police = charte.get("police", {})
    props = {}
    for graisse in ("normal", "moyen", "gras"):
        chemin = police.get(graisse)
        fichier = (SKILL_DIR / chemin) if chemin else None
        if fichier and fichier.exists():
            fm.fontManager.addfont(str(fichier))
            props[graisse] = fm.FontProperties(fname=str(fichier))
        else:
            poids = {"normal": "normal", "moyen": "medium", "gras": "bold"}[graisse]
            props[graisse] = fm.FontProperties(family="DejaVu Sans", weight=poids)
            if chemin:
                print(f"! Police introuvable ({chemin}) : repli sur DejaVu Sans")
    return props


def largeur_pt(texte, prop, taille):
    p = prop.copy()
    p.set_size(taille)
    return TextPath((0, 0), texte, prop=p).get_extents().width


def couper(texte, prop, taille, largeur_max_pt):
    lignes = []
    for paragraphe in texte.split("\n"):
        ligne = ""
        for mot in paragraphe.split():
            essai = f"{ligne} {mot}".strip()
            if ligne and largeur_pt(essai, prop, taille) > largeur_max_pt:
                lignes.append(ligne)
                ligne = mot
            else:
                ligne = essai
        lignes.append(ligne)
    return lignes


def ajuster(texte, prop, taille, frac_largeur, lignes_max, taille_min):
    """Coupe le texte à la largeur voulue et réduit la taille s'il dépasse lignes_max."""
    largeur = frac_largeur * FIG_W * 72
    while True:
        lignes = couper(texte, prop, taille, largeur)
        if len(lignes) <= lignes_max or taille <= taille_min:
            return "\n".join(equilibrer(texte, prop, taille, largeur, len(lignes))), taille
        taille -= 1


def equilibrer(texte, prop, taille, largeur, nb_lignes):
    """Resserre la largeur tant que le nombre de lignes ne change pas : évite un mot seul en dernière ligne."""
    meilleur = couper(texte, prop, taille, largeur)
    if nb_lignes < 2:
        return meilleur
    essai = largeur
    while essai > largeur * 0.6:
        essai *= 0.97
        lignes = couper(texte, prop, taille, essai)
        if len(lignes) != nb_lignes:
            break
        meilleur = lignes
    return meilleur


class Carrousel:
    def __init__(self, charte):
        self.c = charte
        self.col = charte["couleurs"]
        self.f = charger_polices(charte)
        self.style = charte.get("style", {})
        self.arrondi = self.style.get("coins") == "arrondis"
        self.bordure = self.style.get("bordure", 4)
        self.maj = self.style.get("titres_majuscules", True)

    def boite(self):
        return "round,pad=0.012" if self.arrondi else "square,pad=0"

    def figure(self):
        return plt.figure(figsize=(FIG_W, FIG_H), facecolor=self.col["fond"])

    def cadre(self, fig, epaisseur=None):
        ep = self.bordure if epaisseur is None else epaisseur
        if ep <= 0:
            return
        fig.add_artist(FancyBboxPatch(
            (0.03, 0.03), 0.94, 0.94, boxstyle=self.boite(),
            transform=fig.transFigure, fill=False,
            edgecolor=self.col["texte"], linewidth=ep, clip_on=False, zorder=10,
        ))

    def signature(self, fig, taille=12, alpha=0.6):
        logo = self.c.get("logo")
        if logo and (SKILL_DIR / logo).exists():
            img = plt.imread(str(SKILL_DIR / logo))
            h = 0.045
            w = h * (img.shape[1] / img.shape[0]) * (FIG_H / FIG_W)
            ax = fig.add_axes([0.07, 0.955 - h, w, h])
            ax.imshow(img)
            ax.axis("off")
            return
        if self.c.get("signature"):
            fig.text(0.07, 0.96, self.c["signature"], ha="left", va="top",
                     fontproperties=self.f["gras"], fontsize=taille,
                     color=self.col["texte"], alpha=alpha)

    def points(self, fig, courant, total):
        ecart = 0.028
        debut = 0.5 - (total - 1) * ecart / 2
        for i in range(total):
            fig.add_artist(Circle(
                (debut + i * ecart, 0.05), 0.006 if i == courant else 0.005,
                transform=fig.transFigure,
                facecolor=self.col["texte"] if i == courant else self.col["discret"],
                edgecolor="none", zorder=10, clip_on=False,
            ))

    def bandeau(self, fig, couleur):
        fig.add_artist(FancyBboxPatch(
            (0.03, 0.92), 0.94, 0.012, boxstyle="square,pad=0",
            transform=fig.transFigure, facecolor=couleur,
            edgecolor=self.col["texte"], linewidth=2 if self.bordure else 0, zorder=5,
        ))

    def enregistrer(self, fig, pdf, dossier_png, index, nom):
        pdf.savefig(fig, dpi=DPI, facecolor=self.col["fond"])
        fig.savefig(str(dossier_png / f"slide_{index:02d}_{nom}.png"), dpi=DPI,
                    facecolor=self.col["fond"])
        plt.close(fig)

    def couverture(self, pdf, dossier_png, data, total):
        fig = self.figure()
        self.cadre(fig, self.bordure + 1 if self.bordure else 0)
        self.signature(fig, taille=14, alpha=0.8)
        titre = data.get("titre", "")
        titre = titre.upper() if self.maj else titre
        texte, taille = ajuster(titre, self.f["gras"], 36, 0.80, 5, 22)
        fig.text(0.5, 0.62, texte, ha="center", va="center",
                 fontproperties=self.f["gras"], fontsize=taille,
                 color=self.col["texte"], linespacing=1.25)
        if data.get("sous_titre"):
            fig.text(0.5, 0.36, data["sous_titre"], ha="center", va="center",
                     fontproperties=self.f["moyen"], fontsize=16,
                     color=self.col["texte_secondaire"])
            fig.add_artist(Line2D([0.3, 0.7], [0.32, 0.32], transform=fig.transFigure,
                                  color=self.col["texte"], linewidth=2.5, zorder=5))
        fig.text(0.5, 0.12, self.c.get("invite_defilement", "glissez pour lire"),
                 ha="center", va="center", fontproperties=self.f["normal"],
                 fontsize=11, color=self.col["texte_secondaire"])
        self.points(fig, 0, total)
        self.enregistrer(fig, pdf, dossier_png, 0, "couverture")

    def empiler(self, fig, blocs, haut, bas):
        """Place les blocs de texte les uns sous les autres, centrés verticalement entre haut et bas."""
        rendu = fig.canvas.get_renderer()
        mesures = []
        for b in blocs:
            art = fig.text(0.5, 0, b["texte"], ha="center", va="top",
                           fontproperties=b["police"], fontsize=b["taille"],
                           color=b["couleur"], linespacing=b.get("interligne", 1.3), zorder=6)
            hauteur = art.get_window_extent(rendu).height / fig.bbox.height
            mesures.append((art, hauteur, b.get("apres", 0.03)))
        total = sum(h + a for _, h, a in mesures) - (mesures[-1][2] if mesures else 0)
        y = min(haut, (haut + bas) / 2 + total / 2)
        for art, hauteur, apres in mesures:
            art.set_y(y)
            y -= hauteur + apres

    def slide(self, pdf, dossier_png, data, index, nb, total):
        fig = self.figure()
        self.cadre(fig)
        self.signature(fig)
        accents = self.col["accents"]
        couleur = accents[(index - 1) % len(accents)]
        self.bandeau(fig, couleur)
        fig.text(0.93, 0.96, f"{index}/{nb}", ha="right", va="top",
                 fontproperties=self.f["moyen"], fontsize=11,
                 color=self.col["texte_secondaire"])

        a_choc = bool(data.get("phrase_choc"))
        a_chiffre = bool(data.get("chiffre"))
        titre = data.get("titre", "")
        titre = titre.upper() if self.maj else titre
        blocs = []

        t_titre, l_titre = (22, 3) if a_chiffre else (27, 4)
        texte, taille = ajuster(titre, self.f["gras"], t_titre, 0.84, l_titre, 15)
        blocs.append({"texte": texte, "police": self.f["gras"], "taille": taille,
                      "couleur": self.col["texte"], "interligne": 1.25, "apres": 0.05})
        if a_chiffre:
            chiffre, t_chiffre = ajuster(data["chiffre"], self.f["gras"], 66, 0.84, 1, 30)
            blocs.append({"texte": chiffre, "police": self.f["gras"], "taille": t_chiffre,
                          "couleur": couleur, "apres": 0.012 if data.get("label") else 0.045})
            if data.get("label"):
                blocs.append({"texte": data["label"], "police": self.f["normal"], "taille": 15,
                              "couleur": self.col["texte_secondaire"], "apres": 0.045})
        if data.get("contexte"):
            t_ctx = 15 if a_chiffre else 17
            contexte, t_ctx = ajuster(data["contexte"], self.f["normal"], t_ctx, 0.80,
                                      6 if a_chiffre else 8, 11)
            blocs.append({"texte": contexte, "police": self.f["normal"], "taille": t_ctx,
                          "couleur": self.col["texte_secondaire"], "interligne": 1.45})

        self.empiler(fig, blocs, 0.88, 0.26 if a_choc else 0.09)

        if a_choc:
            fig.add_artist(FancyBboxPatch(
                (0.07, 0.09), 0.86, 0.14, boxstyle=self.boite(),
                transform=fig.transFigure, facecolor=self.col["encadre"],
                edgecolor=self.col["texte"], linewidth=1.5, zorder=5,
            ))
            choc, t_choc = ajuster(data["phrase_choc"], self.f["moyen"], 14, 0.78, 3, 10)
            fig.text(0.5, 0.16, choc, ha="center", va="center",
                     fontproperties=self.f["moyen"], fontsize=t_choc,
                     color=self.col["texte"], linespacing=1.3, zorder=6)

        self.points(fig, index, total)
        self.enregistrer(fig, pdf, dossier_png, index, f"slide_{index}")

    def fin(self, pdf, dossier_png, total):
        fin = self.c.get("slide_finale", {})
        fig = self.figure()
        self.cadre(fig, self.bordure + 1 if self.bordure else 0)
        blocs = []
        if fin.get("accroche"):
            accroche, t = ajuster(fin["accroche"], self.f["normal"], 16, 0.80, 2, 12)
            blocs.append({"texte": accroche, "police": self.f["normal"], "taille": t,
                          "couleur": self.col["texte_secondaire"], "apres": 0.035})
        if fin.get("nom"):
            nom, t = ajuster(fin["nom"], self.f["gras"], 36, 0.84, 2, 20)
            blocs.append({"texte": nom, "police": self.f["gras"], "taille": t,
                          "couleur": self.col["accents"][0], "interligne": 1.2, "apres": 0.04})
        if fin.get("description"):
            desc, t = ajuster(fin["description"], self.f["normal"], 15, 0.72, 3, 11)
            blocs.append({"texte": desc, "police": self.f["normal"], "taille": t,
                          "couleur": self.col["texte_secondaire"], "interligne": 1.4, "apres": 0.04})
        if fin.get("slogan"):
            slogan, t = ajuster(fin["slogan"], self.f["gras"], 16, 0.80, 3, 11)
            blocs.append({"texte": slogan, "police": self.f["gras"], "taille": t,
                          "couleur": self.col["texte"], "interligne": 1.3})
        self.empiler(fig, blocs, 0.88, 0.32 if fin.get("lien") else 0.1)
        if fin.get("lien"):
            fig.add_artist(FancyBboxPatch(
                (0.15, 0.17), 0.70, 0.075, boxstyle=self.boite(),
                transform=fig.transFigure, facecolor=self.col["texte"],
                edgecolor=self.col["texte"], linewidth=2, zorder=5,
            ))
            lien, t = ajuster(fin["lien"], self.f["gras"], 17, 0.64, 1, 10)
            fig.text(0.5, 0.2075, lien, ha="center", va="center",
                     fontproperties=self.f["gras"], fontsize=t,
                     color=self.col["fond"], zorder=6)
        self.points(fig, total - 1, total)
        self.enregistrer(fig, pdf, dossier_png, total - 1, "fin")


def verifier(textes):
    alertes = []
    for i, s in enumerate(textes["slides"], start=1):
        for champ, limite in LIMITES.items():
            if len(s.get(champ) or "") > limite:
                alertes.append(f"slide {i} : {champ} trop long ({len(s[champ])} > {limite} signes)")
    return alertes


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    charte = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    textes = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    sortie = Path(sys.argv[3])
    dossier_png = sortie / "slides_png"
    dossier_png.mkdir(parents=True, exist_ok=True)

    for alerte in verifier(textes):
        print(f"! {alerte}")

    c = Carrousel(charte)
    nb = len(textes["slides"])
    finale = charte.get("slide_finale", {}).get("active", True)
    total = nb + 1 + (1 if finale else 0)

    fichier_pdf = sortie / "carrousel.pdf"
    with PdfPages(str(fichier_pdf)) as pdf:
        c.couverture(pdf, dossier_png, textes["couverture"], total)
        for i, s in enumerate(textes["slides"], start=1):
            c.slide(pdf, dossier_png, s, i, nb, total)
        if finale:
            c.fin(pdf, dossier_png, total)

    print(f"Carrousel : {fichier_pdf} ({total} slides, 1080x1350 px)")
    print(f"Images : {dossier_png}/")


if __name__ == "__main__":
    main()
