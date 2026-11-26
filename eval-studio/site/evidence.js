window.EVIDENCE = {
 "failure_modes": {
  "note": "Failure modes an AI feature PRD can have. Each is backed by verbatim guest quotes; verify.py checks every quote against the transcript.",
  "modes": [
   {
    "id": "FM01",
    "name": "Vibes-only quality bar",
    "check": "The PRD defines quality only through demos, dogfooding or 'it looks good', with no repeatable measurement.",
    "pass_if": "It names a repeatable check of output quality (a test set, a rubric, or a scored sample) that anyone on the team can rerun.",
    "quotes": [
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:07:47",
      "quote": "Your vibe checks are very important, but they don't scale because they involve you, the human.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=452s"
     },
     {
      "speaker": "Ankur Goyal",
      "file": "episodes/2026-03-20-ankur-goyal-podcast.md",
      "ts": "00:02:10",
      "quote": "once your product gets into production, more people start using it, you have more subject matter experts and engineers at your company that are actually contributing to its quality, then the vibe check version of an eval stops scaling.",
      "episode": "Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)",
      "date": "2026-03-20",
      "youtube": "https://www.youtube.com/watch?v=71qvIkO9d_A&t=115s"
     },
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:07:02",
      "quote": "I've never seen somebody make it through multiple iterations of their product without any evals.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=407s"
     }
    ]
   },
   {
    "id": "FM02",
    "name": "Success criteria aren't measurable",
    "check": "The requirements describe the AI behaviour in qualitative terms that an engineer cannot score.",
    "pass_if": "Requirements include example inputs with expected behaviour, or criteria an engineer could score pass/fail.",
    "quotes": [
     {
      "speaker": "Ankur Goyal",
      "file": "episodes/2026-03-20-ankur-goyal-podcast.md",
      "ts": "00:07:49",
      "quote": "I think the modern PRD is an eval.",
      "episode": "Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)",
      "date": "2026-03-20",
      "youtube": "https://www.youtube.com/watch?v=71qvIkO9d_A&t=454s"
     },
     {
      "speaker": "Daniel McKinnon",
      "file": "episodes/2026-07-28-how-to-build-your-first-eval.md",
      "ts": "00:04:52",
      "quote": "an eval is the best way to communicate what your product should be doing",
      "episode": "How to Build Frontier-Lab Quality Evals with Daniel McKinnon, ex-PM at Meta, Google",
      "date": "2026-07-28",
      "youtube": "https://www.youtube.com/watch?v=ztN6bE_FuQQ&t=277s"
     },
     {
      "speaker": "Aman Khan",
      "file": "episodes/2025-06-15-aman-khan-podcast.md",
      "ts": "01:47:00",
      "quote": "what if evals were your requirements instead of your AI product?",
      "episode": "AI PM Crash Course 2026: Prototyping → Observability → Evals",
      "date": "2025-06-15",
      "youtube": "https://www.youtube.com/watch?v=Ej4pBDaHspk&t=6405s"
     }
    ]
   },
   {
    "id": "FM03",
    "name": "Generic metrics instead of product-specific ones",
    "check": "The eval plan leans on off-the-shelf scores (hallucination score, toxicity, BLEU, public benchmarks) rather than failures specific to this product.",
    "pass_if": "Metrics are tied to concrete ways this product's output goes wrong for its users.",
    "quotes": [
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:17:07",
      "quote": "the first thing to know about evals where people go off the rails is do not reach for generic metrics.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=1012s"
     },
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:42:51",
      "quote": "there's a really big difference between foundation model benchmarks.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=2556s"
     }
    ]
   },
   {
    "id": "FM04",
    "name": "Failure modes guessed, not observed",
    "check": "The listed risks are brainstormed; there is no plan to read real outputs or traces and categorise what actually goes wrong.",
    "pass_if": "It plans error analysis: reviewing a sample of real or realistic outputs and grouping the failures before choosing evals.",
    "quotes": [
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "01:04:24",
      "quote": "you should be grounding it in things that are going wrong or the things that will probably go wrong.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=3849s"
     },
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "01:00:42",
      "quote": "I keep looking at data and I just keep adding to my existing failure modes.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=3627s"
     },
     {
      "speaker": "Teresa Torres",
      "file": "episodes/2025-08-12-teresa-torres-podcast.md",
      "ts": "00:47:42",
      "quote": "for errors that are kind of persistent, I'm going to write an eval.",
      "episode": "Teresa Torres' Step-by-Step Guide to AI Product Discovery",
      "date": "2025-08-12",
      "youtube": "https://www.youtube.com/watch?v=wGuRuuPuYNQ&t=2847s"
     }
    ]
   },
   {
    "id": "FM05",
    "name": "LLM judge nobody checked",
    "check": "The plan uses an LLM to grade outputs but never compares the judge with human labels.",
    "pass_if": "The judge is measured against human-labelled examples, with an agreement target, before its scores are trusted.",
    "quotes": [
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "01:08:29",
      "quote": "80% of people who are using LLM as a judge are just writing a prompt and just praying that is doing the right thing.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=4094s"
     },
     {
      "speaker": "Aman Khan",
      "file": "episodes/2025-06-15-aman-khan-podcast.md",
      "ts": "01:24:40",
      "quote": "I don't see too many people actually, when they talk about evals saying that you need to check the work of the LLM as a judge",
      "episode": "AI PM Crash Course 2026: Prototyping → Observability → Evals",
      "date": "2025-06-15",
      "youtube": "https://www.youtube.com/watch?v=Ej4pBDaHspk&t=5065s"
     }
    ]
   },
   {
    "id": "FM06",
    "name": "Fuzzy rubric",
    "check": "Quality is graded on 1-to-5 or 1-to-10 scales, or with criteria too vague for two people to agree on.",
    "pass_if": "Each criterion is binary (pass or fail) and specific enough that two reviewers would label the same output the same way.",
    "quotes": [
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:09:59",
      "quote": "we say limit yourself to binary, because that is what the LLM can do very well.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=584s"
     },
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:07:47",
      "quote": "In our course, we define that as a rubric of binary criteria.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=452s"
     }
    ]
   },
   {
    "id": "FM07",
    "name": "Evals with no headroom",
    "check": "The launch bar is near-perfect scores on a test set that is easy for today's model, so the evals cannot show progress or regressions.",
    "pass_if": "The test set includes hard cases the current system fails, and the plan expects some evals to fail.",
    "quotes": [
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "00:36:21",
      "quote": "if you're getting 100% accuracy in your evals, it's likely your evals are worthless because they are providing you with no signal.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=2166s"
     },
     {
      "speaker": "Ankur Goyal",
      "file": "episodes/2026-03-20-ankur-goyal-podcast.md",
      "ts": "00:39:12",
      "quote": "one of the most important things is to have evals that fail.",
      "episode": "Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)",
      "date": "2026-03-20",
      "youtube": "https://www.youtube.com/watch?v=71qvIkO9d_A&t=2337s"
     }
    ]
   },
   {
    "id": "FM08",
    "name": "Offline only, no production loop",
    "check": "Evals run before launch only; nothing samples live traffic or user feedback after launch.",
    "pass_if": "It plans online checks: sampling production traces, user feedback signals, or regular re-scoring after launch.",
    "quotes": [
     {
      "speaker": "Daniel McKinnon",
      "file": "episodes/2026-07-28-how-to-build-your-first-eval.md",
      "ts": "00:02:42",
      "quote": "let's ship it into prod and see if they actually like it with an online eval.",
      "episode": "How to Build Frontier-Lab Quality Evals with Daniel McKinnon, ex-PM at Meta, Google",
      "date": "2026-07-28",
      "youtube": "https://www.youtube.com/watch?v=ztN6bE_FuQQ&t=147s"
     },
     {
      "speaker": "Shreya Shankar",
      "file": "episodes/2026-01-15-hamel-shreya-podcast-2.md",
      "ts": "00:53:40",
      "quote": "Every week or so, I'll sample some of my traces, run my LLM-powered evaluators on them, and then kind of just look at the score, see if anything's off or whatnot.",
      "episode": "How to Do AI Evals Step-by-Step with Real Production Data | Tutorial by Hamel Husain and Shreya Shankar",
      "date": "2026-01-15",
      "youtube": "https://www.youtube.com/watch?v=J7N9FMouSKg&t=3205s"
     }
    ]
   },
   {
    "id": "FM09",
    "name": "Cost and latency left out",
    "check": "The PRD picks a model without budgets for cost per task or response time, or without testing whether a cheaper model is good enough.",
    "pass_if": "It states cost and latency targets (ideally p95, not averages) and compares at least one cheaper model on the same eval.",
    "quotes": [
     {
      "speaker": "Ankit Shukla",
      "file": "episodes/2026-02-19-ai-evals-explained-simply.md",
      "ts": "00:15:33",
      "quote": "They can let you understand whether a cheaper model can also go ahead and perform at a similar kind of level or not.",
      "episode": "AI Evals Explained Simply by Ankit Shukla",
      "date": "2026-02-19",
      "youtube": "https://www.youtube.com/watch?v=Raa3qjEBvKE&t=918s"
     },
     {
      "speaker": "Ankit Shukla",
      "file": "episodes/2026-02-19-ai-evals-explained-simply.md",
      "ts": "00:50:28",
      "quote": "we will have the latency so p50 p95 p99 means that whenever we do averaging averaging is not going to give you the right kind of results",
      "episode": "AI Evals Explained Simply by Ankit Shukla",
      "date": "2026-02-19",
      "youtube": "https://www.youtube.com/watch?v=Raa3qjEBvKE&t=3013s"
     },
     {
      "speaker": "Hamel Husain",
      "file": "episodes/2025-07-11-hamel-shreya-podcast.md",
      "ts": "01:05:28",
      "quote": "evals are not free.",
      "episode": "The PM’s Role in AI Evals: Step-by-Step ",
      "date": "2025-07-11",
      "youtube": "https://www.youtube.com/watch?v=g_3LJ2QBOQE&t=3913s"
     }
    ]
   },
   {
    "id": "FM10",
    "name": "Agent judged only on its final answer",
    "check": "A multi-step agent is evaluated like a chatbot: one prompt in, one answer out, with no look at the steps or tool calls.",
    "pass_if": "The plan evaluates whole tasks and inspects intermediate steps or tool calls where failures happen.",
    "quotes": [
     {
      "speaker": "Daniel McKinnon",
      "file": "episodes/2026-07-28-how-to-build-your-first-eval.md",
      "ts": "00:13:35",
      "quote": "this is a totally new paradigm of writing evals because you're no longer thinking about QA, you're thinking about tasks.",
      "episode": "How to Build Frontier-Lab Quality Evals with Daniel McKinnon, ex-PM at Meta, Google",
      "date": "2026-07-28",
      "youtube": "https://www.youtube.com/watch?v=ztN6bE_FuQQ&t=800s"
     },
     {
      "speaker": "Ankur Goyal",
      "file": "episodes/2026-03-20-ankur-goyal-podcast.md",
      "ts": "00:46:20",
      "quote": "I set it up to evaluate every step. Maybe you only want to evaluate the last step",
      "episode": "Evals are the new PRD. Here is the playbook with the CEO of the leader in the space (Ankur Goyal, Founder and CEO, Braintrust)",
      "date": "2026-03-20",
      "youtube": "https://www.youtube.com/watch?v=71qvIkO9d_A&t=2765s"
     }
    ]
   }
  ]
 }
};
