def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [7, 14, 21, 28]
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            inprof = (df["regime"] == "unknown").values
            fc = df["forecast"].values
            s = pd.Series(c)
            r7 = s.pct_change(7)
            ma = r7.abs().rolling(30).mean()
            scaled = (r7 / ma).values
            hi30 = s.rolling(30).max()
            dist = ((hi30 - s) / hi30 * 100).values
            yr = df["timestamp"].astype(str).str[:4].values
            for h in H:
                for i in range(0, n - h, h):
                    recs.append(dict(coin=coin, w=w, h=h, i=i, day=str(df["timestamp"].iloc[i])[:10], yr=yr[i],
                                     ret=c[i + h] / c[i] - 1, prof=inprof[i], fc=fc[i],
                                     scaled=scaled[i], dist=dist[i]))
    R = pd.DataFrame(recs)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["drift"]

    def tday(sub, col="ex"):
        if len(sub) < 3: return np.nan
        m = sub[col].mean()
        g = sub.groupby("day")[col].apply(lambda x: (x - m).sum())
        G = len(g)
        if G < 2: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(sub)
        return m / se

    out = {}
    rows = []
    for h in H:
        p = R[(R.h == h) & R.prof].dropna(subset=["scaled", "dist"])
        groups = [("prof", p),
                  ("dist<=2.5", p[p.dist <= 2.5]),
                  ("dist>2.5", p[p.dist > 2.5]),
                  ("dist==0", p[p.dist <= 0.001]),
                  ("scaled>0&dist<=2.5", p[(p.scaled > 0) & (p.dist <= 2.5)]),
                  ("scaled>0&dist>2.5", p[(p.scaled > 0) & (p.dist > 2.5)]),
                  ("scaled<=0", p[p.scaled <= 0]),
                  ("fc>0", p[p.fc > 0]),
                  ("fc>0&dist<=2.5", p[(p.fc > 0) & (p.dist <= 2.5)])]
        for name, sub in groups:
            rows.append(dict(h=h, grp=name, n=len(sub), days=sub.day.nunique(), mean_ex=sub.ex.mean(),
                             med_ex=sub.ex.median(), share_pos=(sub.ex > 0).mean(), t=tday(sub)))
    out["groups"] = pd.DataFrame(rows)
    p = R[(R.h == 14) & R.prof].dropna(subset=["scaled", "dist"]).copy()
    p["near"] = p.dist <= 2.5
    out["h14_near_by_year"] = p.groupby(["yr", "near"])["ex"].agg(["count", "mean"]).unstack()
    out["h14_near_by_coin"] = p.groupby(["coin", "near"])["ex"].agg(["count", "mean"]).unstack()
    # graded: correlation of ex with 1/(1+dist) and scaled within profile
    for h in H:
        q = R[(R.h == h) & R.prof].dropna(subset=["scaled", "dist"])
        prox = 1 / (1 + q.dist)
        out[f"corr_h{h}"] = pd.Series({"ex~prox": np.corrcoef(prox, q.ex)[0, 1],
                                       "ex~scaled": np.corrcoef(q.scaled, q.ex)[0, 1],
                                       "ex~scaled*prox(pos)": np.corrcoef(np.clip(q.scaled, 0, None) * prox, q.ex)[0, 1],
                                       "n": len(q)})
    # trimmed mean near-high h14 to check outliers
    nh = p[p.near].ex.sort_values()
    out["h14_near_trim"] = pd.Series({"mean": nh.mean(), "trim_top2": nh.iloc[:-2].mean(),
                                      "trim_both2": nh.iloc[2:-2].mean(), "max": nh.max(), "min": nh.min()})
    # usual move std per h, all grid
    out["usual_std"] = R.groupby("h")["ret"].std()
    return out
