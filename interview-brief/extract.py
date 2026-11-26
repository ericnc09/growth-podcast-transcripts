"""Pull every speaker turn that mentions a target company, with speaker, date and timestamp.

Usage: python3 interview-brief/extract.py  ->  writes interview-brief/build/candidates/<company>.json

Each candidate is a short excerpt (the sentences around the mention), not the full turn,
so the output stays a pointer into the transcripts rather than a copy of them.
"""
import csv, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "interview-brief" / "build" / "candidates"

COMPANIES = {
    "google": r"\bGoogle\b|\bDeepMind\b|\bYouTube\b",
    "openai": r"\bOpenAI\b|\bChatGPT\b",
    "meta": r"\bMeta\b|\bFacebook\b|\bInstagram\b|\bWhatsApp\b",
    "microsoft": r"\bMicrosoft\b|\bCopilot\b|\bLinkedIn\b",
    "amazon": r"\bAmazon\b|\bAWS\b",
    "airbnb": r"\bAirbnb\b",
    "figma": r"\bFigma\b",
    "salesforce": r"\bSalesforce\b|\bSlack\b",
    "atlassian": r"\bAtlassian\b|\bJira\b|\bConfluence\b",
    "zapier": r"\bZapier\b",
    "canva": r"\bCanva\b",
    "anthropic": r"\bAnthropic\b",
    "netflix": r"\bNetflix\b",
    "uber": r"\bUber\b",
    "spotify": r"\bSpotify\b",
    "linear": r"\bLinear\b",
    "hubspot": r"\bHubSpot\b",
    "amplitude": r"\bAmplitude\b",
    "stripe": r"\bStripe\b",
    "notion": r"\bNotion\b",
}

INSIDER = re.compile(
    r"\b(when I was at|while I was at|I was at|I worked at|I joined|my time at|I'm at|I am at|here at|"
    r"at \w+,? we|we at|our team at|I led|I run|I lead|I'm the|I was the|I was a PM at|I spent \w+ years at|"
    r"we (built|launched|shipped|hire|hired|interview|look for|do|did|have|had|use|used|call|measure|tested|test))\b",
    re.I,
)

THEMES = {
    "hiring": r"interview|hire|hiring|recruit|candidate|resume|loop|offer|level|promot|career ladder|onboard",
    "how they build": r"roadmap|ship|launch|prototype|spec|PRD|review|planning|process|sprint|experiment|A/B|eval|build",
    "what they value": r"value|culture|care about|principle|bar|ownership|craft|bias|customer|first principles|taste",
    "metrics": r"metric|retention|activation|north star|DAU|MAU|revenue|growth|conversion|KPI|OKR",
    "AI": r"\bAI\b|model|LLM|agent|GPT|Claude|Gemini|copilot|eval",
}

SENT = re.compile(r"(?<=[.!?])\s+")
TURN = re.compile(r"^\*\*(.+?)\*\* \((\d\d:\d\d:\d\d)\)\s*$", re.M)


def secs(ts):
    h, m, s = map(int, ts.split(":"))
    return h * 3600 + m * 60 + s


def turns(path):
    text = path.read_text()
    body = text.split("\n---\n", 1)[1] if text.startswith("---") else text
    marks = list(TURN.finditer(body))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        chunk = body[m.end():end]
        sponsor = "<!-- sponsor -->" in chunk
        chunk = re.sub(r"<!--.*?-->", "", chunk).strip()
        yield m.group(1), m.group(2), chunk, sponsor


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(ROOT / "index.csv")))
    pats = {k: re.compile(v) for k, v in COMPANIES.items()}
    found = {k: [] for k in COMPANIES}
    for r in rows:
        meta = r["title"] + " " + r["subtitle"]
        guests = [g.strip() for g in r["guests"].split(";") if g.strip()]
        for speaker, ts, chunk, sponsor in turns(ROOT / r["file"]):
            if sponsor:
                continue
            sents = SENT.split(chunk.replace("\n", " "))
            for co, pat in pats.items():
                hits = [i for i, s in enumerate(sents) if pat.search(s)]
                if not hits:
                    continue
                i = hits[0]
                excerpt = " ".join(sents[max(0, i - 1): i + 3])
                if len(excerpt.split()) < 25:
                    continue
                is_guest = speaker in guests
                score = 0
                score += 3 if INSIDER.search(excerpt) else 0
                score += 2 if is_guest and pat.search(meta) else 0
                score += 1 if is_guest else 0
                score += min(len(hits), 3)
                themes = [t for t, p in THEMES.items() if re.search(p, excerpt, re.I)]
                found[co].append({
                    "speaker": speaker,
                    "is_guest": is_guest,
                    "date": r["date"],
                    "episode": r["title"],
                    "file": r["file"],
                    "ts": ts,
                    "youtube": r["youtube_url"],
                    "t": secs(ts),
                    "speaker_names": r["speaker_names"],
                    "score": score,
                    "themes": themes,
                    "excerpt": excerpt[:900],
                })
    summary = {}
    for co, items in found.items():
        items.sort(key=lambda x: (-x["score"], x["date"]))
        (OUT / f"{co}.json").write_text(json.dumps(items, indent=1))
        summary[co] = {
            "passages": len(items),
            "episodes": len({x["file"] for x in items}),
            "strong": sum(1 for x in items if x["score"] >= 5),
        }
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
