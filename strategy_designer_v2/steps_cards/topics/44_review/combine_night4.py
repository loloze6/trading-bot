"""Test 2 of runs/NIGHT4_RUN.md: 025-03.d2 combined with momentum, method A of runs/COMBINE_TEST_RUN.md (side by side,
half the capital each: each day the mean of the two books' daily returns), with the earlier test's own functions
(topics/08_review/combine_test.py: step 6's measures; daily returns per coin as step 6 builds them, each day on
the coins both books hold that day). On the folds (the records)
and on the unseen periods (step 4 rerun on each plan with 04_backtest/windows/unseen_*.json, into UNSEEN_ROOT).
No model call. Why this can't leak: it reads finished records after the fact; it changes no decision.

  python3 topics/44_review/combine_night4.py UNSEEN_ROOT
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd

ST = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ST / "topics/08_review"))
from combine_test import measures, coins_of  # noqa: E402
sys.path.insert(0, str(ST / "orchestration/ideas_similarities_check/helper"))
import book_returns as br  # noqa: E402


def per_coin(record):
    """Daily returns per coin (columns), as step 6 builds them; empty when no window ran."""
    cols = {}
    for coin, w, f in br.coin_windows(record):
        d = pd.read_csv(f, usecols=["timestamp", "postRebalance_total_value"])
        cols.setdefault(coin, []).append(br.period_returns(d["postRebalance_total_value"], d["timestamp"], "1d"))
    return pd.DataFrame({c: pd.concat(v).groupby(level=0).last() for c, v in cols.items()})

NEW = ("night4_fallingbounce_run", "025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d")
PAIRS = {"1: with 022-03 strong monthly rises continue": ("paying_rerun_run", "022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d"),
         "2: with 018-02 hourly breakout continuation": ("paying_rerun_run", "018-02_hourly-breakout-multiday-continuation_1h")}
PERIODS = ("folds", "unseen_2016_2017", "unseen_2026")


def rec(period, run, rid, unseen_root):
    return ST / "04_backtest" / run / "backtests" / rid if period == "folds" else Path(unseen_root) / period / rid


def run(unseen_root):
    out = {}
    for pair, other in PAIRS.items():
        for period in PERIODS:
            r1, r2 = rec(period, *NEW, unseen_root), rec(period, *other, unseen_root)
            A, B = per_coin(r1), per_coin(r2)
            coins = sorted(set(A.columns) & set(B.columns))
            if not coins:
                out[f"{pair} | {period}"] = {"no data": "one of the two books has no window on these dates"}
                continue
            A, B = A[coins], B[coins]
            days = A.index.intersection(B.index)
            mask = A.loc[days].notna() & B.loc[days].notna()          # each day, the coins both books hold
            a, b = A.loc[days].where(mask).mean(axis=1), B.loc[days].where(mask).mean(axis=1)
            both = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
            out[f"{pair} | {period}"] = {"coins": coins, "coin_days": int(mask.values.sum()), "correlation": float(np.corrcoef(both["a"], both["b"])[0, 1]),
                                         "025-03.d2": measures(both["a"]), "momentum": measures(both["b"]),
                                         "A: side by side": measures(both.mean(axis=1))}
    return out


if __name__ == "__main__":
    res = run(sys.argv[1])
    (Path(__file__).parent / "combine_night4.json").write_text(json.dumps(res, indent=2, default=float) + "\n")
    for k, v in res.items():
        if "no data" in v:
            print(f"\n== {k}: no data ({v['no data']})"); continue
        print(f"\n== {k} (correlation {v['correlation']:+.2f}; {len(v['coins'])} coins)")
        for who in ("025-03.d2", "momentum", "A: side by side"):
            m = v[who]
            print(f"  {who:16s} Sharpe {m['sharpe']:5.2f}  Calmar {m['calmar']:5.2f}  deepest fall {100*m['deepest_fall']:5.1f} %  "
                  f"daily sd {100*m['daily_sd']:.3f} %  mean {100*m['mean_daily']:+.4f} %  days {m['days']}")
