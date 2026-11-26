"""Topic 47, phase A (runs/BOOK_REFLECTS_IDEA_RUN.md): the five books rebuilt to trade only the idea's situation,
against the same ideas' night-5 books, on the same measures as calmar_gate.py and side_in_fall.py.
  python3 topics/47_review/phase_a_compare.py"""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import calmar_gate as cg   # noqa: E402  (prints its own summary on import)

STEPS = cg.STEPS; RUN = "book_reflects_idea_run"


def measures(run, rid):
    rec = STEPS / "04_backtest" / run / "backtests" / rid
    res = json.load(open(STEPS / "06_profitability" / run / "checks" / rid / "result.json"))
    v = json.load(open(STEPS / "05_verification" / run / "verdicts" / rid / "result.json"))
    br, hr, idx, _, _ = cg.book(rec)
    c, ann, fall, p, t = cg.calmar(br)
    b = pd.read_csv(rec / "chart_bars.csv.gz", parse_dates=["timestamp"])
    b["day"] = b["timestamp"].dt.normalize()
    last = b.groupby(["coin", "window", "day"]).last()
    n, net, gross = cg.trades(rec)
    return {"step5": v.get("status"), "step6": res["status"], "failed": "; ".join(x["label"] for x in res["measures"] if not x["passed"]),
            "days_in_position": float((last["position"] != 0).mean()), "trades": n, "net_per_trade_pct": net, "gross_per_trade_pct": gross,
            "yearly_return": ann, "deepest_fall": fall, "calmar": c, "market_over_the_fall": float(np.prod(1 + hr[p + 1:t + 1]) - 1) if t > p else 0.0}


rows = []
for rec in sorted((STEPS / "04_backtest" / RUN / "backtests").iterdir()):
    if not rec.is_dir(): continue
    rid = rec.name
    src = next(r for r in cg.RUNS if (STEPS / "06_profitability" / r / "checks" / rid / "result.json").exists())
    for name, run in (("night 5", src), ("phase A", RUN)):
        rows.append({"idea": rid.split(".")[-1], "book": name, **measures(run, rid)})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("phase_a_compare.csv"), index=False, float_format="%.4g")
pd.set_option("display.width", 250)
print("\n", d.assign(days_in_position=(100 * d.days_in_position).round(0), yearly_return=(100 * d.yearly_return).round(1),
                     deepest_fall=(100 * d.deepest_fall).round(1), market_over_the_fall=(100 * d.market_over_the_fall).round(0),
                     calmar=d.calmar.round(2), net_per_trade_pct=d.net_per_trade_pct.round(2), gross_per_trade_pct=d.gross_per_trade_pct.round(2))
      [["idea", "book", "step5", "step6", "days_in_position", "trades", "gross_per_trade_pct", "net_per_trade_pct", "yearly_return", "deepest_fall", "market_over_the_fall", "calmar", "failed"]].to_string(index=False))
