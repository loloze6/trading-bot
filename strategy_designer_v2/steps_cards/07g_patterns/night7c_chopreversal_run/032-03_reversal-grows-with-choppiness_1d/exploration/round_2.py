import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []; g7 = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); r = c.pct_change()
            std30 = r.rolling(30, min_periods=20).std()
            vr = std30 / r.rolling(90, min_periods=60).std()
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            ret7 = c / c.shift(7) - 1
            fwd7 = c.shift(-7) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(len(df) - 1):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), wd=ts.iloc[i].dayofweek,
                                 yr=ts.iloc[i].year, fwd1=fwd1.iloc[i],
                                 z1=r.iloc[i] / std30.iloc[i] if std30.iloc[i] > 0 else np.nan,
                                 vr=vr.iloc[i], std30=std30.iloc[i]))
            for i in range(0, len(df), 7):
                if i + 7 >= len(df): break
                g7.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), fwd7=fwd7.iloc[i],
                               s7=ret7.iloc[i] / (std30.iloc[i] * np.sqrt(7)) if std30.iloc[i] > 0 else np.nan,
                               vr=vr.iloc[i], std30=std30.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd1"])
    d["ex"] = d["fwd1"] - d.groupby("coin")["fwd1"].transform("mean")
    d["exs"] = d["ex"] / d["std30"]

    def ct(sub, y):
        s = sub.dropna(subset=[y]).groupby("day")[y].sum()
        n = sub[y].notna().sum()
        m = sub[y].mean()
        dev = (sub[y] - m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum()) / n
        return pd.Series(dict(mean=m, t=m / se, n=n, days=len(dev)))

    def slope(sub, x, y):
        sub = sub.dropna(subset=[x, y])
        if len(sub) < 30: return pd.Series(dict(b=np.nan, t=np.nan, n=len(sub)))
        X = sub[x] - sub[x].mean(); b = (X * sub[y]).sum() / (X**2).sum()
        e = sub[y] - sub[y].mean() - b * X
        sc = (X * e).groupby(sub["day"]).sum(); G = len(sc)
        se = np.sqrt((sc**2).sum() * G / (G - 1)) / (X**2).sum()
        return pd.Series(dict(b=b, t=b / se, n=len(sub)))

    out = {}
    out["weekday next-day excess, day-clustered"] = d.groupby("wd").apply(lambda s: ct(s, "ex"))
    out["weekday Thu+Fri by window"] = d[d.wd.isin([3, 4])].groupby("w").apply(lambda s: ct(s, "ex"))
    out["weekday Thu+Fri by coin"] = d[d.wd.isin([3, 4])].groupby("coin").apply(lambda s: ct(s, "ex"))
    d["zb"] = pd.qcut(d["z1"], 5, labels=False)
    out["next-day excess by z1 quintile clustered"] = d.groupby("zb").apply(lambda s: ct(s, "ex"))
    d["negz"] = d["z1"].clip(upper=0)
    out["slope next-day scaled on down-day size, by window"] = d.groupby("w").apply(lambda s: slope(s, "negz", "exs"))
    out["slope down-day pooled"] = slope(d, "negz", "exs")
    d["vq"] = pd.qcut(d["vr"], 3, labels=["lo", "mid", "hi"])
    out["slope down-day by vol ratio"] = d.groupby("vq").apply(lambda s: slope(s, "negz", "exs"))
    out["slope down-day by coin"] = d.groupby("coin").apply(lambda s: slope(s, "negz", "exs"))
    g = pd.DataFrame(g7)
    g["ex"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    g["exs"] = g["ex"] / (g["std30"] * np.sqrt(7))
    g["vq"] = pd.qcut(g["vr"], 3, labels=["lo", "mid", "hi"])
    out["s7 continuation by vol ratio"] = g.groupby("vq").apply(lambda s: slope(s, "s7", "exs"))
    out["s7 continuation by coin"] = g.groupby("coin").apply(lambda s: slope(s, "s7", "exs"))
    g["pos"] = g["s7"].clip(lower=0); g["neg"] = g["s7"].clip(upper=0)
    out["s7 up part"] = slope(g, "pos", "exs"); out["s7 down part"] = slope(g, "neg", "exs")
    return out
