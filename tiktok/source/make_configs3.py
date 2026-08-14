"""Turn scripts3.json (the 3 'best-of' scripts) into render configs + manifest3.json."""
import json
import pathlib

STYLE = {
    "transformation": {  # counter piece — royal navy + gold, counter ends green
        "slug": "06-objectif-16",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#0A1024", "bg2": "#122448", "bg3": "#183055",
                    "blob1": "#2742A8", "blob2": "#0E7A8F",
                    "accent": "#5B8CFF", "gold": "#F5C542", "emInk": "#0B0E1A",
                    "glow": "rgba(91,140,255,.5)"},
        "seed": 66, "bpm": 96, "transpose": 0,
    },
    "cvdefou": {  # premium near-black + electric blue + gold badges
        "slug": "07-cv-de-fou",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#07080F", "bg2": "#10122A", "bg3": "#181C3A",
                    "blob1": "#2A2AA8", "blob2": "#5A1E8F",
                    "accent": "#4F8CFF", "gold": "#F5C542", "emInk": "#0B0E1A",
                    "glow": "rgba(79,140,255,.55)"},
        "seed": 77, "bpm": 100, "transpose": 2,
    },
    "moyenne": {  # bold violet + hot pink for the engagement-bait one
        "slug": "08-envoie-ta-moyenne",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#1C0A2E", "bg2": "#2A1048", "bg3": "#38155A",
                    "blob1": "#7A2AA8", "blob2": "#B01E6E",
                    "accent": "#FF5C9E", "gold": "#FFD166", "emInk": "#2A0818",
                    "glow": "rgba(255,92,158,.5)"},
        "seed": 88, "bpm": 104, "transpose": -3,
    },
}

scripts = json.loads(pathlib.Path("scripts3.json").read_text())
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
pathlib.Path("manifest3.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
for m in manifest:
    print(m["id"], m["slug"], f"{m['total_s']}s")
