"""Step 7 reads the idea's size, the cost of a trade on its backtest, and the findings register (operator, 2026-11-20).
One rule for every line: in the shared rules, the shared request, the shared card."""
from pathlib import Path
ST = Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
def edit(p, a, b, count=1):
    p = ST / p; t = p.read_text(); assert t.count(a) == count, (p, a[:60]); p.write_text(t.replace(a, b))

# 1. the cost of a trade, measured on a record: one place, next to the size
p = ST / "common/idea_size.py"; t = p.read_text()
t += '''

def trade_cost(record):
    """What one trade (a buy and a sell) cost this backtest, as a share of the value traded: twice its cost per unit
    traded (the book without costs minus the backtest's own book, over the units traded; topics/34_review/book_diagnosis.md)."""
    free = real = units = 0.0
    for coin in sorted(p for p in pathlib.Path(record).iterdir() if p.is_dir()):
        for f in sorted(coin.glob("w*/bars.csv.gz")):
            b = pd.read_csv(f, usecols=["close", "previous_allocation", "postRebalance_current_allocation", "postRebalance_total_value"])
            a = b["postRebalance_current_allocation"].fillna(0).to_numpy(float); prev = b["previous_allocation"].fillna(0).to_numpy(float)
            c = b["close"].to_numpy(float); v = b["postRebalance_total_value"].to_numpy(float)
            units += float(np.abs(a - prev).sum()); free += float((a[:-1] * (c[1:] / c[:-1] - 1)).sum()); real += float((v[1:] / v[:-1] - 1).sum())
    return 2 * (free - real) / units if units else None
'''
p.write_text(t)

# 2. the shared request: the size and the cost, for every line
edit("07_common/helper/analyse.py", "from lib import", "from idea_size import size as idea_size, trade_cost  # noqa: E402  (common/measures.md, \"The size of an idea\")\nfrom lib import")
edit("07_common/helper/analyse.py",
     '''               f"[THE CHECK OF THE BOOK (step 6)]\\n{no_paths(check) if check.exists() else s6}\\n"''',
     '''               f"[THE CHECK OF THE BOOK (step 6)]\\n{no_paths(check) if check.exists() else s6}\\n"
               f"[THE SIZE OF THE IDEA AND THE COST OF A TRADE]\\n{size_and_cost(args.verdicts_dir / rid / 'size.json', record, plan_text)}\\n"''')
edit("07_common/helper/analyse.py", "def with_common(text):", '''def size_and_cost(size_file, record, plan_text):
    """The idea's size (step 5's size.json, or measured the same way when the verdict predates it) and what one trade
    cost this backtest, in words, for every line (common/measures.md, "The size of an idea")."""
    if size_file.exists():
        s = json.loads(size_file.read_text())
    else:
        h = re.search(r"Horizon:\\s*(\\d+)", plan_text)
        s = idea_size(record, int(h.group(1))) if h else {"cases": 0}
    cost = trade_cost(record)
    if not s.get("cases"):
        return "The idea's size: no case to measure." + (f" One trade (a buy and a sell) cost this backtest {100 * cost:.2f} %." if cost else "")
    p = lambda v: f"{100 * v:+.2f} %"
    lines = [f"The idea's size: per case, over its horizon of {s['horizon_bars']} bars, the unusual move is {p(s['unusual_move'])} "
             f"({s['strength']:.3f} of the coin's usual move over that horizon, {100 * s['usual_move']:.2f} %); the coin's normal "
             f"drift in the case's direction is {p(s['normal_drift'])}; the total move is {p(s['total_move'])}; {s['cases']} cases."]
    if cost:
        lines.append(f"One trade (a buy and a sell) cost this backtest {100 * cost:.2f} % of the value traded (fees and slippage, as it paid "
                     f"them). Per case, the total move is {s['total_move'] / cost:.1f} times that cost and the unusual move "
                     f"{s['unusual_move'] / cost:.1f} times.")
    return "\\n".join(lines)


def with_common(text):''')
edit("07_common/helper/analyse.py", "import argparse", "import argparse, json", 1) if "import argparse, json" not in (ST/"07_common/helper/analyse.py").read_text() and "import json" not in (ST/"07_common/helper/analyse.py").read_text() else None

