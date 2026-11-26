"""Check every quote in data/*.json against the transcripts; write site/evidence.js.

A quote passes when: the episode file exists, a turn starts at `ts`, the quote appears verbatim
in that turn (whitespace and curly quotes normalized), and the turn's speaker label matches.
Adds episode title, date and a YouTube link at the second.

Usage: python3 eval-studio/verify.py   (exits 1 on any failure)
"""
import csv, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import turns, secs, norm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
LEAD = 15  # start clips a little early: audio timestamps can drift from the video


def check(q, index, where):
    errs = []
    row = index.get(q["file"])
    if not row:
        return [f"MISSING FILE {where} {q['file']}"]
    match = [t for t in turns(ROOT / q["file"]) if t[1] == q["ts"]]
    if not match:
        return [f"NO TURN AT TS {where}"]
    hit = [t for t in match if norm(q["quote"]).lower() in norm(t[2]).lower()]
    label = (hit or match)[0][0]
    if not hit:
        errs.append(f"QUOTE NOT FOUND {where} | {q['quote'][:70]}")
    if label != q["speaker"] and not q.get("label_note"):
        errs.append(f"SPEAKER MISMATCH {where} label={label}")
    q["episode"] = row["title"]
    q["date"] = row["date"]
    q["youtube"] = f'{row["youtube_url"]}&t={max(0, secs(q["ts"]) - LEAD)}s'
    return errs


def walk(obj, path=""):
    """Yield every dict that looks like a quote (has speaker/file/ts/quote)."""
    if isinstance(obj, dict):
        if {"speaker", "file", "ts", "quote"} <= obj.keys():
            yield path, obj
        for k, v in obj.items():
            yield from walk(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def main():
    index = {r["file"]: r for r in csv.DictReader(open(ROOT / "index.csv"))}
    out, total, errors = {}, 0, []
    for f in sorted((HERE / "data").glob("*.json")):
        data = json.load(open(f))
        for path, q in walk(data):
            total += 1
            errors += check(q, index, f"{f.stem}{path}")
        out[f.stem] = data
    for e in errors:
        print(e)
    print(f"{total} quotes checked, {len(errors)} problems")
    if errors:
        sys.exit(1)
    site = HERE / "site"
    site.mkdir(exist_ok=True)
    (site / "evidence.js").write_text("window.EVIDENCE = " + json.dumps(out, indent=1, ensure_ascii=False) + ";\n")
    print("wrote", (site / "evidence.js").relative_to(ROOT))


if __name__ == "__main__":
    main()
