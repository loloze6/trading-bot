def explore(data):
    import numpy as np, pandas as pd
    H = 14
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # normal drift per coin
        fr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                fr.append(c[i + H] / c[i] - 1)
        drift = np.mean(fr) if fr else np.nan
        sd = np.std(fr, ddof=1) if len(fr) > 2 else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            v = b["volume"]
            r1 = c.pct_change()
            vr = v.rolling(14).mean() / v.rolling(30).mean() - 1
            ret14 = c / c.shift(14) - 1
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            ret3 = c / c.shift(3) - 1
            dist_hi = c / c.rolling(30).max() - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(),
                                 year=ts.iloc[i].year,
                                 fwd=c.iloc[i + H] / c.iloc[i] - 1 - drift,
                                 fwdz=(c.iloc[i + H] / c.iloc[i] - 1 - drift) / sd,
                                 fc=b["forecast"].iloc[i], vr=vr.iloc[i],
                                 ret14=ret14.iloc[i], ret30=ret30.iloc[i], ret60=ret60.iloc[i],
                                 vol30=vol30.iloc[i], ret3=ret3.iloc[i], dhi=dist_hi.iloc[i]))
            # daily-level: next-day return after large daily moves
            nxt = r1.shift(-1)
            z = r1 / r1.rolling(30).std().shift(1)
            daily.append(pd.DataFrame(dict(coin=coin, z=z, nxt=nxt, r1=r1,
                                           wd=ts.dt.weekday, alloc=b["postRebalance_current_allocation"])))
    g = pd.DataFrame(rows)
    d = pd.concat(daily).dropna()

    def clust(df, col, y="fwd"):
        df = df.dropna(subset=[col, y])
        out = []
        df = df.copy()
        df["q"] = pd.qcut(df[col].rank(method="first"), 5, labels=False)
        for q, s in df.groupby("q"):
            pd_ = s.groupby("day")[y].sum()
            n = len(s)
            m = s[y].mean()
            se = np.sqrt((pd_ - pd_.index.map(lambda _: 0)).pow(2).sum()) / n if n else np.nan
            # cluster SE of mean: sqrt(sum_day (sum dev)^2)/n
            dev = (s[y] - m).groupby(s["day"]).sum()
            se = np.sqrt((dev ** 2).sum()) / n
            out.append(dict(q=q, lo=s[col].min(), hi=s[col].max(), n=n, days=s["day"].nunique(),
                            mean_fwd=m, t=m / se))
        return pd.DataFrame(out)

    def slope(df, x, y="fwdz"):
        df = df.dropna(subset=[x, y])
        X = (df[x] - df[x].mean()) / df[x].std()
        e = df[y] - df[y].mean()
        b = (X * e).sum() / (X ** 2).sum()
        res = e - b * X
        sc = (X * res).groupby(df["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(b=b, t=b / se, n=len(df), days=df["day"].nunique()))

    res = {}
    res["q_forecast"] = clust(g, "fc")
    res["q_ret14"] = clust(g, "ret14")
    res["q_ret30"] = clust(g, "ret30")
    res["q_ret60"] = clust(g, "ret60")
    res["q_vol30"] = clust(g, "vol30")
    res["q_dhi"] = clust(g, "dhi")
    sl = {k: slope(g, k) for k in ["fc", "vr", "ret14", "ret30", "ret60", "vol30", "ret3", "dhi"]}
    res["slopes_z_std"] = pd.DataFrame(sl).T
    # vr slope split by sign of ret14
    g["up14"] = g["ret14"] > 0
    res["vr_slope_by_ret14_sign"] = pd.DataFrame({str(k): slope(s, "vr") for k, s in g.groupby("up14")}).T
    # vr slope by vol tercile
    g["volt"] = pd.qcut(g["vol30"], 3, labels=["lowvol", "mid", "high"])
    res["vr_slope_by_vol"] = pd.DataFrame({str(k): slope(s, "vr") for k, s in g.groupby("volt")}).T
    res["vr_slope_by_year"] = pd.DataFrame({str(k): slope(s, "vr") for k, s in g.groupby("year")}).T
    # daily: next-day after big moves
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    res["nextday_by_z"] = d.groupby("zb")["nxt"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    res["by_weekday"] = d.groupby("wd")["nxt"].agg(["count", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    return res
