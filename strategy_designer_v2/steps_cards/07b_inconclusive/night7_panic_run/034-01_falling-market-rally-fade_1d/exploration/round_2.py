def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5]
    drift, usual = {}, {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; r = cl.pct_change()
            sd = r.rolling(30).std(); z = r / sd
            zs = (z - z.rolling(60, min_periods=20).mean()) / z.rolling(60, min_periods=20).std()
            tr = (cl / cl.shift(60) - 1) * 100
            falling = np.where(tr.notna(), tr < -10, df["regime"] == "unknown")
            sdmed = sd.rolling(365, min_periods=90).median()
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    if not (z.iloc[i] > 0) or not falling[i]: continue
                    fr = cl.iloc[i + h] / cl.iloc[i] - 1
                    rows.append(dict(coin=c, win=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     z=z.iloc[i], zs=zs.iloc[i],
                                     agit=(sd.iloc[i] > sdmed.iloc[i]) if pd.notna(sdmed.iloc[i]) else np.nan,
                                     su=-(fr - drift[(c, h)]), st=-(fr - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def ct(g, col="su"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=np.nan, t=np.nan))
        m = g[col].mean(); dev = (g[col] - m).groupby(g["day"]).sum(); D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se > 0 else np.nan))
    def slope(g, x):
        g = g.dropna(subset=[x, "su"])
        res = stats.linregress(g[x], g["su"])
        return pd.Series(dict(n=len(g), slope=res.slope, t=res.slope / res.stderr))
    out = {}
    out["slope_z_by_h"] = d.groupby("h").apply(lambda g: slope(g, "z"))
    out["slope_zs_by_h"] = d.groupby("h").apply(lambda g: slope(g, "zs"))
    out["corr_z_zs_h3"] = d[d.h == 3][["z", "zs"]].corr().iloc[0, 1]
    d3 = d[d.h == 3].copy()
    d3["zq"] = pd.qcut(d3.z, 4, labels=False)
    out["h3_agit_x_zq"] = d3.groupby(["agit", "zq"]).apply(ct)
    out["h3_slope_z_by_agit"] = d3.groupby("agit").apply(lambda g: slope(g, "z"))
    top = d3[d3.zq >= 2]
    out["h3_tophalf_by_coin"] = top.groupby("coin").apply(ct)
    out["h3_tophalf_by_win"] = top.groupby("win").apply(ct)
    d3["zsq"] = pd.qcut(d3.zs, 4, labels=False)
    out["h3_by_zs_quart"] = d3.groupby("zsq").apply(ct)
    for h in [1, 2, 5]:
        dh = d[d.h == h].copy(); dh["zq"] = pd.qcut(dh.z, 4, labels=False)
        out[f"h{h}_by_zq_strength"] = dh.groupby("zq").apply(lambda g: ct(g, "st"))
    out["h3_strength_by_zq"] = d3.groupby("zq").apply(lambda g: ct(g, "st"))
    return out
