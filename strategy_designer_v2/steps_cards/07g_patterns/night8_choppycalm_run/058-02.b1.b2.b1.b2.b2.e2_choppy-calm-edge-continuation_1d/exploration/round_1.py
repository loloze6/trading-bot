def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            hh = h.rolling(20).max(); ll = l.rolling(20).min()
            pos = (c - ll) / (hh - ll) * 2 - 1
            r1 = c.pct_change()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            for hz in (1, 5):
                df[f"f{hz}"] = c.shift(-hz) / c - 1
            df["pos"] = pos; df["r1"] = r1; df["r20"] = r20; df["r60"] = r60; df["vol20"] = vol20
            df["r1z"] = r1 / vol20.shift(1)
            df["inprof"] = (df["regime"] == "unknown").astype(int)
            df["grid5"] = (np.arange(len(df)) % 5 == 0)
            df["coin"] = coin; df["win"] = w
            ts = pd.to_datetime(df["timestamp"])
            df["wd"] = ts.dt.weekday; df["year"] = ts.dt.year; df["dkey"] = ts.dt.floor("D")
            df["alloc"] = df["postRebalance_current_allocation"].astype(float)
            rows.append(df[["coin","win","pos","r1","r20","r60","vol20","r1z","f1","f5","inprof","grid5","wd","year","dkey","alloc","forecast"]])
    A = pd.concat(rows, ignore_index=True)
    # coin mean 5d
    g = A[A.grid5 & A.f5.notna()]
    cm = g.groupby("coin").f5.mean()
    A["u5"] = A.f5 - A.coin.map(cm)
    cm1 = A.groupby("coin").f1.mean()
    A["u1"] = A.f1 - A.coin.map(cm1)
    G = A[A.grid5 & A.u5.notna() & A.pos.notna()].copy()
    def tab(df, key, col="u5"):
        out = df.groupby(key)[col].agg(["mean","count","std"])
        out["t"] = out["mean"]/(out["std"]/np.sqrt(out["count"]))
        return out.round(4)
    G["posq"] = pd.cut(G.pos, [-1.01,-0.6,-0.2,0.2,0.6,1.01])
    res = {}
    res["pos bins, in profile"] = tab(G[G.inprof==1], "posq")
    res["pos bins, out of profile"] = tab(G[G.inprof==0], "posq")
    G["trend"] = pd.cut(G.r60, [-10,-0.1,0.1,10], labels=["falling","choppy","rising"])
    G["volq"] = G.groupby("coin").vol20.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res["pos bins x trend (all)"] = G.groupby(["trend","posq"]).u5.agg(["mean","count"]).round(4).unstack(0)
    res["pos bins x vol tercile"] = G.groupby(["volq","posq"]).u5.agg(["mean","count"]).round(4).unstack(0)
    # slope by trend
    sl = {}
    for k, d in G.groupby("trend"):
        if len(d) > 30:
            r = stats.linregress(d.pos, d.u5); sl[str(k)] = (round(r.slope,4), round(r.slope/r.stderr,2), len(d))
    for k, d in G.groupby("volq"):
        r = stats.linregress(d.pos, d.u5); sl["vol"+str(k)] = (round(r.slope,4), round(r.slope/r.stderr,2), len(d))
    res["slope pos->u5 by group (slope,t,n)"] = pd.DataFrame(sl, index=["slope","t","n"]).T
    # 20-day return as signal
    G["r20q"] = G.groupby("coin").r20.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["r20 quintile -> u5"] = tab(G, "r20q")
    # large daily moves -> next 1 day, all bars
    B = A[A.r1z.notna() & A.u1.notna()].copy()
    B["zq"] = pd.cut(B.r1z, [-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    res["daily z move -> next day u1 (all bars)"] = tab(B, "zq", "u1")
    G5 = A[A.grid5 & A.r1z.notna() & A.u5.notna()].copy()
    G5["zq"] = pd.cut(G5.r1z, [-99,-2,-1,1,2,99])
    res["daily z move -> next 5 days u5 (grid)"] = tab(G5, "zq")
    res["weekday -> next day u1"] = tab(A[A.u1.notna()], "wd", "u1")
    res["year -> pos slope sign: mean u5*sign(pos) in profile"] = G[G.inprof==1].assign(x=lambda d: d.u5*np.sign(d.pos)).groupby("year").x.agg(["mean","count"]).round(4)
    res["share in profile by year"] = A.groupby("year").inprof.mean().round(3)
    return res
