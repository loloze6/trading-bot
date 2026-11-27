def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = (7, 10, 14, 21)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.fall30.last_history_value")
            r30 = pd.Series(c).pct_change(30).values * 100
            r60 = pd.Series(c).pct_change(60).values * 100
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        day=pd.Timestamp(df["timestamp"].iloc[i]).normalize(),
                        inprof=df["regime"].iloc[i] == "unknown",
                        raw=(raw.iloc[i] if raw is not None else np.nan),
                        r30=r30[i], r60=r60[i], fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["sig"] = d["raw"].where(d["raw"].notna(), d["r30"])
    d["choppy"] = d["r60"].between(-10, 10)
    def reg(g):
        g = g.dropna(subset=["sig", "ex"])
        if len(g) < 8: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["sig"], g["ex"])
        sh = -g["ex"]
        dd = sh.groupby(g["day"]).sum()
        tday = sh.mean() / (dd.std() / np.sqrt(len(dd)) * len(dd) / len(g)) if len(dd) > 2 else np.nan
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              short_ex=sh.mean(), t_short_day=tday))
    out = {}
    f = d[d.inprof & (d.sig < 0)]
    out["in profile falls by h"] = f.groupby("h").apply(reg).round(4)
    out["in profile falls by h and year"] = f.groupby(["h", "year"]).apply(reg).round(4)
    fc = d[(~d.inprof) & d.choppy & (d.r30 < 0)].copy()
    fc["sig"] = fc["r30"]
    out["choppy not-agitated (choppy calm approx) falls by h"] = fc.groupby("h").apply(reg).round(4)
    fa = d[d.choppy & (d.r30 < 0)].copy(); fa["sig"] = fa["r30"]
    out["all choppy (trend only) falls by h"] = fa.groupby("h").apply(reg).round(4)
    f14 = f[f.h == 14].copy()
    if len(f14) >= 8:
        f14["half"] = np.where(f14.sig <= f14.sig.median(), "deeper", "shallower")
        out["in profile 14d by half"] = f14.groupby("half")[["sig", "ex"]].agg(["mean", "count"]).round(4)
    return out
