"""Diagnostic (no model call, no new backtest): step 6's measures on one group of a backtest's coins.

  python coin_groups.py STEPS_DIR RECORD COIN [COIN ...]

Used on the more-coins idea (7.b): its 19-coin backtest split into the 6 coins the lineage's analyses read and the
coins they never read. Same code as step 6 (check_profitability.check) on a folder holding only that group's coins.
"""
import sys, tempfile, yaml
from pathlib import Path
STEPS, RECORD, COINS = Path(sys.argv[1]), Path(sys.argv[2]), set(sys.argv[3:])
sys.path.insert(0, str(STEPS / "06_profitability" / "helper"))
import check_profitability as cp
rule = yaml.safe_load(open(STEPS / "06_profitability/helper/rule.yaml"))
with tempfile.TemporaryDirectory() as t:
    for c in RECORD.iterdir():
        if c.is_dir() and c.name in COINS:
            (Path(t) / c.name).symlink_to(c.resolve())
    measures, info = cp.check(Path(t), rule)
print("coins:", ", ".join(info["coins"]), f"({info['windows']} windows, {info['years']:.1f} years)")
for m in measures:
    print(f"  {m['label']}: {m['value']:.4f} ({m['comparison']} {m['threshold']}: {'passed' if m['passed'] else 'failed'})")
print(f"  holding's Sharpe: {info['holding_sharpe']:.3f}; a year: {info['annualised_return']:.1%}; deepest fall: {info['deepest_fall']:.1%}")
