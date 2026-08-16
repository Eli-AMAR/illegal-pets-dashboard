"""Turn scripts6.json (batch 5: six videos) into configs + manifest6.json."""
import json
import pathlib

STYLE = {
    "quizprio": {  # quiz series — electric indigo
        "slug": "15-quiz-priorites",
        "kicker": "QUIZ · MATHS",
        "palette": {"bg1": "#0B0B26", "bg2": "#141438", "bg3": "#1C1C4E",
                    "blob1": "#4A3AB8", "blob2": "#0E6E8F",
                    "accent": "#7B6CFF", "gold": "#F5C542", "emInk": "#0C0A20",
                    "glow": "rgba(123,108,255,.5)"},
        "seed": 165, "bpm": 102, "transpose": 2,
    },
    "quizpct": {  # quiz series — burnt orange
        "slug": "16-quiz-pourcentages",
        "kicker": "QUIZ · MATHS",
        "palette": {"bg1": "#200A12", "bg2": "#301018", "bg3": "#401820",
                    "blob1": "#8F3A0E", "blob2": "#8F0E4A",
                    "accent": "#FF8C42", "gold": "#FFD166", "emInk": "#200D04",
                    "glow": "rgba(255,140,66,.5)"},
        "seed": 176, "bpm": 104, "transpose": -2,
    },
    "astuce11": {  # astuce series brand — emerald
        "slug": "17-astuce-fois-11",
        "kicker": "ASTUCE · MATHS",
        "palette": {"bg1": "#06180F", "bg2": "#0B2A1A", "bg3": "#0F3824",
                    "blob1": "#0E8F5A", "blob2": "#0E6E8F",
                    "accent": "#3DF08C", "gold": "#F5C542", "emInk": "#04160C",
                    "glow": "rgba(61,240,140,.5)"},
        "seed": 187, "bpm": 102, "transpose": 4,
    },
    "astuce25": {  # astuce series brand — emerald, slight teal shift
        "slug": "18-astuce-carre-25",
        "kicker": "ASTUCE · MATHS",
        "palette": {"bg1": "#05171A", "bg2": "#0A2A2A", "bg3": "#0E3836",
                    "blob1": "#0E8F7A", "blob2": "#0E5A8F",
                    "accent": "#3DF0C4", "gold": "#F5C542", "emInk": "#03140F",
                    "glow": "rgba(61,240,196,.5)"},
        "seed": 198, "bpm": 100, "transpose": 7,
    },
    "memoire": {  # brain — deep violet
        "slug": "19-pourquoi-tu-oublies",
        "kicker": "MÉMOIRE · MATHS",
        "palette": {"bg1": "#12102A", "bg2": "#1A1640", "bg3": "#241E54",
                    "blob1": "#5A3AB8", "blob2": "#B83A8F",
                    "accent": "#9D8CFF", "gold": "#FFD166", "emInk": "#100C24",
                    "glow": "rgba(157,140,255,.5)"},
        "seed": 209, "bpm": 88, "transpose": -3,
    },
    "trentemin": {  # focus — warm gold on charcoal
        "slug": "20-trente-minutes",
        "kicker": "MÉTHODE · MATHS",
        "palette": {"bg1": "#16130A", "bg2": "#241E10", "bg3": "#322816",
                    "blob1": "#8F6A0E", "blob2": "#8F3A0E",
                    "accent": "#FFD166", "gold": "#FFD166", "emInk": "#1E1604",
                    "glow": "rgba(255,209,102,.45)"},
        "seed": 220, "bpm": 94, "transpose": 0,
    },
}

scripts = json.loads(pathlib.Path("scripts6.json").read_text())
pathlib.Path("cfg").mkdir(exist_ok=True)
manifest = []
for s in scripts:
    st = STYLE[s["id"]]
    total = round(sum(sc["duration_s"] for sc in s["scenes"]), 3)
    cfg = {"fps": 30, "seed": st["seed"], "kicker": st["kicker"],
           "palette": st["palette"], "scenes": s["scenes"]}
    pathlib.Path(f"cfg/{s['id']}.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
    manifest.append({"id": s["id"], "slug": st["slug"], "total_s": total,
                     "seed": st["seed"], "bpm": st["bpm"], "transpose": st["transpose"],
                     "caption": s["caption"], "hashtags": s["hashtags"]})
pathlib.Path("manifest6.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
for m in manifest:
    print(m["id"], m["slug"], f"{m['total_s']}s")
