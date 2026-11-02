# Installer le skill carrousel-linkedin

> Ce fichier s'adresse à l'agent IA (Claude, ChatGPT, Codex…) à qui l'on a demandé d'installer ce skill. Suis les étapes dans l'ordre. Parle à la personne en français, simplement : elle n'est pas forcément à l'aise avec la technique, ne lui parle ni de JSON ni de dossiers sauf si elle le demande.

Le dépôt : https://github.com/rozieres/halluworld-skills
Le skill : le dossier `carrousel-linkedin/`.

## Étape 1 : récupérer le skill

Essaie dans cet ordre, et passe au suivant si ça échoue :

1. `git clone https://github.com/rozieres/halluworld-skills` (ou télécharger `https://github.com/rozieres/halluworld-skills/archive/refs/heads/main.zip` et le décompresser).
2. Si ton environnement n'a pas accès au réseau mais que tu peux lire des pages web, lis chaque fichier du dossier `carrousel-linkedin/` sur `https://raw.githubusercontent.com/rozieres/halluworld-skills/main/carrousel-linkedin/<chemin>` et recrée-les à l'identique : `SKILL.md`, `charte.json`, `references/ecriture.md`, `references/format_textes.md`, `scripts/generer_carrousel.py`, `exemples/article_exemple.md`. Les polices (`polices/*.ttf`) sont des fichiers binaires : si tu ne peux pas les télécharger, l'étape 3 propose une solution.

## Étape 2 : savoir où tu tournes

C'est ce qui décide de la livraison finale (étape 5) :

- **Claude Code** (ou un autre agent en ligne de commande qui lit `~/.claude/skills/`) : tu installeras le dossier directement.
- **Codex et les agents qui lisent `~/.agents/skills/`** : idem, dans ce dossier.
- **claude.ai** (ou une autre interface web avec exécution de code) : tu fabriqueras un fichier ZIP que la personne déposera elle-même. Vérifie que l'exécution de code fonctionne ; sinon, demande-lui de l'activer (sur claude.ai : Settings > Capabilities, ou Paramètres > Fonctionnalités si l'interface est en français, puis l'exécution de code).

## Étape 3 : personnaliser

Annonce le principe en une phrase : "Je vais te poser six questions pour que tes carrousels te ressemblent. Tu peux répondre 'par défaut' à chaque fois." Pose **une question à la fois**, propose toujours une valeur par défaut, et montre ce que tu as compris avant de passer à la suivante.

1. **Ton nom ou ta marque.** C'est la petite signature en haut de chaque slide (`signature`). As-tu un logo (une image PNG, de préférence sur fond transparent) ? Si oui, demande-la et range-la dans `assets/logo.png` (`logo`).
2. **Tes couleurs.** Demande deux couleurs d'accent (une par slide, en alternance), une couleur de fond et une de texte. Alternative : "Donne-moi l'adresse de ton site, je reprends ses couleurs" ; si tu peux lire la page et ses styles, propose une palette et fais-la valider. Vérifie la lisibilité : le texte et `texte_secondaire` doivent avoir un contraste d'au moins 4,5:1 avec le fond, et chaque accent au moins 3:1 (il sert pour les gros chiffres et le nom en fin de carrousel). Si un accent est trop pâle, propose une version plus foncée de la même teinte. Dérive les couleurs secondaires : `texte_secondaire` (le texte en un peu plus clair), `discret` (gris clair), `encadre` (le fond en un peu plus foncé).
3. **Ta police.** Propose : Space Grotesk (par défaut, géométrique et un peu brute), Inter (neutre et très lisible), DM Sans (ronde et douce), Montserrat (affirmée), IBM Plex Sans (sérieuse), Playfair Display (élégante, à empattements), Atkinson Hyperlegible (conçue pour les malvoyants). Toutes sont libres. Si la personne garde Space Grotesk, il n'y a rien à faire. Sinon, supprime les fichiers de `polices/` et télécharge les trois graisses de la nouvelle police :
   `https://cdn.jsdelivr.net/fontsource/fonts/<id>@latest/latin-<graisse>-normal.ttf` avec `<id>` parmi `space-grotesk`, `inter`, `dm-sans`, `montserrat`, `ibm-plex-sans`, `playfair-display`, `atkinson-hyperlegible`, et `<graisse>` = 400 (normal), 500 (moyen), 700 (gras). Atkinson Hyperlegible n'a pas de 500 : utilise le 400 pour le moyen. Nomme les fichiers `<id>-400.ttf`, `<id>-500.ttf`, `<id>-700.ttf`, mets leurs chemins dans `police`, et télécharge la licence de la police dans `polices/OFL.txt` : `https://raw.githubusercontent.com/google/fonts/main/ofl/<id sans tirets>/OFL.txt` (par exemple `ofl/dmsans/OFL.txt`). Si le téléchargement est impossible, propose à la personne de te déposer les fichiers de police dans la conversation, ou garde Space Grotesk si ses fichiers sont là ; à défaut, le script se replie sur une police standard (DejaVu Sans) : préviens-la.
