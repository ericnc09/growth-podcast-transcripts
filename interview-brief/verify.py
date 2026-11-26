"""Check every brief quote against the transcript, then write the page's data file.

For each point: the episode file exists, a turn starts at `ts`, the quote appears verbatim in that turn
(whitespace-normalized), and the turn's speaker label matches `speaker` (unless `label_note` explains why not).
Adds date, episode title and a YouTube link at the second.

Usage: python3 interview-brief/verify.py   (exits 1 on any failure)
"""
import csv, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract import turns, secs

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "interview-brief"
LEAD = 15  # start clips a little early: audio timestamps can drift from the video


def norm(s):
    return " ".join(s.replace("’", "'").split())


def main():
    data = json.load(open(HERE / "briefs.json"))
    index = {r["file"]: r for r in csv.DictReader(open(ROOT / "index.csv"))}
    errors = 0
    for co in data["companies"]:
        for p in co["points"]:
            where = f'{co["id"]} / {p["speaker"]} {p["ts"]}'
            row = index.get(p["file"])
            if not row:
                print("MISSING FILE", where, p["file"]); errors += 1; continue
            match = [t for t in turns(ROOT / p["file"]) if t[1] == p["ts"]]
            if not match:
                print("NO TURN AT TS", where); errors += 1; continue
            hit = [t for t in match if norm(p["quote"]) in norm(t[2])]
            label, _, text, _ = (hit or match)[0]
            if not hit:
                print("QUOTE NOT FOUND", where, "|", p["quote"][:60]); errors += 1
            if label != p["speaker"] and not p.get("label_note"):
                print("SPEAKER MISMATCH", where, "label:", label); errors += 1
            p["date"] = row["date"]
            p["episode"] = row["title"]
            p["youtube"] = f'{row["youtube_url"]}&t={max(0, secs(p["ts"]) - LEAD)}s'
            p["substack"] = row["substack_url"]
        co["episodes"] = len({p["file"] for p in co["points"]})
        co["people"] = sorted({p["speaker"] for p in co["points"]})
        dates = sorted(p.get("date", "") for p in co["points"])
        co["range"] = [dates[0], dates[-1]]
    total = sum(len(c["points"]) for c in data["companies"])
    print(f"{total} quotes checked, {errors} problems")
    if errors:
        sys.exit(1)
    out = HERE / "site" / "data.js"
    out.parent.mkdir(exist_ok=True)
    out.write_text("window.BRIEFS = " + json.dumps(data, indent=1) + ";\n")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
