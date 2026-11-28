def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [2, 3, 5, 7]
    recs = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rr), np.std(rr, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(30).std()
            s3 = (c / c.shift(3) - 1) / (vol * np.sqrt(3))
            s7 = (c / c.shift(7) - 1) / (vol * np.sqrt(7))
            z = (s3 - s3.rolling(60, min_periods=20).mean()) / s3.rolling(60, min_periods=20).std()
            r60 = c / c.shift(60) - 1
            inprof = (b["regime"] == "unknown").values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for h in H:
                d, sd = drift[(coin, h)]
                for i in range(0, len(c) - h, h):
                    if np.isnan(s3.iloc[i]) or not inprof[i]: continue
                    f = c.iloc[i + h] / c.iloc[i] - 1
                    recs.append(dict(coin=coin, w=w, h=h, s3=s3.iloc[i], s7=s7.iloc[i], z=z.iloc[i],
                                     r60=r60.iloc[i], day=day[i],
                                     su=-(f - d), st=-f, stren=-(f - d) / sd))
    df = pd.DataFrame(recs)

    def summ(g):
        x = g["su"]
        dd = g.groupby("day")["su"].sum()
        t = x.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)) if len(dd) > 2 else np.nan
        return pd.Series(dict(n=len(x), days=len(dd), mean_su=x.mean(), t=t,
                              mean_st=g["st"].mean(), stren=g["stren"].mean()))
    out = {}
    falls = df[df.s3 < 0].copy()
    out["falls_by_h"] = falls.groupby("h").apply(summ)
    falls["zbin"] = pd.cut(falls["z"], [-np.inf, -2, -1, 0, np.inf])
    out["falls_by_h_zbin"] = falls.groupby(["h", "zbin"]).apply(summ)
    out["falls_by_h_s3_tercile"] = falls.groupby(["h", pd.qcut(falls["s3"], 3, labels=["big", "mid", "small"])]).apply(summ)
    f7 = df[df.s7 < 0].copy()
    out["s7falls_by_h_tercile"] = f7.groupby(["h", pd.qcut(f7["s7"], 3, labels=["big", "mid", "small"])]).apply(summ)
    falls["trend"] = pd.cut(falls["r60"], [-np.inf, -0.3, -0.2, -0.1])
    out["falls_h3_by_trend"] = falls[falls.h == 3].groupby("trend").apply(summ)
    out["falls_h3_by_window"] = falls[falls.h == 3].groupby("w").apply(summ)
    cor = {}
    for h in H:
        q = falls[falls.h == h]
        cor[f"h{h}_rho_s3_su"] = stats.spearmanr(-q["s3"], q["su"])[0]
        cor[f"h{h}_rho_z_su"] = stats.spearmanr(-q["z"].fillna(0), q["su"])[0]
    out["grade_rho"] = pd.Series(cor)
    return out
