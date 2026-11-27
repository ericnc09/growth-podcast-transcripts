"""Build the golden set: 30 standard and 12 hard fictional AI-feature PRDs with planted failure modes and exact labels.

Each PRD is assembled from sections. For every failure mode there is a sound version and a flawed
version of the relevant passage, so the label is known by construction, not judged.

Usage: python3 eval-studio/gen_golden.py  ->  writes data/golden.json (cases) and prints label counts
"""
import json, random, pathlib, sys, collections
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from data_src_products import PRODUCTS

HERE = pathlib.Path(__file__).resolve().parent
FMS = [f"FM{i:02d}" for i in range(1, 11)]
EVAL_DEPENDENT = {"FM03", "FM04", "FM05", "FM07", "FM10"}
FAILING = {"flaw", "generic", "fuzzy", "subtle"}   # variants that plant the failure mode
# Variants per failure mode:
#   sound   the passage avoids the problem
#   flaw    the obvious version of the problem (FM03 has two: "generic" metrics or a "fuzzy" rubric)
#   subtle  the problem, stated so it looks reasonable at a glance
#   near    a passage that looks like the problem but is sound (a trap for over-eager judges)
#   split   the sound passage, moved to a section where a judge may not look


def labels_for(p, v):
    out = {}
    for fm in FMS:
        if fm == "FM10" and not p["agent"]:
            out[fm] = "n/a"
        elif v.get("FM01") in FAILING and fm in EVAL_DEPENDENT:
            out[fm] = "n/a"
        else:
            out[fm] = "fail" if v.get(fm, "sound") in FAILING else "pass"
    return out


