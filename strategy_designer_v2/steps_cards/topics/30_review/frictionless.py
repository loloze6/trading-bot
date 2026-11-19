"""The book at the bars' own closes, no friction: sum over bars of allocation held after bar t's close x the next bar's
return. Per idea, over every coin and window; next to the engine's gross (after spread and slippage) and net."""
import sys
from pathlib import Path
import pandas as pd
d = pd.read_csv(Path(sys.argv[1]) / "ideas.csv")
ROOTS = [Path("/home/user/trading-bot/strategy_designer_v2/steps_cards"), Path(sys.argv[1]) / "strategy_designer_v2/steps_cards"]
sel = d[d.run.isin(["slow_1h_run", "intraday_1h_run", "retest_1h_run"]) | (d.run == "night_013_run")]
out = []
for _, r in sel.iterrows():
    root = next(x for x in ROOTS[::-1] if (x / "04_backtest" / r.run / "backtests" / r.bt).exists())
    tot = turn = 0.0; n = 0
    for f in (root / "04_backtest" / r.run / "backtests" / r.bt).glob("*/w*/bars.csv.gz"):
        b = pd.read_csv(f, usecols=["close", "postRebalance_current_allocation"])
        a = b["postRebalance_current_allocation"].fillna(0)
        ret = b["close"].pct_change().shift(-1).fillna(0)
        tot += (a * ret).sum() * 1000; turn += a.diff().abs().sum(); n += 1
    out.append({"run": r.run, "bt": r.bt, "confirmed": r.confirmed, "profitable": r.profitable,
                "at_closes": tot, "gross": r.gross, "net": r.net, "fees": r.fees, "turnover": turn, "windows": n})
o = pd.DataFrame(out); o.to_csv(Path(sys.argv[1]) / "frictionless.csv", index=False)
print(len(o), "ideas")
