def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [7, 14, 28]
    drift, sd = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs) if rs else np.nan
            sd[(c, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].values
            f = df["forecast"].values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in H:
                for i in range(0, len(cl) - h, h):
                    if f[i] > 0:
                        r = cl[i + h] / cl[i] - 1
                        rows.append(dict(coin=c, win=w, h=h, f=f[i], ex=r - drift[(c, h)],
                                         st=(r - drift[(c, h)]) / sd[(c, h)], day=day[i],
                                         year=pd.Timestamp(day[i]).year))
    d = pd.DataFrame(rows)
    out = {}
    def clust_t(g, col="ex", wcol=None):
        w = g[wcol] if wcol else pd.Series(1.0, index=g.index)
        m = (g[col] * w).sum() / w.sum()
        dd = ((g[col] - m) * w).groupby(g.day).sum()
        G = len(dd)
        if G < 2: return m, np.nan, G
        se = np.sqrt(G / (G - 1) * (dd ** 2).sum()) / w.sum()
        return m, m / se, G
    res = []
    for h in H:
        g = d[d.h == h]
        m, t, G = clust_t(g, "ex", "f")
        ms, ts, _ = clust_t(g, "st")
        sl = stats.linregress(g.f, g.ex)
        res.append(dict(h=h, n=len(g), days=G, wmean=m, wt_clust=t, strength=ms, strength_t=ts,
                        slope_per_f=sl.slope, slope_t=sl.slope / sl.stderr if sl.stderr > 0 else np.nan))
    out["clustered_by_h"] = pd.DataFrame(res).set_index("h")
    for h in [7, 14]:
        g = d[d.h == h].copy()
        g["half"] = np.where(g.f > g.f.median(), "upper", "lower")
        out[f"{h}_half_by_year"] = g.groupby(["year", "half"]).ex.agg(["count", "mean"]).unstack()
        out[f"{h}_by_coin"] = g.groupby("coin").ex.agg(["count", "mean"])
    return out
