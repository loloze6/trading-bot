"""Topic 47: when does a trade's edge come, and what follows a loss? From the trade table and the local OHLC bars.
  B. after the entry: for every trade, the price move in the trade's direction from the entry close to k bars later
     (whatever the trade's real exit), against the market's drift (the same coin's mean k-bar move, in the trade's
     direction): the edge at k bars is the difference. Before the entry (C): the move over the k bars before it.
  F2. what follows a loss: on each book and coin, a trade whose previous trade lost against one whose previous trade
     won (the previous trade closed before this one opened: known at entry); and out of fold, skipping the trades that
     follow a loss (or two losses in a row): is the fourth fold's sum better?
  python3 topics/47_review/event_study.py TRADES.csv.gz"""
import sys, pathlib, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
DATA = pathlib.Path(__file__).resolve().parents[4] / "trading-bot" / "local_data"
d = pd.read_csv(sys.argv[1]); d["entry_time"] = pd.to_datetime(d.entry_time, format="ISO8601")
KS = {"1d": [1, 2, 3, 5, 10, 20], "1h": [1, 2, 4, 8, 12, 24, 48]}
BEFORE = {"1d": [1, 3, 5], "1h": [1, 4, 24]}
pd.set_option("display.width", 220)
for bar, x in d.groupby("bar"):
    print(f"\n######## {bar}")
    rows, pre = [], []
    for coin, y in x.groupby("symbol"):
        px = pd.read_csv(DATA / f"kraken_{coin}_{bar}.csv", usecols=["timestamp", "close"]).drop_duplicates("timestamp")
        px["timestamp"] = pd.to_datetime(px.timestamp, format="ISO8601"); px = px.set_index("timestamp").sort_index().close
        c = px.to_numpy(float); ei = px.index.get_indexer(y.entry_time); sgn = np.where(y.direction == "long", 1.0, -1.0)
        for k in KS[bar]:
            ok = (ei >= 0) & (ei + k < len(c))
            mv = np.full(len(y), np.nan); mv[ok] = c[ei[ok] + k] / c[ei[ok]] - 1
            drift = np.nanmean(c[k:] / c[:-k] - 1)
            rows.append(pd.DataFrame({"k": k, "move": 100 * sgn * mv, "edge": 100 * sgn * (mv - drift), "book": y.book.to_numpy()}))
        for k in BEFORE[bar]:
            ok = (ei - k >= 0)
            mv = np.full(len(y), np.nan); mv[ok] = c[ei[ok]] / c[ei[ok] - k] - 1
            pre.append(pd.DataFrame({"k": k, "move_before": 100 * sgn * mv}))
    r = pd.concat(rows)
    t = r.groupby("k").agg(trades=("move", "count"), move_in_direction=("move", "mean"), edge_beyond_drift=("edge", "mean"),
                           edge_t=("edge", lambda s: s.mean() / s.std() * np.sqrt(s.count())), share_positive=("move", lambda s: (s > 0).mean()))
    print("B. after the entry (per unit, %, before costs; edge = the move less the coin's drift in that direction):")
    print(t.round(3).to_string())
    per_book = r.groupby(["book", "k"]).edge.mean().unstack()
    print("   per book: the horizon with the largest edge (count of books):", per_book.idxmax(axis=1).value_counts().sort_index().to_dict())
    p = pd.concat(pre).groupby("k").move_before.agg(["mean", lambda s: (s > 0).mean()])
    p.columns = ["mean move before, in the trade's direction", "share in the trade's direction"]
    print("C. before the entry:"); print(p.round(3).to_string())
    # F2. what follows a loss
    x = x.sort_values(["book", "symbol", "entry_time"]).copy()
    g = x.groupby(["book", "symbol"])
    hours = 24 if bar == "1d" else 1
    prev_exit = g.entry_time.shift(1) + pd.to_timedelta(g.holding_bars.shift(1).fillna(0) * hours, unit="h")
    known = prev_exit <= x.entry_time
    x["after_loss"] = known & (g.win.shift(1) == False)
    x["after_win"] = known & (g.win.shift(1) == True)
    x["after_two_losses"] = x.after_loss & (g.win.shift(2) == False)
    for lab, m in (("after a win", x.after_win), ("after a loss", x.after_loss), ("after two losses", x.after_two_losses)):
        print(f"F2. {lab}: {int(m.sum()):,} trades, win rate {x[m].win.mean():.3f}, mean {x[m].net_pct.mean():+.3f} %")
    for rule, col in (("skip after a loss", "after_loss"), ("skip after two losses", "after_two_losses")):
        better = tot = 0; before = after = 0.0
        for (book, f), y in x.groupby(["book", "fold"]):
            if len(y) < 20: continue
            tot += 1; s0 = y.net_pct.sum(); s1 = y[~y[col]].net_pct.sum(); better += s1 > s0; before += s0; after += s1
        print(f"    {rule}: better on {better} of {tot} book-folds ({better / max(tot, 1):.0%}); summed result {before:,.0f} -> {after:,.0f} points")
