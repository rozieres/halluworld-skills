---
name: carrousel-linkedin
description: Transforme un article, un post ou une note en carrousel LinkedIn (un PDF à faire défiler), aux couleurs de son auteur. Propose d'abord les textes des slides à partir du contenu, attend qu'on les relise et les corrige, puis seulement fabrique le visuel. À utiliser dès qu'on parle de carrousel, de slides LinkedIn ou de transformer un texte en visuel à faire défiler.
---

# Carrousel LinkedIn

Ce skill fabrique un carrousel en deux temps : **tu proposes les textes, la personne les relit, puis tu fabriques le visuel.** Le visuel n'est jamais généré avant que les textes aient été validés explicitement. C'est la règle centrale du skill : l'IA propose, l'humain tranche.

Les fichiers du skill :
- `charte.json` : couleurs, police, signature, ton, slide finale. Personnalisée à l'installation.
- `references/ecriture.md` : les règles d'écriture des slides. À lire avant de rédiger.
- `references/format_textes.md` : comment présenter les textes à relire.
- `scripts/generer_carrousel.py` : le rendu en PDF et en images.

## Étape 0 : vérifier la charte

Lis `charte.json`. Si `"personnalisee"` vaut `false` ou est absent, le skill tourne encore avec la charte de démonstration (celle de la newsletter Hallu World). Dis-le en une phrase et propose de la personnaliser en suivant `INSTALL.md` (étape 3) ; si la personne préfère continuer tel quel, continue.

## Étape 1 : récupérer le contenu

- Un lien : lis la page **en entier**, pas seulement le début.
- Un texte collé ou un fichier : lis-le en entier.
- Si le contenu n'est pas de la personne (article d'un média, post de quelqu'un d'autre), note l'auteur et le média : la source sera citée sur la couverture.

Si le contenu est trop court pour trois slides, dis-le plutôt que de délayer.

## Étape 2 : proposer les textes

Lis `references/ecriture.md`, puis rédige une couverture et 3 à 6 slides. Présente-les comme indiqué dans `references/format_textes.md`, avec le post LinkedIn si `charte.json` le prévoit.

Termine par une invitation claire à relire : ce sont des propositions, chaque chiffre et chaque citation est à vérifier contre l'article, et tout se corrige (texte, ordre, nombre de slides).

**Arrête-toi là.** Attends la réponse. Si la personne corrige, intègre ses corrections telles quelles, remontre la version à jour si les changements sont importants, et attends une validation explicite ("c'est bon", "go", "valide", "génère"...).

## Étape 3 : fabriquer le visuel

1. Écris les textes validés dans un fichier `textes.json`, **dans un dossier de travail hors du dossier du skill** :
   ```json
   {
     "couverture": {"titre": "...", "sous_titre": "..."},
     "slides": [
       {"titre": "...", "chiffre": "...", "label": "...", "contexte": "...", "phrase_choc": "..."}
     ]
   }
   ```
   Les champs `chiffre`, `label` et `phrase_choc` peuvent être vides (`""`). Les retours à la ligne sont calculés par le script : n'en ajoute pas.
2. Lance le rendu depuis le dossier du skill (il faut matplotlib : `pip install matplotlib` s'il manque, ou `uv run --with matplotlib python …` si tu utilises uv) :
   ```bash
   python scripts/generer_carrousel.py charte.json textes.json <dossier_de_sortie>
   ```
   Le script produit `carrousel.pdf` (le fichier à publier sur LinkedIn) et un dossier `slides_png/`.
3. Regarde **chaque image** avant de livrer : texte qui déborde ou se chevauche, slide trop vide ou trop pleine, chiffre illisible. Si le script affiche des alertes de longueur ou si une slide est ratée, raccourcis le texte concerné (en le signalant) et relance.

## Étape 4 : livrer

Donne le PDF, rappelle le post LinkedIn s'il y en a un, et propose un dernier tour de retouches. Rappelle d'un mot que LinkedIn accepte le PDF via "Ajouter un document".
