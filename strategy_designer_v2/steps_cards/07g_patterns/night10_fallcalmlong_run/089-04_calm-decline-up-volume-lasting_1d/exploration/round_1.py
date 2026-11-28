def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        allret = {5: [], 10: []}
        feats = []
        for w, df in ws.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"]; v = df["volume"]
            up = (c.diff() > 0).astype(float)
            f = pd.DataFrame(index=df.index)
            f["ret3"] = c / c.shift(3) - 1
            f["ret10"] = c / c.shift(10) - 1
            f["ret20"] = c / c.shift(20) - 1
            f["upvol20"] = (v * up).rolling(20).sum() / v.rolling(20).sum()
            f["upvol5"] = (v * up).rolling(5).sum() / v.rolling(5).sum()
            f["volratio5"] = v.rolling(5).mean() / v.rolling(60, min_periods=20).mean()
            f["clv"] = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            rng = (df["high"] - df["low"]) / c
            f["range_rel"] = rng.rolling(5).mean() / rng.rolling(60, min_periods=20).mean()
            f["dist_low20"] = c / df["low"].rolling(20).min() - 1
            f["dist_high20"] = c / df["high"].rolling(20).max() - 1
            lr = np.log(c).diff()
            f["vol10_60"] = lr.rolling(10).std() / lr.rolling(60, min_periods=20).std()
            f["updays20"] = up.rolling(20).mean()
            f["wd"] = pd.to_datetime(df["timestamp"]).dt.weekday
            f["fc"] = (df["regime"] == "unknown")
            f["coin"] = coin; f["w"] = w
            f["day"] = pd.to_datetime(df["timestamp"]).dt.floor("D")
            for h in (5, 10):
                g = np.arange(0, len(df) - h, h)
                fr = (c.shift(-h) / c - 1)
                allret[h].extend(fr.iloc[g].dropna().tolist())
                f["fwd%d" % h] = np.nan
                f.loc[g, "fwd%d" % h] = fr.iloc[g].values
            feats.append(f)
        F = pd.concat(feats, ignore_index=True)
        for h in (5, 10):
            F["ex%d" % h] = F["fwd%d" % h] - np.mean(allret[h])
        rows.append(F)
    A = pd.concat(rows, ignore_index=True)
    fc = A[A["fc"]]
    out["falling calm share of bars"] = float(A["fc"].mean())
    fl = ["ret3","ret10","ret20","upvol20","upvol5","volratio5","clv","range_rel","dist_low20","dist_high20","vol10_60","updays20"]
    for h in (10, 5):
        S = fc.dropna(subset=["ex%d" % h])
        res = []
        for x in fl:
            s = S.dropna(subset=[x]).copy()
            s["q"] = s.groupby("coin")[x].transform(lambda z: pd.qcut(z.rank(method="first"), 3, labels=False))
            hi = s[s.q == 2]["ex%d" % h]; lo = s[s.q == 0]["ex%d" % h]; md = s[s.q==1]["ex%d"%h]
            rho, p = stats.spearmanr(s[x], s["ex%d" % h])
            t = stats.ttest_ind(hi, lo, equal_var=False).statistic
            res.append([x, len(s), rho, p, lo.mean(), md.mean(), hi.mean(), t])
        out["fc tercile h%d" % h] = pd.DataFrame(res, columns=["feat","n","rho","p","lo","mid","hi","t_hi_lo"]).round(4)
    S = fc.dropna(subset=["ex10"])
    out["fc ex10 by coin"] = S.groupby("coin")["ex10"].agg(["count","mean"]).round(4)
    out["fc ex10 by window"] = S.groupby("w")["ex10"].agg(["count","mean"]).round(4)
    # daily next-day returns in fc, all bars
    D = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            d = pd.DataFrame({"r": c.pct_change(), "nx": c.shift(-1)/c-1, "fc": df["regime"]=="unknown",
                              "wd": pd.to_datetime(df["timestamp"]).dt.weekday})
            D.append(d)
    D = pd.concat(D).dropna()
    Dc = D[D.fc]
    out["fc next day by weekday"] = Dc.groupby("wd")["nx"].agg(["count","mean"]).round(4)
    Dc = Dc.copy(); Dc["q"] = pd.qcut(Dc["r"], 5, labels=False)
    g = Dc.groupby("q")["nx"].agg(["count","mean","std"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["fc next day by today's return quintile"] = g.round(4)
    return out
