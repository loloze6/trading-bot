def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            sdmed = sd.expanding(min_periods=40).median()
            hi20 = c.rolling(20, min_periods=20).max()
            dfh = c / hi20 - 1
            tr60 = c / c.shift(60) - 1
            r10 = c / c.shift(10) - 1
            z10 = r10 / (sd * np.sqrt(10))
            ts = pd.to_datetime(b["timestamp"])
            f5 = c.shift(-5) / c - 1
            for i in range(0, len(b), 5):
                if np.isnan(sdmed.iloc[i]): ag = np.nan
                else: ag = "agit" if sd.iloc[i] > sdmed.iloc[i] else "calm"
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]), day=ts.iloc[i].normalize(), z=z.iloc[i],
                                 z10=z10.iloc[i], f5=f5.iloc[i], dfh=dfh.iloc[i], tr60=tr60.iloc[i], agit=ag,
                                 wd=ts.iloc[i].dayofweek))
    df = pd.DataFrame(rows)
    dr = df.groupby("coin")["f5"].mean(); us = df.groupby("coin")["f5"].std()
    df["x5"] = df["f5"] - df["coin"].map(dr); df["s5"] = df["x5"] / df["coin"].map(us)
    df["half"] = np.where(df.wn <= 12, "w7-w12", "w13-w18")
    df["trend"] = pd.cut(df["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    def cl(g, x, y="s5"):
        g = g.dropna(subset=[x, y])
        if len(g) < 20: return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t=np.nan))
        X = np.c_[np.ones(len(g)), g[x].values]; Y = g[y].values
        bet = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ bet
        XtXi = np.linalg.inv(X.T @ X); meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        G = g["day"].nunique(); k = (G / (G - 1)) * ((len(g) - 1) / (len(g) - 2))
        V = XtXi @ meat @ XtXi * k
        return pd.Series(dict(n=len(g), days=G, slope=bet[1], t=bet[1] / np.sqrt(V[1, 1])))
    def clmean(g, y="x5"):
        g = g.dropna(subset=[y]); dev = g[y] - g[y].mean()
        s = dev.groupby(g["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean=g[y].mean(), t=g[y].mean() / se))
    calm = df[df.agit == "calm"]; ag = df[df.agit == "agit"]
    out = {}
    out["calm up-day z slope"] = cl(calm[calm.z > 0], "z")
    out["agit up-day z slope"] = cl(ag[ag.z > 0], "z")
    out["calm down-day z slope"] = cl(calm[calm.z < 0], "z")
    out["calm z slope by half"] = calm.groupby("half").apply(lambda g: cl(g, "z"))
    out["calm z slope by trend"] = calm.groupby("trend").apply(lambda g: cl(g, "z"))
    out["calm up z slope by half"] = calm[calm.z > 0].groupby("half").apply(lambda g: cl(g, "z"))
    out["calm z10 slope"] = cl(calm, "z10")
    out["agit z10 slope"] = cl(ag, "z10")
    out["calm z10 slope by half"] = calm.groupby("half").apply(lambda g: cl(g, "z10"))
    out["calm dfh slope by half"] = calm.groupby("half").apply(lambda g: cl(g, "dfh"))
    df["athigh"] = np.where(df.dfh >= -0.0001, "at", "below")
    out["at-high x5 clustered"] = df[df.athigh == "at"].groupby("half").apply(clmean)
    out["weekday x5 clustered by half"] = df.groupby(["wd", "half"]).apply(clmean).unstack()["t"]
    return out
