"""Bundle verified evidence, the golden set and the sample PRD into site/data.json.

Usage: python3 eval-studio/build_site.py  (runs verify.py first)
"""
import json, pathlib, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable, str(HERE / "verify.py")], check=True)
s = (HERE / "site" / "evidence.js").read_text()
ev = json.loads(s[s.index("=") + 1:].strip().rstrip(";"))
golden = json.load(open(HERE / "data" / "golden.json"))["cases"]
sample = (HERE / "data" / "sample_prd.md").read_text()
keep = ("speaker", "ts", "quote", "episode", "date", "youtube")
slim = lambda q: {k: q[k] for k in keep}
modes = [{**{k: m[k] for k in ("id", "name", "check", "pass_if")}, "quotes": [slim(q) for q in m["quotes"]]}
         for m in ev["failure_modes"]["modes"]]
topics = [{**{k: t[k] for k in ("id", "title", "summary")}, "quotes": [slim(q) for q in t["quotes"]]}
          for t in ev["explorer"]["topics"]]
data = {
    "modes": modes,
    "topics": topics,
    "golden": [{**{k: c[k] for k in ("id", "set", "title", "agent", "planted", "variants", "prd")},
                "labels": {fm: ("na" if v == "n/a" else v) for fm, v in c["labels"].items()}} for c in golden],
    "sample": {"title": "Fieldnote Auto-Synthesis", "prd": sample,
               "expected": {"FM01": "pass", "FM02": "pass", "FM03": "fail", "FM04": "fail", "FM05": "fail",
                            "FM06": "fail", "FM07": "fail", "FM08": "pass", "FM09": "fail", "FM10": "na"}},
}
out = HERE / "site" / "data.json"
out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
print("wrote", out.relative_to(HERE.parent), out.stat().st_size, "bytes")
