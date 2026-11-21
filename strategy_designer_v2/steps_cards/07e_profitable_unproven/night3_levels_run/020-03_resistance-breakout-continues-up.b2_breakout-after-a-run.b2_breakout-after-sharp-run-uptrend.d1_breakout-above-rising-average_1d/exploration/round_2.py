def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    hs = [5, 10, 20, 30]
    recs = []
    for c in bars:
        drift = {}
        for h in hs:
            r = []
            for w in bars[c]:
                cl = bars[c][w]["close"].values
                idx = np.arange(0, len(cl)-h, h)
                r.append(cl[idx+h]/cl[idx]-1)
            drift[h] = np.concatenate(r).mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]; f = b["forecast"].fillna(0).values
            sma = cl.rolling(50).mean(); r60 = cl/cl.shift(60)-1
            hi90 = cl.rolling(90, min_periods=60).max().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            n = len(cl)
            for h in hs:
                for i in range(0, n-h, h):
                    if np.isnan(sma[i]) or np.isnan(r60[i]):
                        continue
                    recs.append({"coin": c, "win": w, "h": h, "year": ts[i].year,
                                 "md": cl[i]/sma[i]-1, "r60": r60[i],
                                 "nh": (cl[i]/hi90[i]-1) if not np.isnan(hi90[i]) else np.nan,
                                 "inpos": f[i] > 0,
                                 "u": cl[i+h]/cl[i]-1-drift[h]})
    G = pd.DataFrame(recs)
    G["trend"] = (G["md"] > 0) & (G["r60"] > 0)
    def tt(s):
        return pd.Series({"n": len(s), "mean_u": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["trend_vs_not_by_h"] = G.groupby(["h", "trend"])["u"].apply(tt).unstack()
    T = G[G["trend"]]
    out["trend_inpos_vs_not"] = T.groupby(["h", "inpos"])["u"].apply(tt).unstack()
    for h in [10, 20]:
        s = G[G["h"] == h].copy()
        s["q"] = pd.qcut(s["md"], 6, labels=False)
        out[f"md_sextile_all_h{h}"] = s.groupby("q").agg(lo=("md", "min"), hi=("md", "max"), n=("u", "count"), u=("u", "mean"))
        s2 = s.dropna(subset=["nh"]).copy()
        s2["q"] = pd.qcut(s2["nh"], 6, labels=False, duplicates="drop")
        out[f"nearhigh_sextile_all_h{h}"] = s2.groupby("q").agg(lo=("nh", "min"), hi=("nh", "max"), n=("u", "count"), u=("u", "mean"))
        s3 = s.copy(); s3["q"] = pd.qcut(s3["r60"], 6, labels=False)
        out[f"r60_sextile_all_h{h}"] = s3.groupby("q").agg(lo=("r60", "min"), hi=("r60", "max"), n=("u", "count"), u=("u", "mean"))
    t10 = T[T["h"] == 10]
    out["trend_h10_by_coin"] = t10.groupby("coin")["u"].apply(tt).unstack()
    out["trend_h10_by_year"] = t10.groupby("year")["u"].apply(tt).unstack()
    s = G[G["h"] == 10].dropna(subset=["md", "r60", "nh"])
    out["spearman_h10"] = pd.Series({"md": stats.spearmanr(s["md"], s["u"])[0],
                                     "r60": stats.spearmanr(s["r60"], s["u"])[0],
                                     "nh": stats.spearmanr(s["nh"], s["u"])[0], "n": len(s)})
    return out
