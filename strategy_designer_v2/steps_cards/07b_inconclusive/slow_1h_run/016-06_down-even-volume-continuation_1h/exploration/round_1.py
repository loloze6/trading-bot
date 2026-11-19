def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].astype(float)
            mean72 = v.rolling(72).mean(); med72 = v.rolling(72).median()
            conc = np.log(mean72 / med72.replace(0, np.nan))
            ret72 = b["close"] / b["close"].shift(72) - 1
            n = len(b)
            for i in range(0, n, 72):
                r = {"coin": coin, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "regime": b["regime"].iloc[i], "fc": b["forecast"].iloc[i],
                     "conc": conc.iloc[i], "past": ret72.iloc[i]}
                for h in (24, 72, 168):
                    r[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(r)
    df = pd.DataFrame(rows)
    for h in (24, 72, 168):
        df[f"x{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    def reg(d, x, y):
        d = d[[x, y]].dropna()
        if len(d) < 20: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d[y]); return (s.slope, s.slope/s.stderr, len(d))
    out = {}
    tr = df[df.regime == "trending"]
    res = {}
    res["fc_x72_trend"] = reg(tr, "fc", "x72")
    res["conc_x72_trend"] = reg(tr, "conc", "x72")
    res["conc_x24_trend"] = reg(tr, "conc", "x24")
    res["conc_x168_trend"] = reg(tr, "conc", "x168")
    res["past_x72_trend"] = reg(tr, "past", "x72")
    up = df[df.past > 0]
    res["conc_x72_up"] = reg(up, "conc", "x72")
    res["conc_x168_up"] = reg(up, "conc", "x168")
    res["conc_x72_all"] = reg(df, "conc", "x72")
    out["regs (slope,t,n)"] = pd.DataFrame(res, index=["slope", "t", "n"]).T
    out["by coin fc"] = pd.DataFrame({k: reg(g, "fc", "x72") for k, g in tr.groupby("coin")}, index=["slope","t","n"]).T
    out["by year fc"] = pd.DataFrame({k: reg(g, "fc", "x72") for k, g in tr.groupby("year")}, index=["slope","t","n"]).T
    tr = tr.copy()
    tr["pq"] = pd.qcut(tr["past"], 3, labels=["bigfall","mid","small"])
    out["by fall size fc"] = pd.DataFrame({k: reg(g, "fc", "x72") for k, g in tr.groupby("pq")}, index=["slope","t","n"]).T
    tr["cq"] = pd.qcut(tr["conc"], 5, labels=False)
    out["conc quintile x72"] = tr.groupby("cq").agg(conc=("conc","mean"), fc=("fc","mean"), x72=("x72","mean"), x168=("x168","mean"), n=("x72","count"))
    tr["fq"] = pd.qcut(tr["fc"].rank(method="first"), 5, labels=False)
    out["fc quintile x72"] = tr.groupby("fq").agg(fc=("fc","mean"), conc=("conc","mean"), x72=("x72","mean"), n=("x72","count"))
    out["corr fc conc"] = float(tr[["fc","conc"]].corr().iloc[0,1])
    return out
