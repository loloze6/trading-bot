def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values); n = len(c)
            r1 = c.pct_change(1); vol = r1.rolling(20).std()
            r30 = c.pct_change(30)
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - 1):
                rows.append(dict(coin=coin, wi=int(w[1:]), fwd=c[t+1]/c[t]-1, r1=r1[t],
                                 z1=r1[t]/vol[t] if vol[t] > 0 else np.nan, vol=vol[t], r30=r30[t],
                                 yr=ts.iloc[t].year, wd=ts.iloc[t].dayofweek))
    df = pd.DataFrame(rows).dropna(subset=["z1"])
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    res = []
    for k, g in df.groupby("yr"):
        rho, p = stats.spearmanr(g["z1"], g["ex"]); res.append(dict(grp=k, n=len(g), rho=rho, p=p))
    out["z1 -> next 1d by year"] = pd.DataFrame(res)
    df["vq"] = df.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False))
    res = []
    for k, g in df.groupby("vq"):
        rho, p = stats.spearmanr(g["z1"], g["ex"])
        b = np.polyfit(g["r1"], g["ex"], 1)[0]
        res.append(dict(vol_tercile=k, n=len(g), rho=rho, p=p, slope_r1=b))
    out["z1 -> next 1d by vol tercile"] = pd.DataFrame(res)
    df["tr"] = np.where(df["r30"] > 0, "up30", "down30")
    res = []
    for k, g in df.dropna(subset=["r30"]).groupby("tr"):
        rho, p = stats.spearmanr(g["z1"], g["ex"]); res.append(dict(trend=k, n=len(g), rho=rho, p=p))
    out["z1 -> next 1d by 30d trend"] = pd.DataFrame(res)
    df["q"] = df.groupby("coin")["z1"].transform(lambda s: pd.qcut(s, 10, labels=False))
    out["z1 decile -> next 1d ex"] = df.groupby("q")["ex"].agg(["count", "mean"]).assign(
        t=df.groupby("q")["ex"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    return out
