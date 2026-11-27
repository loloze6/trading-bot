def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        allr = [b["close"].values[1:]/b["close"].values[:-1]-1 for b in ws.values()]
        drift[coin] = np.nanmean(np.concatenate(allr))
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            h = b["high"].values.astype(float); l = b["low"].values.astype(float)
            rng = pd.Series(h-l)
            m20 = rng.rolling(20, min_periods=20).mean().values
            ratio = (h-l)/m20
            up = np.r_[np.nan, c[1:]/c[:-1]-1]
            tr60 = pd.Series(c).pct_change(60).values*100
            f = b["forecast"].values.astype(float)
            reg = b["regime"].astype(str).values
            n = len(c)
            for i in range(n-1):
                rows.append(dict(coin=coin, w=w, f=f[i], reg=reg[i], ratio=ratio[i], up=up[i], tr60=tr60[i],
                                 r1=c[i+1]/c[i]-1, r2=(c[i+2]/c[i]-1 if i+2<n else np.nan), d=drift[coin],
                                 ts=str(b["timestamp"].iloc[i])[:10], year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)
    def tday(s, keys):
        g = s.groupby(keys).sum(); n=len(g)
        return g.mean()/(g.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan
    def summ(sub, col="ex1"):
        sub = sub.dropna(subset=[col])
        return pd.Series(dict(n=len(sub), days=sub.ts.nunique(), mean=sub[col].mean(),
                              t_day=tday(sub[col], sub.ts) if len(sub)>2 else np.nan, hit=(sub[col]>0).mean()))
    sit = df[(df.up>0)&(df.ratio>1)&(df.tr60< -10)].copy()
    sit["ex1"] = -(sit.r1-sit.d); sit["ex2"] = -(sit.r2-2*sit.d)
    sit["inregime"] = np.where(sit.reg=="mean_reversion","agitated_regime","outside_regime")
    out = {}
    out["falling_by_regime"] = sit.groupby("inregime").apply(summ)
    out["falling_2d"] = summ(sit, "ex2")
    out["falling_by_year"] = sit.groupby("year").apply(summ)
    out["falling_by_window"] = sit.groupby("w").apply(summ)
    out["falling_by_coin"] = sit.groupby("coin").apply(summ)
    sit["rq"] = pd.qcut(sit.ratio.rank(method="first"), 5, labels=["q1","q2","q3","q4","q5"])
    out["falling_ratio_quintile"] = sit.groupby("rq").apply(summ)
    out["falling_ratio_mean_by_quintile"] = sit.groupby("rq").ratio.mean()
    out["falling_weighted_minus_mean"] = float((sit.ex1*sit.ratio).sum()/sit.ratio.sum() - sit.ex1.mean())
    out["falling_corr_ratio_ex1"] = float(sit[["ratio","ex1"]].corr().iloc[0,1])
    out_reg = sit[sit.inregime=="outside_regime"].copy()
    out_reg["rq"] = pd.qcut(out_reg.ratio.rank(method="first"), 3, labels=["narrow","mid","wide"])
    out["outside_regime_ratio_tercile"] = out_reg.groupby("rq").apply(summ)
    return out
