"""Topic 47, measurement 1d-1 (operator's go 2026-11-23): does the idea's edge hold inside crash periods?
For each phase-A book (runs/BOOK_REFLECTS_IDEA_RUN.md: the idea's own situation days only), every trade is placed in
or out of a crash period of its coin, by the coin's state known before the trade (daily closes up to the day before
its entry: no lookahead), with two definitions to see that the answer does not hang on one threshold:
  - C1: the coin's close is at least 30 % below its highest close of the previous 90 days;
  - C2: the coin's 30-day return is -20 % or lower.
Per book and definition: trades, mean return per trade after costs (the engine's), its t, and the share of the book's
summed return made inside. Writes crash_state.csv.
  python3 topics/47_review/crash_state.py"""
import pathlib
import numpy as np, pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
RUN = "book_reflects_idea_run"


def states(coin):
    d = pd.read_csv(DATA / f"kraken_{coin}_1d.csv", usecols=["timestamp", "close"], parse_dates=["timestamp"]).set_index("timestamp")["close"]
    c1 = d / d.rolling(90, min_periods=60).max() - 1 <= -0.30
    c2 = d / d.shift(30) - 1 <= -0.20
    # the state known before a trade entered on day D: the state at D-1's close
    return pd.DataFrame({"C1": c1, "C2": c2}).shift(1)


def tstat(x):
    return float(x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))) if len(x) > 2 and x.std(ddof=1) > 0 else float("nan")


rows = []
seen = set()
for rec in sorted((STEPS / "04_backtest" / RUN / "backtests").iterdir()):
    if not rec.is_dir(): continue
    t = pd.read_csv(rec / "chart_trades.csv.gz", parse_dates=["entry_time"])
    key = (len(t), round(float(t.realized_return.sum()), 6))
    if key in seen: continue                                   # the two absorption ideas give the same book
    seen.add(key)
    t["day"] = t.entry_time.dt.normalize()
    st = pd.concat({c: states(c) for c in t.coin.unique()}, names=["coin", "day"])
    t = t.join(st, on=["coin", "day"])
    total = t.realized_return.sum()
    for k in ("C1", "C2"):
        for inside in (True, False):
            x = t[t[k] == inside].realized_return
            rows.append({"book": rec.name.split(".")[-1], "definition": k, "in_crash": inside, "trades": len(x),
                         "mean_net_pct": float(x.mean()) if len(x) else float("nan"), "t": tstat(x),
                         "share_of_summed_return": float(x.sum() / total) if total else float("nan")})
d = pd.DataFrame(rows); d.to_csv(pathlib.Path(__file__).with_name("crash_state.csv"), index=False, float_format="%.4g")
pd.set_option("display.width", 200)
print(d.assign(mean_net_pct=d.mean_net_pct.round(3), t=d.t.round(2), share_of_summed_return=d.share_of_summed_return.round(2)).to_string(index=False))
