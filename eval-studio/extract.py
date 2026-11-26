"""Pull guest turns about AI evals into build/candidates.json, tagged by topic.

Usage: python3 eval-studio/extract.py
Output is a list of pointers with short excerpts, for curating; it is not shipped.
"""
import csv, json, re, pathlib, sys, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import turns

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "eval-studio" / "build"

TOPICS = {
    "evals": r"\bevals?\b|evaluation",
    "judge": r"LLM.as.a.judge|\bjudge\b|grader|auto.?rater",
    "golden": r"golden (data)?set|ground truth|test set|labell?ed (data|examples)|eval set",
    "hallucination": r"hallucinat|made.up|confabul|factual",
    "human_review": r"human (review|in the loop|label|rater|eval)|vibe.?check|read (the|every) (trace|transcript|output)",
    "error_analysis": r"error analysis|failure mode|edge case|look at the (data|traces)|traces?\b",
    "online": r"\bonline eval|production (data|traffic|monitor)|A/B|thumbs (up|down)|implicit feedback|monitor",
    "cost_latency": r"latency|\bcost\b|token|inference|cheaper model|smaller model|\bspeed\b",
    "guardrails": r"guardrail|safety|jailbreak|prompt injection|red.?team|toxic",
    "agents": r"\bagents?\b|agentic|tool call|multi.step",
    "prd": r"\bPRD\b|spec\b|requirements doc",
    "trust": r"\btrust\b|reliab|non.?determin|probabilistic|99%|accuracy",
}
PATS = {k: re.compile(v, re.I) for k, v in TOPICS.items()}
SENT = re.compile(r"(?<=[.!?])\s+")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "index.csv")))
    found = []
    for r in rows:
        guests = [g.strip() for g in r["guests"].split(";") if g.strip()]
        for speaker, ts, chunk, sponsor in turns(ROOT / r["file"]):
            if sponsor or speaker == "Aakash Gupta":
                continue
            flat = " ".join(chunk.split())
            if len(flat.split()) < 40:
                continue
            tags = {k: len(p.findall(flat)) for k, p in PATS.items()}
            tags = {k: v for k, v in tags.items() if v}
            core = tags.get("evals", 0) + tags.get("judge", 0) + tags.get("golden", 0) + tags.get("error_analysis", 0) + tags.get("human_review", 0)
            if core == 0 and not ("hallucination" in tags and "trust" in tags):
                continue
            found.append({
                "speaker": speaker, "is_guest": speaker in guests, "guests": guests,
                "date": r["date"], "episode": r["title"], "file": r["file"], "ts": ts,
                "speaker_names": r["speaker_names"], "tags": tags,
                "score": core * 2 + len(tags), "words": len(flat.split()), "text": flat,
            })
    found.sort(key=lambda x: -x["score"])
    (OUT / "candidates.json").write_text(json.dumps(found, indent=1))
    c = collections.Counter(t for x in found for t in x["tags"])
    print(len(found), "turns,", len({x['file'] for x in found}), "episodes,", len({x['speaker'] for x in found}), "speakers")
    print(c.most_common())


if __name__ == "__main__":
    main()
