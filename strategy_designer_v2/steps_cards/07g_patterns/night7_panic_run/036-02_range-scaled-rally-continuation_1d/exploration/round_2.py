def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            n = len(d)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=10).std()
            ts = pd.to_datetime(d["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n), "day": ts.dt.floor("D"),
                              "r1s": r1 / sd30, "r14s": (c / c.shift(14) - 1) / sd30,
                              "r30p": c / c.shift(30) - 1, "vol": sd30,
                              "volrank": sd30.rolling(120, min_periods=30).rank(pct=True),
                              "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1,
                              "fwd7": c.shift(-7) / c - 1, "fwd14": c.shift(-14) / c - 1,
                              "yr": ts.dt.year,
                              "clv": (c - l) / (h - l).replace(0, np.nan)})
            rows.append(g)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def daysum_t(G, x, y):
        # slope t with residual-free proxy: mean of y*sign(x) summed per day
        z = G.assign(v=-np.sign(G[x]) * G[y]).groupby("day")["v"].sum()
        return round(z.mean() / (z.std() / np.sqrt(len(z))), 2), len(z)
    G1 = A.dropna(subset=["r1s", "fwd1"]).copy()
    G1["ex1"] = G1["fwd1"] - G1["coin"].map(G1.groupby("coin")["fwd1"].mean())
    G1["b"] = pd.cut(G1["r1s"], [-99, -2, -1, 0, 1, 2, 99])
    o = G1.groupby("b")["ex1"].agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["r1s bins ex1"] = o.round(4)
    res = {}
    for k, s in G1.groupby("coin"):
        r = stats.linregress(s["r1s"], s["ex1"]); res[k] = (round(r.slope * 1e4, 2), round(r.slope / r.stderr, 2))
    out["r1s->ex1 by coin (slope bp per sd, t)"] = pd.DataFrame(res, index=["slope", "t"]).T
    res = {}
    for k, s in G1.groupby("w"):
        r = stats.linregress(s["r1s"], s["ex1"]); res[k] = (round(r.slope * 1e4, 2), round(r.slope / r.stderr, 2), len(s))
    out["r1s->ex1 by window"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    G1["tr"] = pd.cut(G1["r30p"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    G1["ag"] = np.where(G1["volrank"] > 0.5, "agit", "calm")
    res = {}
    for k, s in G1.dropna(subset=["tr", "volrank"]).groupby(["tr", "ag"]):
        r = stats.linregress(s["r1s"], s["ex1"]); res[str(k)] = (round(r.slope * 1e4, 2), round(r.slope / r.stderr, 2), len(s))
    out["r1s->ex1 by trend30 x agit"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    # down vs up side separately
    res = {}
    for nm, s in [("down", G1[G1.r1s < 0]), ("up", G1[G1.r1s > 0])]:
        r = stats.linregress(s["r1s"], s["ex1"]); res[nm] = (round(r.slope * 1e4, 2), round(r.slope / r.stderr, 2), len(s))
    out["r1s->ex1 by side"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    out["daysum sign t ex1"] = pd.Series(daysum_t(G1, "r1s", "ex1"), index=["t", "days"])
    # 2-day non-overlap
    G2 = A[A.pos % 2 == 0].dropna(subset=["r1s", "fwd2"]).copy()
    G2["ex2"] = G2["fwd2"] - G2["coin"].map(G2.groupby("coin")["fwd2"].mean())
    r = stats.linregress(G2["r1s"], G2["ex2"]); out["r1s->ex2 slope t"] = round(r.slope / r.stderr, 2)
    # clv interaction for big down days
    big = G1[G1.r1s < -1].copy()
    big["cb"] = pd.qcut(big["clv"], 3, labels=False)
    o = big.groupby("cb")["ex1"].agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["big down day by close location ex1"] = o.round(4)
    # 14-day momentum
    G7 = A[A.pos % 7 == 0].dropna(subset=["r14s", "fwd7"]).copy()
    G7["ex7"] = G7["fwd7"] - G7["coin"].map(G7.groupby("coin")["fwd7"].mean())
    res = {}
    for k, s in G7.groupby("yr"):
        r = stats.linregress(s["r14s"], s["ex7"]); res[k] = (round(r.slope / r.stderr, 2), len(s))
    out["r14s->ex7 by year (t,n)"] = pd.DataFrame(res, index=["t", "n"]).T
    res = {}
    for k, s in G7.groupby("coin"):
        r = stats.linregress(s["r14s"], s["ex7"]); res[k] = (round(r.slope / r.stderr, 2), len(s))
    out["r14s->ex7 by coin (t,n)"] = pd.DataFrame(res, index=["t", "n"]).T
    G14 = A[A.pos % 14 == 0].dropna(subset=["r14s", "fwd14"]).copy()
    G14["ex14"] = G14["fwd14"] - G14["coin"].map(G14.groupby("coin")["fwd14"].mean())
    r = stats.linregress(G14["r14s"], G14["ex14"]); out["r14s->ex14 slope t, n"] = f"{r.slope/r.stderr:.2f}, {len(G14)}"
    return out
