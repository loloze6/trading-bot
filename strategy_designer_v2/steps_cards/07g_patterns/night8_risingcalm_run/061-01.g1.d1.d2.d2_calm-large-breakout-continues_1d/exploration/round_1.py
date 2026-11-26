def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            tr60 = c / c.shift(60) - 1
            hi20 = c.rolling(20, min_periods=20).max()
            dfh = c / hi20 - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for h in (1, 5):
                pass
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f10 = c.shift(-10) / c - 1
            n = len(b)
            for i in range(0, n, 5):
                rows.append(dict(coin=coin, w=w, z=z.iloc[i], r=r.iloc[i], f5=f5.iloc[i], f1=f1.iloc[i],
                                 f10=f10.iloc[i] if i % 10 == 0 else np.nan,
                                 tr60=tr60.iloc[i], dfh=dfh.iloc[i], clv=clv.iloc[i], sd=sd.iloc[i],
                                 regime=b["regime"].iloc[i], wd=ts.iloc[i].dayofweek,
                                 sdq=np.nan))
    df = pd.DataFrame(rows)
    # coin drift on the grid
    drift = df.groupby("coin")["f5"].mean()
    usual = df.groupby("coin")["f5"].std()
    df["x5"] = df["f5"] - df["coin"].map(drift)
    df["s5"] = df["x5"] / df["coin"].map(usual)
    d1 = df.groupby("coin")["f1"].mean()
    df["x1"] = df["f1"] - df["coin"].map(d1)
    df["inprof"] = np.where(df["regime"] == "chop", "out", "in")
    df["trend"] = pd.cut(df["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    df["zb"] = pd.cut(df["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    def summ(g, col="x5"):
        g = g.dropna(subset=[col])
        m = g[col].mean(); s = g[col].std(); n = len(g)
        return pd.Series(dict(n=n, mean=m, t=m / (s / np.sqrt(n)) if n > 2 else np.nan))
    out = {}
    out["by z bucket, all"] = df.groupby("zb").apply(summ)
    out["by z bucket, in profile"] = df[df.inprof == "in"].groupby("zb").apply(summ)
    out["by z bucket x trend"] = df.groupby(["trend", "zb"]).apply(summ)
    out["by z bucket next day"] = df.groupby("zb").apply(lambda g: summ(g, "x1"))
    # slope of standardized excess on z, by trend
    sl = []
    for k, g in df.dropna(subset=["z", "s5", "trend"]).groupby("trend"):
        res = stats.linregress(g["z"], g["s5"]); sl.append(dict(trend=k, n=len(g), slope=res.slope, t=res.slope / res.stderr))
    g = df.dropna(subset=["z", "s5"]); res = stats.linregress(g["z"], g["s5"])
    sl.append(dict(trend="all", n=len(g), slope=res.slope, t=res.slope / res.stderr))
    out["slope s5 on z by trend"] = pd.DataFrame(sl)
    out["by weekday"] = df.groupby("wd").apply(summ)
    df["dfhb"] = pd.cut(df["dfh"], [-1, -0.3, -0.15, -0.05, -0.0001, 0.01])
    out["by dist from 20d high"] = df.groupby("dfhb").apply(summ)
    df["clvb"] = pd.cut(df["clv"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["by close location"] = df.groupby("clvb").apply(summ)
    df["tr60b"] = pd.cut(df["tr60"], [-10, -0.4, -0.2, -0.1, 0, 0.1, 0.3, 0.6, 10])
    out["by 60d trend"] = df.groupby("tr60b").apply(summ)
    out["by year"] = df.assign(y=df["w"]).groupby("w").apply(summ)
    # book: worst/best days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    out["book days"] = pd.Series(dict(n=len(D), mean=D["book_return"].mean(), std=D["book_return"].std(),
                                      share_nonzero=(D["book_return"].abs() > 1e-9).mean()))
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
