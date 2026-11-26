"""The reading's table of runs/UNSEEN_COINS_RUN.md: one row per book of books.tsv, from the files the run wrote.
  python3 runs/unseen_coins/reading.py      -> runs/unseen_coins/table.csv, and the counts printed
Per book: its unseen-coins entry (orchestration/unseen_test/<run>/<id>.json), its unseen periods' holds (same file),
its in-sample step 6 Sharpe (06_profitability/<run>/checks/<id>/result.json), and, from its unseen-coins record's
run.md, how many (coin, window) pairs were skipped for lack of data and how many the engine refused (warm-up not ready
after a coin's listing)."""
import csv, json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sharpe(check):
    return next((m["value"] for m in (check or {}).get("measures", []) if m["measure"] == "sharpe_min"), None)


said = {True: "holds", False: "does not hold", None: "-"}
rows = []
for line in (HERE / "books.tsv").read_text().splitlines():
    group, run, rid = line.split("\t")
    res = load(STEPS / "orchestration/unseen_test" / run / f"{rid}.json") or {}
    per = res.get("periods") or {}
    c = per.get("unseen_coins")
    rec = STEPS / "04_backtest" / run / "unseen_coins/backtests" / rid / "run.md"
    text = rec.read_text() if rec.exists() else ""
    ins_main = (res.get("in_sample") or {}).get("main")
    rows.append({
        "group": group, "run": run, "book": rid, "bar": rid.rsplit("_", 1)[-1],
        "unseen_coins": ("not run" if c is None else "none" if not c.get("coins_asked") else said[c.get("holds")]),
        "coins_asked": len(c.get("coins_asked") or []) if c else "", "coins_ran": len(c.get("coins") or []) if c else "",
        "coin_windows": c.get("coin_windows", "") if c else "", "years": c.get("years", "") if c else "",
        "skipped_no_data": len(re.findall(r"not run: no historical data", text)),
        "refused_warm_up": len(re.findall(r"not run: the engine stopped", text)),
        "step5": c.get("step5", "") if c else "", "main": c.get("main", "") if c else "", "in_sample_main": ins_main,
        "sharpe": c.get("sharpe", "") if c else "", "holding_sharpe": c.get("holding_sharpe", "") if c else "",
        "step6": c.get("step6", "") if c else "",
        "in_sample_sharpe": sharpe(load(STEPS / "06_profitability" / run / "checks" / rid / "result.json")),
        "unseen_2016_2017": said[(per.get("unseen_2016_2017") or {}).get("holds")],
        "unseen_2026": said[(per.get("unseen_2026") or {}).get("holds")],
    })
with open(HERE / "table.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    for r in rows:
        w.writerow({k: (f"{v:.4g}" if isinstance(v, float) else v) for k, v in r.items()})

tested = [r for r in rows if r["unseen_coins"] in ("holds", "does not hold")]
print(f"books {len(rows)}; with unseen coins and judged {len(tested)}; hold {sum(r['unseen_coins'] == 'holds' for r in tested)}")
for g in ("P4", "P11", "N7"):
    t = [r for r in tested if r["group"] == g]
    print(f"  {g}: {sum(r['unseen_coins'] == 'holds' for r in t)} of {len(t)} hold; none {sum(r['unseen_coins'] == 'none' for r in rows if r['group'] == g)};"
          f" not run {sum(r['unseen_coins'] == 'not run' for r in rows if r['group'] == g)}")
for a in ("holds", "does not hold"):
    for b in ("holds", "does not hold"):
        t = [r for r in tested if r["unseen_2016_2017"] == a and r["unseen_2026"] == b]
        print(f"  2016-17 {a}, 2026 {b}: {sum(r['unseen_coins'] == 'holds' for r in t)} of {len(t)} hold on unseen coins")
for bar in ("1d", "1h"):
    t = [r for r in tested if r["bar"] == bar]
    print(f"  {bar}: {sum(r['unseen_coins'] == 'holds' for r in t)} of {len(t)} hold")
print(f"  skipped (no data) {sum(r['skipped_no_data'] for r in rows)}; refused (warm-up) {sum(r['refused_warm_up'] for r in rows)};"
      f" step 5 refused (no verdict) {sum(r['step5'] == 'no verdict' for r in tested)}")
