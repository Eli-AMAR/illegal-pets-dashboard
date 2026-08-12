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

## Légendes à copier-coller

### 01 — POV Polytechnique
> Ton prof de maths a fait l'X, ENS Ulm, Chicago et la Sorbonne… et il t'explique tout simplement. Tous niveaux, de l'élémentaire à la Licence. Envoie MATHS en MP 📩
>
> #maths #profdemaths #coursparticuliers #polytechnique #lycee #college #pourtoi

### 02 — T'es pas nul en maths
> T'es pas nul en maths — il te manque juste la méthode, et la logique ça s'apprend. Prof particulier formé à Polytechnique, ENS Ulm et la Sorbonne. Envoie MÉTHODE en MP 📩 Tous niveaux, du CM2 à la Licence.
>
> #maths #methode #coursparticuliers #college #lycee #remiseaniveau #pourtoi

### 03 — Parents : le déclic
> Votre enfant bloque en maths ? Ce n'est pas une fatalité — c'est presque toujours une question de méthode. Diplômé de l'École Polytechnique et de l'ENS Ulm, je donne des cours particuliers du primaire au lycée, avec patience et pédagogie. 📩 Envoyez « DÉCLIC » en MP pour réserver.
>
> #maths #coursparticuliers #soutienscolaire #parents #profdemaths #education

### 04 — La fac t'a humilié
> La Licence, c'est un autre monde que le lycée — et ton prof doit suivre le niveau. Prof particulier de maths passé par Polytechnique, ENS Ulm et University of Chicago. Algèbre, analyse, probas : envoie LICENCE en MP 📩
>
> #maths #licence #fac #etudiant #partiels #coursparticuliers

### 05 — 3 erreurs au bac
> Ces 3 erreurs coûtent des points à presque tous les lycéens — et elles se corrigent vite avec la bonne méthode. Prof particulier de maths diplômé de Polytechnique, tous niveaux. Envoie BAC en MP 📩
>
> #bac #terminale #maths #revisions #coursparticuliers #lycee

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
