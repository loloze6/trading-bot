"""Orchestrator tool (overnight run): judges step 7's two modes with closed-book model calls.
1. Stability: for each line, backtest and mode, how many ideas of exercise 2 match an idea of exercise 1.
2. Blind quality: for each line, backtest and exercise, the one-call and split idea sets under random labels A/B."""
import glob, json, random, re, sys
from pathlib import Path
SC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SC / "03_test_plan" / "helper"))
from make_test_plan import call   # noqa: E402
random.seed(13)
JUDGE = "You are an experienced crypto trader and quantitative researcher, asked to judge analysts' output. Be strict and brief."
OBJ = {}
for p in SC.glob("07?_*/card.md"):
    m = re.search(r"## Business objective\n\*\*(.+?)\*\*", p.read_text(), re.S)
    OBJ[p.parent.name] = m.group(1) if m else ""
def ideas_block(o, with_findings=True):
    out = []
    for i, g in enumerate(o["ideas"], 1):
        out.append(f"Idea {i}: {g['idea']}")
        if with_findings:
            out += [f"   supported by {r}: {o['findings'][r]}" for r in g["refs"]]
    return "\n".join(out) or f"(no ideas: {o.get('no_ideas')})"
rows, cost = [], 0.0
cases = sorted({(p.split("/")[0], p.split("/")[3]) for p in glob.glob("07[abcdg]_*/exercise_1/*/*/result.json", root_dir=SC)})
for line, rid in cases:
    for mode in ("one_call", "split"):
        f1, f2 = SC / line / "exercise_1" / mode / rid / "result.json", SC / line / "exercise_2" / mode / rid / "result.json"
        if not (f1.exists() and f2.exists()):
            continue
        o1, o2 = json.loads(f1.read_text()), json.loads(f2.read_text())
        if not o2["ideas"]:
            rows.append(("stability", line, rid, mode, "run 2 has no ideas", 0, 0)); continue
        q = (f"Two runs of the same analysis proposed these ideas.\n[RUN 1]\n{ideas_block(o1, False)}\n[RUN 2]\n{ideas_block(o2, False)}\n\n"
             "For each idea of run 2, say whether run 1 has an idea with the same situation and the same direction (wording and exact settings may differ). "
             "Answer with one line per idea of run 2, 'Idea k: yes' or 'Idea k: no', then a last line 'matched: <n> of <m>'.")
        t, c = call("claude-opus-5-5", JUDGE, q); cost += c
        m = re.search(r"matched:\s*(\d+)\s*of\s*(\d+)", t)
        rows.append(("stability", line, rid, mode, t.strip().splitlines()[-1], int(m.group(1)) if m else -1, int(m.group(2)) if m else -1))
    for ex in ("exercise_1", "exercise_2"):
        fa, fb = SC / line / ex / "one_call" / rid / "result.json", SC / line / ex / "split" / rid / "result.json"
        if not (fa.exists() and fb.exists()):
            continue
        oa, ob = json.loads(fa.read_text()), json.loads(fb.read_text())
        swap = random.random() < 0.5
        A, B = (ob, oa) if swap else (oa, ob)
        q = (f"The analysis's objective: {OBJ.get(line, '')}\n\n[SET A]\n{ideas_block(A)}\n\n[SET B]\n{ideas_block(B)}\n\n"
             "Which set is better, judged on: (1) each idea follows from the findings it cites; (2) the ideas serve the objective; "
             "(3) a trader would act on them; (4) a test on one coin's own bars could check them. More ideas is not better in itself. "
             "Answer in two lines: 'better: A' or 'better: B' or 'better: tie', then 'why: <one sentence>'.")
        t, c = call("claude-opus-5-5", JUDGE, q); cost += c
        m = re.search(r"better:\s*(A|B|tie)", t)
        w = m.group(1) if m else "?"
        winner = {"A": "split" if swap else "one_call", "B": "one_call" if swap else "split"}.get(w, w)
        why = re.search(r"why:\s*(.+)", t)
        rows.append(("quality", line, rid, ex, winner, why.group(1)[:220] if why else t[:200], 0))
out = SC / "overnight_run" / "mode_judgement.json"
out.write_text(json.dumps({"rows": rows, "cost": cost}, indent=1))
for r in rows: print(r)
print("cost", round(cost, 2))
