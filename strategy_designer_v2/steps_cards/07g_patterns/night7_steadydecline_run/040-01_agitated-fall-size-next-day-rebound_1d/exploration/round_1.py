def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["r0"] = c.pct_change()
            d["r3p"] = c / c.shift(3) - 1
            d["n1"] = c.shift(-1) / c - 1
            d["n2"] = c.shift(-2) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            d["cl"] = (c - b["low"]) / rng.replace(0, np.nan)
            d["range"] = rng / c.shift(1)
            d["agit"] = (b["regime"] == "unknown").astype(int)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            d["fc"] = b["forecast"].astype(float)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            v = b["postRebalance_total_value"].astype(float)
            d["bookr"] = v.shift(-1) / v - 1
            d["vol20"] = d["r0"].rolling(20).std()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["n1"].mean()
    D["x1"] = D["n1"] - D["coin"].map(mu)
    sd = D.groupby("coin")["r0"].std()
    D["z0"] = D["r0"] / D["coin"].map(sd)
    D["zr3"] = D["r3p"] / (D["coin"].map(sd) * np.sqrt(3))
    out = {}
    def tab(df, key, val):
        g = df.dropna(subset=[key, val]).groupby(key)[val]
        r = g.agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        return r.drop(columns="std")
    D["zq"] = pd.cut(D["z0"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out["next1 excess by z of day ret, agitated"] = tab(D[D.agit == 1], "zq", "x1")
    out["next1 excess by z of day ret, calm"] = tab(D[D.agit == 0], "zq", "x1")
    # horizons after falls, agitated, grid h
    res = []
    for h in [1, 2, 3]:
        for a in [0, 1]:
            s = D[(D.agit == a) & (D.pos % h == 0) & (D.z0 < -1)]
            m = D.groupby("coin")["n%d" % h].mean()
            x = (s["n%d" % h] - s["coin"].map(m)).dropna()
            res.append({"h": h, "agit": a, "mean": x.mean(), "n": len(x), "t": stats.ttest_1samp(x, 0).statistic})
    out["after z<-1 fall, excess by horizon"] = pd.DataFrame(res)
    # 3-day falls, 3-day forward, grid 3
    s = D[D.pos % 3 == 0].copy()
    m3 = D.groupby("coin")["n3"].mean()
    s["x3"] = s["n3"] - s["coin"].map(m3)
    s["q3"] = pd.cut(s["zr3"], [-99, -2, -1, 0, 1, 2, 99])
    out["3d ret -> next3 excess, agitated"] = tab(s[s.agit == 1], "q3", "x3")
    # close location within falls, agitated
    f = D[(D.agit == 1) & (D.z0 < -1)].copy()
    f["clq"] = pd.cut(f["cl"], [0, 0.25, 0.5, 0.75, 1.0], include_lowest=True)
    out["agit fall z<-1: next1 by close loc"] = tab(f, "clq", "x1")
    # range relative to vol on falls
    f["rr"] = f["range"] / f["vol20"]
    f["rrq"] = pd.qcut(f["rr"], 3, duplicates="drop")
    out["agit fall z<-1: next1 by range/vol20"] = tab(f, "rrq", "x1")
    out["next1 excess by weekday, all"] = tab(D, "wd", "x1")
    out["next1 excess on falls z<-1 agit by year"] = tab(f, "yr", "x1")
    out["next1 excess after falls z<-1 agit by coin"] = tab(f, "coin", "x1")
    # book: largest gains/losses
    bk = D[D.alloc.abs() > 0].dropna(subset=["bookr"])
    q = bk["bookr"].quantile([0.05, 0.95])
    out["book top5% gain days: mean z0, cl, prior r3"] = bk[bk.bookr >= q[0.95]][["z0", "cl", "zr3", "alloc"]].mean()
    out["book bottom5% days: mean z0, cl, prior r3"] = bk[bk.bookr <= q[0.05]][["z0", "cl", "zr3", "alloc"]].mean()
    # up days in agitated: continuation?
    out["corr z0 vs x1 agit / calm"] = pd.Series({"agit": D[D.agit == 1][["z0", "x1"]].corr().iloc[0, 1],
                                                 "calm": D[D.agit == 0][["z0", "x1"]].corr().iloc[0, 1],
                                                 "n_agit": int(D.agit.sum()), "n_calm": int((D.agit == 0).sum())})
    return out
