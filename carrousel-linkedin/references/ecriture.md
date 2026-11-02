# Écrire les textes d'un carrousel

Un carrousel se lit en quelques secondes par slide, sur un téléphone. Chaque mot doit gagner sa place. Le ton vient de `charte.json` (`ton.registre` et `ton.consignes`) ; les règles ci-dessous valent pour tous les tons.

## La règle d'or : rien d'inventé

- **Chaque chiffre, nom, date et citation vient du contenu source.** Si l'article n'a pas de chiffre marquant pour une slide, laisse `chiffre` vide : une slide sans chiffre vaut mieux qu'un chiffre arrondi, extrapolé ou sorti de ta mémoire.
- **Une citation entre guillemets est recopiée mot pour mot.** Pour résumer un propos, sors des guillemets.
- **Ce qu'une entreprise dit d'elle-même lui reste attribué** ("selon OpenAI", "d'après l'entreprise").
- **Pas d'affirmation plus forte que la source.** Une étude préliminaire reste préliminaire, un projet reste un projet.
- Si le contenu n'est pas de la personne, cite la source sur la couverture (`sous_titre` : "D'après [média]" ou "D'après [auteur], [média]").

## La structure

- **Une idée par slide**, dans un ordre qui raconte quelque chose : le fait, puis ce qu'il change, puis ce qu'il cache. Pas un sommaire de l'article.
- **3 à 6 slides.** Moins si le contenu ne porte pas plus.
- **Couverture** : un titre de journal, 6 à 14 mots, qui donne envie de faire défiler. Jamais de "5 leçons à retenir" ni de formule LinkedIn.

## Les champs, slide par slide

| Champ | Ce qu'il fait | Longueur |
|---|---|---|
| `titre` | Le fait, comme un titre de journal | 4 à 9 mots |
| `chiffre` | Le chiffre ou le fait le plus frappant, lisible seul en très gros ("÷3", "40 %", "2 h", "0 ligne") | très court, ou vide |
| `label` | Ce que mesure le chiffre ("de délibération", "des emplois") | 30 signes max |
| `contexte` | Deux ou trois phrases qui expliquent | 250 signes max |
| `phrase_choc` | Optionnelle : une remarque qui fait sourire ou réfléchir, sans signature | 120 signes max |

N'écris des `phrase_choc` que si `ton.phrases_choc` vaut `true`, et pas forcément sur chaque slide : seulement quand elle apporte quelque chose.

## Le style

- **Des phrases construites** (sujet, verbe, complément). Jamais de phrases nominales empilées du type "Coût : 75 €. Résultat : un échec."
- **Pas de fausse profondeur** : bannir "Ce n'est pas X. C'est Y." sous toutes ses formes.
- **Pas de jargon non expliqué.** Un sigle ou un terme technique reçoit quelques mots d'explication, ou disparaît.
- Pas de métadiscours ("il est important de noter que"), pas d'emojis ni de flèches dans les slides (la police risque de ne pas les avoir), pas de texte en gras Unicode.
- Français correct, avec tous les accents.

## Les registres

- **sobre** : informatif, neutre, phrases nettes. Pas d'ironie.
- **pédagogique** : on explique comme à un ami curieux, avec une image concrète par slide si possible.
- **piquant** : lucide et ironique, mais l'ironie reste en dessous de ce que les faits établissent.

Si `ton.consignes` contient un exemple de texte de la personne, imite sa voix (longueur des phrases, vocabulaire, humour), pas son sujet.

## Le post LinkedIn (si `post_linkedin.proposer` vaut `true`)

- 400 à 800 signes, en vrais paragraphes (pas une phrase par ligne).
- La première ligne doit accrocher seule : c'est tout ce que LinkedIn montre avant "voir plus".
- Ne résume pas chaque slide : donne l'angle, la raison de lire.
- Termine par le lien de `post_linkedin.lien` s'il existe, puis le nombre de hashtags prévu, sur la dernière ligne.
