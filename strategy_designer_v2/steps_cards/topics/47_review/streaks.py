"""Topic 47, measurement 1d-3 (operator, 2026-11-23: "the depth comes from a suite of losing bets, not from correlated
coins"). For every real book of night 5, from its per-coin daily book values (chart files, step 6's equal-weight chain):
- together: on days a book opens trades, how many of its coins open the same day, against what the coins' own entry
  frequencies would give if they opened independently;
- decorrelated: each coin's daily returns shifted by a random number of days inside the chain (each coin keeps its own
  sequence, its own winning and losing streaks; only the timing between coins is lost), 200 times: the deepest fall and
  Calmar of the equal-weight book, against the real ones.
Writes streaks.csv.  python3 topics/47_review/streaks.py"""
import pathlib
import numpy as np, pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
rng = np.random.default_rng(1)


def per_coin(rec):
    """Per coin, its daily returns in step 6's chain (windows in window order; days out of a window: none)."""
    b = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "position", "value"], parse_dates=["timestamp"])
    b["day"] = b.timestamp.dt.normalize(); b["w"] = b.window.str[1:].astype(int)
    last = b.groupby(["w", "day", "coin"]).agg(value=("value", "last"), pos=("position", "last")).reset_index()
    ret = last.pivot_table(index=["w", "day"], columns="coin", values="value").groupby(level="w").pct_change()
    pos = last.pivot_table(index=["w", "day"], columns="coin", values="pos").ne(0)
    keep = ret.notna().any(axis=1)
    return ret[keep], pos.reindex(ret.index)[keep]


def calmar(r):
    c = np.cumprod(1 + r); years = len(r) / 365
    ann = c[-1] ** (1 / years) - 1 if c[-1] > 0 else -1.0
    fall = float(np.max(1 - c / np.maximum.accumulate(np.r_[1.0, c])[1:]))
    return (ann / fall if fall > 0 else np.inf), fall


if __name__ == "__main__":
    gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
    rows = []
    for r in gate.itertuples():
        ret, pos = per_coin(STEPS / "04_backtest" / r.run / "backtests" / r.backtest)
        R = ret.to_numpy(); P = pos.fillna(False).to_numpy()
        book = np.nanmean(R, axis=1); book = np.nan_to_num(book)
        cal, fall = calmar(book)
        opens = P & ~np.r_[np.zeros((1, P.shape[1]), bool), P[:-1]]            # a coin enters a position that day
        k = opens.sum(1); days = k > 0
        p = opens.mean(0)                                                       # each coin's own chance to open on a day
        expected = float((p.sum() / (1 - np.prod(1 - p))) if np.prod(1 - p) < 1 else np.nan)   # mean coins opening, given >= 1, if independent
        sims = []
        for _ in range(200):
            S = np.column_stack([np.roll(R[:, j], rng.integers(len(R))) for j in range(R.shape[1])])
            sims.append(calmar(np.nan_to_num(np.nanmean(S, axis=1))))
        sims = np.array(sims)
        rows.append({"run": r.run, "backtest": r.backtest, "pays": r.pays, "coins_opening_together": float(k[days].mean()),
                     "if_independent": expected, "fall": fall, "fall_decorrelated": float(np.median(sims[:, 1])),
                     "calmar": cal, "calmar_decorrelated": float(np.median(sims[:, 0]))})
    d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("streaks.csv"), index=False, float_format="%.4g")
    for g, x in d.groupby("pays"):
        print(f"== {'pays' if g else 'does not pay'} ({len(x)})")
        print(f" coins opening on the same day: {x.coins_opening_together.median():.2f} (if they opened independently: {x.if_independent.median():.2f})")
        print(f" deepest fall: real {100 * x.fall.median():.1f} %, coins decorrelated {100 * x.fall_decorrelated.median():.1f} %")
        print(f" Calmar: real {x.calmar.median():.2f}, coins decorrelated {x.calmar_decorrelated.median():.2f}; passing 0.75 decorrelated: {int((x.calmar_decorrelated > 0.75).sum())}")
