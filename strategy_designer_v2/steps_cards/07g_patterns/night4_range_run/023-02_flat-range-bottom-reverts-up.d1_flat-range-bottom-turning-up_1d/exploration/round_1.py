def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"]; h = d["high"]; l = d["low"]
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            rng = hh - ll
            d["ratio"] = (c - c.shift(29)).abs() / rng
            d["dmid"] = (c - (hh + ll) / 2) / rng   # -0.5..0.5
            d["r10"] = c / c.shift(10) - 1
            d["r1"] = c / c.shift(1) - 1
            d["r30"] = c / c.shift(29) - 1
            d["vol20"] = d["r1"].rolling(20).std()
            d["f5"] = c.shift(-5) / c - 1
            d["f1"] = c.shift(-1) / c - 1
            d["pos"] = np.arange(len(d))
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["coin"] = coin; d["win"] = w
            rows.append(d[["coin","win","pos","ratio","dmid","r10","r1","r30","vol20","f5","f1","wd","forecast","postRebalance_current_allocation"]])
    A = pd.concat(rows, ignore_index=True)
    drift5 = A[A.pos % 5 == 0].groupby("coin")["f5"].mean()
    sd5 = A[A.pos % 5 == 0].groupby("coin")["f5"].std()
    A["u5"] = A["f5"] - A["coin"].map(drift5)
    A["z5"] = A["u5"] / A["coin"].map(sd5)
    G = A[(A.pos % 5 == 0)].dropna(subset=["u5","ratio","dmid","r10","vol20"]).copy()

    def summ(g, col="z5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_z5": x.mean(), "mean_u5": g["u5"].mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    G["flat"] = np.where(G.ratio <= 0.3, "flat", "trend")
    G["dq"] = pd.qcut(G.dmid, 5, labels=["d1low","d2","d3","d4","d5high"])
    out["dmid_quintile_by_flat"] = G.groupby(["flat","dq"]).apply(summ)
    # slope of z5 on dmid within flat and trend
    sl = {}
    for f, g in G.groupby("flat"):
        r = stats.linregress(g.dmid, g.z5); sl[f] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(g)})
    out["z5_on_dmid_slope"] = pd.DataFrame(sl).T
    # r10 quintiles overall and in flat-below
    G["r10z"] = G.r10 / G.vol20
    G["r10q"] = pd.qcut(G.r10z, 5, labels=["q1","q2","q3","q4","q5"])
    out["r10z_quintile_all"] = G.groupby("r10q").apply(summ)
    fb = G[(G.flat == "flat") & (G.dmid < 0)]
    out["r10z_q_flat_below"] = fb.groupby(pd.qcut(fb.r10z, 4)).apply(summ).reset_index(drop=True)
    # r30 (trend) quintiles
    G["r30z"] = G.r30 / (G.vol20 * np.sqrt(30))
    out["r30z_quintile"] = G.groupby(pd.qcut(G.r30z, 5, labels=["q1","q2","q3","q4","q5"])).apply(summ)
    # vol level
    G["volrank"] = G.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=["lo","mid","hi"]))
    out["vol_tercile"] = G.groupby("volrank").apply(summ)
    # large 1d moves: next 1d, all bars
    B = A.dropna(subset=["r1","f1","vol20"]).copy()
    B["r1z"] = B.r1 / B.vol20.shift(0)
    B["bin"] = pd.cut(B.r1z, [-99,-2,-1,0,1,2,99])
    B["f1z"] = B.f1 / B.vol20
    out["next1d_after_1d_move"] = B.groupby("bin").agg(n=("f1z","size"), mean_f1z=("f1z","mean"), sd=("f1z","std"))
    out["weekday_r1"] = A.dropna(subset=["r1"]).groupby("wd")["r1"].agg(["size","mean","std"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["size"])))
    # book: share time in position, by coin
    out["alloc_by_coin"] = A.groupby("coin")["postRebalance_current_allocation"].agg(lambda s: (s.abs() > 0).mean())
    return out
