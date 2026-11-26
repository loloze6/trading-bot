def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    h = 14
    rows = []
    for coin, wins in bars.items():
        recs = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values; v = df["volume"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n - h, h):
                r = c[i + h] / c[i] - 1
                def past(k):
                    return c[i] / c[i - k] - 1 if i >= k else np.nan
                ma30 = c[i-29:i+1].mean() if i >= 29 else np.nan
                ma60 = c[i-59:i+1].mean() if i >= 59 else np.nan
                vr = v[i-13:i+1].mean() / v[i-29:i+1].mean() - 1 if i >= 29 else np.nan
                recs.append(dict(coin=coin, f=f[i], r=r, p7=past(7), p14=past(14), p30=past(30),
                                 above30=np.sign(c[i] / ma30 - 1) if ma30 == ma30 else np.nan,
                                 above60=np.sign(c[i] / ma60 - 1) if ma60 == ma60 else np.nan,
                                 vr=vr, year=yr[i], day=str(df["timestamp"].iloc[i])[:10]))
        d = pd.DataFrame(recs)
        if len(d) == 0: continue
        d["x"] = d["r"] - d["r"].mean()
        d["sd"] = d["r"].std()
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def stat(g, wcol="f"):
        g = g[g[wcol] > 0]
        if len(g) < 5: return pd.Series(dict(n=len(g)))
        wt = g[wcol]
        wm = (wt * g.x).sum() / wt.sum()
        dd = g.assign(dev=wt * (g.x - wm)).groupby("day")["dev"].sum()
        Dn = len(dd)
        se = np.sqrt((dd ** 2).sum() * Dn / max(Dn - 1, 1)) / wt.sum()
        du = g.groupby("day")["x"].sum()
        um = g.x.mean()
        se_u = np.sqrt(((du - du.mean()) ** 2).sum() * Dn / max(Dn - 1, 1)) / len(g)
        sl = np.polyfit(wt, g.x, 1)[0] if len(g) > 10 else np.nan
        return pd.Series(dict(n=len(g), days=Dn, wmean=wm, t=wm / se, unusual=um,
                              t_unusual=um / se_u if se_u > 0 else np.nan,
                              strength=(g.x / g.sd).mean(), slope=sl))
    out = {}
    pos = D[D.f > 0]
    out["by_past30_sign"] = pos.assign(s=np.sign(pos.p30)).groupby("s").apply(stat)
    out["by_past7_sign"] = pos.assign(s=np.sign(pos.p7)).groupby("s").apply(stat)
    out["by_above30ma"] = pos.groupby("above30").apply(stat)
    out["by_above60ma"] = pos.groupby("above60").apply(stat)
    p14 = pos[pos.p14 > 0]
    out["p14pos_by_year"] = p14.groupby("year").apply(stat)
    out["p14pos_by_fq"] = p14.assign(fq=pd.qcut(p14.f, 3, labels=False)).groupby("fq").apply(stat)
    # graded alternative: swell weighted only when 14-day return up, all grid cells
    D2 = D.copy()
    D2["g"] = np.where(D2.p14 > 0, D2.f, 0.0)
    out["swell_on_rise_all"] = stat(D2, "g")
    D2["g2"] = np.where(D2.p14 > 0, D2.f * D2.p14 / D2.p14.std(), 0.0)
    out["swell_x_rise_all"] = stat(D2, "g2")
    D2["g3"] = np.where(D2.above30 > 0, D2.f, 0.0)
    out["swell_above30_all"] = stat(D2, "g3")
    return out
