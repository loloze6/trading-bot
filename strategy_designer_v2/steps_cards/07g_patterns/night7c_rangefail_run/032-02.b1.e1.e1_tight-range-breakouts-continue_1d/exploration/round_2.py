def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r1 = c.pct_change()
            feats = {}
            for L in (20, 30, 60):
                feats[f"dh{L}"] = c / c.shift(1).rolling(L, min_periods=L).max() - 1
            mad20 = r1.abs().rolling(20, min_periods=20).mean()
            feats["dh20z"] = feats["dh20"] / mad20
            feats["zr1_20"] = r1 / mad20
            alloc = df["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    d = dict(coin=coin, w=w, h=h, fwd=c[i+h]/c[i]-1, inpos=float(alloc[i] != 0))
                    for k, v in feats.items():
                        d[k] = v[i]
                    rows.append(d)
    X = pd.DataFrame(rows)
    X["ex"] = X["fwd"] - X.groupby(["coin", "h"])["fwd"].transform("mean")
    out = {}
    corr = []
    for h in (5, 10, 20):
        s = X[X.h == h]
        for f in ["dh20", "dh30", "dh60", "dh20z", "zr1_20"]:
            t = s[[f, "ex"]].dropna()
            rho = stats.spearmanr(t[f], t["ex"])[0]
            corr.append(dict(h=h, feat=f, n=len(t), rho=rho, t=rho*np.sqrt((len(t)-2)/(1-rho**2))))
    out["rank corr"] = pd.DataFrame(corr)
    s = X[X.h == 10][["dh20", "ex", "w", "coin", "inpos"]].dropna().copy()
    s["q"] = pd.qcut(s["dh20"], 5, labels=False)
    g = s.groupby("q")["ex"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["mid"] = s.groupby("q")["dh20"].median()
    out["h10 quintiles dh20"] = g
    def rr(t):
        if len(t) < 8: return np.nan
        return stats.spearmanr(t["dh20"], t["ex"])[0]
    out["h10 rho dh20 by coin"] = s.groupby("coin").apply(rr)
    out["h10 rho dh20 by window"] = s.groupby("w").apply(rr)
    # exclude bars in position (not explained by the idea)
    so = s[s.inpos == 0]
    rho = stats.spearmanr(so.dh20, so.ex)[0]
    out["h10 rho dh20 out of position, n"] = f"{rho:.3f}, {len(so)}"
    # weekday on 5d with 20-bar-aligned bars: daily next-day return by weekday
    dd = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            wd = pd.to_datetime(df["timestamp"]).dt.weekday.reset_index(drop=True)
            nr = c.shift(-1)/c - 1
            dd.append(pd.DataFrame(dict(wd=wd, nr=nr, coin=coin)))
    D = pd.concat(dd).dropna()
    D["ex"] = D["nr"] - D.groupby("coin")["nr"].transform("mean")
    g = D.groupby("wd")["ex"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["next-day ex by weekday of close"] = g
    return out
