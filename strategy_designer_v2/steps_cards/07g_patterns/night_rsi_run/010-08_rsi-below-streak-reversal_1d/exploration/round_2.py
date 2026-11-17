def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)),
                "r1": r1.values, "vol20": vol20.values,
                "z1": (r1/vol20).values,
                "z3": ((c/c.shift(3)-1)/(vol20*np.sqrt(3))).values,
                "dd28": (c/c.rolling(28).max()-1).values,
                "vz": ((np.log(v)-np.log(v).rolling(20).mean())/np.log(v).rolling(20).std()).values,
                "rng": ((b["high"]-b["low"])/c).values,
                "f1": (c.shift(-1)/c-1).values, "f3": (c.shift(-3)/c-1).values, "f7": (c.shift(-7)/c-1).values,
                "alloc": b["postRebalance_current_allocation"].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            rows.append(df)
    A = pd.concat(rows); A = A[A["i"] >= 28]
    def reg(h, fcol, x):
        G = A[A["i"] % h == 0].dropna(subset=[fcol, x]).copy()
        G["ex"] = G[fcol] - A[A["i"] % h == 0].groupby("coin")[fcol].transform("mean").reindex(G.index) if False else G[fcol] - G.groupby("coin")[fcol].transform("mean")
        r = stats.linregress(G[x], G["ex"])
        return [round(r.slope,5), round(r.slope/r.stderr,2), len(G)]
    tab = {}
    for h, f in [(1,"f1"),(3,"f3"),(7,"f7")]:
        for x in ["z1","z3","dd28","vz","rng","vol20"]:
            tab[f"{f}~{x}"] = reg(h, f, x)
    out["regressions slope,t,n"] = pd.DataFrame(tab, index=["slope","t","n"]).T
    # by coin and by half for z1 -> f1 and z3 -> f3
    G1 = A.dropna(subset=["f1","z1"]).copy(); G1["ex"] = G1["f1"] - G1.groupby("coin")["f1"].transform("mean")
    G1["half"] = np.where(G1["year"] <= 2021, "early", "late")
    out["z1->f1 by coin/half t"] = G1.groupby(["coin","half"]).apply(lambda g: stats.linregress(g["z1"], g["ex"]).slope/stats.linregress(g["z1"], g["ex"]).stderr)
    G1["neg"] = G1["z1"].clip(upper=0)
    out["neg part z1 -> f1 (slope,t)"] = str([round(x,5) for x in (lambda r: (r.slope, r.slope/r.stderr))(stats.linregress(G1["neg"], G1["ex"]))])
    # weekday by coin and half
    D = A.dropna(subset=["r1"]).copy(); D["half"] = np.where(D["year"] <= 2021, "early", "late")
    out["weekday mean r1 by half"] = D.groupby(["wd","half"])["r1"].mean().unstack()
    out["weekday t by coin"] = D.groupby(["wd","coin"])["r1"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s))).unstack()
    # book: worst/best days context
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    B = pd.concat(bd).dropna(subset=["book_return"])
    q = B["book_return"].quantile([0.02, 0.98])
    out["book tails count / mean coin ret"] = pd.DataFrame({
        "worst2%": [ (B["book_return"]<=q.iloc[0]).sum(), B.loc[B["book_return"]<=q.iloc[0],"coin_return"].mean()],
        "best2%": [ (B["book_return"]>=q.iloc[1]).sum(), B.loc[B["book_return"]>=q.iloc[1],"coin_return"].mean()]}, index=["n","coin_ret"])
    # position: market part vs timing
    A2 = A.dropna(subset=["f1","alloc"])
    mu = A2.groupby("coin")["f1"].transform("mean")
    out["gain parts (mean/bar)"] = pd.Series({"total": (A2["alloc"]*A2["f1"]).mean(), "market": (A2["alloc"]*mu).mean(), "timing": (A2["alloc"]*(A2["f1"]-mu)).mean(), "mean alloc": A2["alloc"].mean()})
    return out
