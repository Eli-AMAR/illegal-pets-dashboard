"""Turn scripts4.json (batch 3: piege/parents/rentree) into render configs + manifest4.json."""
import json
import pathlib

STYLE = {
    "piege": {  # quiz — deep teal + cyan chips
        "slug": "09-le-calcul-piege",
        "kicker": "QUIZ · MATHS",
        "palette": {"bg1": "#071720", "bg2": "#0C2A38", "bg3": "#103848",
                    "blob1": "#0E5A8F", "blob2": "#0E8F6E",
                    "accent": "#35D0FF", "gold": "#F5C542", "emInk": "#04121A",
                    "glow": "rgba(53,208,255,.5)"},
        "seed": 99, "bpm": 100, "transpose": 5,
    },
    "parents": {  # premium navy + gold, calm tempo
        "slug": "10-message-aux-parents",
        "kicker": "SOUTIEN SCOLAIRE · MATHS",
        "palette": {"bg1": "#0B0F1E", "bg2": "#142244", "bg3": "#1A2E55",
                    "blob1": "#1E4D8F", "blob2": "#8F6A0E",
                    "accent": "#F5C542", "gold": "#F5C542", "emInk": "#141405",
                    "glow": "rgba(245,197,66,.45)"},
        "seed": 110, "bpm": 80, "transpose": -4,
    },
    "rentree": {  # back-to-school warmth — indigo + orange
        "slug": "11-rentree-avance",
        "kicker": "RENTRÉE 2026 · MATHS",
        "palette": {"bg1": "#140E22", "bg2": "#221436", "bg3": "#2E1A42",
                    "blob1": "#5A2AA8", "blob2": "#A85A0E",
                    "accent": "#FFA94D", "gold": "#FFD166", "emInk": "#1E1005",
                    "glow": "rgba(255,169,77,.5)"},
        "seed": 121, "bpm": 98, "transpose": 1,
    },
}

scripts = json.loads(pathlib.Path("scripts4.json").read_text())
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
pathlib.Path("manifest4.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
for m in manifest:
    print(m["id"], m["slug"], f"{m['total_s']}s")
