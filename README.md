# Les skills de Hallu World

Des outils gratuits pour faire travailler votre IA à votre façon, par l'équipe de [Hallu World](https://halluworld.fr), la newsletter hebdomadaire gratuite sur l'IA générative.

Un "skill", c'est un mode d'emploi rangé dans un dossier : votre assistant IA l'ouvre tout seul quand vous lui demandez la tâche qu'il décrit. Pour en savoir plus : [le guide d'Anthropic](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## carrousel-linkedin

Transforme un article, un post ou une note en carrousel LinkedIn (un PDF à faire défiler), à vos couleurs.

Il travaille en deux temps : il vous **propose** les textes des slides, vous les relisez et les corrigez, et c'est seulement après votre feu vert qu'il fabrique le visuel. L'IA propose, vous tranchez : vérifiez chaque chiffre, c'est vous qui signez.

### L'installer

1. Ouvrez [Claude](https://claude.ai) (le compte gratuit suffit) et activez l'exécution de code : **Settings > Capabilities** (Paramètres > Fonctionnalités).
2. Écrivez-lui :

   > Installe-moi ce skill : https://github.com/rozieres/halluworld-skills

3. Répondez à ses six questions (votre nom, vos couleurs, votre police, votre style, votre ton, la dernière slide). Il vous montre un carrousel de test, puis vous donne un fichier à déposer dans **Customize > Skills**.

Ça marche aussi avec Claude Code, et en principe avec les autres assistants qui lisent les skills (Codex, ChatGPT…), sans garantie : on ne les a pas tous testés.

### S'en servir

> Fais-moi un carrousel à partir de cet article : [lien ou texte]

### Ce qu'il y a dedans

- `INSTALL.md` : le déroulé de l'installation, écrit pour l'IA.
- `carrousel-linkedin/SKILL.md` : le mode d'emploi du skill.
- `carrousel-linkedin/charte.json` : vos couleurs, votre police, votre ton. Par défaut, ceux de Hallu World.
- `carrousel-linkedin/references/` : les règles d'écriture des slides (rien d'inventé, une idée par slide, pas de jargon).
- `carrousel-linkedin/scripts/generer_carrousel.py` : le script qui dessine les slides (Python et matplotlib).

## Licence

Code et textes sous licence MIT : servez-vous, modifiez, partagez. Les polices sont sous licence SIL Open Font License (voir `carrousel-linkedin/polices/OFL.txt`).

Une idée, un bug ? Ouvrez une issue, ou écrivez-nous en répondant à la newsletter.
