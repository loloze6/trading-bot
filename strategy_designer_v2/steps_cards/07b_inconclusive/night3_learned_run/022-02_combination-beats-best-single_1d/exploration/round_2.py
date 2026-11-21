def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    C = "debug_info.components.combined.post_pipeline_value"
    rows = []
    for coin, ws in bars.items():
        for H in [5, 10, 20]:
            grid = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                cl = pd.Series(df["close"].values)
                n = len(df)
                r28 = cl.pct_change(28).values
                r1 = cl.pct_change(1).values
                hi = (cl / cl.rolling(90).max()).values
                vol = cl.pct_change().rolling(30).std().values
                for i in range(0, n - H, H):
                    grid.append(dict(coin=coin, w=w, H=H, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     ret=cl[i+H]/cl[i]-1, c=df[C].iloc[i] if C in df else np.nan,
                                     r28=r28[i], r1=r1[i], hi=hi[i], vol=vol[i]))
            g = pd.DataFrame(grid)
            g["y"] = g["ret"] - g["ret"].mean()
            g["usual"] = g["ret"].std()
            rows.append(g)
    d = pd.concat(rows)
    out = {}
    def ct(x, k):
        x = x.dropna(subset=[k, "y"])
        r = x["y"].corr(x[k]); n = len(x)
        return r, r*np.sqrt((n-2)/(1-r*r)), n
    res = []
    for H in [5, 10, 20]:
        dh = d[d.H == H]
        for k in ["r28", "r1", "hi", "vol", "c"]:
            r, t, n = ct(dh, k)
            res.append(dict(H=H, sig=k, corr=r, t=t, n=n))
    out["corr_by_H"] = pd.DataFrame(res)
    d5 = d[d.H == 5]
    pc = []
    for coin, x in d5.groupby("coin"):
        for k in ["r28", "hi", "c"]:
            r, t, n = ct(x, k)
            pc.append(dict(coin=coin, sig=k, corr=r, t=t, n=n))
    out["by_coin_5d"] = pd.DataFrame(pc).pivot(index="coin", columns="sig", values="corr")
    # year-to-year persistence of each signal's correlation
    yc = d5.groupby("year").apply(lambda x: pd.Series({k: x["y"].corr(x[k]) for k in ["r28","r1","hi","vol"]}))
    out["year_corr_5d"] = yc
    out["lag1_persistence"] = pd.Series({k: yc[k].corr(yc[k].shift(1)) for k in yc.columns}).to_frame("corr_with_prev_year")
    # r28 quintiles, 5d and 20d, strength
    for H in [5, 20]:
        dh = d[d.H == H].dropna(subset=["r28"]).copy()
        dh["q"] = pd.qcut(dh["r28"], 5, labels=False)
        out[f"r28_quint_{H}d"] = dh.groupby("q").agg(n=("y","size"), r28=("r28","mean"), mean_y=("y","mean"),
                                                     strength=("y", lambda s: (s / dh.loc[s.index, "usual"]).mean()))
    return out
