def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        allg = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allg.append(c[i + H] / c[i] - 1)
        dr = np.mean(allg)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(30).max()
            lo = b["low"].astype(float).rolling(30).min()
            R30 = c / c.shift(30) - 1
            s = ((c - c.shift(30)).abs() / (hi - lo)).clip(upper=1)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            R5 = c / c.shift(5) - 1
            al = b["postRebalance_current_allocation"].astype(float)
            for i in range(0, len(c) - H, H):
                f = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 R30=R30.iloc[i], s=s.iloc[i], vol=vol30.iloc[i], R5=R5.iloc[i],
                                 al=al.iloc[i], fwd=f, ex=f - dr))
    g = pd.DataFrame(rows).dropna(subset=["R30", "vol"])
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), share_pos=(x > 0).mean(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    g["rv"] = pd.qcut(g["R30"], 20, labels=False)
    b0 = g[g["rv"] == 0]
    out["bottom ventile summary"] = tt(b0["ex"])
    out["bottom ventile R30 range, s mean, vol mean vs all"] = pd.Series(dict(
        R30_max=b0["R30"].max(), R30_mean=b0["R30"].mean(), s_mean=b0["s"].mean(),
        vol_mean=b0["vol"].mean(), vol_all=g["vol"].mean()))
    out["bottom ventile by coin"] = b0.groupby("coin")["ex"].agg(["count", "mean"])
    out["bottom ventile by year"] = b0.groupby("year")["ex"].apply(tt).unstack()
    # graded: among R30<0 with s>0.8 (fall spanning range), slope of ex on R30
    f = g[(g["R30"] < 0)]
    f = f.assign(sb=pd.cut(f["s"], [0, .4, .6, .8, .9, 1.0001], include_lowest=True))
    out["falls: excess by share bucket"] = f.groupby("sb")["ex"].apply(tt).unstack()
    ri = g[g["R30"] > 0]
    ri = ri.assign(sb=pd.cut(ri["s"], [0, .4, .6, .8, .9, 1.0001], include_lowest=True))
    out["rises: excess by share bucket"] = ri.groupby("sb")["ex"].apply(tt).unstack()
    # falls with s>0.8: slope ex on R30 / (vol*sqrt30)
    fx = f[f["s"] > 0.8].copy()
    fx["z"] = fx["R30"] / (fx["vol"] * np.sqrt(30))
    sl = stats.linregress(fx["z"], fx["ex"])
    out["falls s>0.8: slope ex on vol-scaled R30"] = pd.Series(dict(n=len(fx), slope=sl.slope, t=sl.slope / sl.stderr))
    # short side by sign of R30
    a = g.dropna(subset=["al"])
    sh = a[a["al"] < 0]
    sh = sh.assign(gain=sh["al"] * sh["fwd"], sb=pd.cut(sh["s"], [0, .4, .6, .8, 1.0001], include_lowest=True))
    out["short gain by share bucket"] = sh.groupby("sb")["gain"].apply(tt).unstack()
    lg = a[a["al"] > 0]
    lg = lg.assign(gain=lg["al"] * lg["fwd"], sb=pd.cut(lg["s"], [0, .4, .6, .8, 1.0001], include_lowest=True))
    out["long gain by share bucket"] = lg.groupby("sb")["gain"].apply(tt).unstack()
    out["short gain by year"] = sh.groupby("year")["gain"].apply(tt).unstack()
    return out
