def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    ev = []; base = []; allbars = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; l = b["low"].values; h = b["high"].values; o = b["open"].values
            n = len(b)
            # baseline grid
            for i in range(0, n - H, H):
                base.append((coin, w, c[i + H] / c[i] - 1))
            ts = pd.to_datetime(b["timestamp"])
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol20 = pd.Series(r1).rolling(20).std().values
            volmed = pd.Series(vol20).expanding(20).median().values
            for i in range(n):
                fwd = c[i + H] / c[i] - 1 if i + H < n else np.nan
                fwd1 = c[i + 1] / c[i] - 1 if i + 1 < n else np.nan
                p30 = np.nanmin(l[i - 30:i]) if i >= 30 else np.nan
                ret60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                ret20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                rng = (h[i] - l[i]) / c[i]
                cl = (c[i] - l[i]) / (h[i] - l[i]) if h[i] > l[i] else np.nan
                allbars.append(dict(coin=coin, w=w, i=i, cell=i // H, fwd=fwd, fwd1=fwd1, r1=r1[i],
                                    ret60=ret60, ret20=ret20, rng=rng, cl=cl,
                                    hiv=(vol20[i] > volmed[i]) if not np.isnan(vol20[i]) else np.nan,
                                    wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                    rec=(l[i] < p30 and c[i] >= p30) if not np.isnan(p30) else False,
                                    brk=(c[i] < p30) if not np.isnan(p30) else False,
                                    depth=(p30 - l[i]) / c[i] if not np.isnan(p30) else np.nan,
                                    fc=b["forecast"].iloc[i], pos=b["postRebalance_current_allocation"].iloc[i]))
    B = pd.DataFrame(allbars)
    drift = pd.DataFrame(base, columns=["coin", "w", "r"]).groupby("coin")["r"].mean()
    usual = pd.DataFrame(base, columns=["coin", "w", "r"]).groupby("coin")["r"].std()
    B["ab"] = B["fwd"] - B["coin"].map(drift)
    B["str"] = B["ab"] / B["coin"].map(usual)
    def summ(df):
        d = df.dropna(subset=["ab"]).drop_duplicates(["coin", "w", "cell"])
        if len(d) < 3: return pd.Series(dict(n=len(d), mean=np.nan, t=np.nan, strength=np.nan))
        return pd.Series(dict(n=len(d), mean=d["ab"].mean(), t=d["ab"].mean() / (d["ab"].std() / np.sqrt(len(d))),
                              strength=d["str"].mean()))
    out = {}
    R = B[B.rec]
    out["reclaim all"] = summ(R)
    R2 = R.copy(); R2["r60g"] = pd.cut(R2["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["reclaim by 60d trend"] = R2.groupby("r60g").apply(summ)
    R2["dq"] = pd.qcut(R2["depth"], 3, labels=["shallow", "mid", "deep"])
    out["reclaim by depth"] = R2.groupby("dq").apply(summ)
    R2["clq"] = pd.qcut(R2["cl"], 3, labels=["lowclose", "midclose", "highclose"])
    out["reclaim by close loc"] = R2.groupby("clq").apply(summ)
    out["reclaim by hivol"] = R2.groupby("hiv").apply(summ)
    out["closed below low (break)"] = summ(B[B.brk])
    Bb = B[B.brk].copy(); Bb["r60g"] = pd.cut(Bb["ret60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["break by 60d trend"] = Bb.groupby("r60g").apply(summ)
    A = B.copy()
    A["r1q"] = pd.qcut(A["r1"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["all by 1d ret quintile"] = A.groupby("r1q").apply(summ)
    A["r20q"] = pd.qcut(A["ret20"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["all by 20d ret quintile"] = A.groupby("r20q").apply(summ)
    A["rngq"] = pd.qcut(A["rng"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    out["all by range quintile"] = A.groupby("rngq").apply(summ)
    out["next-day ret by weekday"] = B.groupby("wd")["fwd1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(x.count())])
    out["all by year"] = B.groupby("yr").apply(summ)
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    out["book days"] = pd.Series(dict(n=len(D), mean=D["book_return"].mean(), share_nonzero=(D["book_return"].abs() > 1e-9).mean()))
    T = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by window"] = T.groupby("w")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
