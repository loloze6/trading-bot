import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["fwd"] = c.shift(-H) / c - 1
            b["r1"] = c.pct_change()
            b["vol20"] = b["r1"].rolling(20).std()
            ph = c.shift(1).rolling(20).max()
            pl = c.shift(1).rolling(20).min()
            # graded breakout strength: excess of close over prior 20-day high close, in vol units
            b["up_x"] = (c / ph - 1) / b["vol20"]
            b["dn_x"] = (pl / c - 1) / b["vol20"]
            # failed breakdown: within last 3 bars closed below prior 20-day low, now back above; graded by recovery
            rec = pd.Series(np.nan, index=b.index)
            for k in range(3, 0, -1):
                lvl = pl.shift(k)
                was = c.shift(k) < lvl
                m = was & (c > lvl)
                rec = rec.where(~m, (c / lvl - 1) / b["vol20"])
            b["fdn_rec"] = rec
            b["r1z"] = b["r1"] / b["vol20"].shift(1)
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            rows.append(b.iloc[::H].copy())
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["usual"] = G.groupby("coin")["fwd"].transform("std")
    G["ex"] = G["fwd"] - G["drift"]
    G["str"] = G["ex"] / G["usual"]
    out = {}
    def summ(x, key):
        r = x.groupby(key)["ex"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["strength"] = x.groupby(key)["str"].mean()
        return r.drop(columns="std").round(4)
    U = G[G["up_x"] > 0].copy()
    U["q"] = pd.qcut(U["up_x"].rank(method="first"), 3, labels=False)
    out["breakout up by strength tercile"] = summ(U, "q")
    out["breakout up by coin"] = summ(U, "coin")
    out["breakout up by year"] = summ(U, "year")
    out["breakout up spearman"] = str(stats.spearmanr(U["up_x"], U["ex"]))
    F = G[G["fdn_rec"].notna()].copy()
    F["q"] = pd.qcut(F["fdn_rec"].rank(method="first"), 3, labels=False)
    out["failed breakdown by recovery tercile"] = summ(F, "q")
    out["failed breakdown by coin"] = summ(F, "coin")
    out["failed breakdown by year"] = summ(F, "year")
    out["failed breakdown spearman"] = str(stats.spearmanr(F["fdn_rec"], F["ex"]))
    D = G[G["dn_x"] > 0].copy()
    out["breakdown spearman"] = str(stats.spearmanr(D["dn_x"], D["ex"]))
    G["r1q"] = G.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out["by r1z decile"] = summ(G, "r1q")
    out["weekday by year half"] = G.assign(h=(G["year"] >= 2022).astype(int)).groupby(["h", "wd"])["ex"].mean().unstack().round(4)
    # book: largest gain/loss days
    days = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; days.append(d)
    Dd = pd.concat(days).dropna(subset=["book_return"])
    nz = Dd[Dd["book_return"].abs() > 1e-9]
    out["book active days"] = int(len(nz))
    out["book active days mean, t"] = str((nz["book_return"].mean(), nz["book_return"].mean() / (nz["book_return"].std() / np.sqrt(len(nz)))))
    out["book active by coin"] = nz.groupby("coin")["book_return"].agg(["count", "mean", "sum"]).round(4)
    return out
