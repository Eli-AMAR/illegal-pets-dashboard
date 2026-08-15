"""Turn scripts5.json (batch 4: astuce/talent/premiercours) into configs + manifest5.json."""
import json
import pathlib

STYLE = {
    "astuce": {  # mind-blown trick — emerald green, energetic
        "slug": "12-astuce-pourcentages",
        "kicker": "ASTUCE · MATHS",
        "palette": {"bg1": "#06180F", "bg2": "#0B2A1A", "bg3": "#0F3824",
                    "blob1": "#0E8F5A", "blob2": "#0E6E8F",
                    "accent": "#3DF08C", "gold": "#F5C542", "emInk": "#04160C",
                    "glow": "rgba(61,240,140,.5)"},
        "seed": 132, "bpm": 102, "transpose": 4,
    },
    "talent": {  # myth-buster — warm crimson, emotional
        "slug": "13-le-talent-nexiste-pas",
        "kicker": "COURS PARTICULIERS · MATHS",
        "palette": {"bg1": "#1C0E16", "bg2": "#2A1220", "bg3": "#38162A",
                    "blob1": "#8F1E3C", "blob2": "#3C2A8F",
                    "accent": "#FF6B5C", "gold": "#FFC26B", "emInk": "#230A0A",
                    "glow": "rgba(255,107,92,.5)"},
        "seed": 143, "bpm": 90, "transpose": -1,
    },
    "premiercours": {  # calm professional — steel blue premium
        "slug": "14-le-premier-cours",
        "kicker": "MÉTHODE · MATHS",
        "palette": {"bg1": "#0D141C", "bg2": "#152232", "bg3": "#1C3044",
                    "blob1": "#2A5A8F", "blob2": "#1E8F8A",
                    "accent": "#8FB8FF", "gold": "#F5C542", "emInk": "#0A1220",
                    "glow": "rgba(143,184,255,.5)"},
        "seed": 154, "bpm": 86, "transpose": -3,
    },
}

scripts = json.loads(pathlib.Path("scripts5.json").read_text())
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
pathlib.Path("manifest5.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
for m in manifest:
    print(m["id"], m["slug"], f"{m['total_s']}s")
