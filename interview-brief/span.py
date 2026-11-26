"""Print every turn in an episode between two timestamps (dev helper)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract import turns, secs
f, a, b = sys.argv[1], secs(sys.argv[2]), secs(sys.argv[3])
maxw = int(sys.argv[4]) if len(sys.argv) > 4 else 400
for sp, ts, tx, s in turns(pathlib.Path(f)):
    if a <= secs(ts) <= b:
        print(f"[{sp} {ts}] " + " ".join(tx.split()[:maxw]) + "\n")
