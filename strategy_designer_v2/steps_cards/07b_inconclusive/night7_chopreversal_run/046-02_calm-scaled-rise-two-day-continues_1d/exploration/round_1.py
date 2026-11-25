def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            d2 = c.shift(-2) / c.shift(-1) - 1
            f3 = c.shift(-3) / c - 1
            f5 = c.shift(-5) / c - 1
            calm = d["regime"].astype(str) != "chop"
            fc = d["forecast"].astype(float)
            n = len(d)
            pos = np.arange(n)
            t = pd.DataFrame({"coin": coin, "win": w, "pos": pos, "z": z, "r": r, "calm": calm,
                              "fc": fc, "f1": f1, "f2": f2, "d2": d2, "f3": f3, "f5": f5,
                              "tr60": tr60, "year": pd.to_datetime(d["timestamp"]).dt.year})
            rows.append(t)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin: mean of 2-bar grid returns over all windows
    g2 = A[A.pos % 2 == 0]
    drift2 = g2.groupby("coin")["f2"].mean()
    A["ex2"] = A["f2"] - A["coin"].map(drift2)
    g1 = A.groupby("coin")["f1"].mean()
    A["ex1"] = A["f1"] - A["coin"].map(g1)
    A["exd2"] = A["d2"] - A["coin"].map(g1)
    G = A[(A.pos % 2 == 0)].dropna(subset=["z", "f2"])
    S = G[(G.z > 0) & G.calm]
    out = {}
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    S = S.copy()
    S["zq"] = pd.qcut(S.z, 5, labels=False)
    out["calm up, by z quintile: ex2"] = S.groupby("zq")["ex2"].apply(tt).unstack()
    out["calm up, by z quintile: ex1 (day1)"] = S.groupby("zq")["ex1"].apply(tt).unstack()
    out["calm up, by z quintile: exd2 (day2 alone)"] = S.groupby("zq")["exd2"].apply(tt).unstack()
    out["calm up, z quint mean z"] = S.groupby("zq")["z"].mean()
    # agitated comparison
    Ag = G[(G.z > 0) & (~G.calm)].copy()
    Ag["zq"] = pd.qcut(Ag.z, 5, labels=False)
    out["agitated up, by z quintile ex2"] = Ag.groupby("zq")["ex2"].apply(tt).unstack()
    # down days calm
    Dn = G[(G.z < 0) & G.calm].copy()
    Dn["zq"] = pd.qcut(Dn.z, 5, labels=False)
    out["calm down, by z quintile ex2"] = Dn.groupby("zq")["ex2"].apply(tt).unstack()
    # slope by coin, by window, by trend
    def sl(x):
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        res = stats.linregress(x.z, x.ex2)
        return pd.Series({"n": len(x), "slope": res.slope, "t": res.slope/res.stderr})
    out["slope by coin"] = S.groupby("coin").apply(sl)
    out["slope by window"] = S.groupby("win").apply(sl)
    S["trend"] = np.where(S.tr60 > 0.10, "rising", np.where(S.tr60 < -0.10, "falling", "choppy"))
    out["slope by trend"] = S.groupby("trend").apply(sl)
    out["ex2 by trend"] = S.groupby("trend")["ex2"].apply(tt).unstack()
    # horizons for top quintile
    top = S[S.zq == 4]
    for h in ["f1", "f2", "f3", "f5"]:
        out[f"top quint raw {h} mean%"] = 100*top[h].mean()
    out["all calm grid raw f2 mean%"] = 100*G[G.calm]["f2"].mean()
    return out
