"""Shared helpers: parse speaker turns out of an episode file."""
import re

TURN = re.compile(r"^\*\*(.+?)\*\* \((\d\d:\d\d:\d\d)\)\s*$", re.M)


def secs(ts):
    h, m, s = map(int, ts.split(":"))
    return h * 3600 + m * 60 + s


def norm(s):
    return " ".join(s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').split())


def turns(path):
    """Yield (speaker, ts, text, is_sponsor) for each speaker turn."""
    text = path.read_text()
    body = text.split("\n---\n", 1)[1] if text.startswith("---") else text
    marks = list(TURN.finditer(body))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        chunk = body[m.end():end]
        sponsor = "<!-- sponsor -->" in chunk
        chunk = re.sub(r"<!--.*?-->", "", chunk).strip()
        yield m.group(1), m.group(2), chunk, sponsor
