def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(df)
            r28 = pd.Series(c).pct_change(28).values
            lr = np.log(pd.Series(c))
            dr = lr.diff()
            # steadiness: 28-day log return over the sum of absolute daily log moves
            eff = (lr.diff(28) / dr.abs().rolling(28).sum()).values
            vol28 = dr.rolling(28).std().values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, i=i, ts=df["timestamp"].iloc[i],
                                 ret=c[i + H] / c[i] - 1, fc=df["forecast"].iloc[i],
                                 reg=df["regime"].iloc[i], r28=r28[i], eff=eff[i], vol28=vol28[i]))
    d = pd.DataFrame(rows)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    d["drift"] = d.groupby("coin")["ret"].transform("mean")
    d["adj"] = d["ret"] - d["drift"]
    d["sadj"] = -d["adj"]
    d["r28z"] = d["r28"] / (d["vol28"] * np.sqrt(28))

    def clus(g, x, y="adj"):
        g = g.dropna(subset=[x, y])
        if len(g) < 15:
            return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t_ols=np.nan, t_day=np.nan))
        X = np.column_stack([np.ones(len(g)), g[x].values])
        Y = g[y].values
        XtX_inv = np.linalg.inv(X.T @ X)
        b = XtX_inv @ X.T @ Y
        e = Y - X @ b
        s = stats.linregress(g[x], g[y])
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            u = X[idx].T @ e[idx]
            meat += np.outer(u, u)
        G = g["day"].nunique()
        k = 2
        corr = G / (G - 1) * (len(g) - 1) / (len(g) - k)
        V = corr * XtX_inv @ meat @ XtX_inv
        return pd.Series(dict(n=len(g), days=G, slope=b[1], t_ols=s.slope / s.stderr, t_day=b[1] / np.sqrt(V[1, 1])))

    out = {}
    cases = d[(d.reg == "mean_reversion") & (d.fc < 0)]
    thinfall = d[(d.reg == "mean_reversion") & (d.r28 < 0)]
    out["thin cases: forecast vs raw r28 vs vol-scaled r28"] = pd.DataFrame({
        "fc": clus(cases, "fc"), "r28_cases": clus(cases, "r28"),
        "r28_thinfalls": clus(thinfall, "r28"), "r28z_thinfalls": clus(thinfall, "r28z")}).T
    out["corr fc vs r28 in cases"] = float(cases[["fc", "r28"]].corr().iloc[0, 1])
    out["raw r28 slope, thin falls, by year"] = thinfall.groupby("year").apply(lambda g: clus(g, "r28"))
    out["raw r28 slope, thin falls, by coin"] = thinfall.groupby("coin").apply(lambda g: clus(g, "r28"))
    tf = thinfall.copy()
    tf["q"] = pd.qcut(tf["r28"], 5, labels=False)
    out["thin falls by r28 quintile (0 deepest)"] = tf.groupby("q").agg(n=("adj", "size"), r28=("r28", "mean"),
        sadj=("sadj", "mean"), t=("sadj", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))), raw=("ret", "mean"))
    # steadiness within thin falls
    tf["steady"] = pd.qcut(tf["eff"], 2, labels=["choppy", "steady"])
    out["thin falls: r28 slope by steadiness"] = tf.groupby("steady").apply(lambda g: clus(g, "r28"))
    # all falls, non-thin, by quintile for contrast
    nf = d[(d.reg != "mean_reversion") & (d.r28 < 0)].copy()
    nf["q"] = pd.qcut(nf["r28"], 3, labels=False)
    out["non-thin falls by r28 tercile (0 deepest)"] = nf.groupby("q").agg(n=("adj", "size"), r28=("r28", "mean"),
        sadj=("sadj", "mean"), t=("sadj", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    return out
