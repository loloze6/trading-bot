def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def agg(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    # per-horizon grids
    res = {}
    allrows = {}
    for h in [1, 3, 5, 10]:
        rows = []
        for coin, wins in data["bars"].items():
            tmp = []
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float)
                r1 = c.pct_change()
                sd = r1.rolling(20, min_periods=15).std()
                df = pd.DataFrame({"coin": coin, "win": w, "z": r1 / sd,
                                   "fh": c.shift(-h) / c - 1,
                                   "p20": c / c.shift(20) - 1,
                                   "p60": c / c.shift(60) - 1,
                                   "z3": (c / c.shift(3) - 1) / (sd * np.sqrt(3)),
                                   "fall": (b["regime"] == "mean_reversion").astype(int),
                                   "yr": pd.to_datetime(b["timestamp"]).dt.year})
                tmp.append(df.iloc[::h])
            d = pd.concat(tmp)
            d["u"] = d["fh"] - d["fh"].mean()
            d["us"] = d["u"] / d["fh"].std()
            rows.append(d)
        G = pd.concat(rows).dropna(subset=["u", "z"])
        allrows[h] = G
        G["zb"] = pd.cut(G["z"], [-99, -1, 0, 1, 2, 99])
        tab = G.groupby(["fall", "zb"], observed=True)["us"].apply(agg).unstack()
        res[h] = tab
    for h in [1, 3, 10]:
        out[f"strength (u/usual) by z x fall, h={h}d"] = res[h]
    G = allrows[5]
    G["half"] = np.where(G["yr"] <= 2021, "2018-21", "2022-25")
    sub = G[G.z > 1]
    out["h5 u after z>1 by fall x half"] = sub.groupby(["fall", "half"])["u"].apply(agg).unstack()
    out["h5 u after z>1 by fall, coin count positive"] = sub.groupby(["fall", "coin"])["u"].mean().groupby(level=0).apply(lambda s: pd.Series({"coins": len(s), "share_pos": (s > 0).mean()})).unstack()
    # graded slope of u on z within regimes, z>0
    for f in [0, 1]:
        s = G[(G.fall == f) & (G.z > 0)].dropna(subset=["us"])
        lr = stats.linregress(s["z"], s["us"])
        out[f"slope us on z (z>0), fall={f}"] = pd.Series({"n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
    # trend: 60d return quintile, all bars
    G2 = G.dropna(subset=["p60"]).copy()
    G2["q"] = G2.groupby("coin")["p60"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["h5 strength by past60d quintile"] = G2.groupby("q")["us"].apply(agg).unstack()
    G2["half"] = np.where(G2["yr"] <= 2021, "2018-21", "2022-25")
    out["h5 strength by past60d quintile x half"] = G2.groupby(["half", "q"])["us"].apply(agg).unstack()
    # weekday on cross-coin daily mean
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    m = D.groupby(["win", "day"])["coin_return"].mean().dropna().reset_index()
    dt = pd.to_datetime(m["day"])
    m["wd"] = dt.dt.weekday; m["half"] = np.where(dt.dt.year <= 2021, "2018-21", "2022-25")
    out["cross-coin daily mean by weekday"] = m.groupby("wd")["coin_return"].apply(agg).unstack()
    out["cross-coin daily mean by weekday x half"] = m.groupby(["half", "wd"])["coin_return"].apply(agg).unstack()["t"].unstack()
    btc = D[D.coin == "BTCUSD"].copy(); btc["wd"] = pd.to_datetime(btc["day"]).dt.weekday
    out["BTC daily by weekday"] = btc.groupby("wd")["coin_return"].apply(agg).unstack()
    return out
