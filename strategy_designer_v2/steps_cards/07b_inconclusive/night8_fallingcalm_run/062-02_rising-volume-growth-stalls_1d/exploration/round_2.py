def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].astype(float)
            m1 = v.rolling(30).mean(); m0 = v.shift(30).rolling(30).mean()
            lvr = np.log(m1 / m0)
            ret60 = df["close"] / df["close"].shift(60) - 1
            ret20 = df["close"] / df["close"].shift(20) - 1
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h,
                        day=str(df["timestamp"].iloc[i])[:10],
                        fwd=c[i+h]/c[i]-1, fc=df["forecast"].iloc[i],
                        lvr=lvr.iloc[i], r60=ret60.iloc[i], r20=ret20.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin","h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    r = d[(d.r60 > .1)].dropna(subset=["lvr","ex"]).copy()
    out = {}
    def cl(g, x):
        g = g.dropna(subset=[x,"ex"])
        if len(g) < 15: return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t_cl=np.nan))
        X = np.column_stack([np.ones(len(g)), g[x].values]); y = g["ex"].values
        b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2,2))
        for _, idx in g.groupby("day").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s)
        V = XtXi @ meat @ XtXi
        return pd.Series(dict(n=len(g), days=g.day.nunique(), slope=b[1], t_cl=b[1]/np.sqrt(V[1,1])))
    out["rising_rawlvr_clustered_by_h"] = r.groupby("h").apply(lambda g: cl(g, "lvr"))
    r5 = r[r.h == 5].copy()
    r5["shrink"] = -r5["lvr"]
    r5["shrink_pos"] = r5["shrink"].clip(lower=0)
    r5["growth_pos"] = r5["lvr"].clip(lower=0)
    out["rising_h5_shrinkpart_vs_growthpart"] = pd.DataFrame({
        "shrink_only": cl(r5[r5.lvr < 0], "shrink"),
        "growth_only": cl(r5[r5.lvr >= 0], "lvr")}).T
    r5["shrq"] = pd.qcut(r5["lvr"], 3, labels=["shrunk","mid","grown"])
    r5["r60q"] = pd.qcut(r5["r60"], 2, labels=["weaker","stronger"])
    out["rising_h5_tercile_x_trend_ex"] = r5.groupby(["r60q","shrq"]).agg(
        n=("ex","size"), ex=("ex","mean"),
        t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["rising_h5_slope_by_trendhalf"] = r5.groupby("r60q").apply(lambda g: cl(g, "lvr"))
    out["rising_h5_slope_by_coin"] = r5.groupby("coin").apply(lambda g: cl(g, "lvr"))
    out["rising_h5_shrunk_tercile_by_window"] = r5[r5.shrq=="shrunk"].groupby("win").agg(
        n=("ex","size"), ex=("ex","mean"))
    out["rising_h5_corr_fc_lvr"] = float(r5.dropna(subset=["fc"]).query("fc!=0")[["fc","lvr"]].corr().iloc[0,1])
    return out