def prd(p, v):
    g = lambda fm: v.get(fm, "sound")
    L = [f"# {p['company']} {p['feature']}: product requirements",
         "",
         f"*{p['company']} is a fictional {p['kind']}. This PRD is a test case, not a real document.*",
         "",
         "## Problem", "", p["problem"], "",
         "## Users", "", f"Primary users are {p['users']}.", "",
         "## Proposed solution", "", p["solution"], "",
         "## Requirements", ""]
    if g("FM02") == "flaw":
        L += [p["vague"], "",
              f"- The {p['output']} uses all relevant context available to it.",
              "- It handles edge cases gracefully.",
              "- It feels natural and on-brand.", ""]
    else:
        L += ["Expected behaviour on representative inputs. Each row is also a test case in the eval set.", "",
              "| Input | Expected behaviour |", "| --- | --- |"]
        if g("FM02") == "subtle":
            vague = ["Responds helpfully and accurately", "Handles the situation appropriately", "Gives the user a good result"]
            L += [f"| {a} | {b} |" for (a, _), b in zip(p["examples"], vague)]
        else:
            L += [f"| {a} | {b} |" for a, b in p["examples"]]
        L += [""]
        if g("FM02") == "near":
            L += [f"Beyond these cases, the {p['output']} should feel natural and on-brand.", ""]
    L += ["## Quality and evaluation", ""]
    if g("FM01") == "flaw":
        L += [f"Our own team will dogfood {p['feature']} for two weeks before the beta. "
              "We will ship when the team agrees the quality feels right, and keep an eye on customer feedback after that.", ""]
    else:
        if g("FM01") == "near":
            L += [f"Our own team will also dogfood {p['feature']} for two weeks before the beta, "
                  "but dogfooding doesn't decide the launch. The eval below does.", ""]
        if g("FM04") == "flaw":
            L += ["Risks we anticipate: the model may hallucinate, may show bias, or may be off-tone. We will write evals for each of these.", ""]
        elif g("FM04") == "subtle":
            obs = "; ".join(p["observed"])
            L += [f"We listed failure modes from published research on LLM errors and a team brainstorm. "
                  f"The ones we expect most are: {obs}. We will write an eval for each before the prototype is built.", ""]
        else:
            obs = "; ".join(p["observed"])
            L += [f"Before choosing metrics, we reviewed 100 {p['outputs']} from the prototype and grouped what went wrong. "
                  f"The most common failures were: {obs}. We repeat this review whenever we change the prompt or the model.", ""]
        L += [f"We will measure {p['generic_metrics'] if g('FM03') == 'generic' else p['specific_metrics']}.", ""]
        if g("FM03") == "near":
            L += [f"We also log {p['generic_metrics']} for reference, but they don't gate the launch.", ""]
        if g("FM03") == "fuzzy":
            L += [f"Graders rate each {p['output']} from 1 to 5 on accuracy, helpfulness and tone, and we track the average.", ""]
        elif g("FM03") == "subtle":
            L += [f"Each criterion is pass/fail. For example: \"Is the {p['output']} high quality and useful? (pass/fail)\"", ""]
        else:
            L += [f"Each criterion is pass/fail. For example: \"{p['judge_criterion']}\"", ""]
        if g("FM05") == "flaw":
            L += ["An LLM judge scores every criterion automatically, so we don't need human reviewers in the loop.", ""]
        elif g("FM05") == "subtle":
            L += ["An LLM judge scores each criterion. The PM read the judge's prompt closely and spot-checked about ten of its scores, which looked right.", ""]
        elif g("FM05") == "near":
            L += [f"An LLM judge scores each criterion. A team lead labelled 100 {p['outputs']} by hand, and the judge "
                  "agreed with those labels 91% of the time against a target of 90%. We recheck agreement every quarter.", ""]
        else:
            L += [f"An LLM judge scores each criterion. Before we trust it, two of us label 100 {p['outputs']} by hand, "
                  "and the judge must agree with our labels at least 90% of the time. We recheck agreement monthly.", ""]
        if g("FM07") == "flaw":
            L += ["Launch bar: 98% or higher on the eval set, which is built from common, straightforward requests.", ""]
        elif g("FM07") == "subtle":
            L += ["Launch bar: 95% on the eval set, which we sampled from last month's 300 most common requests.", ""]
        elif g("FM07") == "near":
            L += [f"Launch bar: 98% on the core regression set of common requests. A separate hard set ({p['hard_cases']}) "
                  "starts at about 55% and is tracked every release. We expect it to keep failing for a while.", ""]
        else:
            L += [f"The eval set deliberately includes {p['hard_cases']}. The prototype passes about 60% of it today, "
                  "which leaves room to show progress and catch regressions.", ""]
        if p["agent"]:
            if g("FM10") == "flaw":
                L += [f"We score the final {p['output']} only.", ""]
            elif g("FM10") == "subtle":
                L += [f"Each run is scored on whether the final {p['output']} is correct. We log every tool call so engineers can debug failures.", ""]
            elif g("FM10") == "sound":
                L += [f"Because this is an agent, each run is scored as a whole task and step by step ({p['steps']}), "
                      "so we can see which step failed.", ""]
    L += ["## Safety and guardrails", ""]
    if g("FM06") == "flaw":
        L += ["We will follow the company's responsible AI guidelines and add guardrails if issues come up during the beta.", ""]
    elif g("FM06") == "subtle":
        L += [f"The system prompt tells the model it must never {p['never']}.", ""]
    else:
        L += [f"The feature must never {p['never']}. {p['guard']}. "
              f"The eval set includes {p['safety_tests']}, and any failure there blocks a release.", ""]
    L += ["## Launch and monitoring", ""]
    if g("FM08") == "flaw":
        L += ["Once the eval passes, we launch to all customers. After that, improvements follow the regular roadmap.", ""]
    elif g("FM08") == "subtle":
        L += ["Beta with 20 customers, then general availability. After launch we track weekly active users, retention and adoption of the feature.", ""]
    else:
        L += [f"Beta with 20 customers, then general availability. After launch we track {p['online']}.", ""]
    if p["agent"] and g("FM10") == "split" and g("FM01") not in FAILING:
        L += [f"Both the eval set and a weekly sample of beta runs are scored as whole tasks and step by step ({p['steps']}), "
              "so we can see which step failed.", ""]
    if g("FM09") == "split":
        L += [f"Launch targets: {p['latency']}, and {p['cost']}. Before launch we also test {p['cheap_compare']}, "
              "and pick the cheapest setup that holds quality.", ""]
    L += ["## Cost and latency", ""]
    if g("FM09") == "flaw":
        L += [f"We will use {p['model_plan']} to give users the best experience. Cost and speed can be optimized after launch.", ""]
    elif g("FM09") == "subtle":
        L += [f"Target: {p['latency']}. We will use {p['model_plan']} so quality is never the bottleneck.", ""]
    elif g("FM09") == "split":
        L += ["Targets and the cheaper-model test are in the launch plan above.", ""]
    else:
        L += [f"Targets: {p['latency']}, and {p['cost']}. We will also test {p['cheap_compare']}, "
              "and pick the cheapest setup that holds quality.", ""]
    return "\n".join(L).strip() + "\n"


