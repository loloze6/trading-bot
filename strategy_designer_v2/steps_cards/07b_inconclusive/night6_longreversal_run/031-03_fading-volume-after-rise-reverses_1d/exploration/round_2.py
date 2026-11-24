def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allg = {}
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values; n = len(df)
            for h in (5, 10, 15):
                for i in range(0, n - h, h):
                    allg.setdefault((coin, h), []).append(c[i+h]/c[i]-1)
            for i in range(0, n - 10, 10):
                r = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(df["timestamp"].iloc[i]).normalize(),
                     "reg": df["regime"].iloc[i] == "mean_reversion", "fc": df["forecast"].iloc[i],
                     "r10": c[i+10]/c[i]-1}
                r["p30"] = c[i]/c[i-30]-1 if i >= 30 else np.nan
                r["p20"] = c[i]/c[i-20]-1 if i >= 20 else np.nan
                r["vr14_30"] = v[i-13:i+1].mean()/v[i-29:i+1].mean()-1 if i >= 29 else np.nan
                rows.append(r)
    g = pd.DataFrame(rows)
    mu = {k[0]: np.mean(x) for k, x in allg.items() if k[1] == 10}
    sd = {k[0]: np.std(x, ddof=1) for k, x in allg.items() if k[1] == 10}
    g["x10"] = g["r10"] - g["coin"].map(mu)
    g["s10"] = g["x10"] / g["coin"].map(sd)
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s) > 1 else np.nan})
    out = {}
    reg = g[g.reg]; non = g[~g.reg]
    out["x10 regime vs not (10-grid)"] = pd.DataFrame({"regime": tt(reg.x10), "not": tt(non.x10)})
    out["welch regime-not x10"] = str(stats.ttest_ind(reg.x10, non.x10, equal_var=False))
    d = reg.groupby("day")["x10"].sum()
    out["regime x10 day-grouped t"] = f"days={len(d)} mean_case={reg.x10.mean():.4f} t={d.mean()/(d.std(ddof=1)/np.sqrt(len(d))):.2f}"
    out["regime strength s10 mean"] = round(reg.s10.mean(), 4)
    out["regime x10 by coin"] = reg.groupby("coin")["x10"].apply(tt).unstack()
    out["regime x10 by year"] = reg.groupby("year")["x10"].apply(tt).unstack()
    out["regime x10 short-forecast vs 0"] = reg.groupby(reg.fc < 0)["x10"].apply(tt).unstack()
    for col in ("p30", "p20", "vr14_30"):
        s = reg[[col, "x10"]].dropna()
        if len(s) > 8:
            lr = stats.linregress(s[col], s.x10)
            out["regime slope x10 on " + col] = f"n={len(s)} slope={lr.slope:.4f} t={lr.slope/lr.stderr:.2f}"
        s = g[[col, "x10"]].dropna()
        lr = stats.linregress(s[col], s.x10)
        out["all slope x10 on " + col] = f"n={len(s)} slope={lr.slope:.4f} t={lr.slope/lr.stderr:.2f}"
    s = reg[["p30", "x10"]].dropna()
    if len(s) > 9:
        s["q"] = pd.qcut(s.p30, 3, labels=["low", "mid", "high"])
        out["regime x10 by p30 tercile"] = s.groupby("q")["x10"].apply(tt).unstack()
    return out
