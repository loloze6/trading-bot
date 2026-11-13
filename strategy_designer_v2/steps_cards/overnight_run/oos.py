"""Orchestrator tool (overnight run): the unseen-coin check of a plan. Copies a test plan and its config unchanged,
except its data: coins the analyst never saw, in the folds where they all have data. The copy's id ends in `_oos`.

  python oos.py PLAN.md OUT_DIR
"""
import re, shutil, sys
from pathlib import Path
COINS, PERIOD = "ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ", "folds A, D"
plan, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
new = plan.stem + "_oos"
t = plan.read_text()
t = re.sub(r"(?m)^data-instruments:.*$", f"data-instruments: {COINS}", t, count=1)
t = re.sub(r"(?m)^data-period:.*$", f"data-period: {PERIOD}", t, count=1)
t = t.replace(f"Config: {plan.stem}_config.json", f"Config: {new}_config.json")
(out / f"{new}.md").write_text(t)
shutil.copy(plan.with_name(plan.stem + "_config.json"), out / f"{new}_config.json")
print(out / f"{new}.md")
