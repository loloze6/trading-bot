def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r = pd.Series(c).pct_change()
            sd = r.rolling(30).std()
            sd30 = sd.values
            r3 = pd.Series(c).pct_change(3).values
            r60 = pd.Series(c).pct_change(60).values
            agi = (sd > sd.expanding(30).median()).values
            agi_ok = sd.expanding(30).count().values >= 30
            fc = df["forecast"].astype(float).values
            prev = 0.0
            for t in range(0, n, 7):
                d = {"coin": coin, "w": w, "t": t, "fc": fc[t], "day": str(df["timestamp"].iloc[t])[:10],
                     "z": r3[t] / (sd30[t] * np.sqrt(3)) if sd30[t] == sd30[t] and sd30[t] > 0 else np.nan,
                     "r60": r60[t], "agi": agi[t] if agi_ok[t] else np.nan, "sd30": sd30[t]}
                for h in [7, 14, 21]:
                    d[f"f{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                    # window mean of grid-h returns (market move inside window, informative)
                rows.append(d)
    D = pd.DataFrame(rows)
    for h in [7, 14, 21]:
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(D.groupby("coin")[f"f{h}"].mean())
        D[f"x{h}"] = D[f"f{h}"] - D.groupby(["coin", "w"])[f"f{h}"].transform("mean")
    def ct(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        g = x.groupby("d")["v"].sum()
        G = len(g)
        if G < 3: return (len(x), G, np.nan, np.nan)
        m = x["v"].mean()
        dev = x.groupby("d")["v"].apply(lambda v: (v - m).sum())
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x)
        return (len(x), G, m, m / se)
    out = {}
    cs = D[D["fc"] >= 2]
    res = {}
    for name, sub in [("all", cs), ("calm", cs[cs["agi"] == 0]), ("agitated", cs[cs["agi"] == 1])]:
        for h in [7, 14, 21]:
            for k in ["u", "x"]:
                res[(name, f"{k}{h}")] = ct(sub[f"{k}{h}"], sub["day"])
    out["cases fc>=2: n, days, mean, cluster t (u=vs drift, x=vs window mean)"] = pd.DataFrame(res, index=["n", "days", "mean", "t"]).T
    # grading within calm / agitated on all grid bars with z>0
    g = {}
    for name, sub in [("calm", D[(D["agi"] == 0) & (D["z"] > 0)]), ("agitated", D[(D["agi"] == 1) & (D["z"] > 0)]), ("all z>0", D[D["z"] > 0])]:
        for h in [7, 14]:
            x = sub[["z", f"u{h}"]].dropna()
            sl = stats.linregress(x["z"], x[f"u{h}"])
            g[(name, h)] = {"n": len(x), "slope": sl.slope, "t": sl.slope / sl.stderr, "spearman": stats.spearmanr(x["z"], x[f"u{h}"])[0]}
    out["grading z>0 grid bars"] = pd.DataFrame(g).T
    # calm cases by window
    cc = cs[cs["agi"] == 0]
    out["calm cases u7 by window"] = cc.groupby("w")["u7"].agg(["count", "mean"])
    out["agitated cases u7 by window"] = cs[cs["agi"] == 1].groupby("w")["u7"].agg(["count", "mean"])
    D["zq"] = pd.qcut(D["z"], 5, labels=False, duplicates="drop")
    out["z quintile, calm only, u7/u14"] = D[D["agi"] == 0].groupby("zq").agg(n=("u7", "count"), u7=("u7", "mean"), u14=("u14", "mean"))
    out["z quintile, agitated only, u7/u14"] = D[D["agi"] == 1].groupby("zq").agg(n=("u7", "count"), u7=("u7", "mean"), u14=("u14", "mean"))
    return out
