def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    raw_col = "debug_info.components.low_prox.last_history_value"
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            p20 = pd.Series(c).pct_change(20).values
            p60 = pd.Series(c).pct_change(60).values
            for h in [5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], fc=df["forecast"].iloc[i],
                                     raw=df[raw_col].iloc[i], ret=c[i + h] / c[i] - 1, p20=p20[i], p60=p60[i],
                                     day=str(df["timestamp"].iloc[i])[:10]))
    R = pd.DataFrame(rows)
    R["ex"] = R["ret"] - R.groupby(["coin", "h"])["ret"].transform("mean")
    R["D"] = 1 / R["raw"] - 1
    tt = lambda s: s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan
    bins = [-0.01, 5, 15, 30, 60, 120, 1e9]
    R["Dbin"] = pd.cut(R["D"], bins)
    out["ex by D bin and h"] = R.groupby(["h", "Dbin"])["ex"].agg(["size", "mean", tt]).unstack(0)
    for h in [5, 10, 20]:
        Rh = R[R.h == h].copy()
        Rh["fq"] = pd.qcut(Rh["fc"].rank(method="first"), 5, labels=False)
        top = Rh[Rh.fq == 4]
        out[f"h{h} top fc fifth by coin"] = top.groupby("coin")["ex"].agg(["size", "mean", tt])
        out[f"h{h} top fc fifth by year"] = top.groupby("year")["ex"].agg(["size", "mean", tt])
        # day-clustered t for top minus rest
        d = top.groupby("day")["ex"].sum()
        out[f"h{h} top fifth ex, day-clustered"] = pd.Series({"n": len(top), "days": len(d), "mean": top.ex.mean(),
                                                              "t_day": top.ex.sum() / len(d) / (d.std() / np.sqrt(len(d))) if len(d) > 2 else np.nan})
        # among forecast>=10 (near own-year low), slope on fc
        hi = Rh[Rh.fc >= 10]
        r = stats.linregress(hi.fc, hi.ex)
        out[f"h{h} slope within fc>=10"] = pd.Series({"n": len(hi), "slope": r.slope, "t": r.slope / r.stderr})
        Rh["p60s"] = np.where(Rh.p60 < 0, "down", "up")
        out[f"h{h} top fifth by p60"] = Rh[Rh.fq == 4].groupby("p60s")["ex"].agg(["size", "mean", tt])
    return out
