"""Combining two strategies (runs/COMBINE_TEST_RUN.md). Method A: two books side by side, half the capital each: the
combination's daily return is the mean of the two books' daily returns. Each book's daily returns as step 6 builds them
(per coin, then the mean of the coins), on the coins named. Measures as step 6 computes them. No backtest, no model call.

  python3 topics/08_review/combine_test.py
"""
import json, math, re, sys
from pathlib import Path
import numpy as np, pandas as pd

ST = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ST / "orchestration/ideas_similarities_check/helper"))
import book_returns as br  # noqa: E402

PAIRS = {"different": ("d1_strong-monthly-rises-continue_1d", "g2_volatile-reversal-completes-quickly_1d"),
         "in between": ("g1_rising-month-weekly-momentum_1d", "c1_high-rsi-trend-continuation_1d"),
         "similar": ("d2_strong-rises-keep-rising_1d", "d1_strong-monthly-rises-continue_1d")}


def record(suffix, root=ST / "04_backtest/paying_rerun_run/backtests"):
    hits = [p for p in root.iterdir() if p.name.endswith(suffix)]
    assert len(hits) == 1, (suffix, hits)
    return hits[0]


def coins_of(rec):
    return sorted(p.name for p in rec.iterdir() if p.is_dir())


def daily(rec, coins):
    parts = {}
    for coin, w, f in br.coin_windows(rec):
        if coin not in coins:
            continue
        d = pd.read_csv(f, usecols=["timestamp", "close", "postRebalance_total_value"])
        parts.setdefault(w, []).append(br.period_returns(d["postRebalance_total_value"], d["timestamp"], "1d").rename(coin))
    rows = [pd.DataFrame({"window": w, "period": s.index, "r": s.to_numpy()})
            for w in sorted(parts) for s in [pd.concat(parts[w], axis=1, sort=True).mean(axis=1)]]
    return pd.concat(rows, ignore_index=True).set_index(["window", "period"])["r"]


def measures(r):
    r = r.sort_index().to_numpy(float)
    sd = r.std(ddof=1)
    curve = np.cumprod(1 + r); years = len(r) / 365
    ann = curve[-1] ** (1 / years) - 1 if curve[-1] > 0 else -1.0
    fall = float(np.max(1 - curve / np.maximum.accumulate(np.concatenate([[1.0], curve]))[1:]))
    return {"sharpe": r.mean() / sd * math.sqrt(365), "calmar": ann / fall if fall > 0 else math.inf, "deepest_fall": fall,
            "daily_sd": sd, "mean_daily": r.mean(), "days": len(r)}


def run():
    out = {}
    for name, (s1, s2) in PAIRS.items():
        r1, r2 = record(s1), record(s2)
        common = sorted(set(coins_of(r1)) & set(coins_of(r2)))
        views = {"common coins": (common, common)}
        if coins_of(r1) != coins_of(r2):
            views["as recorded"] = (coins_of(r1), coins_of(r2))
        for view, (c1, c2) in views.items():
            a, b = daily(r1, c1), daily(r2, c2)
            both = pd.concat([a.rename("a"), b.rename("b")], axis=1, join="inner").dropna()
            res = {"book 1": measures(both["a"]), "book 2": measures(both["b"]), "A: side by side": measures(both.mean(axis=1)),
                   "correlation": float(np.corrcoef(both["a"], both["b"])[0, 1]), "coins": [c1, c2]}
            out[f"{name} | {view}"] = res
    return out


if __name__ == "__main__":
    res = run()
    (Path(__file__).parent / "combine_test_A.json").write_text(json.dumps(res, indent=2, default=float) + "\n")
    for k, v in res.items():
        print(f"\n== {k} (correlation {v['correlation']:+.2f}; coins {len(v['coins'][0])} and {len(v['coins'][1])})")
        for who in ("book 1", "book 2", "A: side by side"):
            m = v[who]
            print(f"  {who:16s} Sharpe {m['sharpe']:.2f}  Calmar {m['calmar']:.2f}  deepest fall {100*m['deepest_fall']:5.1f} %  "
                  f"daily sd {100*m['daily_sd']:.3f} %  mean {100*m['mean_daily']:.4f} %  days {m['days']}")
