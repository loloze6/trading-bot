def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    sd = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1,3,5,10,20)}
        for w, df in wins.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c)-h, h)
                allr[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        sd[coin] = {h: np.std(v, ddof=1) for h, v in allr.items()}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            # 30-day return computed in window
            r30 = pd.Series(c).pct_change(30).values
            idx = np.arange(0, n-5, 5)
            for i in idx:
                d = {"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "r30": r30[i],
                     "regime": df["regime"].iloc[i]}
                for h in (1,3,5,10,20):
                    if i+h < n:
                        d[f"x{h}"] = c[i+h]/c[i]-1-drift[coin][h]
                        d[f"z{h}"] = d[f"x{h}"]/sd[coin][h]
                rows.append(d)
    g = pd.DataFrame(rows)
    def reg(sub, col="x5"):
        s = sub.dropna(subset=[col])
        if len(s) < 10 or s["f"].std() == 0:
            return pd.Series({"n": len(s), "npos": (s["f"]>0).sum(), "slope": np.nan, "t": np.nan})
        r = stats.linregress(s["f"], s[col])
        return pd.Series({"n": len(s), "npos": int((s["f"]>0).sum()), "slope": r.slope, "t": r.slope/r.stderr})
    out = {}
    out["pooled_check"] = reg(g)
    out["by_horizon"] = pd.DataFrame({h: reg(g, f"z{h}") for h in (1,3,5,10,20)}).T
    out["by_coin"] = g.groupby("coin").apply(reg)
    out["by_year"] = g.groupby("year").apply(reg)
    a = g[g["f"] > 0].copy()
    a["fq"] = pd.qcut(a["f"], 4, labels=False, duplicates="drop")
    out["active_by_fq"] = a.groupby("fq").agg(n=("x5","size"), fmean=("f","mean"), x5=("x5","mean"), z5=("z5","mean"))
    out["active_mean_t"] = pd.Series({"n": len(a), "x5": a["x5"].mean(), "t": stats.ttest_1samp(a["x5"].dropna(),0).statistic})
    tr = g[g["regime"]=="trending"].copy()
    out["trending_zero_vs_pos"] = tr.assign(pos=tr["f"]>0).groupby("pos").agg(n=("x5","size"), x5=("x5","mean"))
    a["r30q"] = pd.qcut(a["r30"], 3, labels=False, duplicates="drop")
    out["active_by_r30"] = a.groupby("r30q").agg(n=("x5","size"), r30=("r30","mean"), x5=("x5","mean"), z5=("z5","mean"))
    out["active_by_r30_reg"] = a.groupby("r30q").apply(reg)
    out["by_regime"] = g.groupby("regime").agg(n=("x5","size"), x5=("x5","mean"))
    return out
