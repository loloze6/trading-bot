"""Topic 47, measurement 1b (operator, 2026-11-23: a crash hurts a book only if it is on the wrong side): for every
confirmed book of the night-5 runs, which sides it takes (share of its coin-days in a position that are long, short),
and over its deepest fall (step 6's chain), which side it held and what holding its coins did. Writes side_in_fall.csv.
  python3 topics/47_review/side_in_fall.py"""
import json, pathlib, sys
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from calmar_gate import STEPS, RUNS, calmar, chain   # noqa: E402  (importing runs calmar_gate's summary once)

rows = []
gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
for _, g in gate.iterrows():
    rec = STEPS / "04_backtest" / g.run / "backtests" / g.backtest
    b = pd.read_csv(rec / "chart_bars.csv.gz", parse_dates=["timestamp"])
    b["day"] = b["timestamp"].dt.normalize(); b["w"] = b["window"].str[1:].astype(int)
    last = b.groupby(["coin", "w", "day"]).last().reset_index()
    pos = np.sign(last["position"].astype(float))
    on = pos != 0
    long_share = float((pos > 0).sum() / max(on.sum(), 1)); short_share = float((pos < 0).sum() / max(on.sum(), 1))
    # the chain in step 6's order, with each day's mean side over coins
    bk, hd, side = {}, {}, {}
    for (coin, w), d in last.groupby(["coin", "w"]):
        d = d.set_index("day")
        bk.setdefault(w, []).append(d["value"].pct_change().dropna().rename(coin))
        hd.setdefault(w, []).append(d["close"].pct_change().dropna().rename(coin))
        side.setdefault(w, []).append(np.sign(d["position"].astype(float)).iloc[:-1].set_axis(d.index[1:]).rename(coin))  # side held into the day
    br, hr, sd = chain(bk), chain(hd), chain(side)
    _, _, fall, p, t = calmar(br)
    span = slice(p + 1, t + 1)
    rows.append({"run": g.run, "backtest": g.backtest, "pays": g.pays, "net_per_trade_pct": g.net_per_trade_pct,
                 "deepest_fall": fall, "long_share": long_share, "short_share": short_share,
                 "two_sided": long_share > 0.05 and short_share > 0.05,
                 "holding_over_the_fall": float(np.prod(1 + hr[span]) - 1) if t > p else 0.0,
                 "mean_side_over_the_fall": float(np.nanmean(sd[span])) if t > p else 0.0,
                 "days_in_a_position_over_the_fall": float(np.nanmean(np.abs(sd[span]))) if t > p else 0.0})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("side_in_fall.csv"), index=False, float_format="%.4g")
n = d[~d.pays]
A = n.net_per_trade_pct <= 0; B = (~A) & (n.holding_over_the_fall < -0.2)
print("\n== side of the books (not paying 72; paying 9)")
for name, x in (("not paying", n), ("paying", d[d.pays])):
    print(f" {name}: long only {int((x.short_share <= 0.05).sum())}, short only {int((x.long_share <= 0.05).sum())}, both sides {int(x.two_sided.sum())}")
b = n[B]
print(f"\n== the {len(b)} books whose deepest fall came while their coins fell more than 20 %")
print(f" long only {int((b.short_share <= 0.05).sum())}, short only {int((b.long_share <= 0.05).sum())}, both sides {int(b.two_sided.sum())}")
print(" mean side held over the fall (+1 all long, -1 all short), quartiles:", b.mean_side_over_the_fall.quantile([.25, .5, .75]).round(2).tolist())
print(" share of coin-days in a position over the fall, quartiles:", b.days_in_a_position_over_the_fall.quantile([.25, .5, .75]).round(2).tolist())
tw = b[b.two_sided]
if len(tw):
    print(" the two-sided ones: mean side over the fall", tw.mean_side_over_the_fall.round(2).tolist())
