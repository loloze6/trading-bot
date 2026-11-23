def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    drift = {}; sd = {}
    for coin, wins in bars.items():
        v = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c)-5, 5)
            v += list(c[idx+5]/c[idx]-1)
        drift[coin] = np.mean(v); sd[coin] = np.std(v, ddof=1)
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            s = pd.Series(c)
            r30 = s.pct_change(30).values
            r10 = s.pct_change(10).values
            hi90 = s.rolling(90, min_periods=30).max().values
            near = c/hi90 - 1
            raw = df["debug_info.components.power_turn.last_history_value"].values
            for i in range(0, n-5, 5):
                rows.append({"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "r30": r30[i],
                             "r10": r10[i], "near": near[i], "raw": raw[i],
                             "regime": df["regime"].iloc[i],
                             "x5": c[i+5]/c[i]-1-drift[coin], "z5": (c[i+5]/c[i]-1-drift[coin])/sd[coin]})
    g = pd.DataFrame(rows)
    def reg(sub, x, y="x5"):
        s = sub.dropna(subset=[x, y])
        if len(s) < 10 or s[x].std() == 0:
            return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan})
        r = stats.linregress(s[x], s[y])
        return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope/r.stderr})
    out = {}
    tr = g[g["regime"] == "trending"]
    a = g[g["f"] > 0]
    out["trending_x5_on_f"] = reg(tr, "f")
    out["trending_x5_on_r30"] = reg(tr, "r30")
    out["active_x5_on_r30"] = reg(a, "r30")
    out["active_x5_on_near"] = reg(a, "near")
    out["trending_x5_on_near"] = reg(tr, "near")
    out["all_x5_on_f_ex2021"] = reg(g[g["year"] != 2021], "f")
    out["active_mean_ex2021"] = pd.Series({"n": int((a["year"]!=2021).sum()),
        "x5": a[a["year"]!=2021]["x5"].mean(),
        "t": stats.ttest_1samp(a[a["year"]!=2021]["x5"], 0).statistic})
    lo = a[a["r30"] < a["r30"].quantile(1/3)]["x5"]; hi = a[a["r30"] >= a["r30"].quantile(1/3)]["x5"]
    out["active_r30_hi_minus_lo"] = pd.Series({"n_hi": len(hi), "n_lo": len(lo), "diff": hi.mean()-lo.mean(),
        "t": stats.ttest_ind(hi, lo, equal_var=False).statistic})
    trz = tr[tr["f"] == 0]
    out["trending_zero_by_r30q"] = trz.assign(q=pd.qcut(trz["r30"], 3, labels=False)).groupby("q").agg(n=("x5","size"), r30=("r30","mean"), x5=("x5","mean"))
    out["active_by_year_mean"] = a.groupby("year").agg(n=("x5","size"), x5=("x5","mean"))
    out["active_vs_trendzero_welch"] = pd.Series({"diff": a["x5"].mean()-trz["x5"].mean(),
        "t": stats.ttest_ind(a["x5"], trz["x5"], equal_var=False).statistic})
    out["active_rank_corr_f"] = pd.Series(stats.spearmanr(a["f"], a["x5"])._asdict())
    return out
