"""Print guest turns from one episode that match a regex (dev helper for curating briefs)."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract import turns
f, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 220
for sp, ts, tx, sponsor in turns(pathlib.Path(f)):
    if sp != "Aakash Gupta" and not sponsor and pat.search(tx):
        w = tx.replace("\n", " ").split()
        # center window on first match
        m = pat.search(" ".join(w)); pos = len(" ".join(w)[:m.start()].split())
        a = max(0, pos - maxw // 3)
        print(f"[{sp} {ts}] " + " ".join(w[a:a + maxw]) + "\n")
