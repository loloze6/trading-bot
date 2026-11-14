"""Orchestrator tool (overnight run, not a step). Turns a chosen step 7 idea into a clean idea file for step 3: the
brief and the data lines, then `Idea:` and `Consequence:` only. Step 7's `Why` (numbers measured on the data) and its
origin lines are left out, so step 3 stays closed book. The lineage goes to a log next to the hand-off folder.

  python handoff.py STEP7_IDEA_FILE NEW_ID OUT_DIR [--instruments ...] [--period ...] [--bar ...]
"""
import argparse, re
from pathlib import Path

a = argparse.ArgumentParser()
a.add_argument("idea", type=Path)
a.add_argument("new_id")
a.add_argument("out_dir", type=Path)
a.add_argument("--instruments"); a.add_argument("--period"); a.add_argument("--bar")
args = a.parse_args()
text = args.idea.read_text()
m = re.match(r"\s*---\n(.*?)---\n(.*)", text, re.S)
h = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)}
body = m.group(2)
idea = re.search(r"^Idea:\s*(.+)$", body, re.M).group(1).strip()
cons = re.search(r"^Consequence:\s*(.+)$", body, re.M).group(1).strip()
data = {k: getattr(args, k) or h.get(k) for k in ("instruments", "bar", "period")}
args.out_dir.mkdir(parents=True, exist_ok=True)
out = "---\n" + f"brief: {h['brief']}\n" + "".join(f"{k}: {v}\n" for k, v in data.items() if v) + "---\n" + f"Idea: {idea}\nConsequence: {cons}\n"
(args.out_dir / f"{args.new_id}.md").write_text(out)
with open(args.out_dir / "LINEAGE.md", "a") as f:
    f.write(f"- `{args.new_id}` <- `{args.idea.stem}` (line {h.get('line', '')}; backtest {h.get('backtest', '')})\n")
print(args.new_id)
