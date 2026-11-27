def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            rng = h - l
            loc = np.where(rng > 0, (c - l) / np.where(rng > 0, rng, 1), np.nan)
            cs = pd.Series(c)
            r1 = cs.pct_change().values
            ret5 = cs.pct_change(5).values
            ret60 = cs.pct_change(60).values
            vol30 = pd.Series(r1).rolling(30).std().values
            ts = pd.to_datetime(df["timestamp"])
            for H in (2, 5):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, loc=loc[i], ret5=ret5[i], ret60=ret60[i], r1=r1[i],
                                     vol30=vol30[i], inprof=df["regime"].iloc[i] != "chop",
                                     wd=ts.iloc[i].dayofweek, day=ts.iloc[i].normalize(),
                                     year=ts.iloc[i].year, fwd=c[i + H] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "H"])["fwd"].transform("mean")
    g["un"] = g["fwd"] - g["drift"]
    g["volrel"] = g["vol30"] / g.groupby("coin")["vol30"].transform("median")
    def cl(x):
        x = x.dropna(subset=["un"])
        if len(x) < 3:
            return pd.Series(dict(n=len(x), days=x.day.nunique(), mean=x.un.mean() if len(x) else np.nan, tday=np.nan))
        s = x.groupby("day")["un"].sum()
        m = x.un.mean(); k = len(s); N = len(x)
        dev = x.groupby("day")["un"].apply(lambda v: (v - m).sum())
        se = np.sqrt((dev ** 2).sum() * k / (k - 1)) / N
        return pd.Series(dict(n=N, days=k, mean=m, tday=m / se))
    out = {}
    # 1. upper-half close after negative 5d, out of profile, H2 and H5, day-clustered
    for H in (2, 5):
        s = g[(g.H == H)]
        sit = s[(s["loc"] > 0.5) & (s["ret5"] < 0)]
        out[f"H{H} sit inprof"] = sit.groupby("inprof").apply(cl)
        out[f"H{H} sit by window"] = sit[~sit.inprof].groupby("w").apply(cl)
        sit = sit.copy()
        sit["tr"] = np.where(sit.ret60 > 0.10, "rising", np.where(sit.ret60 < -0.10, "falling", np.where(sit.ret60.isna(), "na", "choppy")))
        sit["ag"] = np.where(sit.volrel > 1, "agit", "calm")
        out[f"H{H} sit trend x agit"] = sit.groupby(["tr", "ag"]).apply(cl)
        sit["locb"] = pd.cut(sit["loc"], [0.5, 0.75, 0.9, 1.01])
        out[f"H{H} sit by loc"] = sit.groupby("locb").apply(cl)
        sit["r5b"] = pd.qcut(sit["ret5"], 3, labels=["deep", "mid", "shallow"])
        out[f"H{H} sit by r5 depth"] = sit.groupby("r5b").apply(cl)
        out[f"H{H} sit spearman"] = pd.Series(dict(
            loc=stats.spearmanr(sit["loc"], sit["un"])[0],
            ret5=stats.spearmanr(sit["ret5"], sit["un"])[0],
            n=len(sit)))
        # control: upper close after positive 5d
        ctl = s[(s["loc"] > 0.5) & (s["ret5"] >= 0)]
        out[f"H{H} upper close r5pos"] = cl(ctl)
        out[f"H{H} lower close r5neg"] = cl(s[(s["loc"] <= 0.5) & (s["ret5"] < 0)])
    # 2. weekday at H2, day-clustered, by year
    s2 = g[g.H == 2]
    out["H2 weekday clustered"] = s2.groupby("wd").apply(cl)
    out["H2 sunday by year"] = s2[s2.wd == 6].groupby("year").apply(cl)
    # 3. 20d-ish: 60-day trend H5 quintiles clustered
    s5 = g[g.H == 5].dropna(subset=["ret60"]).copy()
    s5["r60b"] = pd.qcut(s5["ret60"], 5, labels=False)
    out["H5 ret60 quintile"] = s5.groupby("r60b").apply(cl)
    return out
