def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    P = "debug_info.components.range_pos.post_pipeline_value"
    rows = []
    h = 5
    allret = {}
    for c in bars:
        out = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                out.append(cl[i + h] / cl[i] - 1)
        allret[c] = (np.mean(out), np.std(out, ddof=1))
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            r1 = cl.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            r5p = cl / cl.shift(5) - 1
            r20p = cl / cl.shift(20) - 1
            fr = (cl.shift(-h) / cl - 1).values
            yr = pd.Timestamp(df["timestamp"].iloc[0]).year
            for i in range(0, len(df) - h, h):
                if pd.isna(df.loc[i, P]):
                    continue
                rows.append(dict(coin=c, w=w, yr=yr, day=str(df.loc[i, "timestamp"])[:10],
                                 f=df.loc[i, P], ex=fr[i] - allret[c][0],
                                 exn=(fr[i] - allret[c][0]) / allret[c][1],
                                 vol=vol30[i], r5=r5p[i], r20=r20p[i]))
    d = pd.DataFrame(rows)
    d["volrank"] = d.groupby("coin")["vol"].rank(pct=True)
    def slope(g, x="f", y="ex"):
        g = g.dropna(subset=[x, y])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g[y])
        sp = stats.spearmanr(g[x], g[y])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr, rho=sp.correlation))
    out = {}
    out["all"] = slope(d)
    out["excl_w16"] = slope(d[d.w != "w16"])
    out["by_year"] = d.groupby("yr").apply(slope)
    d["volq"] = pd.qcut(d["volrank"], 3, labels=["low", "mid", "high"])
    out["by_volterc"] = d.groupby("volq").apply(slope)
    out["by_side"] = d.groupby(d.f > 0).apply(slope)
    # signed case returns: sign(f)*ex per case, day-clustered t
    d["s"] = np.sign(d.f) * d.ex
    g = d.groupby("day")["s"].sum()
    out["signed_case_mean"] = pd.Series(dict(n=len(d), mean=d.s.mean(), days=len(g),
                                             t_day=g.mean() / g.std(ddof=1) * np.sqrt(len(g)) ))
    out["signed_by_volterc"] = d.groupby("volq")["s"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["normed_slope"] = slope(d, y="exn")
    out["f_abs_terc"] = d.groupby(pd.qcut(d.f.abs(), 3, labels=False))["s"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["slope_r20"] = slope(d, x="r20")
    return out
