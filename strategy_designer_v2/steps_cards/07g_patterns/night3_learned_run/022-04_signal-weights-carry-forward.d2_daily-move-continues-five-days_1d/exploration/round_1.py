def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < 30: continue
            r1 = pd.Series(c).pct_change()
            lr = np.log(pd.Series(c)).diff()
            vol20 = lr.rolling(20, min_periods=10).std()
            vol60 = lr.rolling(60, min_periods=20).std()
            mom5 = pd.Series(c).pct_change(5)
            mom20 = pd.Series(c).pct_change(20)
            mom60 = pd.Series(c).pct_change(60)
            hi30 = pd.Series(df["high"].astype(float).values).rolling(30, min_periods=10).max()
            lo30 = pd.Series(df["low"].astype(float).values).rolling(30, min_periods=10).min()
            near = (pd.Series(c) - lo30) / (hi30 - lo30)
            rng = (df["high"].astype(float) - df["low"].astype(float)) / df["close"].astype(float)
            rngz = rng / rng.rolling(60, min_periods=20).mean()
            vol = df["volume"].astype(float)
            volz = np.log(vol / vol.rolling(60, min_periods=20).mean())
            clv = (df["close"].astype(float) - df["low"].astype(float)) / (df["high"].astype(float) - df["low"].astype(float))
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 5, 5):
                rows.append(dict(coin=coin, w=w, wnum=int(w[1:]), f=df["forecast"].iloc[i],
                    r1=r1.iloc[i], fwd=c[i+5]/c[i]-1, fwd1=c[i+1]/c[i]-1,
                    v20=vol20.iloc[i], vr=vol20.iloc[i]/vol60.iloc[i] if vol60.iloc[i] else np.nan,
                    m5=mom5.iloc[i], m20=mom20.iloc[i], m60=mom60.iloc[i], near=near.iloc[i],
                    rngz=rngz.iloc[i], volz=volz.iloc[i], clv=clv.iloc[i], wd=ts.iloc[i].weekday(),
                    yr=ts.iloc[i].year, alloc=df["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd"].transform("std")
    g["ex"] = (g["fwd"] - g["drift"]) / g["sd"]   # strength units
    out = {}
    def slope(col, sub=None):
        d = g if sub is None else sub
        d = d[[col, "ex"]].replace([np.inf, -np.inf], np.nan).dropna()
        x = d[col].groupby(g.loc[d.index, "coin"]).transform(lambda s: (s - s.mean())/s.std())
        r = stats.linregress(x, d["ex"])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope/r.stderr))
    feats = ["f","r1","m5","m20","m60","near","v20","vr","rngz","volz","clv"]
    out["slope per feature (z-scored, strength units)"] = pd.DataFrame({k: slope(k) for k in feats}).T
    # quintiles of several
    for k in ["m20","m60","near","v20","volz","clv"]:
        d = g[[k,"ex","coin"]].replace([np.inf,-np.inf],np.nan).dropna()
        q = d.groupby("coin")[k].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out[f"quintile {k}"] = d.groupby(q)["ex"].agg(["count","mean"]).assign(t=d.groupby(q)["ex"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    out["weekday"] = g.groupby("wd")["ex"].agg(["count","mean"])
    # per coin slopes for m20, m60
    pc = {}
    for coin in g.coin.unique():
        sub = g[g.coin==coin]
        pc[coin] = pd.Series({k: slope(k, sub)["t"] for k in ["f","m20","m60","near","v20","volz"]})
    out["t by coin"] = pd.DataFrame(pc).T
    # year stability for m20, m60, near
    yy = {}
    for y in sorted(g.yr.unique()):
        sub = g[g.yr==y]
        if len(sub) > 60:
            yy[y] = pd.Series({k: slope(k, sub)["t"] for k in ["f","m20","m60","near"]})
    out["t by year"] = pd.DataFrame(yy).T
    # forecast extremes: large abs r1, sign-adjusted fwd
    d = g.dropna(subset=["r1"]).copy()
    d["absz"] = d.groupby("coin")["r1"].transform(lambda s: (s.abs()/s.abs().mean()))
    d["sx"] = np.sign(d["r1"]) * d["ex"]
    q = pd.qcut(d["absz"].rank(method="first"), 5, labels=False)
    out["signed continuation by abs day move quintile"] = d.groupby(q)["sx"].agg(["count","mean"]).assign(t=d.groupby(q)["sx"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    out["n grid"] = len(g)
    out["usual 5d move pct by coin"] = (g.groupby("coin")["sd"].first()*100)
    return out
