"""Turn scripts.json into per-video render configs + a build manifest."""
import json
import pathlib

STYLE = {
    "video1": {  # POV flex — electric blue on deep navy
        "slug": "01-pov-polytechnique",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#0B0E1A", "bg2": "#121A36", "bg3": "#1B2440",
                    "blob1": "#2742A8", "blob2": "#0E7A8F",
                    "accent": "#4F8CFF", "gold": "#F5C542", "emInk": "#0B0E1A",
                    "glow": "rgba(79,140,255,.55)"},
        "seed": 11, "bpm": 88, "transpose": 0,
    },
    "video2": {  # "t'es pas nul" — violet
        "slug": "02-pas-nul-methode",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#150A22", "bg2": "#22103A", "bg3": "#2E1650",
                    "blob1": "#5B2AA8", "blob2": "#8F0E5E",
                    "accent": "#C77DFF", "gold": "#FFD166", "emInk": "#1A0B2E",
                    "glow": "rgba(199,125,255,.55)"},
        "seed": 22, "bpm": 90, "transpose": 3,
    },
    "video3": {  # parents — premium navy + gold
        "slug": "03-parents-declic",
        "kicker": "SOUTIEN SCOLAIRE · MATHS",
        "palette": {"bg1": "#0A0E1C", "bg2": "#11203A", "bg3": "#152B46",
                    "blob1": "#1E4D8F", "blob2": "#8F6A0E",
                    "accent": "#F5C542", "gold": "#F5C542", "emInk": "#141405",
                    "glow": "rgba(245,197,66,.45)"},
        "seed": 33, "bpm": 82, "transpose": -2,
    },
    "video4": {  # licence/fac — coral on charcoal
        "slug": "04-licence-fac",
        "kicker": "MATHS · SUPÉRIEUR",
        "palette": {"bg1": "#170D13", "bg2": "#26121E", "bg3": "#331528",
                    "blob1": "#8F2742", "blob2": "#2A3F8F",
                    "accent": "#FF5C6C", "gold": "#FFC26B", "emInk": "#20080D",
                    "glow": "rgba(255,92,108,.5)"},
        "seed": 44, "bpm": 92, "transpose": -5,
    },
    "video5": {  # 3 erreurs bac — mint on dark teal
        "slug": "05-trois-erreurs-bac",
        "kicker": "SPÉ MATHS · BAC",
        "palette": {"bg1": "#07161A", "bg2": "#0B2630", "bg3": "#0E3240",
                    "blob1": "#0E6E8F", "blob2": "#1E8F5A",
                    "accent": "#2EE6A8", "gold": "#F5C542", "emInk": "#04140E",
                    "glow": "rgba(46,230,168,.5)"},
        "seed": 55, "bpm": 96, "transpose": 1,
    },
}

scripts = json.loads(pathlib.Path("scripts.json").read_text())
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
                     "caption": s["caption"], "hashtags": s["hashtags"], "target": s["target"]})
pathlib.Path("manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
for m in manifest:
    print(m["id"], m["slug"], f"{m['total_s']}s")