# 3. the shared rules: how every line reads the size against the cost; the findings register
edit("07_common/helper/common_rules.md",
     "You are given: the trading theory (the brief), the idea that was tested, its test plan (its fidelity, its forecast in\nwords, its strategy config and its criterion), the verdict on the idea's reality, the check of the book's\nprofitability, and a description of the backtest's data. You do not see the data's rows.",
     """You are given: the trading theory (the brief), the idea that was tested, its test plan (its fidelity, its forecast in
words, its strategy config and its criterion), the verdict on the idea's reality, the check of the book's
profitability, the idea's size and what one trade cost this backtest, and a description of the backtest's data. You do
not see the data's rows.

The size of the idea against the cost of a trade. The verdict says whether the idea is real; its size says how large
its move is, per case, over its horizon (HOW THE WORKFLOW MEASURES: "The size of an idea"). A book can only pay if the
move it captures per case covers what a trade costs: the total move (the coin's normal drift included) for the book to
earn at all, the unusual move alone for it to do better than holding the coin. When the move per case is smaller than
the cost, no change of holding, sizing or threshold makes the book pay; what changes it is an idea whose move is larger,
and the ideas you write say how. Read the size with the findings below; it is evidence, never a reason to stop.

What the runs have found so far (evidence from earlier runs, each with its source; a finding is not a rule, and your
own data may say otherwise):
{{FINDINGS}}""")

# 4. the findings register: now read by step 7
edit("common/findings.md", "**Draft for the operator's review (improvement I2, `topics/30_review/WORKFLOW_REVIEW.md`). No step reads it yet.**",
     "**Read by step 7 (every line; operator's go, 2026-11-20). Still a draft for the operator's review: which other steps read it, and who adds entries.**")
edit("common/findings.md", "Proposed readers: step 1 (briefs), step\n2 (ideas), step 7 (the next ideas).", "Readers: step 7 (the next ideas); proposed: step 1 (briefs), step 2 (ideas).")
edit("common/README.md", "| none yet (proposed: steps 1, 2, 7) |", "| step 7 (every line); proposed: steps 1, 2 |")
edit("common/README.md", "| step 5 |", "| steps 5 and 7 (`trade_cost`: step 7) |")

# 5. the shared card
edit("07_common/card.md", "the plan it ran and its brief, step 5's verdict on the idea and step 6's check of the book.",
     """the plan it ran and its brief, step 5's verdict on the idea and step 6's check of the book, **the idea's size and what one
trade cost the backtest** (operator, 2026-11-20): step 5's `size.json`, or the size measured the same way
(`../common/idea_size.py`) when the verdict predates it, and the cost of a buy and a sell measured on the record. Why:
of 103 confirmed ideas that did not pay, 53 had a move per case smaller than the cost of a trade, and none of those
paid (`../runs/RETRO_DIAGNOSIS_RUN.md`); a line that does not see it proposes more ideas of the same small kind. And the
findings register (`../common/findings.md`): what earlier runs measured, as evidence, not rules.""")
edit("07_common/card.md", "**Prompts.** `helper/common_rules.md` + the workflow's measuring definitions (`../common/measures.md`)",
     "**Prompts.** `helper/common_rules.md` (with the findings register, `../common/findings.md`, pasted at `{{FINDINGS}}`) + the workflow's measuring definitions (`../common/measures.md`)")
edit("07_common/card.md", "- **How many looks at the data** a line takes before its ideas.",
     "- **How many looks at the data** a line takes before its ideas.\n- **Ideas after a move too small for its cost** (since 2026-11-20): do they make the move larger (a longer horizon, a\n  stronger situation), and do those ideas pay when tested? First read: `../runs/STEP7_SIZE_AB_RUN.md`.")
print("applied")