def plan():
    """Deterministic flaw sets: 5 standard cases per product, each failure mode planted about 6 times."""
    rng = random.Random(11)
    used = collections.Counter()
    sizes = [2, 1, 3, 2, 2]
    cases = []
    fm03_style = 0
    for p in PRODUCTS:
        pool = [fm for fm in FMS if fm != "FM01" and (fm != "FM10" or p["agent"])]
        sets = []
        if p["id"] in ("helpdesk", "analytics", "travel"):
            sets.append(set())
        if p["id"] in ("notes", "contracts", "sales"):
            extra = min(["FM08", "FM09", "FM02", "FM06"], key=lambda fm: (used[fm], rng.random()))
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
            v = {}
            for fm in s:
                if fm == "FM03":
                    v[fm] = ("generic", "fuzzy")[fm03_style % 2]; fm03_style += 1
                else:
                    v[fm] = "flaw"
            cases.append((p, v, f"{p['id']}-{n + 1}", "standard"))
    return cases


# Hard cases: subtle flaws, sound passages that look like flaws, and sound passages in an unexpected section.
HARD = {
    "helpdesk": [{"FM02": "subtle", "FM05": "near", "FM07": "near", "FM09": "split"},
                 {"FM03": "subtle", "FM04": "subtle", "FM06": "subtle"}],
    "notes": [{"FM05": "subtle", "FM07": "subtle", "FM03": "near"},
              {"FM08": "subtle", "FM01": "near", "FM09": "subtle"}],
    "sales": [{"FM10": "subtle", "FM06": "subtle", "FM02": "near"},
              {"FM10": "split", "FM04": "subtle", "FM07": "near", "FM05": "subtle"}],
    "contracts": [{"FM03": "subtle", "FM08": "subtle", "FM09": "split"},
                  {"FM01": "near", "FM02": "subtle", "FM05": "near", "FM07": "subtle"}],
    "analytics": [{"FM10": "subtle", "FM09": "subtle", "FM03": "near"},
                  {"FM10": "split", "FM06": "subtle", "FM08": "subtle", "FM04": "subtle"}],
    "travel": [{"FM07": "subtle", "FM05": "subtle", "FM02": "near", "FM01": "near"},
               {"FM10": "split", "FM09": "split", "FM03": "near", "FM07": "near"}],
}


def hard_plan():
    return [(p, v, f"{p['id']}-h{n + 1}", "hard") for p in PRODUCTS for n, v in enumerate(HARD[p["id"]])]


def main():
    out = []
    for p, v, cid, kind in plan() + hard_plan():
        out.append({"id": cid, "set": kind, "product": p["id"], "title": f"{p['company']} {p['feature']}",
                    "agent": p["agent"], "planted": sorted(fm for fm, x in v.items() if x in FAILING),
                    "variants": dict(sorted(v.items())), "labels": labels_for(p, v), "prd": prd(p, v)})
    (HERE / "data" / "golden.json").write_text(json.dumps({"cases": out}, indent=1))
    for kind in ("standard", "hard"):
        xs = [x for x in out if x["set"] == kind]
        c = collections.Counter((fm, v) for x in xs for fm, v in x["labels"].items())
        print(kind, len(xs), "cases")
        for fm in FMS:
            print(" ", fm, "fail", c[(fm, "fail")], "pass", c[(fm, "pass")], "n/a", c[(fm, "n/a")])
    print("clean cases:", [x["id"] for x in out if not x["planted"]])


if __name__ == "__main__":
    main()
