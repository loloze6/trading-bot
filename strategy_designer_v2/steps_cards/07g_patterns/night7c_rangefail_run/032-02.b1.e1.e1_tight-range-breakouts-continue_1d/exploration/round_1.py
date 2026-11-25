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
            hi60 = c.shift(1).rolling(60, min_periods=60).max()
            lo60 = c.shift(1).rolling(60, min_periods=60).min()
            mad = r1.abs().rolling(60, min_periods=60).mean()
            dist_hi = c / hi60 - 1
            dist_lo = c / lo60 - 1
            ret60 = c / c.shift(60) - 1
            ret20 = c / c.shift(20) - 1
            ret5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20, min_periods=20).std()
            vol60 = r1.rolling(60, min_periods=60).std()
            width = (hi60 / lo60 - 1) / mad
            fc = df["forecast"].astype(float).reset_index(drop=True)
            wd = pd.to_datetime(df["timestamp"]).dt.weekday.reset_index(drop=True)
            for h in (5, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i+h]/c[i]-1,
                        dist_hi=dist_hi[i], dist_lo=dist_lo[i], ret60=ret60[i], ret20=ret20[i],
                        ret5=ret5[i], volratio=vol20[i]/vol60[i] if vol60[i] else np.nan,
                        width=width[i], fc=fc[i], wd=wd[i], r1=r1[i],
                        zr1=r1[i]/mad[i] if mad[i] else np.nan))
    X = pd.DataFrame(rows)
    out = {}
    corr = []
    for h in (5, 20):
        s = X[X.h == h].copy()
        s["ex"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
        for f in ["dist_hi", "dist_lo", "ret60", "ret20", "ret5", "volratio", "width", "r1", "zr1"]:
            t = s[[f, "ex"]].dropna()
            if len(t) > 10:
                rho, p = stats.spearmanr(t[f], t["ex"])
                corr.append(dict(h=h, feat=f, n=len(t), rho=rho, t=rho*np.sqrt((len(t)-2)/(1-rho**2))))
    out["rank corr feature vs excess fwd"] = pd.DataFrame(corr)
    s = X[X.h == 20].copy()
    s["ex"] = s["fwd"] - s.groupby("coin")["fwd"].transform("mean")
    for f in ["ret60", "dist_hi", "volratio", "width"]:
        t = s[[f, "ex"]].dropna().copy()
        t["q"] = pd.qcut(t[f], 5, labels=False, duplicates="drop")
        g = t.groupby("q")["ex"].agg(["count", "mean", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["feat_mid"] = t.groupby("q")[f].median()
        out["h20 quintiles " + f] = g
    # breaks only: distance of break vs fwd
    b = s[s.dist_hi > 0][["dist_hi", "width", "ret60", "ex"]].dropna()
    out["h20 breaks n"] = len(b)
    if len(b) > 10:
        out["h20 breaks rho dist"] = float(stats.spearmanr(b.dist_hi, b.ex)[0])
        out["h20 breaks rho ret60"] = float(stats.spearmanr(b.ret60, b.ex)[0])
        out["h20 breaks mean ex"] = float(b.ex.mean())
    nb = s[(s.dist_hi <= 0)]["ex"].dropna()
    out["h20 nonbreak mean ex, n"] = f"{nb.mean():.4f}, {len(nb)}"
    # weekday on 5d
    s5 = X[X.h == 5].copy()
    s5["ex"] = s5["fwd"] - s5.groupby("coin")["fwd"].transform("mean")
    g = s5.groupby("wd")["ex"].agg(["count", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["h5 by weekday"] = g
    # book by window/coin
    d = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            d.append(dict(coin=coin, w=w, book=df["book_return"].mean()*365, coin_r=df["coin_return"].mean()*365))
    D = pd.DataFrame(d)
    out["book ann mean by window"] = D.groupby("w")[["book", "coin_r"]].mean()
    out["book ann mean by coin"] = D.groupby("coin")[["book", "coin_r"]].mean()
    return out
