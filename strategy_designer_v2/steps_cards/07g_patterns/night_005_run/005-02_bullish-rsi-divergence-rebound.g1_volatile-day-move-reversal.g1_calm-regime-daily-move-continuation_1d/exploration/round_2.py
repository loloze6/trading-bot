def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    rows = []
    for H in [5, 10]:
        for c in coins:
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"].values; n = len(b)
                r1 = b["close"].pct_change()
                absm = r1.abs().rolling(60, min_periods=30).mean()
                vol20 = r1.rolling(20, min_periods=15).std()
                vrank = vol20.rolling(100, min_periods=50).rank(pct=True)
                r5p = b["close"].pct_change(5)
                for i in range(0, n - H, H):
                    rows.append(dict(H=H, coin=c, w=w, f=b["forecast"].iloc[i],
                                     r1=r1.iloc[i], sm=r1.iloc[i] / absm.iloc[i] if absm.iloc[i] else np.nan,
                                     vr=vrank.iloc[i], r5p=r5p.iloc[i] / (absm.iloc[i] * np.sqrt(5)) if absm.iloc[i] else np.nan,
                                     fwd=cl[i + H] / cl[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby(["H", "coin"])["fwd"].transform("mean")
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    g["vrq"] = pd.qcut(g["vr"], 3, labels=["lowvol", "mid", "highvol"])
    g["up"] = np.where(g["r1"] > 0, "up", "down")
    g["big"] = g["sm"].abs() > g.groupby("H")["sm"].transform(lambda s: s.abs().quantile(0.6))
    out["H5 excess by vol tercile x up/down, big moves only"] = g[(g.H == 5) & g.big].groupby(["vrq", "up"])["ex"].apply(tt).unstack()
    out["H10 excess by vol tercile x up/down, big moves only"] = g[(g.H == 10) & g.big].groupby(["vrq", "up"])["ex"].apply(tt).unstack()
    # graded slope: fwd excess on scaled move, by vol tercile (H5)
    res = {}
    for H in [5, 10]:
        for v in ["lowvol", "mid", "highvol"]:
            s = g[(g.H == H) & (g.vrq == v)].dropna(subset=["sm", "ex"])
            lr = stats.linregress(s["sm"], s["ex"])
            res[f"H{H}_{v}"] = dict(n=len(s), slope=lr.slope, t=lr.slope / lr.stderr)
    out["slope of excess on signed scaled move"] = pd.DataFrame(res).T
    # 5-day past return (scaled) vs next
    res = {}
    for H in [5, 10]:
        for v in ["lowvol", "mid", "highvol"]:
            s = g[(g.H == H) & (g.vrq == v)].dropna(subset=["r5p", "ex"])
            lr = stats.linregress(s["r5p"], s["ex"])
            res[f"H{H}_{v}"] = dict(n=len(s), slope=lr.slope, t=lr.slope / lr.stderr)
    out["slope of excess on scaled 5d past return"] = pd.DataFrame(res).T
    # per coin, per signed forecast quintile H5
    s = g[g.H == 5].copy()
    s["fq"] = s.groupby("coin")["f"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["H5 excess by coin x forecast quintile (mean)"] = s.groupby(["coin", "fq"])["ex"].mean().unstack()
    out["H5 excess, f<0 vs f>0 vs f==0"] = s.groupby(np.sign(s["f"]))["ex"].apply(tt).unstack()
    # weekday by coin, daily returns (all days)
    D = pd.concat([days[c][w].assign(coin=c, w=w) for c in coins for w in days[c]])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["ex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["daily coin excess by weekday"] = D.groupby("wd")["ex"].apply(tt).unstack()
    D["y"] = pd.to_datetime(D["day"]).dt.year
    out["daily coin excess Monday by year"] = D[D.wd == 0].groupby("y")["ex"].apply(tt).unstack()
    out["daily coin excess Wednesday by year"] = D[D.wd == 2].groupby("y")["ex"].apply(tt).unstack()
    # book's largest days: coin return next 5 days after top/bottom 5% book days
    D = D.sort_values(["coin", "w", "day"])
    D["next5"] = D.groupby(["coin", "w"])["coin_return"].transform(lambda x: (1 + x).rolling(5).apply(np.prod, raw=True).shift(-5) - 1)
    D["next5ex"] = D["next5"] - D.groupby("coin")["next5"].transform("mean")
    q = D["book_return"].quantile([0.05, 0.95])
    D["bk"] = np.where(D.book_return <= q.iloc[0], "worst5%", np.where(D.book_return >= q.iloc[1], "best5%", "mid"))
    out["coin next-5d excess after book's extreme days"] = D.groupby("bk")["next5ex"].apply(tt).unstack()
    return out
