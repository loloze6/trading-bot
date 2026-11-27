def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            n = len(b)
            r = c.pct_change()
            hi20 = c.rolling(20, min_periods=20).max()
            sd20 = r.rolling(20, min_periods=20).std()
            raw = ((c / hi20 - 1) / sd20).values
            sd30 = r.rolling(30, min_periods=30).std()
            agit = (sd30 > sd30.rolling(365, min_periods=100).median()).values
            reg = b["regime"].values
            f = b["forecast"].values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64").values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], reg=reg[i], raw=raw[i], day=day[i],
                                     up=r.values[i] > 0, ag=agit[i], fr=c.values[i + h] / c.values[i] - 1))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fr"].transform("mean")
    df["ex"] = df["fr"] - df["drift"]
    ch = df[(df.reg == "unknown") & df.raw.notna()].copy()

    def cl_t(s, x, y):
        s = s.dropna(subset=[x, y])
        X = s[x].values; Y = s[y].values
        Xm = X - X.mean(); b = (Xm * (Y - Y.mean())).sum() / (Xm ** 2).sum()
        a = Y.mean() - b * X.mean(); e = Y - a - b * X
        g = pd.Series(Xm * e).groupby(s["day"].values).sum().values
        G = len(g); N = len(s)
        v = (g ** 2).sum() / (Xm ** 2).sum() ** 2 * G / (G - 1) * (N - 1) / (N - 2)
        return pd.Series(dict(n=N, days=s["day"].nunique(), slope=b, t=b / np.sqrt(v)))

    out["choppy: ex on raw depth, by h (t clustered)"] = pd.DataFrame({h: cl_t(ch[ch.h == h], "raw", "ex") for h in H}).T.round(5)
    out["choppy signals: ex on forecast, by h"] = pd.DataFrame({h: cl_t(ch[(ch.h == h) & (ch.f < 0)], "f", "ex") for h in H}).T.round(5)
    c5 = ch[ch.h == 5]
    out["h5 raw by coin"] = c5.groupby("coin").apply(lambda s: cl_t(s, "raw", "ex")).round(4)
    out["h5 raw by up day"] = c5.groupby("up").apply(lambda s: cl_t(s, "raw", "ex")).round(4)
    out["h5 raw by agitated"] = c5.groupby("ag").apply(lambda s: cl_t(s, "raw", "ex")).round(4)
    c5 = c5.copy(); c5["half"] = np.where(c5.w.isin(["w7","w8","w9","w10","w11","w12"]), "B", "C")
    out["h5 raw by fold"] = c5.groupby("half").apply(lambda s: cl_t(s, "raw", "ex")).round(4)
    out["corr raw vs forecast (choppy, h1 grid)"] = float(ch[(ch.h == 1)][["raw", "f"]].corr().iloc[0, 1])
    c10 = ch[ch.h == 10].copy()
    out["h10 raw by coin"] = c10.groupby("coin").apply(lambda s: cl_t(s, "raw", "ex")).round(4)
    return out
