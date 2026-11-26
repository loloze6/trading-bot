def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    # coin drift over all windows (daily)
    rows = []
    drift = {}
    for coin, ws in bars.items():
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        drift[coin] = np.nanmean(np.concatenate(allr)) if allr else 0.0
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
            n = len(c)
            for i in range(n-1):
                fw = {k: (c[i+k]/c[i]-1 if i+k < n else np.nan) for k in (1,2,3,5)}
                rows.append(dict(coin=coin, w=w, i=i, f=f[i], ratio=ratio[i], up=up[i], tr60=tr60[i],
                                 r1=fw[1], r2=fw[2], r3=fw[3], r5=fw[5], d=drift[coin],
                                 ts=str(b["timestamp"].iloc[i])[:10],
                                 year=str(b["timestamp"].iloc[i])[:4]))
    df = pd.DataFrame(rows)
    out = {}
    cs = df[df.f <= -2].copy()
    cs["ex1"] = -(cs.r1 - cs.d)
    def tday(s, keys):
        g = s.groupby(keys).sum()
        n=len(g); return g.mean()/(g.std(ddof=1)/np.sqrt(n)) if n>2 else np.nan
    def summ(sub, col="ex1"):
        sub = sub.dropna(subset=[col])
        return pd.Series(dict(n=len(sub), days=sub.ts.nunique(), mean=sub[col].mean(),
                              t_day=tday(sub[col], sub.ts) if len(sub)>2 else np.nan,
                              hit=(sub[col]>0).mean()))
    out["all_cases_BC"] = summ(cs)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_window"] = cs.groupby("w").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    cs["fq"] = pd.qcut(cs.f.rank(method="first"), 3, labels=["strongest","mid","weakest"])
    out["by_forecast_tercile"] = cs.groupby("fq").apply(summ)
    cs["rq"] = pd.qcut(cs.ratio.rank(method="first"), 3, labels=["narrow","mid","wide"])
    out["by_ratio_tercile"] = cs.groupby("rq").apply(summ)
    cs["upq"] = pd.qcut(cs.up.rank(method="first"), 3, labels=["small_up","mid_up","big_up"])
    out["by_up_size_tercile"] = cs.groupby("upq").apply(summ)
    for k in (2,3,5):
        cs[f"ex{k}"] = -(cs[f"r{k}"] - k*cs.d)
        out[f"horizon_{k}d"] = summ(cs, f"ex{k}")
    # same situation in all trends (recomputed, no agitation), up day ratio>1
    sit = df[(df.up>0)&(df.ratio>1)].copy()
    sit["ex1"] = -(sit.r1-sit.d)
    sit["trend"] = np.where(sit.tr60< -10,"falling",np.where(sit.tr60>10,"rising","choppy"))
    out["situation_by_trend_allagit"] = sit.dropna(subset=["tr60"]).groupby("trend").apply(summ)
    sit["rq"] = pd.qcut(sit.ratio.rank(method="first"), 3, labels=["narrow","mid","wide"])
    fall = sit[sit.tr60< -10]
    out["falling_by_ratio_tercile"] = fall.groupby("rq").apply(summ)
    out["corr_ratio_ex1_cases"] = float(cs[["ratio","ex1"]].corr().iloc[0,1])
    return out