4. **Ton style visuel.** Trois choix : brut (bordures épaisses, coins carrés : `bordure` 4, `coins` "carres"), sobre (filet fin : `bordure` 1), doux (`coins` "arrondis", `bordure` 2). Et les titres : en majuscules ou non (`titres_majuscules`). Demande au passage la petite invitation de la couverture (`invite_defilement`, par défaut "glissez pour lire"), sans flèche ni emoji : toutes les polices ne les ont pas.
5. **Ton ton.** Sobre, pédagogique ou piquant (`ton.registre`). Propose-lui de coller un court texte qu'elle a écrit (un post, un paragraphe) : résume en deux phrases ce qui caractérise sa voix et mets-le dans `ton.consignes`. Sans texte, remplace les consignes de démonstration (celles de Hallu World) par deux phrases qui décrivent le registre choisi et le sujet de la personne. Demande si elle veut des phrases choc (`ton.phrases_choc`) et un post LinkedIn proposé avec chaque carrousel (`post_linkedin.proposer`, avec le lien à mettre à la fin s'il y en a un et le nombre de hashtags, 0 à 5, dans `post_linkedin.hashtags`).
6. **La dernière slide.** Une slide d'appel à la fin : une accroche, un nom, une phrase de description, un slogan, un lien (`slide_finale`). Ou pas de slide finale (`active` : false). Ne laisse pas le texte de démonstration de Hallu World, sauf si la personne le veut.

Écris le résultat dans `charte.json`, mets `"personnalisee": true`, et ne touche à rien d'autre dans le skill.

## Étape 4 : tester

Fabrique un carrousel de démonstration à partir de `exemples/article_exemple.md`, en suivant `SKILL.md` mais en sautant l'étape de relecture (c'est un test, dis-le). Écris tous les fichiers du test (`textes.json`, PDF, images) **hors du dossier du skill**, dans un dossier de travail à part, pour qu'ils ne finissent pas dans le skill livré. Montre les images et demande si le rendu lui plaît. Ajuste la charte si besoin et refais un test. Supprime ensuite le dossier de test.

## Étape 5 : livrer

- **Claude Code** : copie le dossier `carrousel-linkedin/` dans `~/.claude/skills/` (ou `.claude/skills/` du projet si la personne préfère). Le skill sera disponible dans la prochaine session.
- **Codex et compatibles** : copie-le dans `~/.agents/skills/`.
- **claude.ai** : crée un ZIP qui contient le dossier `carrousel-linkedin/` lui-même (le nom du dossier doit rester `carrousel-linkedin`, identique au `name` du `SKILL.md`), donne-le en téléchargement, puis explique : "Va dans Customize > Skills (Personnaliser > Skills en français), clique sur +, puis Create skill > Upload a skill, et choisis ce fichier."
- **Ailleurs** : donne le ZIP et explique où ton outil range les skills, si tu le sais ; sinon, dis-le honnêtement.

Termine en expliquant comment s'en servir, en une phrase : "Écris 'fais-moi un carrousel à partir de cet article' avec un lien ou un texte : je te proposerai les textes, tu les corriges, puis je fabrique le PDF."
