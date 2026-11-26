def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            hi60 = c.shift(1).rolling(60, min_periods=60).max()
            lo60 = c.shift(1).rolling(60, min_periods=60).min()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "day": ts.dt.floor("D"),
                "yr": ts.dt.year, "wd": ts.dt.weekday,
                "r1": c.pct_change(), "f1": c.shift(-1) / c - 1,
                "dist": (c / c.rolling(60, min_periods=60).max() - 1) * 100,
                "margin": (c / hi60 - 1) * 100, "width": hi60 / lo60 - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "ret60": c / c.shift(60) - 1,
            })
            for h in [3, 5]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    def clus_t(df, ycol, xcol):
        d = df.dropna(subset=[ycol, xcol])
        x = d[xcol].values; y = d[ycol].values
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in d.groupby("day").indices.items():
            s = X[idx].T @ e[idx]
            meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return pd.Series({"slope": beta[1], "t_clustered": beta[1] / np.sqrt(V[1, 1]), "n": len(d), "days": d["day"].nunique()})
    # weekday: day-clustered (average across coins per day)
    dm = D.dropna(subset=["r1"]).groupby(["day", "wd", "yr"])["r1"].mean().reset_index()
    dm["mkt_excess"] = dm["r1"] - dm["r1"].mean()
    r = dm.groupby("wd")["r1"].agg(["count", "mean", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
    out["weekday daily return, coins averaged per day"] = r.round(5)
    dm["frisat"] = dm["wd"].isin([4, 5])
    r = dm.groupby(["yr", "frisat"])["r1"].mean().unstack().round(5)
    out["Fri+Sat vs other days mean, by year"] = r
    D["frisat"] = D["wd"].isin([4, 5])
    r = D.dropna(subset=["r1"]).groupby(["coin", "frisat"])["r1"].mean().unstack().round(5)
    out["Fri+Sat vs other days mean, by coin"] = r
    # weekday effect conditional on vol: |r1| scale
    # distance from 60-day high, graded, grid 3 / grid 5
    for h in [3, 5]:
        G = D[D["pos"] % h == 0].copy()
        G[f"x{h}"] = G[f"f{h}"] - G["coin"].map(G.groupby("coin")[f"f{h}"].mean())
        G["distz"] = G["dist"]
        out[f"x{h} on distance from 60d high (pct), grid {h}"] = clus_t(G, f"x{h}", "distz").round(4)
        G["dq"] = pd.qcut(G["dist"], 5, labels=False, duplicates="drop")
        out[f"x{h} by distance quintile, by year (mean)"] = G.groupby(["yr", "dq"])[f"x{h}"].mean().unstack().round(4)
    G = D[D["pos"] % 3 == 0].copy()
    G["x3"] = G["f3"] - G["coin"].map(G.groupby("coin")["f3"].mean())
    G["dq"] = pd.qcut(G["dist"], 5, labels=False, duplicates="drop")
    out["x3 by distance quintile, by coin (mean)"] = G.groupby(["coin", "dq"])["x3"].mean().unstack().round(4)
    # breaks: follow-through vs prior range width (continuous), deduped
    brk = D[D["margin"] > 0].dropna(subset=["f3"]).copy()
    keep = []
    for (cn, w), g in brk.groupby(["coin", "win"]):
        last = -999
        for i, p in zip(g.index, g["pos"]):
            if p - last > 3:
                keep.append(i); last = p
    B = brk.loc[keep].copy()
    B["x3"] = B["f3"] - B["coin"].map(G.groupby("coin")["f3"].mean())
    B["x5"] = B["f5"] - B["coin"].map(D[D["pos"] % 5 == 0].groupby("coin")["f5"].mean())
    B["width_vol"] = B["width"] / (B["vol20"] * np.sqrt(60))
    out["break x3 on prior range width"] = clus_t(B, "x3", "width").round(4)
    out["break x3 on width/vol"] = clus_t(B, "x3", "width_vol").round(4)
    out["break x3 on margin"] = clus_t(B, "x3", "margin").round(4)
    out["break x5 on prior range width"] = clus_t(B, "x5", "width").round(4)
    out["break x3 on 60d return"] = clus_t(B, "x3", "ret60").round(4)
    # book: largest days, what preceded
    dd = pd.concat([d.assign(coin=c, win=w) for c, ws in data["days"].items() for w, d in ws.items()])
    bk = dd.groupby("day")["book_return"].mean().dropna()
    q = bk.quantile([0.02, 0.98])
    big = bk[(bk <= q.iloc[0]) | (bk >= q.iloc[1])]
    out["book extreme days count up/down"] = pd.Series({"up": int((big > 0).sum()), "down": int((big < 0).sum()), "share of total gain from top2% days": float(bk[bk >= q.iloc[1]].sum() / bk.sum())}).round(3)
    bkd = bk.reset_index(); bkd["wd"] = pd.to_datetime(bkd["day"]).dt.weekday
    out["book mean by weekday"] = bkd.groupby("wd")["book_return"].agg(["count", "mean"]).round(5)
    return out
