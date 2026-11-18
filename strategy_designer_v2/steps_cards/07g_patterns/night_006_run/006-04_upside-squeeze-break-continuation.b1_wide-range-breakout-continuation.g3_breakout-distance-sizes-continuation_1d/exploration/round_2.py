def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1 / vol20.shift(1)
            prior_hi = hi.shift(1).rolling(20).max(); prior_lo = lo.shift(1).rolling(20).min()
            width = (prior_hi - prior_lo) / c
            width_rel = width / width.rolling(120, min_periods=40).median()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame(dict(coin=coin, win=w, z=z, r1=r1, fwd1=c.shift(-1)/c-1, fwd3=c.shift(-3)/c-1,
                                   fwd10=c.shift(-10)/c-1, width_rel=width_rel, vol20=vol20,
                                   wd=ts.dt.weekday, yr=ts.dt.year, pos=np.arange(len(b))))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["fwd1ex"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())
    g3 = A[A.pos % 3 == 0]
    A["fwd3ex"] = A["fwd3"] - A["coin"].map(g3.groupby("coin")["fwd3"].mean())
    def tt(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "n": len(s), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    dn = A[A.z <= -1]
    out["down-day next-day ex by coin"] = dn.groupby("coin")["fwd1ex"].apply(tt).unstack()
    out["down-day next-day ex by year"] = dn.groupby("yr")["fwd1ex"].apply(tt).unstack()
    # graded: regress fwd1ex on min(z,0) among z<0
    neg = A[(A.z < 0)].dropna(subset=["z", "fwd1ex"])
    sl = stats.linregress(neg["z"].clip(lower=-6), neg["fwd1ex"])
    out["slope fwd1ex on z (z<0)"] = pd.Series({"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(neg)})
    per = {}
    for coin, g in neg.groupby("coin"):
        s = stats.linregress(g["z"].clip(lower=-6), g["fwd1ex"]); per[coin] = (s.slope, s.slope/s.stderr, len(g))
    out["slope per coin z<0"] = pd.DataFrame(per, index=["slope", "t", "n"]).T
    # 3-day after down day on 3-grid
    d3 = A[(A.pos % 3 == 0) & (A.z <= -1)]
    out["down-day 3d ex by coin"] = d3.groupby("coin")["fwd3ex"].apply(tt).unstack()
    out["down-day 3d all"] = tt(d3["fwd3ex"])
    # weekday by year
    out["friday next-day ex by year"] = A[A.wd == 4].groupby("yr")["fwd1ex"].apply(tt).unstack()
    out["friday by coin"] = A[A.wd == 4].groupby("coin")["fwd1ex"].apply(tt).unstack()
    # compression abs move: 10-grid
    G = A[A.pos % 10 == 0].dropna(subset=["width_rel", "fwd10"]).copy()
    G["absf"] = G["fwd10"].abs(); G["absrel"] = G["absf"] / G["coin"].map(G.groupby("coin")["absf"].mean())
    G["q"] = G.groupby("coin")["width_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    lo_q = G[G.q == 0]["absrel"]; rest = G[G.q > 0]["absrel"]
    out["compressed abs move vs rest"] = pd.Series({"q0": lo_q.mean(), "rest": rest.mean(), "welch_t": stats.ttest_ind(lo_q, rest, equal_var=False).statistic, "n0": len(lo_q)})
    out["compressed absrel by coin"] = G[G.q == 0].groupby("coin")["absrel"].mean()
    G["absvolnorm"] = G["absf"] / (G["vol20"] * np.sqrt(10))
    out["abs move / own vol by q"] = G.groupby("q")["absvolnorm"].agg(["mean", "count"])
    return out
