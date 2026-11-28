def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [1, 3, 5, 10]
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
            s = (c / c.shift(3) - 1) / (r1.rolling(30).std() * np.sqrt(3))
            inprof = (b["regime"] == "unknown").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            fc = b["forecast"].values
            for h in H:
                for i in range(0, len(c) - h, h):
                    if np.isnan(s.iloc[i]): continue
                    f = c.iloc[i + h] / c.iloc[i] - 1
                    d, sd = drift[(coin, h)]
                    recs.append(dict(coin=coin, w=w, h=h, s=s.iloc[i], prof=inprof[i],
                                     yr=yr[i], day=day[i], fc=fc[i],
                                     short_unusual=-(f - d), short_total=-f, strength=-(f - d) / sd))
    df = pd.DataFrame(recs)

    def summ(g):
        x = g["short_unusual"]
        dd = g.groupby("day")["short_unusual"].sum()
        t = x.mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)) if len(dd) > 2 else np.nan
        return pd.Series(dict(n=len(x), mean_short_unusual=x.mean(), t=t,
                              mean_short_total=g["short_total"].mean(), strength=g["strength"].mean()))
    out = {}
    df["sbin"] = pd.cut(df["s"], [-np.inf, -1.5, -0.75, 0, 0.75, 1.5, np.inf])
    out["prof_by_h_sbin"] = df[df.prof].groupby(["h", "sbin"]).apply(summ)
    out["outprof_h3_sbin"] = df[(~df.prof) & (df.h == 3)].groupby("sbin").apply(summ)
    p = df[df.prof & (df.s < 0)]
    out["prof_falls_by_coin_h"] = p.groupby(["coin", "h"]).apply(summ)
    out["prof_falls_h3_by_year"] = p[p.h == 3].groupby("yr").apply(summ)
    q = df[df.prof & (df.h == 3)]
    out["prof_h3_spearman_s_vs_fwdret"] = pd.Series(dict(zip(["rho", "p"], stats.spearmanr(q["s"], -q["short_total"]))))
    q5 = df[df.prof & (df.h == 5)]
    out["prof_h5_spearman"] = pd.Series(dict(zip(["rho", "p"], stats.spearmanr(q5["s"], -q5["short_total"]))))
    out["prof_rises_by_coin_h3"] = df[df.prof & (df.s > 0) & (df.h == 3)].groupby("coin").apply(summ)
    return out
