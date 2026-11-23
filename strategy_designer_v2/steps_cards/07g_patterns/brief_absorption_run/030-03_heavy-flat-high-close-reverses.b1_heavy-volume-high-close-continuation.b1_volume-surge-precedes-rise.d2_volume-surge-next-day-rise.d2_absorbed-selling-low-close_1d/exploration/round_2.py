def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            o = b["open"].astype(float); v = b["volume"].astype(float)
            rng = (h - l).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "loc": (h - c) / rng,
                "vr": v / v.shift(1).rolling(20, min_periods=20).mean(),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "r0": c / c.shift(1) - 1,
                "r5p": c / c.shift(5) - 1,
                "r20p": c / c.shift(20) - 1,
                "rngp": rng / c,
                "body": (c - o).abs() / rng,
                "wd": ts.dt.weekday, "yr": ts.dt.year,
                "pv": b["postRebalance_total_value"].astype(float),
            })
            for k in (1, 3, 5):
                d[f"f{k}"] = c.shift(-k) / c - 1
            d["vol20"] = d["r0"].rolling(20, min_periods=15).std()
            d["rngrel"] = d["rngp"] / d["rngp"].shift(1).rolling(20, min_periods=15).mean()
            d["bookr_next"] = d["pv"].shift(-1) / d["pv"] - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in (1, 3, 5):
        mu = {}
        for coin, g in D.groupby("coin"):
            mu[coin] = g.loc[g.pos % k == 0, f"f{k}"].mean()
        D[f"x{k}"] = D[f"f{k}"] - D["coin"].map(mu)
    out = {}
    def tstat(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean%": 100*s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    def reg(g, xcol, ycol):
        g = g.dropna(subset=[xcol, ycol])
        if len(g) < 30:
            return pd.Series({"slope%": np.nan, "t": np.nan, "n": len(g)})
        r = stats.linregress(g[xcol], g[ycol])
        return pd.Series({"slope%": 100*r.slope, "t": r.slope/r.stderr, "n": len(g)})
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as e:
            out[name] = "error: " + str(e)[:150]
    def fq():
        res = {}
        for k in (1, 3, 5):
            G = D[(D.pos % k == 0)].dropna(subset=["fc", f"x{k}"])
            G = G.assign(q=pd.qcut(G.fc.rank(method="first"), 5, labels=False))
            res[f"h{k}"] = G.groupby("q")[f"x{k}"].apply(lambda s: 100*s.mean())
            res[f"t{k}"] = G.groupby("q")[f"x{k}"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
        return pd.DataFrame(res)
    safe("fc quintile excess % by horizon", fq)
    G = D.dropna(subset=["loc", "vr", "x1"]).copy()
    G["lq"] = pd.qcut(G["loc"].rank(method="first"), 5, labels=False)
    G["vq"] = pd.qcut(G["vr"].rank(method="first"), 3, labels=["lowV", "midV", "highV"])
    safe("x1 % by loc quintile (0=close at high) x vol tercile", lambda: G.pivot_table(index="lq", columns="vq", values="x1", aggfunc=lambda s: 100*s.mean()))
    safe("slope x1 on loc by vol tercile", lambda: G.groupby("vq").apply(lambda g: reg(g, "loc", "x1")))
    safe("slope x3 on loc by vol tercile (3d grid)", lambda: G[G.pos % 3 == 0].groupby("vq").apply(lambda g: reg(g, "loc", "x3")))
    safe("slope x1 on vr alone", lambda: reg(G, "vr", "x1"))
    def pq(col, k):
        G2 = D[D.pos % k == 0].dropna(subset=[col, f"x{k}"]).copy()
        G2["q"] = pd.qcut(G2[col].rank(method="first"), 5, labels=False)
        return G2.groupby("q")[f"x{k}"].apply(tstat).unstack()
    safe("x1 by prior 5d return quintile", lambda: pq("r5p", 1))
    safe("x5 by prior 5d return quintile (5d grid)", lambda: pq("r5p", 5))
    safe("x5 by prior 20d return quintile (5d grid)", lambda: pq("r20p", 5))
    safe("x1 by today's return quintile", lambda: pq("r0", 1))
    safe("x1 by range-vs-20d-range quintile", lambda: pq("rngrel", 1))
    safe("x1 by vol20 quintile", lambda: pq("vol20", 1))
    G5 = D.dropna(subset=["vol20", "loc", "x1"]).copy()
    G5["volq"] = pd.qcut(G5.vol20.rank(method="first"), 3, labels=["calm", "mid", "wild"])
    safe("slope x1 on loc by vol regime", lambda: G5.groupby("volq").apply(lambda g: reg(g, "loc", "x1")))
    G6 = D.dropna(subset=["r20p", "loc", "x1"]).copy()
    G6["trq"] = pd.qcut(G6.r20p.rank(method="first"), 3, labels=["down20", "flat20", "up20"])
    safe("slope x1 on loc by 20d trend", lambda: G6.groupby("trq").apply(lambda g: reg(g, "loc", "x1")))
    safe("x1 by weekday", lambda: D.groupby("wd")["x1"].apply(tstat).unstack())
    safe("loc slope by coin", lambda: G.groupby("coin").apply(lambda g: reg(g, "loc", "x1")))
    safe("loc slope by year", lambda: G.groupby("yr").apply(lambda g: reg(g, "loc", "x1")))
    safe("loc slope by window", lambda: G.groupby("win").apply(lambda g: reg(g, "loc", "x1"))[["slope%", "t"]].describe())
    safe("book alloc stats", lambda: pd.Series({"mean_alloc": D.alloc.mean(), "share>0.01": (D.alloc > 0.01).mean(), "corr_alloc_fc": D[["alloc", "fc"]].corr().iloc[0, 1], "share fc>0": (D.fc > 0).mean(), "mean_vol20_when_alloc_top": D.loc[D.alloc > D.alloc.quantile(0.8), "vol20"].mean(), "mean_vol20_all": D.vol20.mean()}))
    def bookext():
        E = D.dropna(subset=["bookr_next", "x1"]).copy()
        lo, hi = E.bookr_next.quantile(0.02), E.bookr_next.quantile(0.98)
        sel = {"worst2%": E[E.bookr_next <= lo], "best2%": E[E.bookr_next >= hi], "all": E}
        return pd.DataFrame({k: {"n": len(g), "loc": g["loc"].mean(), "vr": g.vr.mean(), "r0%": 100*g.r0.mean(), "r5p%": 100*g.r5p.mean(), "vol20%": 100*g.vol20.mean(), "alloc": g.alloc.mean(), "fc": g.fc.mean()} for k, g in sel.items()})
    safe("bar state before book's largest next-bar gains/losses", bookext)
    def bigmove():
        E = D.dropna(subset=["r0", "vol20", "x1", "x3"]).copy()
        E["z"] = E.r0 / E.vol20.shift(0)
        E["zq"] = pd.cut(E.z, [-99, -2, -1, 1, 2, 99], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
        a = E.groupby("zq")["x1"].apply(tstat).unstack()
        b = E[E.pos % 3 == 0].groupby("zq")["x3"].apply(tstat).unstack().add_prefix("h3_")
        return pd.concat([a, b], axis=1)
    safe("x1/x3 after today's return in vol units", bigmove)
    return out
