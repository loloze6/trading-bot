import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 5
    rows = []
    trades_all = []
    book = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; hi = b["high"]; lo = b["low"]
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["r5"] = c / c.shift(5) - 1
            b["r20"] = c / c.shift(20) - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["volrank"] = b["vol20"] / b["vol20"].rolling(60, min_periods=20).mean()
            ph = hi.shift(1).rolling(20).max()
            pl = lo.shift(1).rolling(20).min()
            b["brk_up"] = (c > c.shift(1).rolling(20).max()).astype(float)
            b["brk_dn"] = (c < c.shift(1).rolling(20).min()).astype(float)
            b["pos_range"] = (c - pl) / (ph - pl)
            # failed breakout: close above prior 20-close high within last 3 bars, now back below that level
            prior = c.shift(1).rolling(20).max()
            fb = np.zeros(len(b))
            for k in range(1, 4):
                lvl = prior.shift(k)
                was = c.shift(k) > lvl
                fb = np.where((was & (c < lvl)).values, 1, fb)
            b["failed_up"] = fb
            pf = np.zeros(len(b))
            priorl = c.shift(1).rolling(20).min()
            for k in range(1, 4):
                lvl = priorl.shift(k)
                was = c.shift(k) < lvl
                pf = np.where((was & (c > lvl)).values, 1, pf)
            b["failed_dn"] = pf
            b["range_rel"] = (hi - lo) / c / b["vol20"]
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin; b["win"] = w
            g = b.iloc[::H].copy()
            rows.append(g)
            t = data["trades"][coin][w]
            if len(t):
                t = t.copy(); t["coin"] = coin; trades_all.append(t)
            d = data["days"][coin][w].copy(); d["coin"] = coin; d["win"] = w
            book.append(d)
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["ex"] = G["fwd"] - G["drift"]
    out = {}
    def grp(col, q=None):
        x = G.dropna(subset=[col]).copy()
        if q:
            x["k"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        else:
            x["k"] = x[col]
        r = x.groupby("k")["ex"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std").round(4)
    out["by r1 quintile"] = grp("r1", 5)
    out["by r5 quintile"] = grp("r5", 5)
    out["by r20 quintile"] = grp("r20", 5)
    out["by vol20 quintile"] = grp("vol20", 5)
    out["by volrank quintile"] = grp("volrank", 5)
    out["by pos_range quintile"] = grp("pos_range", 5)
    out["by range_rel quintile"] = grp("range_rel", 5)
    out["by weekday"] = grp("wd")
    out["brk_up"] = grp("brk_up")
    out["brk_dn"] = grp("brk_dn")
    out["failed_up"] = grp("failed_up")
    out["failed_dn"] = grp("failed_dn")
    G["active"] = (G["postRebalance_current_allocation"] < 0).astype(float)
    out["active"] = grp("active")
    G["year"] = pd.to_datetime(G["timestamp"]).dt.year
    out["by year"] = grp("year")
    if trades_all:
        T = pd.concat(trades_all)
        out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
        out["trade dur days"] = float((T["duration_minutes"] / 1440).mean())
    B = pd.concat(book)
    out["share days in position"] = float((G["active"]).mean())
    out["book ret by coin"] = B.groupby("coin")[["book_return", "coin_return"]].mean().round(5)
    return out
