def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.fall30.last_history_value")
            pp = df.get("debug_info.components.fall30.post_pipeline_value")
            r30 = pd.Series(c).pct_change(30).values * 100
            for h in (3, 7, 14):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        inprof=df["regime"].iloc[i] == "unknown",
                        raw=(raw.iloc[i] if raw is not None else np.nan),
                        pp=(pp.iloc[i] if pp is not None else np.nan),
                        r30=r30[i], fwd=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    # drift per coin per h over all windows
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["sig"] = d["raw"].where(d["raw"].notna(), d["r30"])
    out = {}
    def reg(g, x="sig"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 8: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr, mean_ex=g["ex"].mean(),
                              t_mean=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g)))))
    p = d[d.inprof]
    out["in profile, by h and side (sig=raw 30d ret %)"] = p.assign(side=np.where(p.sig < 0, "fall", "rise")).groupby(["h", "side"]).apply(reg).round(4)
    out["in profile both sides by h"] = p.groupby("h").apply(reg).round(4)
    out["out of profile both sides by h"] = d[~d.inprof].groupby("h").apply(reg).round(4)
    f7 = p[(p.h == 7) & (p.sig < 0)]
    out["fall 7d by coin"] = f7.groupby("coin").apply(reg).round(4)
    out["fall 7d by year"] = f7.groupby("year").apply(reg).round(4)
    f7 = f7.copy(); f7["q"] = pd.qcut(f7["sig"], 4, labels=["deepest", "q2", "q3", "shallow"])
    out["fall 7d by quartile of fall"] = f7.groupby("q")[["sig", "ex", "fwd"]].agg(["mean", "count"]).round(4)
    r7 = p[(p.h == 7) & (p.sig >= 0)].copy()
    if len(r7) > 8:
        r7["q"] = pd.qcut(r7["sig"], 4, labels=["small", "q2", "q3", "largest"])
        out["rise 7d by quartile"] = r7.groupby("q")[["sig", "ex", "fwd"]].agg(["mean", "count"]).round(4)
    out["fall 7d pp slope"] = reg(f7, "pp").round(4)
    return out
