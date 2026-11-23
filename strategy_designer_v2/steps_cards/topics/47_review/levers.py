"""Topic 47, measurement 1d-5 (operator, 2026-11-23: what can we act on to limit losing streaks, and to limit each
trade's absolute outcome while keeping the total positive?). On every real book of night 5, from its per-coin daily
returns (step 6's equal-weight chain), each lever applied with only what is known before the day (no lookahead):
  L1 crowd(m):  a day's book return x min(1, m / coins held into the day): a crowded day sized as m bets at most
  L2 voltarget: the book's return x (its median daily swing / its swing over the previous 60 days), at most 2x
  L3 brake(x):  the book's return halved while it was x below its peak at the previous close
  L4 stop(s):   per coin, the rest of a trade earns 0 once the trade has lost s (on daily closes)
  L5 target(t): per coin, the rest of a trade earns 0 once the trade has gained t
  L6 stop(s)+target(t)
Calmar (step 6's: yearly return over the deepest fall, calendar days), yearly return, deepest fall. All settings are
reported (a small grid), not the best one. Writes levers.csv.  python3 topics/47_review/levers.py"""
import pathlib, warnings
import numpy as np, pandas as pd
import streaks as st

warnings.simplefilter("ignore")


def stats(r):
    c = np.cumprod(1 + r); years = len(r) / 365
    ann = c[-1] ** (1 / years) - 1 if c[-1] > 0 else -1.0
    fall = float(np.max(1 - c / np.maximum.accumulate(np.r_[1.0, c])[1:]))
    return (ann / fall if fall > 0 else np.inf), ann, fall


def held_into(P, w):
    """Coin held a position into the day: its position at the previous day's close, inside the same window."""
    H = np.r_[np.zeros((1, P.shape[1]), bool), P[:-1]]
    H[np.r_[True, w[1:] != w[:-1]]] = False
    return H


def trade_cut(R, H, w, stop=None, target=None):
    """Per coin: inside each run of held days (a trade), the days after the trade's running return reached -stop or
    +target earn 0 (known at that day's open: the running return to the previous close)."""
    out = R.copy()
    for j in range(R.shape[1]):
        run, done = 0.0, False
        for i in range(len(R)):
            if not H[i, j] or (i and w[i] != w[i - 1]):
                run, done = 0.0, False
                if not H[i, j]: continue
            if done: out[i, j] = 0.0; continue
            run = (1 + run) * (1 + (R[i, j] if np.isfinite(R[i, j]) else 0.0)) - 1
            if (stop is not None and run <= -stop) or (target is not None and run >= target):
                done = True
    return out


if __name__ == "__main__":
    gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
    rows = []
    for b in gate.itertuples():
        ret, pos = st.per_coin(st.STEPS / "04_backtest" / b.run / "backtests" / b.backtest)
        R = ret.to_numpy(); P = pos.fillna(False).to_numpy(); w = ret.index.get_level_values("w").to_numpy()
        H = held_into(P, w); n_in = H.sum(1)
        base = np.nan_to_num(np.nanmean(R, axis=1))
        variants = {"L0 none": base}
        for m in (1, 2, 3):
            variants[f"L1 crowd({m})"] = base * np.where(n_in > m, m / np.maximum(n_in, 1), 1.0)
        sd = pd.Series(base).rolling(60, min_periods=20).std().shift(1).to_numpy()
        med = np.nanmedian(pd.Series(base).rolling(60, min_periods=20).std())
        variants["L2 voltarget"] = base * np.nan_to_num(np.clip(med / sd, 0, 2), nan=1.0)
        for x in (0.10, 0.20):
            c = np.cumprod(1 + base); dd = 1 - c / np.maximum.accumulate(c)
            scale = np.r_[1.0, np.where(dd[:-1] >= x, 0.5, 1.0)]
            # the brake acts on the braked book's own path: recompute it step by step
            v, peak, cur = np.empty_like(base), 1.0, 1.0
            for i, r in enumerate(base):
                s = 0.5 if (1 - cur / peak) >= x else 1.0
                v[i] = s * r; cur *= 1 + v[i]; peak = max(peak, cur)
            variants[f"L3 brake({int(100 * x)}%)"] = v
        for s_ in (0.05, 0.10):
            variants[f"L4 stop({int(100 * s_)}%)"] = np.nan_to_num(np.nanmean(trade_cut(R, H, w, stop=s_), axis=1))
        for t_ in (0.05, 0.10):
            variants[f"L5 target({int(100 * t_)}%)"] = np.nan_to_num(np.nanmean(trade_cut(R, H, w, target=t_), axis=1))
        variants["L6 stop(5%)+target(10%)"] = np.nan_to_num(np.nanmean(trade_cut(R, H, w, stop=0.05, target=0.10), axis=1))
        for k, r in variants.items():
            cal, ann, fall = stats(r)
            rows.append({"run": b.run, "backtest": b.backtest, "pays": b.pays, "lever": k, "calmar": cal, "yearly": ann, "fall": fall})
    d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("levers.csv"), index=False, float_format="%.4g")
    base = d[d.lever == "L0 none"].set_index("backtest").calmar
    d["better"] = d.calmar > d.backtest.map(base)
    pd.set_option("display.width", 200)
    for g, x in d.groupby("pays"):
        print(f"\n== {'pays' if g else 'does not pay'} ({x.backtest.nunique()})")
        print(x.groupby("lever").agg(calmar=("calmar", "median"), yearly=("yearly", "median"), fall=("fall", "median"),
                                     passing=("calmar", lambda s: int((s > 0.75).sum())), books_improved=("better", "sum")).round(3).to_string())
