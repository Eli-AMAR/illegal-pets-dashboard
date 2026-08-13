# 🎬 Vidéos TikTok — Recrutement d'élèves (cours particuliers de maths)

5 vidéos verticales **1080×1920, 30 fps, H.264 + AAC** (format natif TikTok / Reels / Shorts),
avec musique originale libre de droits (synthétisée pour ce projet). Objectif : générer des DM.

## Les 5 vidéos

| Fichier | Cible | Mot-clé DM |
|---|---|---|
| `videos/01-pov-polytechnique.mp4` | Tous (crédibilité / flex du parcours) | **MATHS** |
| `videos/02-pas-nul-methode.mp4` | Collégiens & lycéens découragés | **MÉTHODE** |
| `videos/03-parents-declic.mp4` | Parents (primaire → lycée) | **DÉCLIC** |
| `videos/04-licence-fac.mp4` | Étudiants en Licence / fac | **LICENCE** |
| `videos/05-trois-erreurs-bac.mp4` | Première / Terminale (spé maths) | **BAC** |

## Descriptions à copier-coller (optimisées algorithme + recherche TikTok)

Recette des hashtags : **2 méga-tags** de portée (#pourtoi / #fyp) + **3-4 tags de niche**
(là où sont vraiment les élèves) + **1 tag saisonnier** (#rentree2026, #bac2027).
La première phrase de la description sert au SEO TikTok : elle contient les mots-clés
que les gens tapent dans la recherche (« prof de maths », « réviser le bac »…).

### 01 — POV Polytechnique
> POV : ton prof particulier de maths a fait Polytechnique, ENS Ulm, University of Chicago et la Sorbonne 🎓 Et il t'explique tout simplement, du primaire à la Licence (remise à niveau incluse). Envoie « MATHS » en MP pour réserver 📩
>
> #pourtoi #fyp #maths #profdemaths #coursparticuliers #polytechnique #grandesecoles #rentree2026

### 02 — T'es pas nul en maths
> T'es pas nul en maths, on t'a juste jamais montré la méthode 🧠 La logique, ça s'apprend — pas le par cœur. Prof particulier formé à Polytechnique, ENS Ulm, la Sorbonne et University of Chicago, de la primaire à la Licence. Envoie « MÉTHODE » en MP 📩
>
> #pourtoi #maths #ecole #college #lycee #methodedetravail #revisions #studytok

### 03 — Parents : le déclic
> Votre enfant décroche en maths ? Ce n'est presque jamais une question d'intelligence — c'est une question de méthode. Professeur formé à Polytechnique, ENS Ulm, University of Chicago et la Sorbonne, je remets les bases en place avant la rentrée : primaire, collège, lycée. Envoyez « DÉCLIC » en MP pour réserver 📩
>
> #parents #education #soutienscolaire #rentreescolaire #rentree2026 #maths #ecole #pourtoi

### 04 — La fac t'a humilié
> La fac t'a humilié en maths ? Normal, la Licence c'est un autre sport 📚 Algèbre, analyse, probas : je t'explique tout simplement (parcours : Polytechnique, ENS Ulm, University of Chicago). Envoie « LICENCE » en MP avant les partiels 📩
>
> #etudiant #fac #universite #licence #partiels #maths #etudessuperieures #pourtoi

### 05 — 3 erreurs au bac
> 3 erreurs qui te coûtent des points au bac de maths ❌ réviser sans annales, bâcler la rédaction, tout apprendre par cœur. On corrige ça ensemble : méthode + entraînement, avec un prof diplômé de Polytechnique. Envoie « BAC » en MP 📩
>
> #bac #bac2027 #terminale #spemaths #revisions #lycee #pourtoi #studytok

Astuces : les hashtags vont **dans la description** (pas en commentaire) ; alternez
#pourtoi et #fyp d'une vidéo à l'autre pour tester ; ne dépassez pas ~8 hashtags,
l'algorithme préfère la précision à l'accumulation.

## Conseils de publication (pour maximiser les DM)

1. **Autorisez les MP de tout le monde** : Profil → Paramètres → Confidentialité → Messages directs → « Tout le monde ». Sans ça, les élèves qui ne vous suivent pas ne peuvent pas écrire.
2. **Bio conseillée** : `🎓 Polytechnique · ENS Ulm · UChicago · Sorbonne | Prof particulier de maths | Tous niveaux 📩 MP pour réserver`
3. **Rythme** : 1 vidéo par jour pendant 5 jours (plutôt que tout d'un coup), entre 18h et 21h en semaine, dimanche 17h-20h. Commencez par la 02 ou la 05 (les plus « algorithme-friendly »), gardez la 01 pour la fin de semaine et **épinglez-la** sur votre profil.
4. **Son tendance** : les vidéos ont leur propre musique, mais l'algorithme favorise les sons tendance. Astuce : dans TikTok, ajoutez un son tendance à ~10 % de volume par-dessus (le son de la vidéo à 100 %).
5. **Répondez vite aux DM** (< 1 h idéalement). Les mots-clés (MATHS, MÉTHODE, DÉCLIC, LICENCE, BAC) vous disent quelle vidéo a amené l'élève et donc quel niveau/besoin.
6. **Répondez aux commentaires en vidéo** (fonction « répondre par une vidéo ») : c'est le levier n°1 pour enchaîner du contenu qui convertit.
7. C'est le bon moment : **août = rentrée dans 3 semaines**, pic de recherche de profs particuliers et de remises à niveau.

## Régénérer / modifier les vidéos

Tout le pipeline est dans `source/` (aucune dépendance externe payante) :

```bash
cd tiktok/source
npm install playwright-core        # capture des frames (Chromium)
pip install numpy imageio-ffmpeg   # musique + encodage
bash build.sh                      # régénère les 5 MP4 dans out/
```

- `scripts.json` — les textes des 5 vidéos (modifiez librement : hooks, scènes, durées)
- `make_configs.py` — palettes de couleurs, musique (BPM/tonalité) par vidéo
- `template.html` — le moteur d'animation (typographie cinétique déterministe)
- `audio.py` — synthèse de la musique lo-fi (aucun sample, 100 % libre de droits)
