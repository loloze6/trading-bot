"""Topic 47, measurement 1d-6: make each trade a bet on the coin against the market, so the coins' common move cancels
(the lever the decorrelation test points to: with the coins' timing scrambled, the deepest fall halved). Per coin and
day: its book return less its allocation held into the day (known at the previous close) times the market's return
(the equal-weight daily return of the book's own coins). Costs of the market leg are not counted: an upper bound.
Every real book of night 5. Writes hedge.csv.  python3 topics/47_review/hedge.py"""
import pathlib, warnings
import numpy as np, pandas as pd
import streaks as st
from levers import stats

warnings.simplefilter("ignore")
gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
rows = []
for b in gate.itertuples():
    rec = st.STEPS / "04_backtest" / b.run / "backtests" / b.backtest
    x = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "close", "position", "value"], parse_dates=["timestamp"])
    x["day"] = x.timestamp.dt.normalize(); x["w"] = x.window.str[1:].astype(int)
    last = x.groupby(["w", "day", "coin"]).last().reset_index()
    val = last.pivot_table(index=["w", "day"], columns="coin", values="value")
    cls = last.pivot_table(index=["w", "day"], columns="coin", values="close")
    alloc = last.pivot_table(index=["w", "day"], columns="coin", values="position")
    R = val.groupby(level="w").pct_change(fill_method=None)
    C = cls.groupby(level="w").pct_change(fill_method=None)
    A = alloc.groupby(level="w").shift(1)                              # the allocation held into the day
    mkt = C.mean(axis=1)
    H = R.sub(A.mul(mkt, axis=0).fillna(0.0))
    keep = R.notna().any(axis=1)
    base = np.nan_to_num(R[keep].mean(axis=1).to_numpy()); hedged = np.nan_to_num(H[keep].mean(axis=1).to_numpy())
    for name, r in (("as built", base), ("against the market", hedged)):
        cal, ann, fall = stats(r)
        rows.append({"run": b.run, "backtest": b.backtest, "pays": b.pays, "book": name, "calmar": cal, "yearly": ann, "fall": fall,
                     "sharpe": float(r.mean() / r.std() * np.sqrt(365)) if r.std() > 0 else np.nan})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("hedge.csv"), index=False, float_format="%.4g")
base = d[d.book == "as built"].set_index("backtest").calmar; d["better"] = d.calmar > d.backtest.map(base)
for g, x in d.groupby("pays"):
    print(f"\n== {'pays' if g else 'does not pay'} ({x.backtest.nunique()})")
    print(x.groupby("book").agg(calmar=("calmar", "median"), sharpe=("sharpe", "median"), yearly=("yearly", "median"), fall=("fall", "median"),
                                passing=("calmar", lambda s: int((s > 0.75).sum())), improved=("better", "sum")).round(3).to_string())
