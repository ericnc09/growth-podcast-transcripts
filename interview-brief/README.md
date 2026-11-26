# Interview Brief

Pick the company you're interviewing with and see what people who worked there said on The Growth Podcast about
what they value, how they build and how they hire. Every point is dated, attributed, and links to the second on YouTube.
Each brief also has talking points, questions to ask, and a short listening playlist.

Built on the transcripts of [The Growth Podcast with Aakash Gupta](https://www.news.aakashg.com). Guests and the show
don't endorse this tool.

## How it's made

1. `extract.py` finds every speaker turn that mentions a target company and scores it for insider signals
   ("when I was at X", the guest's own company in the episode title). Output goes to `build/` (not committed).
2. `insiders.json` lists which guests actually worked at each company, checked against episode titles and intros.
3. `briefs.json` is hand-curated from those passages: 40 points across 10 companies. Points, talking points and
   questions are summaries; quotes are verbatim.
4. `verify.py` checks every quote against the transcript turn at its timestamp and checks the speaker label,
   then writes `site/data.js`. It fails the build on any mismatch.
5. `site/index.html` is a single static page. Open it directly or host it anywhere.

```
python3 interview-brief/extract.py   # optional: refresh candidate passages
python3 interview-brief/verify.py    # check quotes and rebuild site/data.js
```

`turns.py` and `span.py` are small helpers for reading passages while curating.

## Accuracy notes

- Transcripts are machine-made. Play the clip before repeating a quote.
- Clip links start 15 seconds early because audio timestamps can drift from the video.
- In at least one episode (2025-04-14) the speaker labels are swapped between host and guest. Points from that
  episode carry a `label_note` and are attributed by content.
- Most guests have since left the company they describe, so every point shows when it was said.

## Adding a company

Add the guests to `insiders.json`, run `extract.py`, read `build/read_<company>.txt` or use `turns.py`, add a block to
`briefs.json`, then run `verify.py`.
