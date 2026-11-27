def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); n = len(b)
            r1 = c / c.shift(1) - 1
            r60 = c / c.shift(60) - 1
            r7b = c / c.shift(7) - 1
            sd30 = r1.rolling(30).std()
            ag = sd30 / sd30.expanding(30).median()
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            clpos = (b["close"] - b["low"]) / hl
            rng = hl / c
            rngz = rng / rng.rolling(30).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            for H in (1, 3, 7):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n, H):
                    rows.append(dict(H=H, coin=coin, w=w, clpos=clpos.iloc[i], rng=rng.iloc[i], rngz=rngz.iloc[i],
                                     r1=r1.iloc[i], r7b=r7b.iloc[i], r60=r60.iloc[i], ag=ag.iloc[i], fwd=fwd.iloc[i],
                                     wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year, day=ts.iloc[i].floor("D")))
    df = pd.DataFrame(rows).dropna(subset=["fwd", "clpos"])
    df["ex"] = df["fwd"] - df.groupby(["H", "coin"])["fwd"].transform("mean")
    df["cq"] = pd.qcut(df["clpos"], 5, labels=False)
    df["s"] = df["clpos"] - 0.5
    df["trend"] = np.where(df.r60 > 0.1, "rising", np.where(df.r60 < -0.1, "falling", np.where(df.r60.isna(), "na", "choppy")))
    df["agit"] = np.where(df.ag > 1, "agit", np.where(df.ag.isna(), "na", "calm"))
    out = {}
    def tday(g):
        s = g.groupby("day")["ex"].sum(); nd = len(s)
        m = g["ex"].mean(); se = np.sqrt((s - s.mean()*0 - g.groupby("day")["ex"].size()*m).pow(2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=nd, ex=m, t=m / se if se > 0 else np.nan))
    out["ex by clpos quintile and H"] = df.groupby(["H", "cq"]).apply(tday).unstack(0)
    d7 = df[df.H == 7]
    # signed (clpos-0.5) x ex: graded slope
    def slope(g):
        g = g.dropna(subset=["s", "ex"])
        if len(g) < 15: return pd.Series(dict(n=len(g), rho=np.nan, top_minus_bot=np.nan))
        rho = stats.spearmanr(g["s"], g["ex"])[0]
        tb = g[g.s > 0.3]["ex"].mean() - g[g.s < -0.3]["ex"].mean()
        return pd.Series(dict(n=len(g), rho=rho, top_minus_bot=tb))
    out["7d clpos slope by window"] = d7.groupby("w").apply(slope)
    out["7d clpos slope by year"] = d7.groupby("yr").apply(slope)
    out["7d clpos slope by coin"] = d7.groupby("coin").apply(slope)
    out["7d clpos slope by trend x agit"] = d7.groupby(["trend", "agit"]).apply(slope)
    out["7d clpos slope by day sign"] = d7.assign(up=d7.r1 > 0).groupby("up").apply(slope)
    d7 = d7.copy(); d7["rq"] = pd.qcut(d7["rngz"], 3, labels=False)
    out["7d ex clpos tercile x range tercile"] = d7.assign(ct=pd.qcut(d7.clpos, 3, labels=False)).groupby(["rq", "ct"])["ex"].agg(["count", "mean"]).unstack()
    out["7d ex by rngz quintile"] = d7.dropna(subset=["rngz"]).assign(q=lambda x: pd.qcut(x.rngz, 5, labels=False)).groupby("q").apply(tday)
    out["7d rngz slope by trend"] = d7.dropna(subset=["rngz"]).groupby("trend").apply(lambda g: pd.Series(dict(n=len(g), rho=stats.spearmanr(g.rngz, g.ex)[0])))
    # weekday on 1d, demeaned
    d1 = df[df.H == 1]
    out["1d ex by weekday"] = d1.groupby("wd").apply(tday)
    out["1d weekday mean by year (ex)"] = d1.groupby(["yr", "wd"])["ex"].mean().unstack()
    return out
