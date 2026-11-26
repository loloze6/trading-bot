def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    def gm(coin, h):
        v = []
        for w, b in bars[coin].items():
            c = b["close"].values
            for i in range(0, len(c) - h, h):
                v.append(c[i + h] / c[i] - 1)
        return np.mean(v)
    def clus_t(x, y, d):
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtX = np.linalg.inv(X.T @ X)
        df = pd.DataFrame({"d": d, "a": e, "b": e * x})
        S = df.groupby("d")[["a", "b"]].sum().values
        V = XtX @ (S.T @ S) @ XtX
        return beta[1], beta[1] / np.sqrt(V[1, 1])
    def mean_t(y, d):
        df = pd.DataFrame({"d": d, "y": y - y.mean()})
        s = df.groupby("d")["y"].sum().values
        return y.mean(), y.mean() / (np.sqrt((s ** 2).sum()) / len(y))
    recs = []
    for h in (1, 2, 3, 5):
        for coin in bars:
            g = gm(coin, h)
            for w, b in bars[coin].items():
                b = b.reset_index(drop=True)
                c = b["close"]; r = c.pct_change()
                sd = r.rolling(20).std()
                sma = c.rolling(20).mean()
                st = (c - sma) / (sma * sd)
                z1 = r / sd
                rngz = ((b["high"] - b["low"]) / c) / sd
                pc = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
                tr = c / c.shift(60) - 1
                ag = (b["regime"] == "chop").astype(int)
                day = pd.to_datetime(b["timestamp"]).dt.floor("D").astype("int64")
                cv = c.values
                for i in range(0, len(cv) - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, st=st.iloc[i], z1=z1.iloc[i], rngz=rngz.iloc[i],
                                     pc=pc.iloc[i], tr=tr.iloc[i], ag=ag.iloc[i], day=day.iloc[i],
                                     y=cv[i + h] / cv[i] - 1 - g))
    D = pd.DataFrame(recs).replace([np.inf, -np.inf], np.nan)
    D["trend"] = np.where(D.tr > 0.1, "rising", np.where(D.tr < -0.1, "falling", np.where(D.tr.notna(), "choppy", "na")))
    out = {}
    res = []
    for h in (1, 2, 3, 5):
        g = D[(D.h == h) & (D.ag == 1) & (D.trend == "falling")].dropna(subset=["z1"])
        up = g[g.z1 > 0]
        if len(up) > 40:
            s, t = clus_t(up.z1.values, up.y.values, up.day.values)
            m, mt = mean_t(up.y.values, up.day.values)
            wpos = (up.groupby("w").y.mean() < 0).mean()
            res.append(dict(h=h, n=len(up), slope=round(s, 5), t=round(t, 2), mean=round(m, 4), mean_t=round(mt, 2), share_windows_neg=round(wpos, 2)))
    out["falling_agit_upday_fade"] = pd.DataFrame(res)
    res = []
    for h in (1, 2):
        for ag in (0, 1):
            g = D[(D.h == h) & (D.ag == ag)].dropna(subset=["rngz", "pc"])
            for var in ["rngz", "pc"]:
                s, t = clus_t(g[var].values, g.y.values, g.day.values)
                res.append(dict(h=h, ag=ag, var=var, n=len(g), slope=round(s, 5), t=round(t, 2)))
    out["range_close_clustered"] = pd.DataFrame(res)
    res = []
    for h in (2, 3, 5):
        g = D[(D.h == h) & (D.ag == 0)].dropna(subset=["st"])
        for trd in ["rising", "choppy", "falling"]:
            gg = g[g.trend == trd]
            s, t = clus_t(gg.st.values, gg.y.values, gg.day.values)
            res.append(dict(h=h, trend=trd, n=len(gg), slope=round(s, 5), t=round(t, 2),
                            win_pos=round((gg.groupby("w").apply(lambda x: np.corrcoef(x.st, x.y)[0, 1] if len(x) > 5 else np.nan) > 0).mean(), 2)))
    out["calm_stretch_trend_h"] = pd.DataFrame(res)
    return out
