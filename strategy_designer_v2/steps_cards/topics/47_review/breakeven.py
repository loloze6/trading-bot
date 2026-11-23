"""Topic 47: protect a gain without capping it (daily books). Once a trade's best move after its entry bar reaches +A %,
its stop moves to the entry price: if the price later comes back to the entry, the trade ends at 0 less costs;
otherwise it ends as it did. Bar by bar on the local daily OHLC (the bars after the entry bar, up to the exit bar); a
bar that arms the stop only checks it from the next bar (the order inside a bar is unknown). Judged out of fold like
trade_rules.py (no choice: every A shown).  python3 topics/47_review/breakeven.py TRADES.csv.gz"""
import sys, pathlib, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
DATA = pathlib.Path(__file__).resolve().parents[4] / "trading-bot" / "local_data"
d = pd.read_csv(sys.argv[1], parse_dates=["entry_time"]); d = d[d.bar == "1d"].copy()
AS = (1, 2, 3, 5)
for A in AS: d[f"be{A}"] = d.net_pct
for coin, idx in d.groupby("symbol").groups.items():
    px = pd.read_csv(DATA / f"kraken_{coin}_1d.csv", usecols=["timestamp", "high", "low", "close"], parse_dates=["timestamp"]).drop_duplicates("timestamp").set_index("timestamp").sort_index()
    H, L, C = px.high.to_numpy(float), px.low.to_numpy(float), px.close.to_numpy(float)
    t = d.loc[idx]; ei = px.index.get_indexer(t.entry_time); hb = t.holding_bars.fillna(1).astype(int).to_numpy()
    longs = (t.direction == "long").to_numpy()
    res = {A: t.net_pct.to_numpy().copy() for A in AS}
    for k in range(len(t)):
        e = ei[k]
        if e < 0 or e + hb[k] >= len(C): continue
        entry = C[e]
        for A in AS:
            armed = False
            for i in range(e + 1, e + max(hb[k], 1) + 1):
                if armed and ((longs[k] and L[i] <= entry) or (not longs[k] and H[i] >= entry)):
                    res[A][k] = -0.10; break                       # out at the entry price, less the fee
                if (longs[k] and H[i] >= entry * (1 + A / 100)) or (not longs[k] and L[i] <= entry * (1 - A / 100)):
                    armed = True
    for A in AS: d.loc[idx, f"be{A}"] = res[A]
rows = []
for book, x in d.groupby("book"):
    for f in sorted(x.fold.dropna().unique()):
        te = x[x.fold == f]
        if len(te) < 20: continue
        for A in AS:
            rows.append({"book": book, "fold": f, "A": A, "win_before": (te.net_pct > 0).mean(), "win_after": (te[f"be{A}"] > 0).mean(),
                         "mean_before": te.net_pct.mean(), "mean_after": te[f"be{A}"].mean(), "better": te[f"be{A}"].sum() > te.net_pct.sum()})
r = pd.DataFrame(rows)
print(r.groupby("A").agg(win_before=("win_before", "median"), win_after=("win_after", "median"), mean_before=("mean_before", "median"),
                         mean_after=("mean_after", "median"), book_folds_better=("better", "mean")).round(3).to_string())
