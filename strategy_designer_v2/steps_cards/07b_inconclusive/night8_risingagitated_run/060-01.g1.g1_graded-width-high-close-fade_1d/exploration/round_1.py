def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        rets = []
        for w, df in ws.items():
            c = df["close"].values
            rets.append(c[1:] / c[:-1] - 1)
        r = np.concatenate(rets)
        drift[coin] = np.nanmean(r); usual[coin] = np.nanstd(r)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            rng = h - l
            cl = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            mr20 = pd.Series(rng / c).rolling(20, min_periods=20).mean().values
            wid = (rng / c) / mr20
            r1 = np.full(n, np.nan); r1[:-1] = c[1:] / c[:-1] - 1
            r3 = np.full(n, np.nan); r3[:-3] = c[3:] / c[:-3] - 1
            prev = np.full(n, np.nan); prev[1:] = c[1:] / c[:-1] - 1
            for i in range(n):
                f = df["forecast"].iloc[i]
                inprof = df["regime"].iloc[i] != "chop"
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                                 f=f, inprof=inprof, cl=cl[i], wid=wid[i],
                                 ex1=-(r1[i] - drift[coin]), ex3=-(r3[i] - 3 * drift[coin]),
                                 tot1=-r1[i], prev=prev[i], usual=usual[coin]))
    d = pd.DataFrame(rows)
    def summ(g, col="ex1"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series(dict(n=len(g), mean=np.nan, t=np.nan))
        s = g.groupby("day")[col].sum()
        m = g[col].mean()
        se = s.std(ddof=1) * np.sqrt(len(s)) / len(g)
        return pd.Series(dict(n=len(g), days=len(s), mean=m, t=m / se if se > 0 else np.nan))
    cases = d[d["f"] < 0].copy()
    out = {}
    out["all cases"] = summ(cases).to_frame().T
    out["all cases 3d"] = summ(cases, "ex3").to_frame().T
    out["by coin"] = cases.groupby("coin").apply(summ)
    out["by window"] = cases.groupby("w").apply(summ)
    out["by year"] = cases.groupby("year").apply(summ)
    cases["fq"] = pd.qcut(cases["f"].abs(), 4, labels=False, duplicates="drop")
    out["by |forecast| quartile"] = cases.groupby("fq").apply(summ)
    cases["clq"] = pd.cut(cases["cl"], [0.5, 0.625, 0.75, 0.875, 1.0001])
    out["by close location"] = cases.groupby("clq").apply(summ)
    cases["prevsign"] = np.sign(cases["prev"])
    out["by prior day sign"] = cases.groupby("prevsign").apply(summ)
    # profile, lower-half closes for comparison
    prof = d[d["inprof"] & d["f"].notna()]
    lower = prof[(prof["cl"] <= 0.5)]
    out["in-profile lower-half closes (short dir)"] = summ(lower).to_frame().T
    upp_prof = d[d["inprof"] & (d["cl"] > 0.5)]
    upp_prof = upp_prof.assign(wq=pd.qcut(upp_prof["wid"], 4, labels=False, duplicates="drop"))
    out["in-profile upper closes by width quartile"] = upp_prof.groupby("wq").apply(summ)
    out["n inprof bars"] = int(d["inprof"].sum())
    return out
