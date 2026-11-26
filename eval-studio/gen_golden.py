"""Build the golden set: 30 fictional AI-feature PRDs with planted failure modes and exact labels.

Each PRD is assembled from sections. For every failure mode there is a sound version and a flawed
version of the relevant passage, so the label is known by construction, not judged.

Usage: python3 eval-studio/gen_golden.py  ->  writes data/golden.json (cases) and prints label counts
"""
import json, random, pathlib, sys, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data_src_products import PRODUCTS

HERE = pathlib.Path(__file__).resolve().parent
FMS = [f"FM{i:02d}" for i in range(1, 11)]
EVAL_DEPENDENT = {"FM03", "FM04", "FM05", "FM06", "FM07", "FM10"}


def labels_for(p, flaws):
    out = {}
    for fm in FMS:
        if fm == "FM10" and not p["agent"]:
            out[fm] = "n/a"
        elif "FM01" in flaws and fm in EVAL_DEPENDENT:
            out[fm] = "n/a"
        else:
            out[fm] = "fail" if fm in flaws else "pass"
    return out


def prd(p, flaws):
    f = lambda fm: fm in flaws
    L = [f"# {p['company']} {p['feature']}: product requirements",
         "",
         f"*{p['company']} is a fictional {p['kind']}. This PRD is a test case, not a real document.*",
         "",
         "## Problem", "", p["problem"], "",
         "## Users", "", f"Primary users are {p['users']}.", "",
         "## Proposed solution", "", p["solution"], "",
         "## Requirements", ""]
    if f("FM02"):
        L += [p["vague"], "",
              f"- The {p['output']} uses all relevant context available to it.",
              "- It handles edge cases gracefully.",
              "- It feels natural and on-brand.", ""]
    else:
        L += [f"Expected behaviour on representative inputs. Each row is also a test case in the eval set.", "",
              "| Input | Expected behaviour |", "| --- | --- |"]
        L += [f"| {a} | {b} |" for a, b in p["examples"]]
        L += [""]
    L += ["## Quality and evaluation", ""]
    if f("FM01"):
        L += [f"Our own team will dogfood {p['feature']} for two weeks before the beta. "
              "We will ship when the team agrees the quality feels right, and keep an eye on customer feedback after that.", ""]
    else:
        if f("FM04"):
            L += [f"Risks we anticipate: the model may hallucinate, may show bias, or may be off-tone. We will write evals for each of these.", ""]
        else:
            obs = "; ".join(p["observed"])
            L += [f"Before choosing metrics, we reviewed 100 {p['outputs']} from the prototype and grouped what went wrong. "
                  f"The most common failures were: {obs}. We repeat this review whenever we change the prompt or the model.", ""]
        L += [f"We will measure {p['generic_metrics'] if f('FM03') else p['specific_metrics']}.", ""]
        if f("FM06"):
            L += [f"Graders rate each {p['output']} from 1 to 5 on accuracy, helpfulness and tone, and we track the average.", ""]
        else:
            L += [f"Each criterion is pass/fail. For example: \"{p['judge_criterion']}\"", ""]
        if f("FM05"):
            L += ["An LLM judge scores every criterion automatically, so we don't need human reviewers in the loop.", ""]
        else:
            L += [f"An LLM judge scores each criterion. Before we trust it, two of us label 100 {p['outputs']} by hand, "
                  "and the judge must agree with our labels at least 90% of the time. We recheck agreement monthly.", ""]
        if f("FM07"):
            L += ["Launch bar: 98% or higher on the eval set, which is built from common, straightforward requests.", ""]
        else:
            L += [f"The eval set deliberately includes {p['hard_cases']}. The prototype passes about 60% of it today, "
                  "which leaves room to show progress and catch regressions.", ""]
        if p["agent"]:
            if f("FM10"):
                L += [f"We score the final {p['output']} only.", ""]
            else:
                L += [f"Because this is an agent, each run is scored as a whole task and step by step ({p['steps']}), "
                      "so we can see which step failed.", ""]
    L += ["## Launch and monitoring", ""]
    if f("FM08"):
        L += ["Once the eval passes, we launch to all customers. After that, improvements follow the regular roadmap.", ""]
    else:
        L += [f"Beta with 20 customers, then general availability. After launch we track {p['online']}.", ""]
    L += ["## Cost and latency", ""]
    if f("FM09"):
        L += [f"We will use {p['model_plan']} to give users the best experience. Cost and speed can be optimized after launch.", ""]
    else:
        L += [f"Targets: {p['latency']}, and {p['cost']}. We will also test {p['cheap_compare']}, "
              "and pick the cheapest setup that holds quality.", ""]
    return "\n".join(L).strip() + "\n"


def plan():
    """Deterministic flaw sets: 5 cases per product, each failure mode planted about 6 times."""
    rng = random.Random(11)
    used = collections.Counter()
    sizes = [2, 1, 3, 2, 2]
    cases = []
    for p in PRODUCTS:
        pool = [fm for fm in FMS if fm != "FM01" and (fm != "FM10" or p["agent"])]
        sets = []
        if p["id"] in ("helpdesk", "analytics", "travel"):
            sets.append(set())
        if p["id"] in ("notes", "contracts", "sales"):
            extra = min(["FM08", "FM09", "FM02"], key=lambda fm: (used[fm], rng.random()))
            used[extra] += 1
            sets.append({"FM01", extra})
        i = 0
        while len(sets) < 5:
            k = sizes[i % len(sizes)]; i += 1
            pick = sorted(pool, key=lambda fm: (used[fm], rng.random()))[:k]
            s = set(pick)
            if s in sets:
                continue
            used.update(s)
            sets.append(s)
        for n, s in enumerate(sets):
            cases.append((p, s, n))
    return cases


def main():
    out = []
    for p, flaws, i in plan():
        cid = f"{p['id']}-{i + 1}"
        out.append({"id": cid, "product": p["id"], "title": f"{p['company']} {p['feature']}",
                    "agent": p["agent"], "planted": sorted(flaws), "labels": labels_for(p, flaws),
                    "prd": prd(p, flaws)})
    (HERE / "data" / "golden.json").write_text(json.dumps({"cases": out}, indent=1))
    c = collections.Counter((fm, v) for x in out for fm, v in x["labels"].items())
    print(len(out), "cases")
    for fm in FMS:
        print(fm, "fail", c[(fm, "fail")], "pass", c[(fm, "pass")], "n/a", c[(fm, "n/a")])
    print("clean cases:", [x["id"] for x in out if not x["planted"]])


if __name__ == "__main__":
    main()
